var http = require('http');
var fs = require('fs');
var addresser = "";
var x=1;
var app = http.createServer(function(request,response){
    var url = request.url;
    if(url == '/'&&x==1){
      url = '/webandmapdispalay.html';
      response.writeHead(200);
      response.end(fs.readFileSync(__dirname + url));
      x=0
    }
    var body = [];
    request.on('data', function(chunk){
      body.push(chunk);
    }).on('end', function(){
      body = Buffer.concat(body).toString();
      addresser = body;
      
    });if(addresser!=""){
      console.log(addresser);
      response.end(addresser);
    }else{
      response.end()
    }
    
    

});
app.listen(3000);