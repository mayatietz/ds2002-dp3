import boto3
from botocore.exceptions import ClientError
import requests
import json

url = "https://sqs.us-east-1.amazonaws.com/440848399208/met9krd"
sqs = boto3.client('sqs')

# Function to retrieve messages from SQS queue
def get_messages(url):
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
    messages = response.get('Messages', [])
    return messages

# make phrase
def make_phrase(messages):
    phrase_dict = {}
    max_order = 0
    for message in messages:
        order = int(message['MessageAttributes']['order']['StringValue'])
        word = message['MessageAttributes']['word']['StringValue']
        phrase_dict[order] = word
        max_order = max(max_order, order) 
    
    print("phrase_dict:", phrase_dict)
    print("max_order:", max_order)

    phrase = ' '.join([phrase_dict.get(i, '') for i in range(max_order + 1)])
    return phrase

# delete messages from SQS queue
def delete_messages(url, messages):
    try:
        for message in messages:
            handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=url,
                ReceiptHandle=handle
            )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])


def main():
    messages = get_messages(url)
    if messages:
        phrase = make_phrase(messages)
        print("Assembled phrase:", phrase)
        
        with open("myfile.txt", "a") as file: # append to file
            file.write(phrase)
        
        delete_messages(url, messages)
        print("Messages deleted successfully.")
    else:
        print("No messages found in the queue.")

if __name__ == "__main__":
    main()