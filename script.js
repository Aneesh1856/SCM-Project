document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("feedback-form");
    const responseMsg = document.getElementById("response-msg");
    const feedbackList = document.getElementById("feedback-list");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const message = document.getElementById("message").value.trim();

        if (!message) {
            responseMsg.textContent = "Please enter your feedback before submitting.";
            responseMsg.style.color = "red";
            return;
        }

        try {
            const res = await fetch("/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, message })
            });

            const data = await res.json();
            if (data.status === "success") {
                responseMsg.textContent = "Feedback submitted successfully!";
                responseMsg.style.color = "green";
                form.reset();
                loadFeedbacks();
            } else {
                responseMsg.textContent = "There was an error submitting feedback.";
                responseMsg.style.color = "red";
            }
        } catch (error) {
            responseMsg.textContent = "Network error. Please try again later.";
            responseMsg.style.color = "red";
            console.error("Submission error:", error);
        }
    });

    async function loadFeedbacks() {
        try {
            const res = await fetch("/feedbacks");
            const feedbacks = await res.json();

            feedbackList.innerHTML = "";
            feedbacks.reverse().forEach(fb => {
                const item = document.createElement("li");
                item.className = "feedback-entry";
                item.innerHTML = `
                    <strong>${fb.name || "Anonymous"}</strong> 
                    <p>${fb.message}</p>
                    <small>${fb.timestamp}</small>
                `;
                feedbackList.appendChild(item);
            });
        } catch (error) {
            console.error("Error loading feedbacks:", error);
            feedbackList.innerHTML = "<li>Failed to load feedback. Please refresh.</li>";
        }
    }

    loadFeedbacks();
});
