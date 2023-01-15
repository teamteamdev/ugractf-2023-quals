FROM python:alpine
RUN pip3 install Pillow
RUN mkdir /root/output
COPY pic.jpg jb-mono.ttf add_flag.py run.sh /root
CMD /root/run.sh
