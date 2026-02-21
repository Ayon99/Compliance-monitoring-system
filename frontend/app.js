document.addEventListener("DOMContentLoaded", function () {

    console.log("JS loaded");

    const form = document.getElementById("loginForm");

    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        console.log("Login clicked");
    
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const error = document.getElementById("error");

        try {
            const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    grant_type: "password"
                    username: username,
                    password: password
                })
            });

            console.log("Response status:", response.status);

            if (!response.ok) {
                throw new Error("Invalid credentials");
            }

            const data = await response.json();

            localStorage.setItem("token", data.access_token);
            window.location.href = "dashboard.html";

        } catch (err) {
            error.textContent = "Login failed.";
        }
    });

});