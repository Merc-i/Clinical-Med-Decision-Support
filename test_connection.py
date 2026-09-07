import os
from redis import Redis
import psycopg2  # pyright: ignore[reportMissingModuleSource]
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]  # This is used to load environment variables from a .env file

load_dotenv()

try:
    #Testing PostgreSQL connection
    connection = psycopg2.connect(
        dbname="ClinicalMed_db",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        host = "localhost",
        port = "5433"
    )
    print("Successfully connected to PostgreSQL")
    connection.close()
except Exception as e:
    print(f"Failed to connect to PostgreSQL: {e}")


try:
    #Testing Redis connection
    redis_url = os.getenv("REDIS_URL")
    redis_client = Redis.from_url(redis_url)
    if redis_client.ping():
        print("Successfully connected to Redis")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
    



