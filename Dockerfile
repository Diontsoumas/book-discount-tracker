FROM python:3.6-alpine

copy . /app

WORKDIR /app

ENV PKGS=''
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run.py"]