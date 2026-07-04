from fastapi import FastAPI
from dotenv import load_dotenv

from constants.common import ENV_FILE_PATH

# LOAD ENV FIRST
load_dotenv(
    dotenv_path=ENV_FILE_PATH,
    override=True
)

from routes.user_route import user_router
from routes.auth_route import auth_router
from db.main import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from utils.response import (
    validation_exception_handler,
    http_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)

import models.User
import controllers.user_controller
import controllers.auth_controller

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from utils.rate_limit import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI()

import os

print(f"Worker Started: {os.getpid()}")

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)

# Serve frontend folder

app.mount(
    "/frontend",
    StaticFiles(
        directory="frontend"
    ),
    name="frontend"
)

# Redirect root URL to login page

@app.get("/")
def root():

    return RedirectResponse(
        url="/frontend/pages/login.html"
    )

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.include_router(user_router)
app.include_router(
    auth_router
)
from utils.security_headers import SecurityHeadersMiddleware

app.add_middleware(SecurityHeadersMiddleware)