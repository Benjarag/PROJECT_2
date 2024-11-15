import uvicorn
from fastapi import FastAPI
from endpoints import router  

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router) 
    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001, reload=True)
