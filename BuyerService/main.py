from fastapi import FastAPI
from endpoints import router
from container import Container
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router with endpoints
app.include_router(router)

# Wire the container for dependency injection
@app.on_event("startup")
async def startup():
    container = Container()
    container.config.from_env_file(".env")  # If using environment variables
