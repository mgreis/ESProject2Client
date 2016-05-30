from flask import Flask, request, render_template, Response, send_file

import os
import json
import base64
import uuid

import boto3
import decimal

application = app = Flask(__name__)
app.secret_key = os.urandom(64)

'''
Created on 27 de Mai de 2016

@author:  mgreis, auxiliar
'''

sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='queue')


sdb = boto3.client('sdb')  # Simple DB

sdb.create_domain(DomainName="ES2016")  # create Domain
#sdb.delete_domain (DomainName='ES2016')
print (sdb.list_domains())


def decode_boto3(string):

    filename = str(uuid.uuid4()) + ".txt"
    s3 = boto3.resource('s3')

    s3.Bucket('eu-west-1-mgreis-es-instance1').put_object(Key=filename, Body=string)

    return "https://s3-eu-west-1.amazonaws.com/eu-west-1-mgreis-es-instance1/" + filename


def delete_boto3(url):
    s3 = boto3.resource('s3')
    filename = url.replace("https://s3-eu-west-1.amazonaws.com/eu-west-1-mgreis-es-instance1/", "")
    print(filename)
    s3.Object('eu-west-1-mgreis-es-instance1', filename).delete()

def delete_job(job_id):


def get_jobs():
    answer = sdb.select(SelectExpression="select * from ES2016")
    string = []

    if "Items" in answer:
        string = answer.get("Items")[0].get("Attributes")
    else:
        string = []

    string2 = []
    for i in string:
        string2.append(json.dumps(i.get('Value')))
    out = "[ " + " , ".join(string2) + " ]"
    out = out.replace("\"", "")
    out = out.replace("'", "\"")
    return Response(out, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

def post_job(job_submitted):
    print('post 1')
    value = str({"job_id": str(job_submitted), "job_state": "submitted", "job_submitted": str(job_submitted), "job_started": "-1","job_finished": "-1", "job_file": "exp.txt"})
    print ("This "+value)
    sdb.put_attributes(DomainName="ES2016", ItemName='jobs',
                     Attributes= [{'Name': str(job_submitted), 'Value': value}])  # new job in SDB
    print('post 2')


def put_into_database(job_id,job_submitted,job_file):
    return "hello"

def send_message (job_id, job_submitted, job_file):
    queue.send_message(MessageBody='boto3', MessageAttributes={
        'job_id': str (job_id),
        'job_submitted': str(job_submitted),
        'job_file': str(job_file)
    })




@app.route('/templates/<path:filename>', methods=['GET', 'POST'])
def return_files_tut(filename):
    try:
        print(filename)
        return send_file('templates/' + filename, attachment_filename=filename)
    except Exception as e:
        return str(e)


@app.route('/css/<path:filename>', methods=['GET', 'POST'])
def return_files_tut2(filename):
    try:
        print(filename)
        return send_file('css/' + filename, attachment_filename=filename)
    except Exception as e:
        return str(e)


@app.route('/images/<path:filename>', methods=['GET', 'POST'])
def return_files_tut3(filename):
    try:
        print(filename)
        return send_file('images/' + filename, attachment_filename=filename)
    except Exception as e:
        return str(e)




@app.route('/')
def main():
    return render_template('index.html')


@app.route('/manage_jobs_react', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_jobs_react():
    if request.method == 'GET':
        return get_jobs()

    if request.method == 'POST':
        print(request.form['job_submitted'])
        post_job(request.form['job_submitted'])
        return get_jobs()

    if request.method == 'DELETE':
        print(request.form['job_id'])
        delete_job(request.form['job_id'])
        return get_jobs()




if __name__ == "__main__":
    #application.debug = True
    application.run(host="0.0.0.0")







