import os
from dotenv import load_dotenv


IS_RUN_LIKE_A_DOCKER_CONTAINER = os.environ.get('RUN_LIKE_A_DOCKER_CONTAINER', False)
if not IS_RUN_LIKE_A_DOCKER_CONTAINER:
    load_dotenv('.env')
    load_dotenv('bot.env')

SETTINGS = {
    'POSTGRES_DB': os.environ['POSTGRES_DB'],

    'POSTGRES_HOST': os.environ['POSTGRES_IP']
    if IS_RUN_LIKE_A_DOCKER_CONTAINER
    else 'localhost',

    'POSTGRES_PORT': os.environ['DEFAULT_POSTGRES_PORT']
    if IS_RUN_LIKE_A_DOCKER_CONTAINER
    else os.environ['POSTGRES_PORT'],

    'POSTGRES_USER': os.environ['POSTGRES_USER'],
    'POSTGRES_PASSWORD': os.environ['POSTGRES_PASSWORD'],

    'TOKEN_BOT': os.environ['TOKEN_BOT']
}
