from celery import shared_task
import requests
from django.core.mail import send_mail
from django.http import HttpResponse


@shared_task
def send_email_celery():
    subject = 'FogsDemy lesson'
    email_from = 'dchenk@gmail.com'
    message = 'Поздравляю с окончанием блока Celery!'
    recipient_list = ['dchenk@gmail.com', 'vitalzekromx@mail.ru']
    send_mail(subject, message, email_from, recipient_list)
    print('письмо ушло, запись в лог')
    return HttpResponse('ok')

@shared_task
def send_telegram_celery(bot_token, ids, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    for chat_id in ids:
        data = {
            "chat_id": chat_id,
            "text": message
        }
        requests.post(url, data=data)
    print('сообщение в телегу ушло, запись в лог')
