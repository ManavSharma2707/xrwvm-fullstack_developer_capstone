const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());

// Seed files live next to app.js in the Docker image and in ./data locally
function loadJson(name) {
  const candidates = [name, path.join('data', name)];
  const found = candidates.find((f) => fs.existsSync(f));
  return JSON.parse(fs.readFileSync(found, 'utf8'));
}

const reviews_data = loadJson('reviews.json');
const dealerships_data = loadJson('dealerships.json');

// "mongo_db" is the service name in docker-compose.yml
const mongoUrl = process.env.MONGO_URL || 'mongodb://mongo_db:27017/';
mongoose.connect(mongoUrl, { dbName: 'dealershipsDB' });

const Reviews = require('./review');

const Dealerships = require('./dealership');

// Reset the collections to the contents of the JSON files on every start
Reviews.deleteMany({})
  .then(() => Reviews.insertMany(reviews_data.reviews))
  .then(() => Dealerships.deleteMany({}))
  .then(() => Dealerships.insertMany(dealerships_data.dealerships))
  .catch((error) => console.error('Error seeding database', error));

// Express route to home
app.get('/', async (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const documents = await Dealerships.find({ id: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by id' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  // express.raw gives us the untouched body; accept it whatever the
  // Content-Type header says (curl -d sends form-encoded by default)
  let data;
  try {
    data = JSON.parse(req.body);
  } catch (error) {
    return res.status(400).json({ error: 'Request body must be valid JSON' });
  }
  // New reviews get the next free id
  const documents = await Reviews.find().sort({ id: -1 });
  const new_id = documents.length > 0 ? documents[0].id + 1 : 1;

  const review = new Reviews({
    id: new_id,
    name: data.name,
    dealership: data.dealership,
    review: data.review,
    purchase: data.purchase,
    purchase_date: data.purchase_date,
    car_make: data.car_make,
    car_model: data.car_model,
    car_year: data.car_year,
    user_id: data.user_id,
    time: data.time,
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
