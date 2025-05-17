document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("feedback-form");
    const responseMsg = document.getElementById("response-msg");
    const feedbackList = document.getElementById("feedback-list");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("name").value;
        const message = document.getElementById("message").value;

        const res = await fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, message })
        });

