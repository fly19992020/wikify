function on_login() {
    let name = document.getElementById("name").textContent;
    let password = document.getElementById("password").textContent;
    let obj = {name: name, password: password};
    let f = fetch("login.html", {method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json",
        }
    }).then(_ => (alert("OK. ")));
}