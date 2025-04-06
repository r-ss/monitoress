# monitoress

Personal service for gathering health status from my servers and apps. Provides API for status information and notifications in my telegram if some of the monitored items fails.

Implemented in Python on [FastAPI](https://fastapi.tiangolo.com) and [Pydantic](https://pydantic-docs.helpmanual.io)

Also have a frontend part in repo [status.ress.ws](https://github.com/r-ss/status.ress.ws)

Deployed to fold VDS @ Hetzner.

To deploy code:
rsync -e 'ssh' -thvr --progress --delete-after --exclude='.git' --exclude='.venv' --exclude='__pycache__' monitoress ress@fold:~/

To run:
1. create tmux session "monitoress"
2. ~/.local/bin/poetry run python src/main.py