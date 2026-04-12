import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      login(data.access_token);
      navigate("/dashboard");
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <div style={container}>

      <div style={card}>
        <h2 style={{ marginBottom: "20px" }}>Login</h2>

        <input
          style={input}
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <input
          style={input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <button style={button} onClick={handleLogin}>
          Login
        </button>
      </div>

    </div>
  );
}

export default Login;

/* ================= STYLES ================= */

const container = {
  height: "100vh",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  background: "#0f172a"
};

const card = {
  background: "#1e293b",
  padding: "40px",
  borderRadius: "12px",
  width: "300px",
  display: "flex",
  flexDirection: "column",
  gap: "15px",
  boxShadow: "0 4px 20px rgba(0,0,0,0.4)",
  color: "white"
};

const input = {
  padding: "10px",
  borderRadius: "6px",
  border: "none",
  outline: "none"
};

const button = {
  padding: "10px",
  borderRadius: "6px",
  border: "none",
  background: "#38bdf8",
  color: "white",
  fontWeight: "bold",
  cursor: "pointer"
};