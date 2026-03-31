import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

function Logs() {

  const { token } = useAuth();
  const [logs, setLogs] = useState([]);

useEffect(() => {

  const fetchLogs = () => {
    fetch("http://127.0.0.1:8000/logs", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => setLogs(data.logs));
  };

  fetchLogs();

  const interval = setInterval(fetchLogs, 3000);

  return () => clearInterval(interval);

}, [token]);

  return (
    <div style={{ maxWidth: "900px", margin: "40px auto", fontFamily: "Arial" }}>
      
      <h1>System Logs</h1>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
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

              <td style={{ ...cell, color: getLevelColor(log.level), fontWeight: "bold" }}>
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
  );
}

const header = {
  borderBottom: "2px solid #ccc",
  textAlign: "left",
  padding: "10px"
};

const cell = {
  borderBottom: "1px solid #eee",
  padding: "10px"
};

function getLevelColor(level) {
  if (level === "ERROR") return "red";
  if (level === "WARNING") return "orange";
  if (level === "INFO") return "green";
  return "black";
}

export default Logs;