import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function Dashboard() {

  const { token, logout, user } = useAuth();
  const navigate = useNavigate();

  const [violations, setViolations] = useState([]);
  const [logs, setLogs] = useState([]);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {

    const fetchData = () => {

      // violations
      fetch("http://127.0.0.1:8000/violations", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setViolations(data);
          } else {
            setViolations([]);
          }
        });

      // logs
      fetch("http://127.0.0.1:8000/logs", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(data => setLogs(data.logs || []));
    };

    fetchData();

    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);

  }, [token]);

  // Stats
  const errorCount = logs.filter(log => log.level === "ERROR").length;

  // Chart data
  const violationStats = {};

  violations.forEach(v => {
    const rule = v[0];
    violationStats[rule] = (violationStats[rule] || 0) + 1;
  });

  const chartData = Object.entries(violationStats).map(([key, value]) => ({
    name: String(key),   // force string
    count: Number(value) // force number
  }));
  return (
    <div style={{ maxWidth: "900px", margin: "40px auto", fontFamily: "Arial" }}>

      {/* NAVBAR */}
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "30px" }}>
        
        <div>
          <strong>Compliance Monitoring</strong>

          <span 
            style={{ marginLeft: "20px", cursor: "pointer" }} 
            onClick={() => navigate("/dashboard")}
          >
            Dashboard
          </span>

          <span 
            style={{ marginLeft: "15px", cursor: "pointer" }} 
            onClick={() => navigate("/logs")}
          >
            Logs
          </span>
        </div>

        <button onClick={handleLogout}>Logout</button>

      </div>

      <h1>Dashboard</h1>

      {/* STATS */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "30px" }}>

        <div style={card}>
          <h3>Total Logs</h3>
          <p style={cardNumber}>{logs.length}</p>
        </div>

        <div style={card}>
          <h3>Total Violations</h3>
          <p style={cardNumber}>{violations.length}</p>
        </div>

        <div style={card}>
          <h3>Error Logs</h3>
          <p style={{ ...cardNumber, color: "red" }}>{errorCount}</p>
        </div>

      </div>

      {/* CHART */}
      <h2>Violations Overview</h2>

      {chartData.length === 0 ? (
        <p style={{ color: "#777" }}>No data for chart</p>
      ) : (
        <div style={{ width: "100%", height: 300 }}>
          <BarChart width={600} height={300} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </div>
      )}

      {/* USER INFO */}
      <div style={{ marginBottom: "20px" }}>
        Logged in as: <strong>{user?.role}</strong>
      </div>

      {/* VIOLATIONS TABLE */}
      <h2>Detected Violations</h2>

      {violations.length === 0 ? (
        <p style={{ color: "#777" }}>No violations detected 🎉</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={cellHeader}>Rule</th>
              <th style={cellHeader}>User</th>
              <th style={cellHeader}>Details</th>
              <th style={cellHeader}>Time</th>
            </tr>
          </thead>

          <tbody>
            {violations.map((v, index) => (
              <tr key={index}>
                <td style={{ ...cell, color: "red", fontWeight: "bold" }}>{v[0]}</td>
                <td style={cell}>{v[1]}</td>
                <td style={cell}>{v[2]}</td>
                <td style={cell}>{v[3]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

    </div>
  );
}

/* STYLES */

const cellHeader = {
  borderBottom: "2px solid #ccc",
  textAlign: "left",
  padding: "10px"
};

const cell = {
  borderBottom: "1px solid #eee",
  padding: "10px"
};

const card = {
  flex: 1,
  border: "1px solid #ddd",
  borderRadius: "8px",
  padding: "15px",
  background: "#f9f9f9"
};

const cardNumber = {
  fontSize: "22px",
  fontWeight: "bold",
  marginTop: "10px"
};

export default Dashboard;