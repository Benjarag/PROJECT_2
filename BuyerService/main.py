
from fastapi import FastAPI, Depends
from BuyerApi.endpoints import router  # Import the router with the endpoints
from BuyerApi.container import Container  # Import the dependency injection container
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
    container.config.from_env_file(".env")  # Load environment variables
    container.wire(modules=["BuyerApi.endpoints"])  # Wire dependencies in the endpoints module
    app.container = container  # Attach the container to the app
