import eventlet
eventlet.monkey_patch()
from curr_conv import socketio, app
from curr_conv.getting_doc import getting_doc_data
from curr_conv.telegram_sender import telegram_sender
import threading

if __name__ == '__main__':
    # Получаю данные из документа при помощи Google Api в отдельном потоке
    thr1 = threading.Thread(target=getting_doc_data)
    thr1.daemon = True
    thr1.start()
    # Отправляю сообщения в телеграм
    thr2 = threading.Thread(target=telegram_sender)
    thr2.daemon = True
    thr2.start()
    # Запускаю сервер
    socketio.run(app, host="0.0.0.0", debug=False, port=2000)
