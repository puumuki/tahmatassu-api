var express = require('express')
var app = express()

app.use(express.static('dist'));

if (require.main === module) {
    var port = process.env.PORT || 8080;
    
    app.listen(port, function() {
      console.log("Started Tahmatassu App Listening on " + port);
    });
}