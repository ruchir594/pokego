var port = process.env.PORT || 5000,
    http = require('http'),
    fs = require('fs'),
    html = fs.readFileSync('p1.html'),
    submit_success = fs.readFileSync('p2.html'),
    image_res = fs.readFileSync('p3.html');

var spawn = require("child_process").spawn;
var PythonShell = require('python-shell');


    server = http.createServer( function(req, res) {

        console.dir(req.param);

        if (req.method == 'POST') {
            console.log("got POST");
            var body = '';
            req.on('data', function (data) {
                body += data;
                console.log("Partial body: " + body);
            });
            req.on('end', function () {
                var tempostr = body.substring(5, body.length)
                var decode = decodeURI(tempostr)
                console.log("Body: " + decode);
                if (decode != "fuckshit321b0") {
                /*var process = spawn('python',["../kgb.py", body.substring(5, body.length)]);

                process.stdout.on('data', function (data){
                    console.log('back in app.js')
                    console.log(data)
                  });*/
                  var options = {
                    mode: 'text',
                    args: ['-a', 'google', '-u', 'max23.pokemon@gmail.com', '-p', 'iceandfire', '-l', decodeURI(body.substring(5, body.length)), '-st', '10', '-H', '0.0.0.0', '-C']
                  };
                PythonShell.run("runserver.py" , options,function (err, results) {
                  if (err) throw err;
                  //console.log('result: %j', results);
                  console.log('back in app.js')
                  console.log(results)
                  var results = String(results)
                  var respon = ""
                  res.writeHead(200, {'Content-Type': 'text/html'});
                  res.end(results);
                }); }
            });
            //res.writeHead(200, {'Content-Type': 'text/html'});
            //res.end('post received ');
        }
        else
        {
            console.log("GET");
            //var html = '<html><body><form method="post" action="http://localhost:3000">Name: <input type="text" name="name" /><input type="submit" value="Submit" /></form></body>';
            var html = fs.readFileSync('p1.html');
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.end(html);
        }

    });

// Listen on port 3000, IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log('Server running at ' + port + '/');
