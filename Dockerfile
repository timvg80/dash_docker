FROM python:3.7.2-slim-stretch

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./financial_time_series_plots.py ./

CMD ["python", "financial_time_series_plots.py"]
