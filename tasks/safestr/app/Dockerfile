FROM ubuntu:22.04
RUN apt-get update && apt-get install -y gcc socat
COPY safestr.c start.sh /app/
WORKDIR /app
ENTRYPOINT ["/app/start.sh"]
