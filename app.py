# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
import cloudscraper
import logging
import requests
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False  # Set to True if using HTTPS
)

# Store your cookies here - update when they expire
WELLFOUND_COOKIES = "ajs_anonymous_id=293ad58c-45fa-4907-a1c8-9949076b2e90; _ga=GA1.1.1493419389.1723635410; logged_in=true; _hjSessionUser_1444722=eyJpZCI6Ijc4NDY0MzZjLTk4NWEtNTU0Yy05MmQxLWJlMGViNzRjNzFjOCIsImNyZWF0ZWQiOjE3MjM2MzU0MTAwODMsImV4aXN0aW5nIjp0cnVlfQ==; ajs_user_id=17646086; _clck=1o9xbqr%7C2%7Cfoc%7C0%7C1687; _wellfound=00df4d6734e326e75085bee740ce6bc6.i; cf_clearance=ceLikvspAdazF7WPHJMpgVRgvXJ6Wa3AnxdmPrahLEU-1735450727-1.2.1.1-xBhh2J0qkYGFzNVzR.zTW8NzNHolGibrXzsMSIzCO0Go5VAeJNQjh27KW.p6Vc7dkpq76e1acxjQnLaUKdlrSEILHfWBXC8N3z2HtHo83ITzZFwd7nZoO9lFbH1TguOQYyPMFv9ZXFu3uQMu_SQXA2amuDoSaAHrjr4vjzc6k0_CQ_I3Qomv86qNV5mNJUHqghoX6TYtd0q1DOT5Kl4AVBc_iTObCxDpLdc2FijlW0Tqd71sLOg2IpR5hg1T_hDfy2Fap0MF8061VgeZuRtWDvzs4Zbrb_6VN4qVx8N8oBDTWW5L0qB3Fapn7UkC5vO.6y59hsZi3hOlZJqi7qPJY2eY_WTiiN1TyMX4SXy0EHZCuH4jOmwOQs9tCkY9QJPB; _hjSession_1444722=eyJpZCI6IjA2YjUwYmEyLTQ4ZTctNDFkNS1iMTdkLTY2YmI5M2NhNDUzMiIsImMiOjE3MzU0NTA3Mjg3NjMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==; datadome=ZfUPEWI~AG6NA0QJOcC5_51TccZR2HMXQYaU4S7tZrgEBCHrYvh1k_MY2VLTcPEm9OGRAWrm250Kh3hbYnn93kZzohxgzehV0_hg9bCWOIihKVLha0eHwbmz3TS7vv4C; _ga_705F94181H=GS1.1.1735450728.5.1.1735451974.59.0.0"
# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_wellfound_message(message, thread_id):
    url = 'https://wellfound.com/graphql'

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
        "accept-language": "en-US,en;q=0.5",
        'apollographql-client-name': 'talent-web',
        'content-type': 'application/json',
        'cookie': WELLFOUND_COOKIES,
        'origin': 'https://wellfound.com',
        'referer': f'https://wellfound.com/jobs/messages/{thread_id}',
        'x-apollo-operation-name': 'CandidateSendMessage',
        'x-requested-with': 'XMLHttpRequest',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Connection": "keep-alive"

    }

    payload = {
        "operationName": "CandidateSendMessage",
        "variables": {
            "input": {
                "id": thread_id,
                "type": "JOBPAIRING",
                "body": message
            }
        },
        "extensions": {
            "operationId": "tfe/1ee8d94da36a0811d05340d91a4427175dbb8abfafe2dab802483d375fdcfb7d"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        thread_id = "966644328"  # Your thread ID

        if not message:
            flash('Please enter a message', 'error')
            return redirect(url_for('index'))

        success, response = send_wellfound_message(message, thread_id)
        if success:
            flash('Message sent successfully!', 'success')
        else:
            flash(f'Error sending message: {response}', 'error')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
