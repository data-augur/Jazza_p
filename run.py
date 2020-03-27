import os

from src.app import create_app
from dotenv import load_dotenv
load_dotenv()


env_name = "production"
app = create_app(env_name)
  # run app
if __name__ == '__main__':  
	app.run(host='0.0.0.0')
