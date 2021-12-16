import uvicorn

from fastapi import FastAPI, HTTPException, status
# from fastapi.testclient import TestClient

from config import config

from info import router as info_router
from send_probe import router as send_probe

routers = [
    info_router,
    send_probe
]



app = FastAPI()
# testclient = TestClient(app)

@app.get('/', tags=['General'])
def read_root():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no root url")


# including routes from our views
for r in routers:
    app.include_router(r)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run('main:app', host=config.HOST, port=config.PORT, reload=True, app_dir='src')

if __name__ == '__main__':
    start()