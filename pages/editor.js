function on_fetch() {
    let uri = document.getElementById("uri").textContent;
    let f = fetch(uri + "?source=true")
        .then(response => response.text())
        .then(s => {document.getElementById("editor").textContent = s;});
}

function on_put() {
    let uri = document.getElementById("uri").textContent;
    let f = fetch(uri, {method: "PUT",
        body: document.getElementById("editor").innerText.replace(/\r\n/g, "\n")});
}
