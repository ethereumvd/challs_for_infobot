FROM alpine:latest

RUN apk add --no-cache openssh-server python3

COPY chall.py readme.txt run.sh /root

EXPOSE 22

CMD ["/root/run.sh"]
