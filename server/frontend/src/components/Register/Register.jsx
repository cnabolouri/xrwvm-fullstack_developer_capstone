import React, { useState } from "react";
import "../assets/style.css";
import "../assets/bootstrap.min.css";

export default function Register() {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    userName: "",
    password: "",
  });
  const [busy, setBusy] = useState(false);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    if (!form.userName || !form.password) {
      alert("Username and password are required.");
      return;
    }
    setBusy(true);
    try {
      const res = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // keep cookies/session
        body: JSON.stringify({
          userName: form.userName,
          password: form.password,
          firstName: form.firstName,
          lastName: form.lastName,
        }),
      });

      if (!res.ok) {
        const msg = (await res.json().catch(() => ({}))).status || "Registration failed";
        alert(msg);
        setBusy(false);
        return;
      }

      const data = await res.json(); // {"userName":"...","status":"Registered"}
      // mirror the lab behavior: cache username for the header
      sessionStorage.setItem("username", data.userName || form.userName);

      // go home after sign-up
      window.location.href = "/";
    } catch (err) {
      alert("Network error while registering.");
      setBusy(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: 520, marginTop: "40px" }}>
      <h1 className="title" style={{ marginTop: 10 }}>SignUp</h1>

      <form onSubmit={submit} className="form_panel" style={{ background: "white" }}>
        <div className="mb-3">
          <label className="form-label">First Name</label>
          <input name="firstName" className="form-control" value={form.firstName} onChange={onChange}/>
        </div>

        <div className="mb-3">
          <label className="form-label">Last Name</label>
          <input name="lastName" className="form-control" value={form.lastName} onChange={onChange}/>
        </div>

        <div className="mb-3">
          <label className="form-label">Username</label>
          <input name="userName" className="form-control" required value={form.userName} onChange={onChange}/>
        </div>

        <div className="mb-3">
          <label className="form-label">Password</label>
          <input name="password" type="password" className="form-control" required value={form.password} onChange={onChange}/>
        </div>

        <button type="submit" className="btn btn-primary" disabled={busy}>
          {busy ? "Registering..." : "Register"}
        </button>
      </form>
    </div>
  );
}
