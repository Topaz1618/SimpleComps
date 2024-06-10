
import os
from dotenv import load_dotenv


environment = os.getenv('ENVIRONMENT', 'dev')  # pre, prod

if environment == 'prod':
    load_dotenv('.env_prod')
elif environment == 'pre':
    load_dotenv('.env_pre')
else:
    load_dotenv('.env')


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_secret_key():
        SECRET_KEY = os.getenv('SECRET_KEY')
        return SECRET_KEY

    @staticmethod
    def get_database_uri():
        username = os.getenv('DATABASE_USERNAME')
        password = os.getenv('DATABASE_PASSWORD')
        hostname = os.getenv('DATABASE_HOSTNAME')
        database = os.getenv('DATABASE_NAME')

        return f'mysql+pymysql://{username}:{password}@{hostname}/{database}?charset=utf8mb4'


    @staticmethod
    def get_redis_uri():
        host = os.getenv('REDIS_HOST')
        port = os.getenv('REDIS_PORT')

        return host, port

    @staticmethod
    def get_google_credential():
        GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
        GOOGLE_SECRET = os.getenv('GOOGLE_SECRET')
        REDIRECT_URI = os.getenv('REDIRECT_URI')
        AUTHORIZATION_URI = os.getenv('AUTHORIZATION_URI')
        TOKEN_URI = os.getenv('TOKEN_URI')

        return GOOGLE_CLIENT_ID, GOOGLE_SECRET, REDIRECT_URI, AUTHORIZATION_URI, TOKEN_URI


if __name__ == "__main__":
    redis_host, redis_port = Config.get_redis_uri()
    # import redis
    # r = redis.Redis(host=redis_host, port=redis_port)
    # r.set("a", 1)
    # print(r.get("a"))
