import uvicorn

# from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.testclient import TestClient

# from repeated_timer import RepeatedTimer

import asyncio


from config import config

from views.info import router as info_router
from views.probe import router as send_probe
from views.selftest import router as selftest_router

from probe_manager import ProbeManager

from apscheduler.schedulers.background import BackgroundScheduler

# from apscheduler.schedulers.blocking import BlockingScheduler

routers = [info_router, send_probe, selftest_router]

pm = ProbeManager()


def timer_tick():
    asyncio.run(pm.check_all())


scheduler = BackgroundScheduler(timezone=config.TZ)
scheduler.add_job(timer_tick, "interval", seconds=config.CHECKS_TICK_INTERVAL)

app = FastAPI()
testclient = TestClient(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def read_root():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no root url")


# including routes from our views
for r in routers:
    app.include_router(r)


def start_uvicorn_server():
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=config.SERVER_WATCH_FILES, app_dir=config.ENTRYPOINT.parent)
    # asyncio.run(pm.check_all())


if __name__ == "__main__":
    scheduler.start()
    start_uvicorn_server()
