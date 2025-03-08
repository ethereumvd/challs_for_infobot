FROM python:3.9-slim 

WORKDIR /diff

COPY . /diff

EXPOSE 7249

CMD ["python3" , "/diff/chall.py"]
