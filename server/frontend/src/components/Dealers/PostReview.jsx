import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

// Form for posting a review of one dealership. Only available when logged in.
const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [purchase, setPurchase] = useState(true);
  const [carIndex, setCarIndex] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;
  const dealer_url = `/djangoapp/dealer/${id}`;
  const review_url = `/djangoapp/add_review`;
  const carmodels_url = `/djangoapp/get_cars`;

  const postreview = async () => {
    const yearNumber = Number(year);
    if (review === "" || date === "" || carIndex === "" || year === "") {
      alert("All details are mandatory");
      return;
    }
    if (!Number.isInteger(yearNumber) || yearNumber < 2015 || yearNumber > 2023) {
      alert("Car year must be a whole number between 2015 and 2023");
      return;
    }

    const car = carmodels[Number(carIndex)];
    // Name and user id are filled in by the server from the login session;
    // the username is sent too so the payload is complete on its own.
    const jsoninput = JSON.stringify({
      "name": sessionStorage.getItem("username"),
      "dealership": id,
      "review": review,
      "purchase": purchase,
      "purchase_date": date,
      "car_make": car.CarMake,
      "car_model": car.CarModel,
      "car_year": yearNumber,
      "time": new Date().toISOString(),
    });

    const res = await fetch(review_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsoninput,
    });

    const json = await res.json();
    if (json.status === 200) {
      window.location.href = window.location.origin + "/dealer/" + id;
    } else if (json.status === 403) {
      alert("Please log in to post a review");
      window.location.href = "/login";
    } else {
      alert("Your review could not be saved. Please try again.");
    }
  };

  const get_dealer = async () => {
    const res = await fetch(dealer_url, { method: "GET" });
    const retobj = await res.json();

    if (retobj.status === 200) {
      const dealerobjs = Array.from(retobj.dealer);
      if (dealerobjs.length > 0) {
        setDealer(dealerobjs[0]);
      }
    }
  };

  const get_cars = async () => {
    const res = await fetch(carmodels_url, { method: "GET" });
    const retobj = await res.json();
    setCarmodels(Array.from(retobj.CarModels));
  };

  useEffect(() => {
    // Anonymous visitors cannot review: send them to the login page
    if (!sessionStorage.getItem("username")) {
      window.location.href = "/login";
      return;
    }
    get_dealer();
    get_cars();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        <textarea id='review' cols='50' rows='7' placeholder="Write your review" onChange={(e) => setReview(e.target.value)}></textarea>
        <div className='input_field' style={{ width: 'auto' }}>
          <label>
            <input type="checkbox" checked={purchase} onChange={(e) => setPurchase(e.target.checked)} /> Purchased a car here
          </label>
        </div>
        <div className='input_field' style={{ width: 'auto' }}>
          Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>
        <div className='input_field' style={{ width: 'auto' }}>
          Car Make
          <select name="cars" id="cars" defaultValue="" onChange={(e) => setCarIndex(e.target.value)}>
            <option value="" disabled hidden>Choose Car Make and Model</option>
            {carmodels.map((carmodel, index) => (
              <option key={index} value={index}>{carmodel.CarMake} {carmodel.CarModel}</option>
            ))}
          </select>
        </div>

        <div className='input_field' style={{ width: 'auto' }}>
          Car Year <input type="number" onChange={(e) => setYear(e.target.value)} max={2023} min={2015} />
        </div>

        <div>
          <button className='postreview' onClick={postreview}>Post Review</button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
