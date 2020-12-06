from flask import Flask, render_template, jsonify, redirect, request, Response
import requests as rq
from flask_restful import Api
import json
import pandas as pd
# Creates the Flask application object
app = Flask(__name__)
api = Api(app)

# Starts the debugger
app.config["DEBUG"] = True


# routing
@app.route('/', methods=['GET'])
def home():
    req = rq.get('https://disease.sh/v3/covid-19/historical/')
    # data = req.content
    # print(data)
    json_data = json.loads(req.content)
    return render_template('home.html', data=json_data)


@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(500)
def http_error_handler(e):
    return Response('{}')


# newCasesPeak - Returns the date (and value) of the highest peak of new Covid-19 cases
# in the last 30 days for a required country.
@app.route('/newCasesPeak', methods=['POST', 'GET'])
def add_newcasespeak():
    try:
        country = request.args.get('country', type=str)
        url = 'https://disease.sh/v3/covid-19/historical/' + country + '?lastdays=31'
        req = rq.get(url)
        timeline = json.loads(req.text)['timeline']
        df = pd.DataFrame.from_dict(timeline)
        df['date'] = df.index
        df['value'] = df['cases']
        df['value'] = df['value'].diff()
        output = df.loc[df['value'].idxmax()]
        output['country'] = country
        output['method'] = 'newCasesPeak'
        output = output[['country', 'method', 'date', 'value']]
        # print(output)
        json_data = output.to_json(orient="index")
        return Response(json_data.replace('\/', '/'))
    except:
        return Response('{}')


# recoveredPeak - Returns the date (and value) of the highest peak of recovered Covid-19 cases
# in the last 30 days for the required country.
@app.route('/RecoveredPeak', methods=['POST', 'GET'])
def add_recoveredpeak():
    try:
        country = request.args.get('country', type=str)
        url = 'https://disease.sh/v3/covid-19/historical/' + country + '?lastdays=31'
        req = rq.get(url)
        timeline = json.loads(req.text)['timeline']
        df = pd.DataFrame.from_dict(timeline)
        print(df)
        df['date'] = df.index
        df['value'] = df['recovered']
        df['value'] = df['value'].diff()
        output = df.loc[df['recovered'].idxmax()]
        output['country'] = country
        output['method'] = 'RecoveredPeak'
        output = output[['country', 'method', 'date', 'recovered']]
        json_data = output.to_json(orient="index")
        return Response(json_data.replace('\/', '/'))
    except:
        return Response('{}')


# deathsPeak - Returns the date (and value) of the highest peak of death Covid-19 cases
# in the last 30 days for a required country.
@app.route('/DeathsPeak', methods=['POST', 'GET'])
def add_deathspeak():
    try:
        country = request.args.get('country', type=str)
        url = 'https://disease.sh/v3/covid-19/historical/' + country + '?lastdays=31'
        req = rq.get(url)
        timeline = json.loads(req.text)['timeline']
        df = pd.DataFrame.from_dict(timeline)
        df['date'] = df.index
        df['value'] = df['deaths']
        df['value'] = df['value'].diff()
        output = df.loc[df['value'].idxmax()]
        output['country'] = country
        output['method'] = 'DeathsPeak'
        output = output[['country', 'method', 'date', 'value']]
        json_data = output.to_json(orient="index")
        return Response(json_data.replace('\/', '/'))
    except:
        return Response('{}')


# status - Returns a value of success / fail to contact the backend API
@app.route('/status', methods=['GET'])
def add_status():
    headers = {'Content-Type': 'application/json'}
    url = 'https://disease.sh/v3/covid-19/historical/'
    response = rq.get(url, headers=headers)

    if (response.status_code == 200):
        return json.dumps({'status': 'success'})

        # Code here will only run if the request is successful
    elif (response.status_code == 404):
        return json.dumps({'status': 'failure'})


app.run(host='127.0.0.1', port=3000)
