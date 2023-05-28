import os
import dotenv


dotenv.load_dotenv("etc/secrets/.env")

TG_KEY = os.environ["TG_KEY"]

GPT_KEY = os.environ["GPT_KEY"]
