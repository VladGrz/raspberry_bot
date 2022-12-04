import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # take environment variables from .env.

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Token for bot
# NASA_TOKEN = os.getenv('NASA_TOKEN')  # Token for NASA API
# MONGO_CLIENT = os.getenv('MONGO_CLIENT')  # Connection string to connect to MongoDB database
