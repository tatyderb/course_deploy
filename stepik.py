# Run with Python 3
"""
API for add, update or delete Stepik objects: steps.
"""
from auth_data import API_HOST, CLIENT_ID, CLIENT_SECRET

import json
import requests
import sys
import traceback

# 2. Get a token
def get_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('{}/oauth2/token/'.format(API_HOST), data={'grant_type': 'client_credentials'}, auth=auth)
    # status code should be 200 (HTTP OK)
    assert(response.status_code == 200)
    token = json.loads(response.text)['access_token']
    print('TOKEN =', token)
    return token


token = get_token(CLIENT_ID, CLIENT_SECRET)


def update_object(object_name, object_id, data, token=token):
    if not token:
        token = get_token()

    api_url = '{}/api/{}/{}'.format(API_HOST, object_name, object_id)
    # use PUT to update existing objects
    response = requests.put(api_url, headers={'Authorization': 'Bearer ' + token}, json=data)
    # status code should be 200 (HTTP OK)
    try:
        assert(response.status_code == 200)
    except AssertionError as e:
        traceback.print_exc()
        print(response.status_code)
        print(response.content)
        print(json.dumps(json.loads(response.content), indent=4))
        sys.exit(1)
    object_id = response.json()[object_name][0]['id']
    return object_id


# 3. Call API (https://stepik.org/api/docs/) using this token.
def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(API_HOST, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]


def fetch_objects(obj_class, obj_ids, keep_order=True):
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format(API_HOST, obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()

        objs += response['{}s'.format(obj_class)]
    if (keep_order):
        return sorted(objs, key=lambda x: obj_ids.index(x['id']))
    return objs


def create_object(object_name, data, token=token):
    if not token:
        token = get_token()

    api_url = '{}/api/{}'.format(API_HOST, object_name)
    # use POST to create new objects
    response = requests.post(api_url, headers={'Authorization': 'Bearer ' + token}, json=data)
    # status code should be 201 (HTTP Created)
    assert(response.status_code == 201)
    object_id = response.json()[object_name][0]['id']
    return object_id


def delete_object(object_name, object_id, token=token):
    if not token:
        token = get_token()

    api_url = '{}/api/{}/{}'.format(API_HOST, object_name, object_id)
    # use POST to create new objects
    response = requests.delete(api_url, headers={'Authorization': 'Bearer ' + token})
    # status code should be 204 (HTTP Created)
    # print(response.status_code)
    assert(response.status_code == 204)


def test_create():
    lesson_id = 239927
    api_url = 'https://stepik.org/api/step-sources'

    data = {
        'stepSource': {
            'block': {
                'name': 'choice',
                'text': 'Pick one!',
                'source': {
                    'options': [
                        {'is_correct': False, 'text': '2+2=3', 'feedback': ''},
                        {'is_correct': True, 'text': '2+2=4', 'feedback': ''},
                        {'is_correct': False, 'text': '2+2=5', 'feedback': ''},
                    ],
                    'is_always_correct': False,
                    'is_html_enabled': True,
                    'sample_size': 3,
                    'is_multiple_choice': False,
                    'preserve_order': False
                }
            },
            'lesson': lesson_id,
            'position': 3
        }
    }
    r = requests.post(api_url, headers={'Authorization': 'Bearer ' + token}, json=data)
    step_id = r.json()['step-sources'][0]['id']
    print('Step ID:', step_id)

if __name__ == '__main__':
    test_create()