import redis
import json

# Connect to Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def set_value(key, value):
    """
    Store simple key-value data
    """
    redis_client.set(key, value)


def get_value(key):
    """
    Retrieve stored value
    """
    return redis_client.get(key)


def delete_key(key):
    """
    Delete stored key
    """
    redis_client.delete(key)


def store_user_data(user_id, data):
    """
    Store user data as JSON
    """

    redis_client.set(
        f"user:{user_id}",
        json.dumps(data)
    )


def get_user_data(user_id):
    """
    Retrieve user data dictionary
    """

    data = redis_client.get(f"user:{user_id}")

    if data:
        return json.loads(data)

    return {}


def update_user_data(user_id, key, value):
    """
    Update a single field inside user memory
    """

    user_data = get_user_data(user_id)

    user_data[key] = value

    store_user_data(user_id, user_data)
