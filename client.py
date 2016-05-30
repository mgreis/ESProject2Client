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

simple_db_client = boto3.client('sdb')


def send_message (job_id, job_submitted, job_file):
    queue.send_message(MessageBody='boto3', MessageAttributes={
        'job_id': str (job_id),
        'job_submitted': str(job_submitted),
        'job_file': str(job_file)
    })

def put_into_database(job_id,job_submitted,job_file):
    return "hello"





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

def get_jobs():
    string=  '[{"job_id": "1", "job_state": "submitted", "job_submitted": "123456", "job_started": "123457","job_finished": "123458", "job_file": "exp.txt"},{"job_id": "2", "job_state": "started", "job_submitted": "123456", "job_started": "123457", "job_finished": "123458", "job_file": "exp2.txt"},{"job_id": "3", "job_state": "finished", "job_submitted": "123456", "job_started": "123457","job_finished": "123458", "job_file": "exp3.txt"}]'
    print (string)
    return Response(string, mimetype='application/json',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})


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
        return get_jobs()

    if request.method == 'DELETE':
        return get_jobs()




if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0")







