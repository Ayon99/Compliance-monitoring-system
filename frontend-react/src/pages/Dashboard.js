import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

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

  // stats
  const errorCount = logs.filter(log => log.level === "ERROR").length;
  const mlCount = violations.filter(v => v.rule === "ml_anomaly").length;

  // chart data
  const violationStats = {};

  violations.forEach(v => {
    if (!v.rule) return;

    const key =
      v.rule === "ml_anomaly" ? "ML Anomaly" : "Rule Violation";

    violationStats[key] = (violationStats[key] || 0) + 1;
  });

  const chartData = Object.keys(violationStats).map(key => ({
    name: key,
    count: violationStats[key]
  }));

  return (
    <div style={container}>

      {/* NAVBAR */}
      <div style={navbar}>
        <h2>Compliance Monitor</h2>

        <div>
          <span style={navItem} onClick={() => navigate("/dashboard")}>
            Dashboard
          </span>

          <span style={navItem} onClick={() => navigate("/logs")}>
            Logs
          </span>

          <button style={logoutBtn} onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <h1 style={{ marginBottom: "20px" }}>Dashboard</h1>

      {/* STATS */}
      <div style={cardContainer}>

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

        <div style={card}>
          <h3>ML Anomalies</h3>
          <p style={{ ...cardNumber, color: "orange" }}>{mlCount}</p>
        </div>

      </div>

      {/* CHART */}
      <div style={chartContainer}>
        <h3>Violations Overview</h3>

        <BarChart width={600} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" />
        </BarChart>
      </div>

      {/* USER */}
      <div style={{ marginBottom: "20px" }}>
        Logged in as: <strong>{user?.role}</strong>
      </div>

      {/* TABLE */}
      <h2>Detected Violations</h2>

      <table style={table}>
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
              <td
                style={{
                  ...cell,
                  color: v.rule === "ml_anomaly" ? "orange" : "red",
                  fontWeight: "bold"
                }}
              >
                {v.rule}
              </td>
              <td style={cell}>{v.user}</td>
              <td style={cell}>{v.details}</td>
              <td style={cell}>{v.time}</td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}

export default Dashboard;

/* ================= STYLES ================= */

const container = {
  minHeight: "100vh",
  background: "#0f172a",
  color: "white",
  padding: "30px",
  fontFamily: "Arial"
};

const navbar = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "30px"
};

const navItem = {
  marginRight: "20px",
  cursor: "pointer"
};

const logoutBtn = {
  padding: "6px 12px",
  cursor: "pointer"
};

const cardContainer = {
  display: "flex",
  gap: "20px",
  marginBottom: "30px"
};

const card = {
  flex: 1,
  background: "#1e293b",
  borderRadius: "12px",
  padding: "20px",
  boxShadow: "0 4px 10px rgba(0,0,0,0.3)"
};

const cardNumber = {
  fontSize: "28px",
  fontWeight: "bold",
  color: "#38bdf8"
};

const chartContainer = {
  background: "#1e293b",
  padding: "20px",
  borderRadius: "12px",
  marginBottom: "30px"
};

const table = {
  width: "100%",
  borderCollapse: "collapse"
};

const cellHeader = {
  borderBottom: "2px solid #334155",
  padding: "12px",
  color: "#94a3b8",
  textAlign: "left"
};

const cell = {
  borderBottom: "1px solid #1e293b",
  padding: "12px"
};