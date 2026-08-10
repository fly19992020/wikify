const form = document.getElementById("editorForm");
const textarea = form.elements.content;

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const uri = form.elements.uri.value;
    const action = event.submitter.value; // fetch 或 commit

    if (action === "fetch") {
        fetch(uri + "?source=true")
            .then(response => response.text())
            .then(text => {
                textarea.value = text;
            });
    }

    if (action === "commit") {
        const body = textarea.value.replace(/\r\n/g, "\n");

        fetch(uri, {
            method: "PUT",
            headers: {
                "Content-Type": "text/plain; charset=utf-8"
            },
            body: body
        }).then(_ => alert("OK. "));
    }
});

let queryString = window.location.search;
let params = new URLSearchParams(queryString);
if (params.get("page")) {
    fetch(params.get("page") + "?source=true")
        .then(response => response.text())
        .then(text => {
            textarea.value = text;
        });
}