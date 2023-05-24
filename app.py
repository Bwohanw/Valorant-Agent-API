from flask import Flask, render_template, request, send_file, make_response
import requests
from PIL import Image
import urllib.request
from io import BytesIO
import os

app = Flask(__name__)


agent_uuid = {}
r = requests.get("https://valorant-api.com/v1/agents")
for entry in r.json()['data']:
    if entry['isPlayableCharacter']:
        agent_uuid[entry['displayName']] = entry['uuid']

print(agent_uuid)
print(len(agent_uuid))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agent', methods=['GET','POST'])
def getagentinfo():
    try:
        agentname = request.form['name'].title()
    except:
        return render_template('404.html')
    info_to_get = []
    try:
        info_to_get.append(request.form['role'])
    except:
        pass
    try:
        info_to_get.append(request.form['description'])
    except:
        pass
    try:
        info_to_get.append(request.form['ability'])
    except:
        pass
    print(agentname)
    r = requests.get("https://valorant-api.com/v1/agents/" + agent_uuid[agentname])
    agentdata = r.json()['data']
    urllib.request.urlretrieve(agentdata['displayIcon'], "out.png")
    with open('out.png', 'rb') as f:
        buffer = f.read()
    os.remove('out.png')
    return send_file(BytesIO(buffer), mimetype='image/png')
    return "success", 200