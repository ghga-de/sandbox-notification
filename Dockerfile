FROM python:3.9-slim

WORKDIR /service

COPY . /service

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD [ "./src/app.py" ]