# -*- coding: utf-8 -*-

from peewee import *
from cliez.conf import settings


class URLField(CharField):
    extra_type = 'url'

    pass


class ModelA(Model):
    CHOICES = (
        (1, 'choice1'),
        (2, 'choice2'),
        (3, 'choice3')
    )

    col1 = IntegerField(verbose_name='column1', choices=CHOICES, help_text="this is column 1")
    col2 = CharField(verbose_name='column2', help_text='this is column2', max_length='10')
    col3 = URLField(verbose_name='url', help_text='set url for frontend', max_length='10')

    class Meta:
        database = settings().app.config['DATABASE']
        db_table = 'table_1'
        pass

    pass


class ModelB(Model):
    CHOICES = (
        (1, 'choice1'),
        (2, 'choice2'),
        (3, 'choice3')
    )

    col1 = IntegerField(verbose_name='column1', choices=CHOICES, help_text="this is column 1")
    col2 = CharField(verbose_name='column2', help_text='this is column2', max_length='10')
    col3 = URLField(verbose_name='url', help_text='set url for frontend', max_length='10')

    class Meta:
        database = settings().app.config['DATABASE']
        db_table = 'table_2'
        pass

    pass


from mongoengine import *


class ModelC(Document):
    CHOICES = (
        (1, 'choice1'),
        (2, 'choice2'),
        (3, 'choice3')
    )

    col1 = IntField(verbose_name='use verbose too', help_text='hello', choices=CHOICES)
    col2 = StringField(verbose_name='use verbose same peewee', max_length='10', help_text='hihi')

    pass
