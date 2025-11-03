// Navbar.jsx
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

export default function Navbar() {
  const [me, setMe] = useState({ loading: true, isAuthenticated: false, userName: "" });
  const location = useLocation();

  useEffect(() => {
    fetch("/api/whoami", { credentials: "include" })
      .then(r => r.json())
      .then(d => setMe({ loading: false, ...d }))
      .catch(() => setMe({ loading: false, isAuthenticated: false, userName: "" }));
  }, []);

  // Hide username/logout while checking, and also hide on the login route
  const onLoginRoute = location.pathname.startsWith("/login");

  return (
    <nav className="navitems">
      <a className="nav_item" href="/">Home</a>
      <a className="nav_item" href="/about/">About</a>
      <a className="nav_item" href="/contact/">Contact Us</a>

      <div className="input_panel" style={{ marginLeft: "auto" }}>
        {!me.loading && !onLoginRoute && (
          me.isAuthenticated ? (
            <>
              <span className="username">{me.userName}</span>
              &nbsp;&nbsp;<a className="nav_item" href="/djangoapp/logout">Logout</a>
            </>
          ) : (
            <a className="nav_item" href="/login/">Login</a>
          )
        )}
      </div>
    </nav>
  );
}
