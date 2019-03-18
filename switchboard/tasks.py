from switchboard.models import Registry, SearchQuery
import requests
import logging
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.cache import caches
import json
import time


class SearchQueryStatusLogger(object):
    ''' A helper class to update status of the Search Query '''

    def __init__(self, registries):
        # status = 0 = Failure , 1 = Success , 2 = Warning
        self.registriesOperationsLog = {}
        for idx, r in enumerate(registries):
            x = {'status':2, 'errors':[],'warnings':[], 'info':[], 'debug':[], 'success':[], 'statustext':"" }
            self.registriesOperationsLog[str(r.id)] = x
        self.current_milli_time = lambda: int(round(time.time() * 1000))
    
    def add_warning(self, registry_id, msg):
        self.registriesOperationsLog[registry_id]['warnings'].append({'msg':msg,'time':self.current_milli_time()})

    def add_success(self, registry_id, msg):
        self.registriesOperationsLog[registry_id]['success'].append({'msg':msg,'time':self.current_milli_time()})
        
    def add_error(self, registry_id, msg):
        self.registriesOperationsLog[registry_id]['errors'].append({'msg':msg,'time':self.current_milli_time()})
        
    def add_info(self, registry_id, msg):
        self.registriesOperationsLog[registry_id]['info'].append({'msg':msg,'time':self.current_milli_time()})

    def add_debug(self, registry_id, msg):
        self.registriesOperationsLog[registry_id]['debug'].append({'msg':msg,'time':self.current_milli_time()})

    def set_statustext(self, registry_id, msg):
        self.registriesOperationsLog[registry_id]['statustext'] = msg

    def set_status(self, registry_id, status, statustext=None):
        self.registriesOperationsLog[registry_id]['status']= status
        if statustext:
            self.registriesOperationsLog[registry_id]['statustext']= statustext

    def get_all_status(self):
        allstatus = {}
        for stage, results in self.registriesOperationsLog.items():
            allstatus[stage] = results['status']
        return allstatus


    def get_allstatuses(self):
        
        return json.dumps(self.registriesOperationsLog)



class BrokerManager(object):
    ''' A helper class to query different registries ''' 
    
    def __init__(self, query_type, query_parameter, query, credentials):
        self.query_type = query_type
        self.query_parameter = query_parameter
        self.query = query      
        self.credentials = credentials

    def get_endpoint(self, registry_endpoint):
        parameter_endpoint = {0: '/operators/', 1: '/rpas/', 2:'/pilot/'}
        query_url = registry_endpoint + parameter_endpoint[self.query_parameter]
        return query_url

    def search_registry(self, registry, logger):
        registry_id = str(registry.id)
        registry_endpoint = registry.endpoint
        url_to_query = self.get_endpoint(registry_endpoint = registry_endpoint)
        url_to_query = url_to_query + self.query
        bearer_token = "Bearer " + self.credentials
        headers = {"Authorization": bearer_token}

        # query different registries
        try:
            r = requests.get(url_to_query, headers = headers)
        except requests.exceptions.ConnectionError as ce:
            logger.add_error(registry_id = registry_id , msg = "Connection error %s" % ce)
        except requests.exceptions.Timeout as te:
            logger.add_error(registry_id = registry_id , msg = "Timout error %s" % te)
   
        else:
            if r.status_code == 200:  
                logger.add_success(registry_id = registry_id , msg = "Registry data retrieved") 
                return r.json()
                
            else: 
                pass


@task(name="QueryRegistries")
def QueryRegistries(jobid):
    sq = SearchQuery.objects.get(id = jobid)

    registries = Registry.objects.all()
    
    myOpsLogger = SearchQueryStatusLogger(registries)
    
    myBrokerHelper = BrokerManager( query_type = sq.query_type, query_parameter= sq.query_parameter, query = sq.query, credentials = sq.credentials)
                
    res = []
    for registry in registries:
        results = myBrokerHelper.search_registry(registry = registry,logger = myOpsLogger)      
        if results and results['id']:  
            res.append(results)
        else:
            myOpsLogger.add_warning(registry_id = str(registry.id), msg= "Data returned but does not contain the ID")

    sq.results = res
    sq.logs = myOpsLogger.get_allstatuses()
    sq.save()


@task(name="Add")
def Add(x, y):
    return x + y