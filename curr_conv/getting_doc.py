from sqlalchemy.orm import scoped_session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from curr_conv import socketio, app, db
from Models import *
import requests
import eventlet
import json
import datetime
from lxml import etree

parser = etree.XMLParser(recover=True)

# код для открытия сессии с бд
@contextmanager
def thread_local_session_scope():
    """Provides a transactional scope around a series of operations.
    Context is local to current thread.
    """
    # See this StackOverflow answer for details:
    # http://stackoverflow.com/a/18265238/1830334
    app.app_context().push()
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    threaded_session = Session()
    try:
        yield threaded_session
        threaded_session.commit()
    except:
        threaded_session.rollback()
        raise
    finally:
        Session.remove()


# проверяем наши данные на валидность
# я сделал это здесь так как использую execute/postgresql insert
# так же добавил проверку на валидность в модели
def validate_date(value):
    try:
        day, month, year = value.split('.')
        datetime.datetime(int(year), int(month), int(day))
        return value
    except Exception:
        return None


def validate_num(value):
    if value is None:
        return value
    if not value.isnumeric():
        return None
    else:
        return value

# парсим xml для перевода валюты в рубли
def parse_xml(time, usd):
    if time is not None:
        rub = ''
        time.replace('.', '/')
        # парсим наш xml файл для получения курса рубля к долллару
        xml = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+time)
        root = etree.fromstring(xml.content, parser=parser)
        for record in root.findall('Valute'):
            rubval = record.find('Value').text
            if record.find('CharCode').text == 'USD':
                rub = rubval.replace(',', '.')
                break
        usd = validate_num(usd)
        if usd is not None and rub != '':
            rub = "{0:.1f}".format(float(usd)*float(rub))
        elif rub == '':
            rub = None

        return rub

# перезагружаем данные из документа в базу при перезапуске сервера
def reload_data(thread_session):
    thread_session.query(Order).delete()
    order = thread_session.query(Order).first()
    # первый запрос resp1 до цикла, для сравнения
    resp1 = requests.get("https://sheets.googleapis.com/v4/spreadsheets/1wCa9s91PxlkQPDS6pxIsR7-2xB7NMDvvmo1VPhaV0Co/values/Лист1?key=AIzaSyCO5Kc4d9n1UFDTGhaBHEGmgiNjYRv8IUk")
    resp1 = resp1.json()
    resp1_tup = tuple(tuple(i) for i in resp1['values'][1:])

    # Добавляем данные из документа в базу данных
    if order is None:
        iresp1 = iter(resp1_tup)
        while True:
            try:
                row = next(iresp1)
                if row[0].isnumeric():
                    order_id = row[1] if len(row) > 1 else None
                    usd = row[2] if len(row) > 2 else None
                    time = row[3] if len(row) > 3 else None

                    # парсим xml, чтобы получить курс рубля
                    rub = parse_xml(time, usd)
                    usd = validate_num(usd)
                    thread_session.execute(insert(Order).values([{
                                'id': row[0], 'order_id': validate_num(order_id),
                                'usd': usd, 'time': validate_date(time), 'rub': rub}])
                                .on_conflict_do_nothing())
            except StopIteration:
                thread_session.commit()
                break

    return resp1_tup

# основная функция получения данных из Google sheets
def getting_doc_data():
    with thread_local_session_scope() as thread_session:
        # начальная загрузка данных в базу
        resp1_tup = reload_data(thread_session)

        # Сравниваем данные после включения сервера и постоянно запрашиваем данные из документа
        # для обеспечения обновления данных в онлайне
        while True:
            resp2 = requests.get("https://sheets.googleapis.com/v4/spreadsheets/1wCa9s91PxlkQPDS6pxIsR7-2xB7NMDvvmo1VPhaV0Co/values/Лист1?key=AIzaSyCO5Kc4d9n1UFDTGhaBHEGmgiNjYRv8IUk")
            resp2 = resp2.json()
            if 'values' in resp2.keys():
                # Я так подумал и посчитал, что перебирать всю таблицу ради отличий плохая идея
                # Наши записи по сути являются множествами
                resp2_tup = tuple(tuple(i) for i in resp2['values'][1:])
                new_Set = set(resp2_tup)
                old_Set = set(resp1_tup)
                # Сначала находим пересечения
                inter_Set = new_Set.intersection(old_Set)
                # находим изменившиеся и удалённые строки в старом множестве, простыми словами находим разницу
                diff_Set = old_Set.difference(inter_Set)
                # удаляем лишние записи из базы
                diff = tuple(diff_Set)
                for row in diff:
                    if row:
                        if row[0].isnumeric():
                            order_id = row[1] if len(row) > 1 else None
                            usd = row[2] if len(row) > 2 else None
                            order_id = validate_num(order_id)
                            usd = validate_num(usd)
                            # Несколько возможных вариантов удаления записей из базы
                            # при пустых значениях ячеек
                            if order_id is not None and usd is not None:
                                thread_session.query(Order).filter_by(id=row[0], order_id=order_id, usd=usd).delete()
                            elif usd is None and order_id is not None:
                                thread_session.query(Order).filter_by(id=row[0], order_id=order_id).delete()
                            elif order_id is None and usd is not None:
                                thread_session.query(Order).filter_by(id=row[0], usd=usd).delete()
                            else:
                                thread_session.query(Order).filter_by(id=row[0], order_id=None, usd=None).delete()
                thread_session.commit()

                # находим изменившиеся строки в новом множестве и добавляем новые данные в базу
                new_Vals = new_Set.difference(inter_Set)
                for new in new_Vals:
                    if new:
                        if new[0].isnumeric():
                            # очередная проверка на валидность
                            order_id = new[1] if len(new) > 1 else None
                            usd = new[2] if len(new) > 2 else None
                            time = new[3] if len(new) > 3 else None
                            rub = parse_xml(time, usd)
                            thread_session.execute(insert(Order).values({'id': new[0],
                                            'order_id': validate_num(order_id),
                                            'usd': validate_num(usd),
                                            'time': validate_date(time), 'rub': rub})
                                            .on_conflict_do_nothing(index_elements=['id']))
                    thread_session.commit()

                # собираем json для фронта
                lshow = []
                backresult = thread_session.query(Order).order_by(Order.id)
                for res in backresult:
                    show = {"show": {"num": res.id, 'order': res.order_id, 'USD': res.usd, 'time': str(res.time), 'RUB': res.rub}}
                    lshow.append(show)
                result = json.loads(json.dumps(lshow))
                resp1_tup = resp2_tup
                # постоянно обновляем данные
                socketio.emit("get_data", result)
            eventlet.sleep(2.5)
