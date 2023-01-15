FROM python:3-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./OpenSans-Light.ttf .
COPY questions.json .
COPY certificate.png .
CMD ["gunicorn", "-b", "unix:/tmp/app.sock", "server:make_app(\"/state\")"]
