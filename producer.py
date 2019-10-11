import os
import re
import socket

from kafka import KafkaProducer
from json import dumps

from flask import Flask, jsonify, request, render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


class ReusableForm(Form):
    user_id = TextField('Please enter your identificator:', validators=[validators.DataRequired()])


# Instantiate our Node
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/", methods=['GET', 'POST'])
def handle_input():
    # Get node name and pod IP address, then pass it to the template
    strNodeName = os.environ['NODE_NAME']
    strPodIP = os.environ['POD_IP']
    strKafkaHost = os.environ['KAFKA_SERVICE_HOST']
    strKafkaPort = os.environ['KAFKA_SERVICE_PORT']
    strTopicName = os.environ['KAFKA_TOPIC']

    flash(strNodeName)
    flash(strPodIP)

    producer = KafkaProducer(bootstrap_servers=[strKafkaHost + ':' + strKafkaPort],
                            value_serializer=lambda x: dumps(x).encode('utf-8'))
    
    # Proceed to the form
    form = ReusableForm(request.form)
 
    print(form.errors)
    
    if (request.method == 'POST'):
        strUserId = request.form['user_id']
 
        if (form.validate()):
            data = {'userId': strUserId, 'nodeName': strNodeName, 'podIP': strPodIP}
            future = producer.send(strTopicName, value=data)
            mt = future.get(timeout=10)
            print(mt.topic, mt.partition, mt.offset)

            flash('Thank you. Your id was sent to the database!')
        else:
            flash('Please enter some id. The input field must not be empty.')
 
    return render_template('handle_input.html', form=form)

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000)

