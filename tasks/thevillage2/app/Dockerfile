FROM imachug/kyzylborda_lib

WORKDIR /app
RUN pip install --no-cache poetry
COPY pyproject.toml poetry.lock /app/
COPY villageblog/__init__.py /app/villageblog/
RUN poetry config virtualenvs.create false && poetry install -n --no-cache --only main

COPY villageblog /app/villageblog

CMD ["uvicorn", "--uds", "/tmp/app.sock", "villageblog.app:app", "--proxy-headers", "--no-access-log", "--forwarded-allow-ips=*"]
