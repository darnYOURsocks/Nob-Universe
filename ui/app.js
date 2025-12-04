function navigate(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

function formatJson(data) {
    return JSON.stringify(data, null, 2);
}

async function loadExperiments() {
    const container = document.getElementById("experiments-list");
    container.innerHTML = "Loading experiments...";

    try {
        const experiments = await fetch("/api/experiments").then(r => r.json());
        if (!experiments.length) {
            container.textContent = "No experiments available.";
            return;
        }

        container.innerHTML = "";
        experiments.forEach(exp => {
            const card = document.createElement("div");
            card.className = "card interactive";
            card.innerHTML = `
                <h3>${exp.name}</h3>
                <p>${exp.description}</p>
                <div class="tags">${exp.tags.map(t => `<span>${t}</span>`).join('')}</div>
                <button class="run-btn" data-exp="${exp.id}">Run</button>
            `;
            container.appendChild(card);
        });

        container.querySelectorAll(".run-btn").forEach(btn => {
            btn.addEventListener("click", () => runExperiment(btn.dataset.exp));
        });
    } catch (err) {
        container.textContent = "Failed to load experiments.";
    }
}

async function runExperiment(name) {
    const output = document.getElementById("experiment-output");
    output.textContent = `Running ${name}...`;

    try {
        const res = await fetch(`/api/experiments/${name}/run`, { method: "POST" });
        const result = await res.json();
        output.textContent = res.ok ? formatJson(result) : `Error: ${result.error || 'Unable to run experiment'}`;
    } catch (err) {
        output.textContent = "Experiment failed to run.";
    }
}

async function loadCodex() {
    const container = document.getElementById("codex-list");
    container.innerHTML = "Loading codex entries...";

    try {
        const files = await fetch("/api/codex/entries").then(r => r.json());

        if (!files.length) {
            container.textContent = "No codex entries found.";
            return;
        }

        container.innerHTML = "";
        files.forEach(entry => {
            const card = document.createElement("div");
            card.className = "card interactive";
            card.innerHTML = `
                <h3>${entry.title}</h3>
                <p>${entry.description}</p>
                <small>${entry.id}</small>
            `;
            card.addEventListener("click", () => loadCodexEntry(entry.id));
            container.appendChild(card);
        });
    } catch (err) {
        container.textContent = "Failed to load codex entries.";
    }
}

async function loadCodexEntry(id) {
    const output = document.getElementById("codex-entry");
    output.textContent = `Loading ${id}...`;

    try {
        const res = await fetch(`/api/codex/entries/${id}`);
        const data = await res.json();
        output.textContent = res.ok ? formatJson(data) : `Error: ${data.error || 'Unable to load entry'}`;
    } catch (err) {
        output.textContent = "Failed to load entry.";
    }
}

// CSV Viewer
document.getElementById("csv-input").addEventListener("change", function() {
    const reader = new FileReader();
    reader.onload = () => {
        document.getElementById("csv-output").textContent = reader.result;
    };
    reader.readAsText(this.files[0]);
});

loadExperiments();
loadCodex();
