FROM python:2.7.16-alpine3.9

WORKDIR /root

RUN pip install flask
RUN pip install wtforms
RUN pip install kafka-python

RUN mkdir templates
COPY handle_input.html templates/handle_input.html
COPY producer.py producer.py

ENV FLASK_APP producer.py

ENTRYPOINT ["flask", "run"]
CMD ["--host=0.0.0.0"]
