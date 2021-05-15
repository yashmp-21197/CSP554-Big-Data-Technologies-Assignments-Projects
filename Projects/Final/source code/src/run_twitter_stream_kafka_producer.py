import os
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API, Stream
from kafka.producer.kafka import KafkaProducer


class TwitterStreamListener(StreamListener):

    def __init__(self, kafka_producer=None, kafka_topic_name=None):
        super().__init__()
        self.kafka_producer = kafka_producer
        self.kafka_topic_name = kafka_topic_name

    def on_connect(self):
        print(f'Connected to twitter\'s streaming server')
        return

    def on_data(self, tweet):
        encoded_tweet = tweet.encode(encoding='utf-8')
        self.kafka_producer.send(self.kafka_topic_name, encoded_tweet)
        json_tweet = json.loads(tweet)
        print(f'Tweet with id:{str(json_tweet["id"])} is sent to Kafka with topic:{self.kafka_topic_name}')
        return True


class Twitter(object):

    def __init__(self):
        self.TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
        self.TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        self.TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
        self.TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
        self.TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')
        self.TWITTER_FILTER_KEYWORD_LIST = list(
            [
                key.strip() for key in os.environ.get('TWITTER_FILTER_KEYWORD_LIST').split(',') if key.strip() != ''
            ]
        )

        self.auth = OAuthHandler(
            consumer_key=self.TWITTER_CONSUMER_KEY,
            consumer_secret=self.TWITTER_CONSUMER_SECRET
        )
        self.auth.set_access_token(
            key=self.TWITTER_ACCESS_TOKEN,
            secret=self.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = API(
            auth_handler=self.auth
        )

    def stream(self, listener=None):
        Stream(
            auth=self.api.auth,
            listener=listener
        ).filter(
            track=self.TWITTER_FILTER_KEYWORD_LIST,
            is_async=False
        )


class KafkaTwitterProducer(object):

    def __init__(self):
        self.KAFKA_HOST_NAME = os.environ.get('KAFKA_HOST_NAME')
        self.KAFKA_PORT = os.environ.get('KAFKA_PORT')
        self.KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')

        self.kafka_twitter_producer = KafkaProducer(
            bootstrap_servers=f'{self.KAFKA_HOST_NAME}:{self.KAFKA_PORT}'
        )

    def produce_tweets(self):
        Twitter().stream(
            listener=TwitterStreamListener(
                kafka_producer=self.kafka_twitter_producer,
                kafka_topic_name=self.KAFKA_TOPIC_NAME
            )
        )


def main():
    KafkaTwitterProducer().produce_tweets()


if __name__ == "__main__":
    main()
