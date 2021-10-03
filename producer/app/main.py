# Dependencies
from kafka import KafkaProducer
from prometheus_client import start_http_server, Summary
import os
import time
import random

# Create a metric to track time spent and requests made.
PRODUCER_TIME = Summary('producer_send_seconds', 'Time between each producer send')

# Get Kafka Service Address
kafka_service = os.environ['KAFKA_SERVICE']
kafka_port = os.environ['KAFKA_PORT']
kafka_full_address = kafka_service + ':' + kafka_port
producer = KafkaProducer(bootstrap_servers=kafka_full_address)

# Start up the server to expose the metrics.
start_http_server(8000)

# Decorate function with metric.
@PRODUCER_TIME.time()
def process_message(in_epochtime_ms_str):
    producer.send('input', str.encode(in_epochtime_ms_str))
    print(in_epochtime_ms_str)
    seconds = float(random.randint(1, 1000)) / 1000.0
    time.sleep(seconds - ((time.time() - starttime) % seconds))

# Send Messages to Input Topic every RANDOM(0.001, 1.000) seconds
starttime = time.time()
epochtime_ms_str = str(starttime * 1000)
while True:
    process_message(epochtime_ms_str)   
    starttime = time.time()
    epochtime_ms_str = str(starttime * 1000)
