import uvicorn
from fastapi import FastAPI
import endpoints 

def initialize_app() -> FastAPI:

    App = FastAPI()

    
    App.include_router(endpoints.router)

    return App


App = initialize_app()

if __name__ == '__main__':
    uvicorn.run('application:app', host='0.0.0.0', port=8003, reload=True)
