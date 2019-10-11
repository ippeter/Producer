FROM python:2.7.16-alpine3.9

WORKDIR /producer

RUN mkdir templates
COPY handle_input.html templates/
COPY producer.py .
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --trusted-host pypi.python.org -r requirements.txt

ENV FLASK_APP producer.py

CMD ["python", "producer.py"]
