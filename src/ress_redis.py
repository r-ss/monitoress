import redis

from config import config

class RessRedisAbstraction:
    def __init__(self, host="localhost", port=6379, db=0, password=None):
        self.r = redis.Redis(host=host, port=port, db=db, password=config.REDIS_PASS)

    def get(self, k):
        v = self.r.get(k)
        if v:
            if v.decode() == "None":
                return None
            return v.decode()
        return None

    def set(self, k, v):
        self.r.set(k, v)
        return True

    def incr(self, k):
        self.r.incr(k)
        return True

    def delete(self, k):
        self.r.delete(k)
        return True

    def ping(self):
        return self.r.ping()


"""

REDIS INSTALLATION

https://betterprogramming.pub/getting-started-with-redis-a-python-tutorial-3a18531a73a6



docker pull redis
docker run -d -p 6379:6379 -v /home/ress/redis_data:/data --name redis-server redis

docker exec -it redis-server redis-cli

Run without persistence:
docker run -d -p 6379:6379 --name redis-server redis --requirepass redisPassword


USAGE EXAMPLE

from ress_redis import RessRedisAbstraction as redis


r = redis()

r.set('hello', 'worlde') # True

value = r.get('hello')
print(value) # b'world'

r.delete('hello') # True
print(r.get('hello')) # None



CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                                       NAMES
876969d5b15e   redis     "docker-entrypoint.s…"   7 seconds ago   Up 7 seconds   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   redis-server


"""
