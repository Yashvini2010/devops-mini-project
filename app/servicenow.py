import os
import random
import requests

MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'


def get_incidents():
    if MOCK_MODE:
        groups = ['Service Desk', 'Network', 'Database', 'Applications']
        return [
            {
                'number': f'INC{1000 + i}',
                'priority': random.choice(['1', '2', '3', '4']),
                'assignment_group': random.choice(groups),
                'state': 'open',
            }
            for i in range(random.randint(15, 30))
        ]

    instance = os.environ['SN_INSTANCE']  # e.g. https://dev12345.service-now.com
    auth = (os.environ['SN_USER'], os.environ['SN_PASSWORD'])
    url = f'{instance}/api/now/table/incident'
    params = {
        'sysparm_query': 'active=true',
        'sysparm_fields': 'number,priority,assignment_group,state',
        'sysparm_limit': 200,
    }
    r = requests.get(url, auth=auth, params=params, timeout=10)
    r.raise_for_status()
    return r.json()['result']