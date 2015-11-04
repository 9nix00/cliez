# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import uuid


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('username help text'),
                                validators=[
                                    validators.RegexValidator(r'^[A-Za-z][A-Za-z0-9_]{4,}', _('please input a valllida username.'), 'invalid')
                                ])

    email = models.EmailField(_('email'), unique=True)
    code = models.UUIDField(_('code'), default=uuid.uuid4, help_text='seed value')
    pass
