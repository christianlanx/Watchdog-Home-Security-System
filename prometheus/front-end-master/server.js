var express = require('express');
var app = express();

// Enable HTML template middleware
app.engine('html', require('ejs').renderFile);

// Enable static CSS styles
app.use(express.static('views'));

// reply to request with "Hello World!"
app.get('/', function (req, res) {
  res.render('index.html');
});

//start a server on port 3333 and log its start to our console
var server = app.listen(3333, function () {

  var port = server.address().port;
  console.log('Example app listening on port ', port);
});