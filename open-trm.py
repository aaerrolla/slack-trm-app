import os
import requests  
from flask import abort, Flask, json, jsonify, request, make_response

app = Flask(__name__)

def is_request_valid(request):
    print(request.form)
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']
    return is_token_valid and is_team_id_valid

@app.route('/open-trm', methods=['POST'])
def open_trm():
    if not is_request_valid(request):
        abort(400)
    trigger_id = request.form.get('trigger_id')
    api_url = 'https://slack.com/api/dialog.open'

    dialog = {
        "callback_id": "ryde-46e2b0",
        "title": "TRM Information",
        "submit_label": "Send",
        "notify_on_cancel": True,                 
        "elements": [
            {
                "type": "text",
                "label": "1. Incident Number",
                "name": "in_number"
            },
            {
                "type": "text",
                "label": "2. On Call PDL",
                "name": "oncall_pdl"
            }
        ]
    }

    api_data = {
        "token": os.environ['SLACK_TOKEN'],
        "trigger_id": trigger_id,
        "dialog": json.dumps(dialog)
    }

    res = requests.post(api_url, data=api_data)
    print(res.content)

    return make_response()

   
@app.route('/send-trm', methods=['POST'])
def send_trm():
    api_url = 'https://slack.com/api/chat.postMessage'
    payload = request.form.getlist('payload')

    json_data = json.loads(payload[0])
    fields = dict( json_data["submission"])
    data = f"New TRM Submitted.  \n  INC Number   ->  {fields['in_number']} \n On Call PDL  ->  {fields['oncall_pdl']}" 
		                
    api_data =  {"token": os.environ['SLACK_TOKEN'], "channel": "CMP7D1NMP", "as_user": "true", "reply_broadcast":"true",	 "text": data }
    
    requests.post(api_url, data=api_data)
    
    return make_response()
