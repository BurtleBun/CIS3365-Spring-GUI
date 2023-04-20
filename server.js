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
const employeeAPI = 'http://127.0.0.1:5000/employees'
const reportAPI = 'http://127.0.0.1:5000/MonthSOReport'

// Home page
app.get('/', function(req, res) {
  res.render('pages/index.ejs', { 
  });
  });

// Customer Login page
app.post('/customerlogin', function(req, res) {
  axios.get('http://127.0.0.1:5000/CustomerLookup')
  .then(response => {
    const matchPhoneNumber = response.data.PrimaryPhoneNumber
    var inputPhoneNumber = req.body.PrimaryPhoneNumber;

  let confirmLogin = 2;
  if (inputPhoneNumber == matchPhoneNumber) {
    confirmLogin = 1;
    custInfo = response.data;
    res.render('pages/selectservice.ejs', {custInfo: custInfo, checkLogin: confirmLogin})
  } 
  else {
      confirmLogin = 0;
      res.render('pages/index.ejs', {checkLogin: confirmLogin});
  }
  })
});

 //Render Reports Page
 app.get('/choosereports', function(req, res) {
  res.render('pages/businessreports.ejs');
});

  //Render Employee Login page
  app.get('/employeelogin', function(req, res) {
    res.render('pages/employeelogin.ejs');
  });

//Render CustomerEdit Page
app.post("/editCustomer", function(req, res) {
  var customerID = req.body.customerID;

  // Make a POST request to your backend API to retrieve the customer data
  axios.post('http://127.0.0.1:5000/customerLook', {
    CustomerID: customerID
  })
  .then(function(response) {
    // Render the edit page with the retrieved customer data
    res.render("pages/customeredit.ejs", {
      customerID: customerID,
      customerData: response.data
    });
  })
  .catch(function(error) {
    console.log(error);
    res.status(500).send('Error retrieving customer data');
  });
});

  
//Employee Login Function
app.post('/employeelogin', function(req, res) {
  var inputUsername = req.body.username;
  var inputPassword = req.body.password;

  let confirmLogin = 2;
  if ((inputUsername == employeeUsername && inputPassword == employeePassword)) {
    confirmLogin = 1;
    res.redirect('/employee');
  } 
  if (inputUsername == managerUsername && inputPassword == managerPassword) {
    confirmLogin = 1;
    res.redirect('manager');
  }
  else {
      confirmLogin = 0;
      res.render('pages/employeelogin.ejs', {checkLogin: confirmLogin});
  }
});

//Run the last month's revenue business report
app.post('/lastMonthRevenueReport', function(req, res) {
  axios.post('http://127.0.0.1:5000/showMonthRevenue')
  .then((response) => {
    const revenueData = response.data;

    res.render('pages/lastmonthrevenue.ejs', {revenueData: revenueData});
  })
  .catch((error) => {
    console.log(error)
    res.status(500).send('Error fetching revenue data');
  })
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


//Manager Page (Overview)
app.get('/manager', function(req, res) {
  axios.get(employeeAPI)
  .then((response) => {
    const allEmployees = response.data;
    res.render('pages/manager.ejs', {employees: allEmployees});
  })
  .catch((error) => {
    console.log(error)
    res.status(500).send('Error fetching employee data');
  })
  });

  app.get('/reports', function(req, res) {
    axios.get(reportsAPI)
    .then((response) => {
      const reportData = response.data;
      res.render('pages/reports.ejs', {reportdata: reportData});
    })
    .catch((error) => {
      console.log(error)
      res.status(500).send('Error fetching customer data');
    })
    });



// Start the server
app.listen(3000, () => {
  console.log('Server started on port 3000');
});