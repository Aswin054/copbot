import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Chatbot from "./components/chatbot"; // Chatbot component
import Login from "./components/login";     // Login component
import "./styles/Chatbot.css";

function App() {
  // ✅ State to manage login
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* ✅ Login Route */}
          <Route
            path="/"
            element={
              isLoggedIn ? (
                <Navigate to="/chatbot" replace />
              ) : (
                <Login setIsLoggedIn={setIsLoggedIn} />
              )
            }
          />

          {/* ✅ Chatbot Route (Protected) */}
          <Route
            path="/chatbot"
            element={
              isLoggedIn ? (
                <Chatbot />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
