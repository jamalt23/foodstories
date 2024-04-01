from django.contrib import admin
from core.models import *

admin.site.register([Post, Category, Comment, Tag, Contact, Subscribe,])
