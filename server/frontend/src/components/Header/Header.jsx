import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

// Top navigation bar shared by every React page. Shows the logged-in
// username with a Logout link, or Login / Register links when anonymous.
const Header = () => {
  const logout = async (e) => {
    e.preventDefault();
    const logout_url = window.location.origin + "/djangoapp/logout";
    const res = await fetch(logout_url, {
      method: "GET",
    });

    const json = await res.json();
    if (json) {
      const username = sessionStorage.getItem('username');
      sessionStorage.removeItem('username');
      alert("Logging out " + username + "...");
      window.location.href = window.location.origin;
    } else {
      alert("The user could not be logged out.");
    }
  };

  // Username of the current session (null when nobody is logged in)
  const curr_user = sessionStorage.getItem('username');

  let home_page_items = (
    <div className="input_panel">
      <a className="nav_item" href="/login">Login</a>
      <a className="nav_item" href="/register">Register</a>
    </div>
  );

  if (curr_user !== null && curr_user !== "") {
    home_page_items = (
      <div className="input_panel">
        <span className="username">{curr_user}</span>
        <a className="nav_item" href="/djangoapp/logout" onClick={logout}>Logout</a>
      </div>
    );
  }

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: "darkturquoise", height: "1in" }}>
        <div className="container-fluid">
          <h2 style={{ paddingRight: "5%" }}>Dealerships</h2>
          <div className="navbar-collapse" id="navbarText">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/about">About Us</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" style={{ fontSize: "larger" }} href="/contact">Contact Us</a>
              </li>
            </ul>
            <span className="navbar-text" style={{ marginLeft: "auto" }}>
              <div className="loginlink" id="loginlogout">
                {home_page_items}
              </div>
            </span>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Header;
