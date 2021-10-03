# Dependencies
from kafka import KafkaConsumer, KafkaProducer
from prometheus_client import start_http_server, Summary
from datetime import datetime, timedelta
import os
import time

# Create a metric to track time spent and requests made.
CONSUMER_TIME = Summary('consumer_receive_seconds', 'Time between each consumer receive')

# Get Kafka Service Address
kafka_service = os.environ['KAFKA_SERVICE']
kafka_port = os.environ['KAFKA_PORT']
kafka_full_address = kafka_service + ':' + kafka_port
consumer = KafkaConsumer(bootstrap_servers=kafka_full_address)
producer = KafkaProducer(bootstrap_servers=kafka_full_address)

# Start up the server to expose the metrics.
start_http_server(8000)

# Convert from Epoch ms to RFC 3339 (UTC)
def from_epoch_ms_to_rfc_3339(epoch_ms):
    utc_dt = datetime(1970, 1, 1) + timedelta(milliseconds=epoch_ms)
    return utc_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

# Decorate function with metric.
@CONSUMER_TIME.time()
def process_message(message):
    print(message.value.decode())
    original_ms_float = float(message.value.decode())
    rfc3339 = from_epoch_ms_to_rfc_3339(original_ms_float)
    print(rfc3339)
    producer.send('output', str.encode(rfc3339))

# Get Messages from Input Topic, transform them into DATE STRING (RFC 3339) and send it to Output Topic
consumer.subscribe(['input'])
for message in consumer:
    process_message(message)
