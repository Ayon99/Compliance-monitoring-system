import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function Logs() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const [logs, setLogs] = useState([]);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {
    const fetchLogs = () => {
      fetch("http://127.0.0.1:8000/logs", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(data => setLogs(data.logs || []));
    };

    fetchLogs();

    const interval = setInterval(fetchLogs, 3000);
    return () => clearInterval(interval);

  }, [token]);

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

      <h1 style={{ marginBottom: "20px" }}>System Logs</h1>

      <div style={tableContainer}>
        <table style={table}>
          <thead>
            <tr>
              <th style={header}>Service</th>
              <th style={header}>Level</th>
              <th style={header}>Message</th>
              <th style={header}>User</th>
              <th style={header}>Time</th>
            </tr>
          </thead>

          <tbody>
            {logs.map((log, i) => (
              <tr key={i}>
                <td style={cell}>{log.service}</td>

                <td style={{
                  ...cell,
                  color: getLevelColor(log.level),
                  fontWeight: "bold"
                }}>
                  {log.level}
                </td>

                <td style={cell}>{log.message}</td>
                <td style={cell}>{log.user_id}</td>
                <td style={cell}>{log.time}</td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  );
}

export default Logs;

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

const tableContainer = {
  background: "#1e293b",
  borderRadius: "12px",
  padding: "20px"
};

const table = {
  width: "100%",
  borderCollapse: "collapse"
};

const header = {
  borderBottom: "2px solid #334155",
  textAlign: "left",
  padding: "12px",
  color: "#94a3b8"
};

const cell = {
  borderBottom: "1px solid #1e293b",
  padding: "12px"
};

/* ================= LOG LEVEL COLORS ================= */

function getLevelColor(level) {
  if (level === "ERROR") return "#ef4444";   // red
  if (level === "WARNING") return "#f59e0b"; // orange
  if (level === "INFO") return "#22c55e";    // green
  return "#94a3b8";                         // default
}