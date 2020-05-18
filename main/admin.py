from django.contrib import admin
from .models import Post,Comments,LikeDislike

# Register your models here.


admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(LikeDislike)
