#coding:utf-8
from os import path, listdir
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from core.manager import FakeDeleteManager
from core.manager import FakeDeleteModel

from utils import auto_code, read_json, dump_json
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext, ugettext_lazy as _
import os,shutil
import simplejson



class CGroup(Group):
    title = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'tcgroup'
        verbose_name  = _('group')
        verbose_name_plural = _('group')
