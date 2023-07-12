from celery import Celery

routes = ["localhost","b_redis"]
for route in routes:
    try:
        celery = Celery(broker=f'redis://{route}:6379')
        print(f"redis connect to {route} success")
    except Exception as e:
        print("redis connect all fail")
        print(e)

