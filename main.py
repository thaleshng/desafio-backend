from database import app
from app.controllers.pessoa_controller import router as pessoa_router

app.include_router(pessoa_router)