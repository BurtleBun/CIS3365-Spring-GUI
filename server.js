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
app.use(bodyParser.urlencoded({ extended: false }));

// Set Employee Accounts
employeeUsername = "empuser"
employeePassword = "emppass"
managerUsername = "manuser"
managerPassword = "manpass"

// Define the API endpoints
const customerAPI = 'http://127.0.0.1:5000/customer'

// Home page
app.get('/', function(req, res) {
  res.render('pages/index', { 
  });
  });

  //Render Employee Login page
  app.get('/employeelogin', function(req, res) {
    res.render('pages/employeelogin.ejs');
  });
  
//Employee Login Function
app.post('/employeelogin', function(req, res) {
  var inputUsername = req.body.username;
  var inputPassword = req.body.password;

  let confirmLogin = 2;
  if ((inputUsername == employeeUsername && inputPassword == employeePassword) || (inputUsername == managerUsername && inputPassword == managerPassword)) {
    confirmLogin = 1;
    res.redirect('/employee');
  } else {
      confirmLogin = 0;
      res.render('pages/employeelogin.ejs', {checkLogin: confirmLogin});
  }
});

//Employee Page (Overview)
app.get('/employee', function(req, res) {
  axios.get(customerAPI)
  .then((response) => {
    const allCustomers = response.data;
    res.render('pages/employee.ejs', {customers: allCustomers});
  })
  .catch((error) => {
    console.log(error)
    res.status(500).send('Error fetching customer data');
  })
  });

//Customer Login
app.get('/customerlogin', function(req, res) {
  res.render('pages/customerwelcome', { 
  });
  });

//Reports Page
app.get('/choosereports', function(req, res) {
  res.render('pages/choosereports', { 
  });
  });

//New looks salon navbar button Page
app.get('/index', function(req, res) {
  res.render('pages/index', { 
  });
  });

// Start the server
app.listen(3000, () => {
  console.log('Server started on port 3000');
});