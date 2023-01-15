FROM python:3-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./comic-sans.ttf /tmp/
RUN mkdir -p /usr/share/fonts/truetype/
RUN install -m644 /tmp/comic-sans.ttf /usr/share/fonts/truetype/
RUN rm /tmp/comic-sans.ttf
CMD ["gunicorn", "-b", "unix:/tmp/app.sock", "server:make_app(\"/state\")"]
