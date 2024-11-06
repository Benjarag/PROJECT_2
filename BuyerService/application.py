import uvicorn
from fastapi import FastAPI
from container import Container
import endpoints

def create_app():
    container = Container()
    container.wire(modules=[endpoints])
    app = FastAPI()
    container.wire(modules=[endpoints])
    app.include_router(endpoints.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run('application:app', host='0.0.0.0', port=8002, reload=True)