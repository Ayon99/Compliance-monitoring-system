import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [violations, setViolations] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    fetch("http://127.0.0.1:8000/violations", {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
      .then((res) => {
        if (res.status === 403) {
          alert("Admin only access");
          navigate("/");
        }
        return res.json();
      })
      .then((data) => {
        setViolations(data);
      })
      .catch((err) => console.error(err));
  }, [navigate]);

  return (
    <div style={{ padding: "50px" }}>
      <h2>Violations</h2>
      <button onClick={() => {
        localStorage.removeItem("token");
        navigate("/");
      }}>
        Logout
      </button>

      <table border="1" style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Rule</th>
            <th>User ID</th>
            <th>Details</th>
            <th>Detected At</th>
          </tr>
        </thead>
        <tbody>
          {violations.map((v, index) => (
            <tr key={index}>
              <td>{v.rule_name}</td>
              <td>{v.user_id}</td>
              <td>{v.details}</td>
              <td>{v.detected_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;