# -*- coding: utf-8 -*-

from peewee import *
from cliez.conf import settings


class ModelA(Model):
    CHOICES = (
        (1, 'choice1'),
        (2, 'choice2'),
        (3, 'choice3')
    )

    col1 = IntegerField(verbose_name='column1', choices=CHOICES, help_text="this is column 1")
    col2 = CharField(verbose_name='column2', help_text='this is column2', max_length='10')

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

    class Meta:
        database = settings().app.config['DATABASE']
        db_table = 'table_2'
        pass

    pass





