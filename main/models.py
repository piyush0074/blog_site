from django.db import models
from django.utils import timezone
import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
	post_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.TextField(max_length=500)
	like = models.IntegerField(default=0)
	dislike = models.IntegerField(default=0)
	post_published = models.DateField(("Date"), default=datetime.date.today)
	post_time = models.TimeField(("Time"),default=now)


class Comments(models.Model):
	post_id = models.BigIntegerField(null=False)
	comment_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=True,related_name='user')
	comment = models.CharField(max_length=100,null='False')
	comment_date = models.DateField(("Date"),default=datetime.date.today)
	comment_time = models.TimeField(("Time"),default=now)

class LikeDislike(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post_id = models.IntegerField(null='False')
	value = models.IntegerField(default=0)
