// The following code was provided from the mjpeg-proxy documentation page.
// Read more at: https://www.npmjs.com/package/mjpeg-proxy

var express = require('express');
var app = express();

var MjpegProxy = require('mjpeg-proxy').MjpegProxy;

app.get('/', new MjpegProxy('http://balena-cam:5150/mjpeg').proxyRequest);
app.listen(5151);

// Enable HTML template middleware
//app.engine('html', require('ejs').renderFile);
//
//// Enable static CSS styles
//app.use(express.static('views'));
//
//// reply to request with "Hello World!"
//app.get('/', function (req, res) {
//  res.render('index.html');
//});
//
////start a server on port 80 and log its start to our console
//var server = app.listen(80, function () {
//
//  var port = server.address().port;
//  console.log('Example app listening on port ', port);
//});