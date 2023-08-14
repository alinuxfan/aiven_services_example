# aiven_services_example
Aiven Kafka Quickstart with Flink and Python

#### 1. Install Dependencies
```pip install -r requirements.txt```

#### 2. Create Aiven Kafka service in UI or CLI
##### UI

##### CLI

1. Create Aiven Account (Use SSO)
2. Create Token for CLI Access in https://console.aiven.io/profile/tokens [How To Create Authentication Tokens](https://docs.aiven.io/docs/platform/howto/create_authentication_token)
Save Token
3. `avn user login email@email.com --token #input token from step 2`

4. Set environment variables
```
KAFKA_INSTANCE_NAME=demokafka
CLOUD_PROVIDER=google-us-central1
AIVEN_PLAN_NAME=startup-2
DESTINATION_FOLDER_NAME=~/kafkacerts
```

5. Use CLI to create Kafka cluster or UI by following [Kafka getting started guide](https://docs.aiven.io/docs/products/kafka/getting-started)
```
avn service create  \
  -t kafka $KAFKA_INSTANCE_NAME \
  --cloud  $CLOUD_PROVIDER \
  -p $AIVEN_PLAN_NAME \
  -c kafka_rest=true \
```

6. Download credentials for Python script
```
avn service user-creds-download $KAFKA_INSTANCE_NAME \
  -d $DESTINATION_FOLDER_NAME \
  --username avnadmin
```

7. return the URI
```
avn service get $KAFKA_INSTANCE_NAME \                
  --format '{service_uri}'
```

8. Wait Until Service is running
```
avn service wait $KAFKA_INSTANCE_NAME
```

9. Create Topic for service in UI or CLI

10. Use Service Name and cert directory for the arguments and run

```
python iot_faker.py \                                           
  --cert-folder ~/kafkacerts/ \
  --host demokafka-username-x11x.aivencloud.com \
  --port 27721 \
  --topic-name iot
```

11. Create Demo Flink Environment with UI or CLI. If UI, follow [Flink getting started guide](https://docs.aiven.io/docs/products/flink/getting-started)

`avn service create demoflink -t flink --plan business-4`

12. Enable Flink Data Service Integration with Kafka

13. Flink - _Create New Application_ in the *Applications* tab

14. Flink - Create New Source Table  
```
CREATE TABLE iot (
    device VARCHAR,
    deviceParameter VARCHAR,
    deviceValue INT,
    dateTime TIMESTAMP
) WITH (
    'connector' = 'kafka',
    'properties.bootstrap.servers' = '',
    'scan.startup.mode' = 'earliest-offset',
    'topic' = 'iot',
    'value.format' = 'json',
    'key.format' = 'json',
    'key.fields' = 'device'
)
```

15. Create Sink Table
```
CREATE TABLE temperatures (
    device VARCHAR,
    deviceValue INT,
    timed TIMESTAMP,
    jitter DOUBLE
) WITH (
    'connector' = 'kafka',
    'properties.bootstrap.servers' = '',
    'scan.startup.mode' = 'earliest-offset',
    'topic' = 'temperatures',
    'value.format' = 'json',
    'key.format' = 'json',
    'key.fields' = 'device'
)
```

16. Create the SQL statement that transforms the data from the source stream.
```
INSERT INTO temperatures
SELECT device, deviceValue, dateTime, RAND() AS jitter
FROM iot
WHERE deviceParameter = 'Temperature'
```

17. Create Deployment of Flink Application

18. Use UI to verify data in the Kafka sink Topic