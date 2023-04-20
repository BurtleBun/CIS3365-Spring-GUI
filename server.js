const express = require('express');
const cors = require('cors');
const axios = require('axios');
const ejs = require('ejs');
const app = express();
const bodyParser = require('body-parser');

// Enable CORS
// Cross Origin Resource Sharing used for the event listeners
// due to same origin policy, we set this so it can contact the backend python
// and the database
app.use(cors());
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With');
  // intercepts OPTIONS method
  if ('OPTIONS' === req.method) {
    // respond with 200
    res.sendStatus(200);
  } else {
    // move on
    next();
  }
});

// Enable JSON body parsing for incoming requests
app.use(express.json());
// Serve static files from the 'public' directory
app.use(express.static('public'));

// set the view engine to ejs
app.set('view engine', 'ejs');

// Set the views directory to the public directory
app.set('views', __dirname + '/public/views');

// parse application/json
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Define the API endpoints


// Index/Home page
app.get('/', function(req, res) {
  res.render('pages/index', { 
  });
  });

//Employees Page
app.get('/employee', function(req, res) {
  res.render('pages/employee', { 
  });
  });

//Welcome customer  Page
app.get('/customerwelcome', function(req, res) {
  res.render('pages/customerwelcome', { 
  });
  });


//Service Order Page
app.get('/createserviceorder', function(req, res) {
  res.render('pages/createserviceorder', { 
  });
  });

// Start the server
app.listen(3000, () => {
  console.log('Server started on port 3000');
});