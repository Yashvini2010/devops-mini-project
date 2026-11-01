from collections import Counter as Tally
from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from app import servicenow

app = Flask(__name__)

REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['endpoint'])
OPEN_INCIDENTS = Gauge('servicenow_open_incidents', 'Open incidents by priority', ['priority'])
FETCH_ERRORS = Counter('servicenow_fetch_errors_total', 'Failed ServiceNow fetches')


def summarize():
    incidents = servicenow.get_incidents()
    by_priority = Tally(i['priority'] for i in incidents)
    return {'total': len(incidents), 'by_priority': dict(by_priority)}


@app.route('/health')
def health():
    REQUESTS.labels('/health').inc()
    return jsonify(status='ok', version='2')


@app.route('/incidents/summary')
def incidents_summary():
    REQUESTS.labels('/incidents/summary').inc()
    return jsonify(summarize())


@app.route('/metrics')
def metrics():
    try:
        data = summarize()
        for p in ['1', '2', '3', '4']:
            OPEN_INCIDENTS.labels(p).set(data['by_priority'].get(p, 0))
    except Exception:
        FETCH_ERRORS.inc()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)