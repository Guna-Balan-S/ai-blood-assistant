// 🌐 Backend URL (IMPORTANT)
const BASE_URL = "https://ai-blood-assistant.onrender.com";

// 🔥 Load donors from backend
async function loadDonors() {
    try {
        const res = await fetch(`${BASE_URL}/api/donors`);
        const data = await res.json();

        const list = document.getElementById("donorList");
        list.innerHTML = "";

        let o = 0, a = 0, b = 0;

        data.forEach(d => {
            const li = document.createElement("li");

            const name = d.name || "Unknown";
            const blood = d.blood || "";
            const location = d.location || "";

            li.textContent = `${name}, ${blood}, ${location}`;
            list.appendChild(li);

            if (blood === "O+") o++;
            if (blood === "A+") a++;
            if (blood === "B+") b++;
        });

        document.getElementById("oCount").innerText = o;
        document.getElementById("aCount").innerText = a;
        document.getElementById("bCount").innerText = b;
        document.getElementById("totalCount").innerText = data.length;

    } catch (error) {
        console.error("Error loading donors:", error);
    }
}

// 🔥 Become donor
async function becomeDonor() {
    const name = prompt("Enter your name:");
    const blood = prompt("Enter blood group:");
    const location = prompt("Enter location:");

    if (!name || !blood || !location) {
        alert("All fields required!");
        return;
    }

    try {
        await fetch(`${BASE_URL}/api/add-donor`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: String(name),
                blood: String(blood),
                location: String(location)
            })
        });

        alert("You are now a donor!");
        loadDonors();

    } catch (error) {
        console.error("Error adding donor:", error);
    }
}

// 🔥 Chat
async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div><b>You:</b> ${message}</div>`;
    input.value = "";

    try {
        const res = await fetch(`${BASE_URL}/chat?query=${encodeURIComponent(message)}`);
        const data = await res.json();

        chatBox.innerHTML += `<div><b>AI:</b><br>${data.results.join("<br>")}</div>`;

    } catch (error) {
        console.error("Chat error:", error);
        chatBox.innerHTML += `<div><b>AI:</b> Server error</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// 🔥 Load on start
loadDonors();