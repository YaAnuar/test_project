from Models import *
from curr_conv import app
from curr_conv.getting_doc import thread_local_session_scope
from datetime import date, timedelta
import eventlet
import requests
from curr_conv.Config import config

def telegram_sender():
    chat_id = config.chat_id
    token = config.token
    yesterday = date.today() - timedelta(days=1)
    # если датой заказа является вчерашний день, отправляем сообщение, что заказ просрочен
    with thread_local_session_scope() as thread_session:
        while True:
            dates = thread_session.query(Order).filter_by(time=yesterday)
            api_string = 'https://api.telegram.org/bot' + token + \
            				'/sendMessage?chat_id='+ chat_id + '&text='		
            info_string = ''
            if dates.count() != 0:
            	info_string = ' Просрочены закаы:\n'
            	for dateval in dates:
	                info_string = info_string + " id = " + str(dateval.id) + ";" \
	                                        " order_id=" + str(dateval.order_id) + ";" \
	                                        " стоимость,$=" + str(dateval.usd) + ";" \
	                                        " стоимость в рублях=" + str(dateval.rub) + ";\n"
            else:
            	info_string = info_string + " Просроченных заказов нет! "

            requests.post(api_string+info_string)
            # раз в сутки
            eventlet.sleep(86400)
