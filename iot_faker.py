from faker import Faker
import json
import random
import datetime
import time
import argparse
from kafka import KafkaProducer

fake = Faker()
deviceNames=[]
for i in range(10):
    deviceNames.append(fake.uuid4())

# generate Temperature values
def getTemperatureValues():
    data = {}
    data['device'] = random.choice(deviceNames)
    data['deviceValue'] = random.randint(15, 35)
    data['deviceParameter'] = 'Temperature'
    data['dateTime'] = str(datetime.datetime.now().isoformat(sep=' '))
    return data

# generate Humidity values
def getHumidityValues():
    data = {}
    data['device'] = random.choice(deviceNames)
    data['deviceValue'] = random.randint(50, 90)
    data['deviceParameter'] = 'Humidity'
    data['dateTime'] = str(datetime.datetime.now().isoformat(sep=' '))
    return data

# generate Sound values
def getSoundValues():
    data = {}
    data['device'] = random.choice(deviceNames)
    data['deviceValue'] = random.randint(100, 140)
    data['deviceParameter'] = 'Sound'
    data['dateTime'] = str(datetime.datetime.now().isoformat(sep=' '))
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cert-folder",
        help="""Path to folder containing required Kafka certificates.
                Required --security-protocol equal SSL or SASL_SSL""",
        required=False,
    )
    parser.add_argument(
        "--host",
        help="Kafka Host (obtained from Aiven console)",
        required=True,
    )
    parser.add_argument(
        "--port",
        help="Kafka Port (obtained from Aiven console)",
        required=True,
    )
    parser.add_argument("--topic-name", help="Topic Name", required=True)

    args = parser.parse_args()
    cert_folder = args.cert_folder
    hostname = args.host
    port = args.port
    topic_name = args.topic_name
    producer = KafkaProducer(
            bootstrap_servers=hostname + ":" + port,
            security_protocol="SSL",
            ssl_cafile=cert_folder + "/ca.pem",
            ssl_certfile=cert_folder + "/service.cert",
            ssl_keyfile=cert_folder + "/service.key",
            value_serializer=lambda x: json.dumps(x).encode("UTF-8"),
            key_serializer=lambda x: json.dumps(x).encode("UTF-8"),
        
        )
    # Generate each parameter's data input in varying proportions
    while True:
        time.sleep(1)
        rnd = random.random()
        if (0 <= rnd < 0.40):
            data = getTemperatureValues()
            print(f"Sending: {data}")
            # sending the message to Kafka
            producer.send(topic_name, key={"key": data['device']}, value=data)
            
        elif (0.40 <= rnd < 0.70):
            data = getHumidityValues()
            print(f"Sending: {data}")
            # sending the message to Kafka
            producer.send(topic_name, key={"key": data['device']}, value=data)

        else:
            data = getSoundValues()
            print(f"Sending: {data}")
            # sending the message to Kafka
            producer.send(topic_name, key={"key": data['device']}, value=data)
        
        # producer.flush()

if __name__ == "__main__":
    main()