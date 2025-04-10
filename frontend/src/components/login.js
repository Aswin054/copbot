import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css"; // ✅ Add a CSS file for styling

function Login({ setIsLoggedIn }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // ✅ Use navigate hook

  const handleLogin = (e) => {
    e.preventDefault();

    // ✅ Hardcoded login for now (replace with API if needed)
    if (username === "admin" && password === "1234567") {
      alert("Login successful! Welcome to CopBot.");
      setIsLoggedIn(true); // ✅ Set login state to true
      navigate("/chatbot"); // ✅ Redirect to chatbot
    } else {
      setError("Invalid username or password.");
    }
  };

  return (
    <div className="login-container">
      {/* ✅ Police Logo */}
      <img
        src="/tamilnadu-police-seeklogo.png"
        alt="Tamil Nadu Police Logo"
        className="police-logo"
      />

      {/* ✅ Login Form */}
      <form className="login-form" onSubmit={handleLogin}>
        <h2>CopBot Admin Login</h2>

        {/* ✅ Username Field */}
        <div className="input-group">
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        {/* ✅ Password Field (Masked as *) */}
        <div className="input-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ WebkitTextSecurity: "disc" }} // ✅ Masked as '*'
          />
        </div>

        {/* ✅ Error Message */}
        {error && <p className="error">{error}</p>}

        {/* ✅ Login Button */}
        <button type="submit" className="btn-login">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
