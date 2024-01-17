from casual import create_app
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".flaskenv")

app = application = create_app()
