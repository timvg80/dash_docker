FROM python:3.7.2-slim-stretch

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
COPY ./runner.py .

EXPOSE 8050

CMD ["gunicorn", "-b", ":8050", "runner:app.server"]
