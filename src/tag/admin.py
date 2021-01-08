from django.contrib import admin


from .models import PostTag, PostTagRelation

admin.site.register(PostTag)
admin.site.register(PostTagRelation)
