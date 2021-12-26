import uvicorn

# from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, status

# from fastapi.testclient import TestClient

# from repeated_timer import RepeatedTimer

from config import config

from views.info import router as info_router
from views.probe import router as send_probe

from probe_manager import ProbeManager

from apscheduler.schedulers.background import BackgroundScheduler

# from apscheduler.schedulers.blocking import BlockingScheduler

# load_dotenv(dotenv_path=config.SECRETS_ENV_PATH)

routers = [info_router, send_probe]

pm = ProbeManager()


def timer_tick():
    pm.check_all()


scheduler = BackgroundScheduler(timezone=config.TZ)
scheduler.add_job(timer_tick, "interval", seconds=config.CHECKS_TICK_INTERVAL)

app = FastAPI()
# testclient = TestClient(app)


@app.get("/", tags=["General"])
def read_root():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no root url")


# including routes from our views
for r in routers:
    app.include_router(r)


def start_uvicorn_server():
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.SERVER_WATCH_FILES,
        app_dir=config.ENTRYPOINT.parent,
    )
    pm.check_all()


if __name__ == "__main__":
    scheduler.start()
    start_uvicorn_server()
