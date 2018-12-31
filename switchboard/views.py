import datetime
import json
from datetime import datetime
from django.views.generic.edit import FormView, CreateView
from .forms import SearchQueryForm
from django.http import JsonResponse
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils import translation
from django.views.generic import TemplateView
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authentication import (SessionAuthentication, TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse_lazy
from .models import SearchQuery
from .serializers import (SearchQuerySerializer)
from django.urls import reverse
from .tasks import QueryRegistries


class AjaxableResponseMixin:

    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

# Create your views here.

class HomeView(CreateView):

    template_name = 'switchboard/index.html'
    form_class = SearchQueryForm
    
   
    def get_success_url(self):	

        QueryRegistries.delay(jobid = self.object.id)
        content = {'Location': '/api/v1/' + self.object.id}
        return Response(content, status=status.HTTP_202_ACCEPTED)
        
        # return reverse('search_details',args=(self.object.id,))



class SearchDetails(mixins.RetrieveModelMixin,
				  generics.GenericAPIView):
	"""
	List all jobs in the database / return value for current job
	"""

	# authentication_classes = (SessionAuthentication,TokenAuthentication)
	# permission_classes = (IsAuthenticated,)

	queryset = SearchQuery.objects.all()
	serializer_class = SearchQuerySerializer


	def get(self, request, *args, **kwargs):
	    return self.retrieve(request, *args, **kwargs)
