from fastapi import FastAPI
from src.routes.auth import router as auth_router
from src.routes.dashboard import router as dashboard_router
from src.routes.plans import router as plans_router

app = FastAPI()

app.include_router(dashboard_router) 
app.include_router(auth_router)
app.include_router(plans_router)










