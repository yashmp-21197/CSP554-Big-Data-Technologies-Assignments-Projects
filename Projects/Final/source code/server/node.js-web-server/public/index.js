google.charts.load('current', {
  'packages':['geochart'],
  'mapsApiKey': 'AIzaSyDPPqYKEGtXWJXWf989HRLAXiKfZi2FuTk'
});
google.charts.setOnLoadCallback(drawMap);

map_data = undefined;
old_map_data = undefined;

const equals = (a, b) => JSON.stringify(a) === JSON.stringify(b);

function drawMap() {
  if(map_data === undefined || equals(map_data, old_map_data))
    return;
  old_map_data = map_data;
  var data = google.visualization.arrayToDataTable(map_data);
  var options = {};
  var chart = new google.visualization.GeoChart(document.getElementById('map'));
  chart.draw(data, options);
}

function addTweet(tweet_data) {
  if(tweet_data === undefined)
    return;
  var html = '<div class="tweet"> <img class="tweet__author-logo" src="%user_img%" /> <div class="tweet__main"> <div class="tweet__header"> <div class="tweet__author-name">%author_name%</div> <div class="tweet__author-slug">%screen_name%</div> <div class="tweet__publish-time"> %posted_time% </div> </div> <div class="tweet__content">%tweet_desc%</div></div> </div>';
  html = html.replace('%user_img%', tweet_data.user.profile_image_url);
  html = html.replace('%author_name%', tweet_data.user.name);
  html = html.replace('%screen_name%', '@'+ tweet_data.user.screen_name);
  html = html.replace('%posted_time%', tweet_data.created_at);
  html = html.replace('%tweet_desc%', tweet_data.text);
  document.querySelector('.container').insertAdjacentHTML('afterbegin', html);
}

const socket = io();

socket.on('broadcast_tweet', function(msg){
  tweet_data = msg;
  addTweet(tweet_data);
});

socket.on('broadcast_map', function(msg){
  map_data = msg;
});

setInterval(() => {
  drawMap();
}, 1000);
