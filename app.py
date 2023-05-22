from flask import Flask, render_template, request
import requests

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
    agentname = request.form['name'].title()
    print(agentname)
    r = requests.get("https://valorant-api.com/v1/agents/" + agent_uuid[agentname])
    data = r.json()['data']
    return data['description']
    return "success", 200