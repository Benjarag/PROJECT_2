import uvicorn
from fastapi import FastAPI
from endpoints import router  # Now we import router directly from endpoints

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)  # Directly register the router here
    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001, reload=True)