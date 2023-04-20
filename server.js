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

// Define the API endpoints




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