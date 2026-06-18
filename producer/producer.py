# import os
# from kafka import KafkaProducer
# from datetime import datetime
# import json

# kafka_broker = os.environ.get("KAFKA_BROKER_URL", "localhost:9093")
# kafka_topic = os.environ.get("KAFKA_TOPIC", "posts")

# producer = KafkaProducer(bootstrap_servers=[kafka_broker], value_serializer=lambda v: json.dumps(v).encode("utf-8"))
# for i in range(5):
#     producer.send(
#         kafka_topic, {"sender": "buildingminds", "content": f"message {i}", "created_at": datetime.now().isoformat()}
#     )
#     print(f"message {i} sent to topic {kafka_topic}")
import os
import json
from datetime import datetime
from kafka import KafkaProducer

kafka_broker = os.environ.get(
    "KAFKA_BROKER_URL",
    "kafka:9092"
)

kafka_topic = os.environ.get(
    "KAFKA_TOPIC",
    "posts"
)

producer = KafkaProducer(
    bootstrap_servers=[kafka_broker],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

for i in range(5):

    message = {
        "sender": "buildingminds",
        "content": f"message {i}",
        "created_at": datetime.now().isoformat(),
    }

    producer.send(kafka_topic, message)

    print(f"Message sent: {message}")

producer.flush()
producer.close()

print("All messages delivered successfully")

print("All messages delivered successfully")