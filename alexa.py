from flask import Flask, render_template
from flask_ask import Ask, statement, question, convert_errors
import requests
import json
import logging

app = Flask(__name__)
ask = Ask(app, '/')
app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.748c8f2a-ce88-4275-9c40-af3adcd3090a'
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@app.route('/')
def index():
    return 'welcome to my site.'

@ask.launch
def launch_intent():
    speech = render_template('welcome')
    return question(speech)

@ask.intent('AMAZON.HelpIntent')
def help_intent():
    speech = render_template('help')
    return question(speech)

@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    speech = render_template('bye')
    return statement(speech)

@ask.intent('AMAZON.StopIntent')
def stop_intent():
    return cancel_intent()

@ask.intent('FactIntent')
def fact_intent(number):
    try:
        fact_number = int(number)
        URL = "http://numbersapi.com/{}".format(fact_number)
        response = requests.get(URL).json()
        if response.status_code != 200:
            speech = render_template('no_fact', number=number)
            return statement(speech)
        else:
            speech = response.content
            return statement(speech)
    except ValueError:
        speech = render_template('need_number')
        again = render_template('need_number_prompt')
        return question(speech).reprompt(again)

if __name__ == '__main__':
    app.run(debug=True)