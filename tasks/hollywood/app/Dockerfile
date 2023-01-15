FROM imachug/kyzylborda_lib
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install uvicorn
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["uvicorn", "--uds", "/tmp/app.sock", "--factory", "server:make_app"]
