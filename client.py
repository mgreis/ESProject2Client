from flask import Flask, request, render_template

import os
import json
import base64
import uuid

import boto3
import decimal

application = app = Flask(__name__)
app.secret_key = os.urandom(64)

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

table = dynamodb.create_table(
    TableName='Movies',
    KeySchema=[
        {
            'AttributeName': 'year',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'title',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'year',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)


def decode_boto3(string):

    filename = "images/" + str(uuid.uuid4()) + ".txt"
    s3 = boto3.resource('s3')

    s3.Bucket('eu-west-1-mgreis-es-instance1').put_object(Key=filename, Body=base64.b64decode(string))

    return "https://s3-eu-west-1.amazonaws.com/eu-west-1-mgreis-es-instance1/" + filename


def delete_boto3(url):
    s3 = boto3.resource('s3')
    filename = url.replace("https://s3-eu-west-1.amazonaws.com/eu-west-1-mgreis-es-instance1/", "")
    print(filename)
    s3.Object('eu-west-1-mgreis-es-instance1', filename).delete()

def get_jobs():
    return '{"job_id" : "1","job_submitted" : "123456", "job_started" : "123457", "job_finished" : "123458", "job_file": "exp.txt"}'


@app.route('/')
def main(name=None):
    return render_template('index.html')


@app.route('/manage_jobs_react', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_jobs_react():
    if request.method == 'GET':
        return get_jobs()

    if request.method == 'POST':
        return '{"job_id" : "1","job_submitted" : "123456", "job_started" : "123457", "job_finished" : "123458", "job_file": "exp.txt"}'

    if request.method == 'DELETE':
        return '{"job_id" : "1","job_submitted" : "123456", "job_started" : "123457", "job_finished" : "123458", "job_file": "exp.txt"}'






if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0")







