fetch('/projects')
    .then(response => response.json())
    .then(data => {
        console.log("Projects:", data);
    });

document.querySelector("#contact-form").addEventListener("submit", function(e) {
    e.preventDefault();
    let formData = {
        name: document.querySelector("#name").value,
        email: document.querySelector("#email").value,
        message: document.querySelector("#message").value
    };

    fetch("/contact", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
    }).then(res => res.json()).then(data => alert(data.message));
});
