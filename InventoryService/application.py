import uvicorn
from fastapi import FastAPI
import endpoints  

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(endpoints.router)

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('application:app', host='0.0.0.0', port=8003, reload=True)
