from __future__ import absolute_import, unicode_literals
from celery import task


@task()
def get_card_list():
    print('HELLO')
