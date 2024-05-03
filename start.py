import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/met9krd"
sqs = boto3.client('sqs')

f = open("myfile.txt", "w")
messages = []

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    global messages
    try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
        response = sqs.receive_message(
            QueueUrl=url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ]
        )
        # Check if there is a message in the queue or not
        print('Response here: ', response)
        if "Messages" in response:
            print('response here: ', response, '\n')
            count = 0
            for i in response['Messages']:
                if count <= len(response['Messages']):
                    order = response['Messages'][count]['MessageAttributes']['order']['StringValue']
                    word = response['Messages'][count]['MessageAttributes']['word']['StringValue']
                    f = open("myfile.txt", "a")
                    print(f"Order: {order}")
                    print(f"Word: {word}", '\n')
                    count += 1
                    pair = {"Order": {order},"Word": {word}}
                    print(pair, )
                    messages.append(pair)
                    print(messages)
                    return messages
                    f.close()  
        else:
            print("No message in the queue")
            exit(1)
# Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])         
def assemble_phrase(pair):
    phrase = ' '.join(pair[order][0] for order in sorted(pair))
    with open('phrase.txt', 'w') as file:
        file.write(phrase)

# Trigger the function
if __name__ == "__main__":
    get_message()
