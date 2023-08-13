# using avn cli
# 1. Create Aiven Account (Use SSO)
# 2. Create Token for CLI Access in https://console.aiven.io/profile/tokens
# Save Token
# 3. avn user login email@email.com --token
# input token from step 2

KAFKA_INSTANCE_NAME=mykafka
CLOUD_PROVIDER=google-us-central1
AIVEN_PLAN_NAME=startup-2
DESTINATION_FOLDER_NAME=~/kafkacerts

avn service create  \
  -t kafka $KAFKA_INSTANCE_NAME \
  --cloud  $CLOUD_PROVIDER \
  -p $AIVEN_PLAN_NAME \
  -c kafka_rest=true \
  -c kafka.auto_create_topics_enable=true \
  -c schema_registry=true

avn service user-creds-download $KAFKA_INSTANCE_NAME \
  -d $DESTINATION_FOLDER_NAME \
  --username avnadmin

avn service get $KAFKA_INSTANCE_NAME \                
  --format '{service_uri}'


avn service wait $KAFKA_INSTANCE_NAME


python main.py \
  --security-protocol ssl \
  --cert-folder ~/kafkaCerts/ \
  --host mykafka-agjennings-d62a.aivencloud.com \
  --port 27721 \

avn service create myflink -t flink --plan business-4

CREATE TABLE iot_data3 (
    deviceValue INT,
    deviceParameter STRING,
    dateTime TIME
) WITH (
    'connector' = 'kafka',
    'properties.bootstrap.servers' = 'mykafka-agjennings-d62a.aivencloud.com:27721',
    'scan.startup.mode' = 'earliest-offset',
    'topic' = 'iot_data3',
    'value.format' = 'json'
)