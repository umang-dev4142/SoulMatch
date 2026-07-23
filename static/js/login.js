// REST call 
// alert("JS Loaded");


// document.getElementById("loginForm").addEventListener("submit", async function(e){
// document.getElementById("loginForm")

document.getElementById("loginForm").addEventListener("submit", async function(e){
    e.preventDefault();

    let login = document.getElementById("login").value;
    let password = document.getElementById("password").value;

    let response = await fetch("/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({
            login: login,
            password: password
        })
    });

    let data = await response.json();

    if(data.success){
        document.getElementById("msg").innerHTML =
            "<span style='color:green'>Login Successful</span>";

        setTimeout(() => {
            window.location.href = data.redirect;
        }, 1000);

    } else {
        document.getElementById("msg").innerHTML =
            "<span style='color:red'>" + data.message + "</span>";
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const loginForm = document.getElementById("loginForm");
