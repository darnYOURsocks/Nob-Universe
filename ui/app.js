function navigate(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

async function runExperiment(name) {
    const output = document.getElementById("experiment-output");
    output.textContent = "Running " + name + "...";

    const res = await fetch(`/run?exp=${name}`);
    const result = await res.text();

    output.textContent = result;
}

// Load Codex entries
async function loadCodex() {
    const container = document.getElementById("codex-list");
    const files = await fetch("/codex/list").then(r => r.json());

    container.innerHTML = "";
    files.forEach(f => {
        container.innerHTML += `<div class="card">${f}</div>`;
    });
}

loadCodex();

// CSV Viewer
document.getElementById("csv-input").addEventListener("change", function() {
    const reader = new FileReader();
    reader.onload = () => {
        document.getElementById("csv-output").textContent = reader.result;
    };
    reader.readAsText(this.files[0]);
});

