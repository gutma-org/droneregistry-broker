from rest_framework import serializers
from switchboard.models import SearchQuery



class SearchQuerySerializer(serializers.ModelSerializer):
    ''' This is the default serializer for a Job '''
    class Meta:
        model = SearchQuery
        fields = ('id', 'query_type', 'query', 'query_parameter',
                   'results')
