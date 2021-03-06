import json

import pika

from django_backend.settings import CLOUDAMQP_URL
from products.models import Product

params = pika.URLParameters(CLOUDAMQP_URL)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    data = json.dumps(body)
    channel.basic_publish(
        exchange='', routing_key='flask', properties=properties, body=data)
    print("[x] Sent message in django " + str(data))
