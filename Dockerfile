FROM tiangolo/uvicorn-gunicorn-fastapi:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python"]

CMD [ "./sandbox_notification/app.py" ]