-   Setup JDK:
    -   Download and install JRE from https://www.oracle.com/java/technologies/javase-jre8-downloads.html

-   Setup Python:
    -   Download and install python:3.6 from https://www.python.org/downloads/
    -   Download and install editor tool pycharm from https://www.jetbrains.com/pycharm/
    -   Download required python libraries using CMD or pycharm terminal:
        -   pip install tweepy
        -   pip install kafka-python
        -   pip install findspark
        -   pip install pyspark==2.4.6
        -   pip install geopy
        -   pip install firebase-admin

-   Setup Node.js:
    -   Download and install node.js from https://nodejs.org/en/
    -   Download and install editor tool atom from https://atom.io/
    -   Go to file->settings->install, and download required atom packages:
        -   platformio-ide-terminal
        -   script

-   Setup Server:
    -   ZooKeeper:
        -   Download and extract zookeeper (note: bin) in project/server directory from https://zookeeper.apache.org/releases.html
        -   Replace zoo_sample.cfg file in project/server/zooKeeper/conf directory with zoo.cfg file in project/config directory
    -   Kafka:
        -   Download and extract kafka (note: not src) in project/server directory from https://kafka.apache.org/downloads.html
        -   Replace server.properties file in project/server/kafka/config directory with server.properties file in project/config directory
    -   Spark:
        -   Download and extract spark (note: 2.4) in project/server directory from https://spark.apache.org/downloads.html
        -   Download and copy spark-streaming-kafka-0-8-assembly.jar in project/server/spark/jars directory from https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly
        -   Hadoop:
            -   Create project/server/hadoop-2.7/bin directory (note: match spark's hadoop version)
            -   Download and copy winutils.exe (note: match spark's hadoop version) in project/server/hadoop-2.7/bin directory from https://github.com/cdarlint/winutils
    -   Node.js:
        -   Go to project/server/node.js path in CMD or open project/server/node.js directory in atom editor tool. 
        -   Download required node.js libraries using CMD or atom terminal using any of these two methods:
            1.  Using pre-setup file
                -   npm install
            2.  Start from beginning 
            -   npm init
                -   Add {"start": "node index.js"} key-value pair in dictionary value of key "scripts" if not exists in package.json file
            -   npm install express
            -   npm install http
            -   npm install firebase-admin
            -   npm install socket.io

-   Setup Twitter:
    -   Signup and login to your twitter developer account
    -   Apply for twitter developer account and receive approval
    -   Create a project and associated app in the developer portal
    -   Navigate to your app's keys and tokens page, and safely save your app's access token, access token secret, consumer key, consumer secret and bearer token

-   Setup Firebase Real-Time Database:
    -   Signup and login to your google account
    -   Go to the firebase console using https://console.firebase.google.com/ and switch to your desired google account
    -   Create and open a project
    -   Go to project settings->service accounts, and generate new private key
    -   Safely store this newly generated private key in project/server/firebase/service-account/admin-sdk directory
    -   Go to build->realtime database and create database
        -   Choose start in test mode in security rules of setup database and then enable it
    -   If you want no security then go to build->realtime database->rules and edit as below
        -   {
                "rules": {
                    ".read": true,
                    ".write": true,
                }
            }
    -   Make note of database_url which is available on build->realtime database->data (e.g. https://databaseName.firebaseio.com)

-   Setup Web-page Visualization:
    -   Signup and login to your google account
    -   Go to the Google Cloud Platform using https://console.cloud.google.com/ and switch to your desired google account
    -   Go to Home->DashBoard
    -   Create and open a new project or open an old project which was created in setup firebase real-time database step
    -   Go to APIs and Services
    -   Enable Maps JavaScript API in ENABLE APIS AND SERVICES
    -   Go to APIs and Services->Credentials and CREATE CREDENTIALS for API key
    -   RESTRICT KEY by API restrictions and then select and add Maps JavaScript API and then save
    -   Copy API key and set it as a value of 'mapsApiKey' key in google.chart.load method's dictionary argument in project/server/node.js/public/index.js file.

-   Setup Environment Variable:
    -   Open file setup_env_var.bat in text editor
    -   Change APP_NAME variable that you want
    -   Change JAVA_HOME variable according to your JRE path and version
    -   Change TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_BEARER_TOKEN according to your twitter app
    -   Change TWITTER_FILTER_KEYWORD_LIST that you want to filter in twitter stream and make sure to write keywords separated by ',' and no extra spaces
    -   Don't change ZOOKEEPER_HOST_NAME, ZOOKEEPER_PORT, KAFKA_HOST_NAME, and KAFKA_PORT variables
    -   Change KAFKA_TOPIC_NAME that you want
    -   Change SPARK_HOME variable according to your spark version
    -   Don't change HADOOP_HOME variable
    -   Change NODE_JS_WEB_SERVER_PORT variable according to your desired node.js web port you want to listen
    -   Don't change DATA_DIR_PATH and SPARK_DATA_DIR_PATH variables
    -   Change GOOGLE_APPLICATION_CREDENTIALS variable according to name of your private key json file
    -   Change FIREBASE_REALTIME_DATABASE_URL according to your database url which is noted in last step of setup firebase real-time database
    -   Don't change SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH variable
    -   Don't change PATH variable

-   Run:
    -   NOTE: in "*", * is a command to run in CMD
    1.  -   Open CMD, make sure your current directory is your project directory, and name this CMD by running "title env_var"
        -   Run "setup_env_var.bat" in env_var CMD
    2.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title ZooKeeper" in newly started CMD
        -   In ZooKeeper CMD, go to project/server/zookeeper/bin directory and run "zkserver" to start zookeeper
    3.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title Kafka_Server" in newly started CMD
        -   In Kafka_Server CMD, go to project/server/kafka directory and run ".\bin\windows\kafka-server-start.bat .\config\server.properties" to start kafka
    4.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title Kafka_Topic" in newly started CMD
        -   In Kafka_Topic CMD, go to project/server/Kafka/bin/windows directory and run "kafka-topics.bat --create --zookeeper %ZOOKEEPER_HOST_NAME%:%ZOOKEEPER_PORT% --replication-factor 1 --partitions 1 --topic %KAFKA_TOPIC_NAME%" to create a kafka topic
    5.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title Kafka_Consumer" in newly started CMD
        -   In Kafka_Consumer CMD, go to project/src directory and run "python run_kafka_consumer.py" to start kafka consumer
    6.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title Kafka_Consumer_Spark_Stream_Firebase" in newly started CMD
        -   In Kafka_Consumer_Spark_Stream_Firebase CMD, go to project/src directory and run "python run_kafka_consumer_spark_stream_firebase.py" to start kafka consumer, spark stream with batch process, and firebase data store
    7.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title Node.js_Web_Server" in newly started CMD
        -   In Node.js_Web_Server CMD, go to project/server/node.js directory and run "npm start" to start node.js server
        -   In web browser, open localhost 127.0.0.1:PORT, where PORT is NODE_JS_WEB_SERVER_PORT variable that was set in setup environment variable step (setup_env_var.bat file)
    8.  -   Open new CMD with running "start" in env_var CMD and name this CMD by running "title Twitter_Stream_Kafka_Producer" in newly started CMD
        -   In Twitter_Stream_Kafka_Producer CMD, go to project/src directory and run "python run_twitter_stream_kafka_producer.py" to start twitter stream and kafka producer

-   References:
    -   Twitter:
        1.  https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction
        2.  https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/introduction
        3.  https://www.extly.com/docs/autotweetng_joocial/tutorials/how-to-auto-post-from-joomla-to-twitter/apply-for-a-twitter-developer-account/#apply-for-a-developer-account
        4.  https://botwiki.org/resource/tutorial/how-to-create-a-twitter-app/
    -   JDK, Python, ZooKeeper, Kafka, Spark:
        1.  https://dzone.com/articles/running-apache-kafka-on-windows-os
        2.  https://phoenixnap.com/kb/install-spark-on-windows-10
        3.  https://towardsdatascience.com/working-with-apache-spark-python-and-pyspark-128a82668e67
    -   Firebase Real-Time Database:
        1.  https://firebase.google.com/docs/admin/setup#python
        2.  https://firebase.google.com/docs/database/admin/start
        3.  https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/
    -   Node.js Server and Web-page Visualization:
        1.  https://www.npmjs.com/package/socket.io
        2.  https://socket.io/get-started/chat
        3.  https://developers.google.com/chart/interactive/docs/gallery/geochart