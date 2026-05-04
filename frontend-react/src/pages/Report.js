import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function Report() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const [report, setReport] = useState(null);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/report", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => setReport(data));
  }, [token]);

  const downloadReport = () => {
    window.open("http://127.0.0.1:8000/report/download");
  };

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

          <span style={navItem} onClick={() => navigate("/report")}>
            Report
          </span>

          <button style={logoutBtn} onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <h1>Report</h1>

      {report && (
        <div style={card}>
          <h3>Total Violations: {report.total_violations}</h3>

          <h3 style={{ marginTop: "20px" }}>Breakdown:</h3>

          {report.breakdown.map((item, i) => (
            <p key={i}>
              {item.rule}: {item.count}
            </p>
          ))}

          <button style={button} onClick={downloadReport}>
            Download Report
          </button>
        </div>
      )}

    </div>
  );
}

export default Report;

/* STYLES */

const container = {
  minHeight: "100vh",
  background: "#0f172a",
  color: "white",
  padding: "30px"
};

const navbar = {
  display: "flex",
  justifyContent: "space-between",
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

const card = {
  background: "#1e293b",
  padding: "20px",
  borderRadius: "12px",
  marginTop: "20px"
};

const button = {
  marginTop: "20px",
  padding: "10px",
  background: "#38bdf8",
  border: "none",
  borderRadius: "6px",
  color: "white",
  cursor: "pointer"
};