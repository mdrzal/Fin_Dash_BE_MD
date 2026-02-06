import redis

# Singleton Redis client for the app
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
