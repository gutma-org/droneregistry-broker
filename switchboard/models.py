from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _
import string, random 
from django.core.validators import RegexValidator

class Registry(models.Model):
    
    VERSION_CHOICES = ((0, _('NA')),(1, _('GUTMA_V1')),(2, _('GUTMA_V2')),)
    AUTHENTICATION_METHOD_CHOICES = ((0, _('None')),(1, _('JWT')),(2, _('TOKEN')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint = models.URLField()
    api_version = models.IntegerField(_('version'),choices=VERSION_CHOICES)
    authentication = models.IntegerField(choices = AUTHENTICATION_METHOD_CHOICES, default = 0)

    def __str__(self):
        return self.endpoint
    def __repr__(self):
        return self.__str__()
    def __uniode__(self):
        return self.__str__()

# A class to store credentials
# class SercureStorage(models.Model):
    # registry = models.ForeignKey(Registry, models.CASACADE)

class SearchQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = ((0, _('Regular')),(1, _('Privileged')),)
    PARAMETER_CHOICES = ((0, _('Operator ID')),(1, _('RPAS ID')),(2, _('Pilot ID')),)
    STATE_CHOICES = ((0, _('PENDING')),(1, _('RECEIVED')),(2, _('STARTED')),(3, _('SUCCESS')),(4, _('RETRY')),(5, _('IGNORED')),)
    
    query = models.CharField(max_length=140)
    query_type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    query_parameter = models.IntegerField(choices=PARAMETER_CHOICES, default=0)
    credentials = models.TextField(default = '')
    more_information_url = models.URLField(blank= True, null=True, default = '')
    state = models.IntegerField(_('state'),choices=STATE_CHOICES, default = 0)
    results = models.TextField(default="Querying registries, this will populate once all queries are complete..")
    logs = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state
    def __repr__(self):
        return self.__str__()
    def __uniode__(self):
        return self.__str__()
 
 