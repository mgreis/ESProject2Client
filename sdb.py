sdb = boto3.client('sdb')  # Simple DB

response = sdb.create_domain(DomainName="ES2016")  # create Domain

while True:
    op = input("1 - List Jobs\n2 - New Job\n0 - Exit\n->")

    if op == "1":
        for job in l:
            response = sdb.get_attributes(DomainName="ES2016", ItemName=job, AttributeNames=[job])
            print('->', response.get('Attributes')[0]['Name'], '   ', response.get('Attributes')[0]['Value'])


    elif op == "2":
        text = input("Job: ")

        s3 = boto3.resource('s3')  # S3
        sqs = boto3.resource('sqs')  # Queue

        queue = sqs.get_queue_by_name(QueueName='ESQueue')  # Get the queue

        nonce = ''.join(random.choice(string.ascii_uppercase) for i in range(10))
        filename = nonce + '.txt'
        l.append(filename)

        open(filename, 'w+').write(text)
        data = open(filename, 'rb')

        s3.Bucket('esbucketp2').put_object(Key=filename, Body=data)  # Send file to s3
        sdb.put_attributes(DomainName="ES2016", ItemName=filename,
                           Attributes=[{'Name': filename, 'Value': 'Unprocessed'}])  # new job in SDB
        response = queue.send_message(MessageBody=filename)  # Put a new message in queue

    elif op == '0':
        break

    else:
        print("Wrong option!\n\n")

response = sdb.delete_domain(DomainName="ES2016")  # delete Domain