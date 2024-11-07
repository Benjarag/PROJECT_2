import uvicorn
from fastapi import FastAPI
import endpoints  # Make sure this imports your endpoints

def create_app() -> FastAPI:
    # Create the FastAPI app
    app = FastAPI()

    # Include the endpoints router
    app.include_router(endpoints.router)

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    uvicorn.run('application:app', host='0.0.0.0', port=8002, reload=True)
