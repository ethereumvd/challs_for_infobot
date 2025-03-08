FROM alpine:latest

RUN apk add --no-cache openssh-server python3

COPY chall.py run.sh readme.txt /root

EXPOSE 22

CMD ["/root/run.sh"]
