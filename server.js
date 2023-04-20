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

// Set the views directory to the public directory
app.set('views', __dirname + '/public/views');

// parse application/json
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Define the API endpoint
const captainAPI = 'http://127.0.0.1:5000/captain';
const homeAPI = 'http://127.0.0.1:5000/enroute';
const toggledHomeAPI = 'http://127.0.0.1:5000/arrived'
const loginAPI = 'http://127.0.0.1:5000/';
const shipAPI = 'http://127.0.0.1:5000/ship';
const cargoAPI = 'http://127.0.0.1:5000/cargo'

// Login Page
app.get('/', (req, res) => {
  res.render('pages/login.ejs');
});

app.post('/signin', function(req, res) {
  axios.get(loginAPI)
  .then(response => {
    // Get masterLogin from the backend server
    const masterUser = response.data.username;
    const masterPass = response.data.password
    console.log('Master Username:', masterUser);  //Debug statement
    console.log('Master Password:', masterPass);  //Debug statement

    // Get inputted Username and Password
    var inputUsername = req.body.username
    var inputPassword = req.body.password
    console.log('Inputted Username:', inputUsername); //Debug statement
    console.log('Inputted Password:', inputPassword); //Debug statement

    let confirmLogin = 0; // 0 is false for incorrect login
    if (inputUsername == masterUser && inputPassword == masterPass) {
        confirmLogin = 1; // 1 is true for correct login
        // Render the overview page with scheduled cargo
        res.redirect('/overview');
      }
    else
      res.render('pages/login.ejs', {checkLogin: confirmLogin})
  });
});


// Home Page (Shows cargo in transit)
app.get('/overview', (req, res) => {
  axios.get(homeAPI)
    .then((response) => {
      const scheduledCargo = response.data;
      res.render('pages/overview.ejs', {cargo: scheduledCargo});
    })
    .catch((error) => {
      console.log(error)
      res.status(500).send('Error fetching cargo data');
    })
  
});

// Toggled Home Page (Shows arrived cargo)
app.get('/toggledOverview', (req, res) => {
  axios.get(toggledHomeAPI)
    .then((response) => {
      const scheduledCargo = response.data;
      res.render('pages/toggledOverview.ejs', {cargo: scheduledCargo});
    })
    .catch((error) => {
      console.log(error)
      res.status(500).send('Error fetching cargo data');
    })
  
});

// Render the captains.ejs file with the captains data
app.get('/captain', (req, res) => {
  // Use axios to fetch the captain data
  axios.get(captainAPI)
    .then((response) => {
      const captains = response.data;
      res.render('pages/captains.ejs', {captains: captains});
    })
    .catch((error) => {
      console.log(error);
      res.status(500).send('Error fetching captain data');
    });
});

// Render the ships.ejs file with the spaceship data
app.get('/ship', (req, res) => {
  // Use axios to fetch the captain data
  axios.get(shipAPI)
    .then((response) => {
      const ships = response.data;
      res.render('pages/ships.ejs', {ships: ships});
    })
    .catch((error) => {
      console.log(error);
      res.status(500).send('Error fetching spaceship data');
    });
});

// Render the cargo.ejs file with the cargo data
// This is just the overview page but showing every single cargo to be editable
app.get('/cargo', (req, res) => {
  // Use axios to fetch the captain data
  axios.get(cargoAPI)
    .then((response) => {
      const cargo = response.data;
      res.render('pages/cargo.ejs', {cargo: cargo});
    })
    .catch((error) => {
      console.log(error);
      res.status(500).send('Error fetching cargo data');
    });
});

// Start the server
app.listen(3000, () => {
  console.log('Server started on port 3000');
});







// Handle PUT requests to /captain
// app.put('/captain', (req, res) => {
//     // Parse the data sent from the client
//     const captain = req.body;
  
//     // Use axios to make a PUT request to the captain API with the updated data
//     axios.put(captainAPI, captain)
//       .then((response) => {
//         console.log('Captain updated successfully');
//         res.send('Captain updated successfully');
//       })
//       .catch((error) => {
//         console.log(error);
//         res.status(500).send('Error updating captain');
//       });
//   });  

// // Handle POST requests to /deleteCaptain
// app.post('/deleteCaptain', (req, res) => {
//   console.log(req.body);
//   const captainid = req.body.captainid;
//   // Delete captain with the given ID from the database
//   axios.delete(captainAPI, { 
//     headers: { 'Content-Type': 'application/json' }, 
//     data: { captainid: captainid } 
//   })
//     .then((response) => {
//       console.log(`Captain with ID ${captainid} deleted successfully`);
//       res.redirect('/');
//     })
//     .catch((error) => {
//       console.log(error);
//       res.status(500).send('Error deleting captain');
//     });
// });