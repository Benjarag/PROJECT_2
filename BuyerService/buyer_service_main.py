import uvicorn
from fastapi import FastAPI
from buyer_service_container import Container
import buyer_service_endpoints as endpoints  

def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8002, reload=True)
