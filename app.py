# This is a basic REST micro service example for python using the flask library
# Docs: http://flask.pocoo.org/docs/1.0/
import re
import os

from flask import Flask, jsonify, request
from example_data import customers
import requests
import json

app = Flask(__name__)


# -----------------------------------------------------
# Basic 'customer' example for REST like resource paths
# -----------------------------------------------------


@app.route('/health', methods=['GET'])
def health():
    return 'OK Healthy User !!!'


@app.route('/notify', methods=['GET'])
def notify():
    response = call_notify_service(
        ['rajakumar@gmail.com'],
        'Index Root Access'
    )
    return response

# Get a list of resources
@app.route('/customers', methods=['GET'])
def find_all_customers():
    return jsonify(list(customers.values()))


# Get a single resource
@app.route('/customers/<customer_id>', methods=['GET'])
def find_single_customer(customer_id):
    if customer_id not in customers:
        return '', 404
    return jsonify(customers[customer_id])


# Update a resource
@app.route('/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    if customer_id in customers:

        for key in request.json:
            customers[customer_id][key] = request.json[key]

        return jsonify(customers[customer_id])
    else:
        return 'not found', 404


# Delete a resource
@app.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    if customer_id in customers:
        del customers[customer_id]
        return 'okay', 200
    else:
        return 'not found', 404


# Save a resource
def find_last_key(customers):
    last_key = 0
    for customer in customers:
        m = re.search(r'customer_(\d+)', customer)
        if int(m.group(1)) > last_key:
            last_key = int(m.group(1))

    return last_key


@app.route('/customers', methods=['POST'])
def save_customer():
    customer_id = 'customer_{0}'.format(find_last_key(customers) + 1)
    customers[customer_id] = request.json
    customers[customer_id]['customer_id'] = customer_id

    return jsonify(customers[customer_id])


# -----------------------------------------------------
# Basic example for an async method call
# -----------------------------------------------------

@app.route('/do_your_magic', methods=['POST'])
def do_magic():
    data = request.json

    print(data)
    # process the data

    response_object = {
        'list_of_magic_things': [
            {'id': 'magic_thing_1'},
            {'id': 'magic_thing_2'},
            {'id': 'magic_thing_3'},
        ]
    }

    success = True
    call_notify_service(
        ['rajakumar.1@gmail.com', 'rajakumar.thangavelu@yahoo.co.in'],
        'Do Magic',
        'Magic Text',
        '<h1>MAGIC</h1>'
    )
    # return status code and response
    if success:
        return jsonify(response_object), 200
    else:
        print('Uuuups something broke')
        return 'Magic Error Message', 500


def get_notification_service_url():
    hostname = os.environ['NOTIFICATION_SERVICE_HOSTNAME']
    port = os.environ['NOTIFICATION_SERVICE_PORT']
    url = 'http://%s:%s' % (hostname, port)
    print('url : %s' % url)
    return url

def call_notify_service(toEmails, subject, body_text_content='test', body_html_content='test'):

    base_url = get_notification_service_url()
    url = '%s/notify' % base_url

    print('notify url : %s' % url)
    data = {
        "subject": subject,
        "body_text_content": body_text_content,
        "body_html_content": body_html_content,
        "toEmails": toEmails
    }
    print('Url before request %s ' % url)
    response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return response.text

if __name__ == '__main__':

    #os.environ['NOTIFICATION_SERVICE_HOSTNAME'] = 'publiclb-devfargatelbstack-152781351.us-east-1.elb.amazonaws.com'
    #os.environ['NOTIFICATION_SERVICE_PORT'] = '80'

    #NOTIFICATION_SERVICE_HOSTNAME = localhost
    #NOTIFICATION_SERVICE_PORT = 8080
    app_port = os.environ['APPLICATION_PORT']
    print(os.environ['APPLICATION_PORT'])
    print(os.environ['NOTIFICATION_SERVICE_HOSTNAME'])
    print(os.environ['NOTIFICATION_SERVICE_PORT'])

    # app.register_error_handler(Exception, app_error)
    app.run(host='0.0.0.0', port=app_port)