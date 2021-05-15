APP_NAME = process.env.APP_NAME;
NODE_JS_WEB_SERVER_PORT = process.env.NODE_JS_WEB_SERVER_PORT;
GOOGLE_APPLICATION_CREDENTIALS = process.env.GOOGLE_APPLICATION_CREDENTIALS;
FIREBASE_REALTIME_DATABASE_URL = process.env.FIREBASE_REALTIME_DATABASE_URL
SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH = process.env.SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH;

if(APP_NAME === undefined){
  console.log('environment variable "APP_NAME" is not set');
  process.exit(1);
}
if(NODE_JS_WEB_SERVER_PORT === undefined){
  console.log('environment variable "NODE_JS_WEB_SERVER_PORT" is not set');
  process.exit(1);
}
if(GOOGLE_APPLICATION_CREDENTIALS === undefined){
  console.log('environment variable "GOOGLE_APPLICATION_CREDENTIALS" is not set');
  process.exit(1);
}
if(FIREBASE_REALTIME_DATABASE_URL === undefined){
  console.log('environment variable "FIREBASE_REALTIME_DATABASE_URL" is not set');
  process.exit(1);
}
if(SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH === undefined){
  console.log('environment variable "SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH" is not set');
  process.exit(1);
}


const express = require('express');
const app = express();
app.use(express.static('./public'));

const http = require('http');
const server = http.createServer(app);

const socket = require('socket.io');
const io = socket(server);

const firebase_admin = require('firebase-admin');
const google_application_credentials = require(GOOGLE_APPLICATION_CREDENTIALS);
const firebase_app = firebase_admin.initializeApp({
  credential: firebase_admin.credential.cert(google_application_credentials),
  databaseURL: FIREBASE_REALTIME_DATABASE_URL
}, APP_NAME);
db_ref = firebase_admin.database(firebase_app).ref(SPARK_DATA_FIREBASE_REALTIME_DATABASE_PATH);


app.get('/', (req, res) => {
  res.sendFile(__dirname+'/public/index.html');
});


user_counter=0
const map_data = new Map();


function broadcast_map() {
  const tmp_map_data = new Array();
  tmp_map_data.push(['Country Code', 'Tweet Count']);
  for(const [key, value] of map_data.entries()){
    tmp_map_data.push([key, value]);
  }
  io.emit('broadcast_map', tmp_map_data);
}


io.on('connection', (socket) => {
  user_counter++;
  console.log(`a user connected => number of connected users:${user_counter}`);
  broadcast_map();
  socket.on('disconnect', () => {
    user_counter--;
    console.log(`a user disconnected => number of connected users:${user_counter}`);
  });
});


db_ref.on('child_added', (snapshot) => {
  const key = snapshot.key;
  const tweet = snapshot.val();
  console.log(`broadcast tweet with id:${key}`);
  io.emit('broadcast_tweet', snapshot.val());
  country_code = tweet.user.place.country_code;
  if(country_code !== undefined){
    map_data.set(country_code, (map_data.has(country_code) ? map_data.get(country_code) : 0) + 1);
    broadcast_map();
  }
});


server.listen(NODE_JS_WEB_SERVER_PORT, () => {
  console.log(`you are listening to the port:${NODE_JS_WEB_SERVER_PORT}`);
});
