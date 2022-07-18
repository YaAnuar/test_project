from Models import *
from curr_conv.getting_doc import thread_local_session_scope
from datetime import date, timedelta
import eventlet
import requests


token = '1861574126:AAH2c9Mmt87CMB1FvRWUTxIOFvrpyEDo9dY'
# установите ваш чат id, получить можно у бота @getmyid_bot
chat_id = '828686133'


def telegram_sender():
    yesterday = date.today() - timedelta(days=1)
    with thread_local_session_scope() as thread_session:
        while True:
            dates = thread_session.query(Order).filter_by(time=yesterday)
            api_string = 'https://api.telegram.org/bot' + token + \
            				'/sendMessage?chat_id='+ chat_id + \
            				'&text='+' Просрочены закаы:\n'
            infostring = ''
            for dateval in dates:
                infostring = infostring + " id = " + str(dateval.id) + ";" \
                                        " order_id=" + str(dateval.order_id) + ";" \
                                        " стоимость,$=" + str(dateval.usd) + ";" \
                                        " стоимость в рублях=" + str(dateval.rub) + ";\n"

            requests.post(api_string+infostring)
            eventlet.sleep(86400)
