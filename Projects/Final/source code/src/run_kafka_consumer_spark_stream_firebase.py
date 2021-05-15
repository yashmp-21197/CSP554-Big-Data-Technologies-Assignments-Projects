import os
import json
import findspark
findspark.init()
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from geopy.geocoders import Nominatim
import firebase_admin
from firebase_admin import credentials, db


class SparkTwitterStreaming(object):

    def __init__(self):
        self.APP_NAME = os.environ.get('APP_NAME')
        self.KAFKA_HOST_NAME = os.environ.get('KAFKA_HOST_NAME')
        self.KAFKA_PORT = os.environ.get('KAFKA_PORT')
        self.KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')

        self.batch_duration = 10

        self.sc = SparkContext(master='local[*]', appName=self.APP_NAME)
        self.sc.setLogLevel('WARN')
        self.s = SparkSession(self.sc)
        self.ssc = StreamingContext(self.sc, batchDuration=self.batch_duration)

    def stream(self, batch_json_tweet_process=None):

        def batch_process(time=None, rdd=None):
            print('-------------------------------------------')
            print('Time: %s' % time)
            print('-------------------------------------------')
            batch_json_tweet_process(rdd=rdd, s=self.s)
            print('')

        kafka_topic_name = self.KAFKA_TOPIC_NAME

        batch_json_tweet = KafkaUtils.createDirectStream(
            self.ssc,
            [kafka_topic_name],
            {'metadata.broker.list': f'{self.KAFKA_HOST_NAME}:{self.KAFKA_PORT}'}
        ).map(
            lambda tweet: json.loads(tweet[1])
        )

        batch_json_tweet.map(lambda json_tweet: f'Tweet with id:{str(json_tweet["id"])} is received from Kafka with topic:{kafka_topic_name} and is about to be processed').pprint(num=500000)
        batch_json_tweet.count().map(lambda count: f'Number of tweets in this batch: {str(count)}').pprint()
        batch_json_tweet.foreachRDD(batch_process)

        self.ssc.start()
        self.ssc.awaitTermination()


def main():

    schema = StructType(
        [
            StructField('timestamp_ms', StringType(), True),
            StructField('created_at', StringType(), True),
            StructField('id_str', StringType(), True),
            StructField('text', StringType(), True),
            StructField('user', StructType(
                [
                    StructField('id_str', StringType(), True),
                    StructField('name', StringType(), True),
                    StructField('screen_name', StringType(), True),
                    StructField('location', StringType(), True),
                    StructField('profile_image_url', StringType(), True)
                ]
            ), True)
        ]
    )

    def batch_json_tweet_processing(rdd=None, s=None):

        def find_coordinated(record):
            try:
                APP_NAME = os.environ.get('APP_NAME')
                geo_locator = Nominatim(user_agent=APP_NAME)
                json_record = json.loads(record)
                location = geo_locator.geocode(json_record['user']['location'])
                location = location.raw
                json_record['user']['place'] = {}
                json_record['user']['place']['coordinates'] = {}
                json_record['user']['place']['coordinates']['lat'] = location['lat']
                json_record['user']['place']['coordinates']['lon'] = location['lon']
                location = geo_locator.reverse((location['lat'], location['lon']))
                location = location.raw
                address = location.get('address', {})
                json_record['user']['place']['country_code'] = address.get('country_code')
                json_record['user']['place']['country'] = address.get('country')
                json_record['user']['place']['state'] = address.get('state')
                json_record['user']['place']['city'] = address.get('city')
                return json_record
            except BaseException as e:
                return json.loads(record)

        if not rdd.isEmpty():
            app_name = os.environ.get('APP_NAME')
            spark_data_dir_local_path = os.environ.get('SPARK_DATA_DIR_LOCAL_PATH')
            google_application_credentials = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            firebase_realtime_database_url = os.environ.get('FIREBASE_REALTIME_DATABASE_URL')
            spark_data_firebase_realtime_database_path = os.environ.get('SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH')

            df = s.createDataFrame(rdd, schema=schema)
            df = df.filter(df.user.isNotNull() & df.user.location.isNotNull())
            new_schema = df.schema
            new_schema['user'].dataType.add(StructField('place', StructType(
                [
                    StructField('coordinates', StructType(
                        [
                            StructField('lat', StringType(), True),
                            StructField('lon', StringType(), True)
                        ]
                    ), True),
                    StructField('country_code', StringType(), True),
                    StructField('country', StringType(), True),
                    StructField('state', StringType(), True),
                    StructField('city', StringType(), True)
                ]
            ), True))
            df = s.createDataFrame(df.toJSON().map(find_coordinated), schema=new_schema)
            df = df.filter(
                df.user.place.isNotNull()
                & df.user.place.coordinates.isNotNull()
                & df.user.place.coordinates.lat.isNotNull()
                & df.user.place.coordinates.lon.isNotNull()
                & df.user.place.country_code.isNotNull()
                & df.user.place.country.isNotNull()
            )
            print(f'Number of tweets in this batch after processing: {str(len(df.collect()))}')
            print('')

            if not df.rdd.isEmpty():
                print('==>>', f'Storage Location of this Batch is:')
                print('    ',
                      f'on Firebase Real-Time Database: {firebase_realtime_database_url}{spark_data_firebase_realtime_database_path}')
                print('    ', f'on Local Machine: {spark_data_dir_local_path}')
                print('')

                df.write.save(
                    path=spark_data_dir_local_path,
                    format='json',
                    mode='append'
                )
                firebase_app = firebase_admin.initialize_app(
                    credential=credentials.Certificate(google_application_credentials),
                    options={
                        'databaseURL': firebase_realtime_database_url
                    },
                    name=app_name
                )
                db_ref = db.reference(
                    path=spark_data_firebase_realtime_database_path,
                    app=firebase_app,
                )
                rdd = df.toJSON().map(
                    lambda record: json.loads(record)
                )
                for record in rdd.toLocalIterator():
                    db_ref.child(record['id_str']).set(record)
                    print(f'Tweet with id:{record["id_str"]} is processed and is saved on Firebase Real-Time Database and on Local Machine')
                firebase_admin.delete_app(firebase_app)

    SparkTwitterStreaming().stream(batch_json_tweet_process=batch_json_tweet_processing)


if __name__ == "__main__":
    main()
