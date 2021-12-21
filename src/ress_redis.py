import redis

class RessRedisAbstraction:

    def __init__(self, host='localhost', port=6379, db=2):
        self.r = redis.Redis(host=host, port=port, db=db)

    def get(self, k):
        v = self.r.get(k)
        if v:
            if v.decode() == 'None':
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
docker run -d -p 6379:6379 --name redis-server redis

docker exec -it redis-server redis-cli




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