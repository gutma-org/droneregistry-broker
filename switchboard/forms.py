from django.forms import ModelForm
from .models import SearchQuery

class SearchQueryForm(ModelForm):
    
    class Meta:
        model = SearchQuery
        fields = ['query_parameter','query']
        