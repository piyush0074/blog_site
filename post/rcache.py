import redis
import settings
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=0)


def readytoset(post_id,un,user_id,post):
	#redis_instance = redis.Redis()
	if not redis_instance.keys('*'):
		print("hi")
	else :
		redis_instance.rpush('yo',post_id,un,user_id,post,60)
		print("\n cache:")
		print(redis_instance.lrange('yo', 0,-1))
		print("\n")
	return redis_instance.lrange('yo',0,-1)




print("enter post id, user name,user id,post")
post_id =input()
un= input()
user_id=input()
post=input()
readytoset(post_id,un,user_id,post)
#redis_instance.blpop('yo')
#redis_instance.blpop('yo')
#redis_instance.blpop('yo')
#redis_instance.blpop('yo')
#print(redis_instance.lrange('yo',0,-1))

