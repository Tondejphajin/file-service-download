from utils.redis_utils import RedisClient

redis_client = RedisClient()
p = redis_client.client.pubsub()

p.psubscribe("__keyevent@0__:expired")

while True:
    message = p.get_message()
    if message:
        print(message)
        key_expired = message["data"]
        print("Key expired: ", key_expired)
        break

