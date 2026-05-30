from fastapi import FastAPI
from dotenv import load_dotenv
from constants.common import ENV_FILE_PATH
import os
from routes.user_route import user_router
# Load .env
load_dotenv(dotenv_path=ENV_FILE_PATH, override=True)
from db.main import engine,Base
# Import models so SQLAlchemy registers tables
import models.User
# Import controller so routes register
import controllers.user_controller
# Create all tables in MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(user_router)

