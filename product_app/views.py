# product_app/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from product_app.models import Product
from product_app.serializers import ProductSerializer
from elasticsearch import Elasticsearch
from product_app.tasks import add_product_to_elasticsearch, update_product_in_elasticsearch, delete_product_from_elasticsearch

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        add_product_to_elasticsearch.delay(instance.id)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        update_product_in_elasticsearch.delay(instance.id)

    def perform_destroy(self, instance):
        delete_product_from_elasticsearch.delay(instance.id)
        instance.delete()

class ProductSearchView(APIView):
    def get(self, request):
        elasticsearch_conf = settings.ELASTICSEARCH_DSL['default']  # get configration of elastic search from settings.py
        # Connect to Elasticsearch 
        es = Elasticsearch(hosts=elasticsearch_conf['hosts'],   
                           basic_auth=elasticsearch_conf['basic_auth'],
                           verify_certs= elasticsearch_conf['verify_certs'])
        search_term = request.GET.get('q', None)    # get query parameter from url 
        if search_term:     # check query null or not
            fields = ['size', 'name', 'description', 'color']   # search query/toekn/term in this field
            # make elastic search query
            body = {
                'query': {
                    'multi_match': {
                        'query': search_term,
                        'fields': fields
                    }
                }
            }
            response = es.search(index='products', body=body)  # give index name when you give at index creation time
            total_record = response['hits']['total']['value']
            # if total record is 0 then give message.
            if total_record == 0:   
                return Response({"message": "No products found!"})
            product_data = response['hits']['hits'][0]['_source']  # get all products data
            return Response(product_data)
        else:
            return Response({"message":"Query not found!"})