import os
import json
from kafka.consumer.group import KafkaConsumer


class KafkaTwitterConsumer(object):

    def __init__(self):
        self.KAFKA_HOST_NAME = os.environ.get('KAFKA_HOST_NAME')
        self.KAFKA_PORT = os.environ.get('KAFKA_PORT')
        self.KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')

        self.kafka_twitter_consumer = KafkaConsumer(
            self.KAFKA_TOPIC_NAME,
            bootstrap_servers=f'{self.KAFKA_HOST_NAME}:{self.KAFKA_PORT}'
        )

    def consume_tweets(self):
        for record_tweet in self.kafka_twitter_consumer:
            encoded_tweet = record_tweet.value
            decoded_tweet = encoded_tweet.decode(encoding='utf-8')
            json_tweet = json.loads(decoded_tweet)
            print(f'Tweet with id:{str(json_tweet["id"])} is received from Kafka with topic:{self.KAFKA_TOPIC_NAME}')


def main():
    KafkaTwitterConsumer().consume_tweets()


if __name__ == "__main__":
    main()
