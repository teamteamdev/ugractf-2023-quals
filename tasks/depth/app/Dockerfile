FROM imachug/kyzylborda_lib
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install gunicorn
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Nginx prevents DoS by a long request line
CMD ["gunicorn", "-b", "unix:/tmp/app.sock", "--limit-request-line", "0", "server:make_app(\"/state\")"]
