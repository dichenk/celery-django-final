from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
import time
import requests
from .tasks import send_email_celery, send_telegram_celery


bot_token = 'your telegram bot token'
chat_id = ['id1', 'id2']
message = "Hello from FogsDemy в тележеньку"


def index(request):
    return render(request, 'app/index.html')

@csrf_exempt
def button(request):
    if request.method == 'POST':
        start = time.time()
        print('Нажали кнопку')
        # send_email(request)
        send_email_celery.delay()
        # send_telegram(bot_token, chat_id, message)
        send_telegram_celery.delay(bot_token, chat_id, message)
        finish = time.time()
        print(f'запрос обработан за {finish - start} секунд')
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})


def send_email(request):
    subject = 'FogsDemy lesson'
    email_from = 'email_from'
    message = 'Поздравляю с окончанием блока Celery!'
    recipient_list = ['email_number_one', 'another_emails']
    send_mail(subject, message, email_from, recipient_list)
    time.sleep(10)
    print('письмо ушло, запись в лог')
    return HttpResponse('ok')


def send_telegram(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    for chat in chat_id:
        data = {
            "chat_id": chat,
            "text": message
        }
        time.sleep(10)
        requests.post(url, data=data)
    print('сообщение в телегу ушло, запись в лог')

