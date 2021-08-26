import json
import os

import django
import pika

from django_backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')
django.setup()

from products.models import Product


params = pika.URLParameters(settings.CLOUDAMQP_URL)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='django')


def callback(ch, method, properties, body):
    print(" [x] Received in django " + str(body))
    id = json.loads(body)
    product = Product.objects.get(id=id)
    product.like += 1
    product.save()
    print('Product like increased!')


channel.basic_consume(
    queue='django', on_message_callback=callback, auto_ack=True)

print('[*] Waiting for messages in django:')
channel.start_consuming()
channel.close()
