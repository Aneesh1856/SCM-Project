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

        const data = await res.json();
        if (data.status === "success") {
            responseMsg.textContent = "Feedback submitted successfully!";
            form.reset();
            loadFeedbacks();
        } else {
            responseMsg.textContent = "There was an error submitting feedback.";
        }
    });

    async function loadFeedbacks() {
        const res = await fetch("/feedbacks");
        const feedbacks = await res.json();
        feedbackList.innerHTML = "";
        feedbacks.reverse().forEach(fb => {
            const entry = document.createElement("div");
            entry.className = "feedback-entry";
            entry.innerHTML = `
                <div class="name">${fb.name || "Anonymous"}</div>
                <div class="message">${fb.message}</div>
                <div class="timestamp">${fb.timestamp}</div>
            `;
            feedbackList.appendChild(entry);
        });
    }

    loadFeedbacks();
});
