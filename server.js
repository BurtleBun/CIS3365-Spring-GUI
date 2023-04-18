const express = require('express');
const cors = require('cors');
const axios = require('axios');
const ejs = require('ejs');
const app = express();
const bodyParser = require('body-parser');

var path = require('path');

var routes = require('./routes/index');

// Configure view engine to render EJS templates.
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

// Use application-level middleware for common functionality, including logging, parsing, and session handling.
app.use(require('morgan')('combined'));
app.use(require('cookie-parser')());
app.use(require('body-parser').urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '/views')));


app.use('/', routes);

const port_runing = 3000;

app.listen(port_runing);

console.log("Application running at: " + port_runing)