FROM python:3.11

COPY . /app
WORKDIR /app
# EXPOSE 5001

# install poetry and dependencies
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python
ENV PATH "/etc/poetry/venv/bin/:${PATH}"
RUN poetry install --no-root

# run server
CMD ["poetry", "run", "python", "src/main.py"]

# docker build -t ress/monitoress .
# docker run ress/monitoress