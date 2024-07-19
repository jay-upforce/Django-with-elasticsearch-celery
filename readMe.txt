Task:
-----
- create product model with name, description,size,capacity, color, price, quantity, image(upload multiple images) field.
- perform CRUD operation.
- when user insert/update/delete record at that time also record insert/update/delete in elastic search using Celery
- user can perform seach operation on name, description,size,capacity, color field using elastic search not data getting from DB.


Used Tools:
----------
- python
- django
- elastic search engine
- docker
- redis (celery)
- git
- postman - API testing collection


Project Structure:
-------------------
/project_folder
├── /DRF_elastic_celery_pro
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── /media
├── /product_app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── documents.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── readMe.txt
├── requirements.txt
├── Dockerfile
└── docker-compose.ymlxs


Elastic Search setup:
---------------------
- create model into models.py then makemigrate and migrate it.
- install elastic search lib = "django-elasticsearch-dsl".
- register in installed app of settings.py file.
- create document.py file and add model and field with elastic search settings.
- build index in elasticsearch using "python manage.py search_index --rebuild". 
Note: elasticsearch engine is running. (in this project i user docker image of elastic search so start docker "docker compose up")


celery to auto insert, update, delete, search in elastic search:
----------------------------------------------------------------
- create celery.py file in project_folder(like settings.py)
- add some configration in project_folder/__init__.py file
- add some configration related to celery into setting.py file 
- create tasks.py file to execute tasks related to elastic search
- add task module/function into views.py file.
- run celery "celery -A project_name worker -l info"


Run process:
------------
- start docker desktop app
- start elastic search from docker-compose file using "docker compose up" to run the docker image.
- now you can access elastic search and kibana at "http://localhost:9200" & "http://localhost:5601"
- now run makemigrations and migrate command in django terminal
- now run "python manage.py search_index --rebuild" command in django terminal to the initial index build we need to run:.
- start redis-server for executing celery task (after installtion use command in mac: brew services start redis)
- run "redis-cli ping" to check redis server running or not?
- run "celery -A DRF_elastic_celery_pro worker -l info" command into calery terminal to Start Celery worker
- run "python manage.py runserver" command in django terminal to run project.
