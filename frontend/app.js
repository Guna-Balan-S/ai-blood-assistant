const donors = [
    "Arun, O+, Karur",
    "Siva, O+, Karur",
    "Ravi, A+, Trichy",
    "Kumar, B+, Chennai"
];

// 🔥 Load dashboard stats
function loadDashboard() {
    let o = 0, a = 0, b = 0;

    donors.forEach(d => {
        if (d.includes("O+")) o++;
        if (d.includes("A+")) a++;
        if (d.includes("B+")) b++;
    });

    document.getElementById("oCount").innerText = o;
    document.getElementById("aCount").innerText = a;
    document.getElementById("bCount").innerText = b;
    document.getElementById("totalCount").innerText = donors.length;

    // Fill donor list
    const list = document.getElementById("donor-list");
    donors.forEach(d => {
        list.innerHTML += `<li>${d}</li>`;
    });
}

// 🔥 Chat function
async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div><b>You:</b> ${message}</div>`;

    input.value = "";

    const res = await fetch(`http://127.0.0.1:8000/chat?query=${message}`);
    const data = await res.json();

    chatBox.innerHTML += `<div><b>AI:</b><br>${data.results.join("<br>")}</div>`;

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Load on start
loadDashboard();


async function addDonor() {
    const name = prompt("Enter name");
    const blood = prompt("Enter blood group");
    const location = prompt("Enter location");

    await fetch("http://127.0.0.1:8000/add-donor", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, blood, location})
    });

    alert("You are now a donor!");
}