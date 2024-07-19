# product_app/tasks.py
from celery import shared_task
from elasticsearch import Elasticsearch
from .models import Product
from .documents import ProductDocument

@shared_task
def add_product_to_elasticsearch(product_id):   # add document in product index
    product = Product.objects.get(id=product_id)    # get product id from product table
    product_doc = ProductDocument(      # create document with passing their field
        meta={'id': product.id},
        id=product.id,
        name=product.name,
        description=product.description,
        size=product.size,
        color=product.color,
        capacity=product.capacity
    )
    product_doc.save()  # save document

@shared_task
def update_product_in_elasticsearch(product_id):    # update document in product index
    product = Product.objects.get(id=product_id)    # get product id from product table
    product_doc = ProductDocument.get(id=product.id)    # get document id for updating their data
    product_doc.name = product.name     # update name
    product_doc.description = product.description   # update description
    product_doc.size = product.size     
    product_doc.color = product.color
    product_doc.capacity = product.capacity
    product_doc.save()

@shared_task
def delete_product_from_elasticsearch(product_id):      # delete document in product index
    product_doc = ProductDocument.get(id=product_id)    # get document id
    product_doc.delete()    # delete document