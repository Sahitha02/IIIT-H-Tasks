import dramatiq
from dramatiq.brokers.redis import RedisBroker

# Configure Redis broker
redis_broker = RedisBroker(url="redis://localhost:6379/0")
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def log_action(user_id, action):
    print(f"[ASYNC LOG] User {user_id} performed: {action}")