const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const rootDir = __dirname;
const experimentsDir = path.join(rootDir, "experiments");
const codexEntriesDir = path.join(rootDir, "codex", "entries");

app.use(express.json());
app.use("/ui", express.static(path.join(rootDir, "ui")));
app.use("/visualizers", express.static(path.join(rootDir, "visualizers")));

app.get("/", (req, res) => {
  res.sendFile(path.join(rootDir, "ui", "index.html"));
});

function safeResolve(baseDir, candidate) {
  const resolved = path.resolve(baseDir, candidate);
  if (!resolved.startsWith(baseDir)) {
    return null;
  }
  return resolved;
}

app.get("/api/experiments", (req, res) => {
  if (!fs.existsSync(experimentsDir)) {
    return res.json([]);
  }

  const files = fs.readdirSync(experimentsDir).filter(file => file.endsWith(".js"));
  const experiments = files.map(file => {
    const experiment = require(path.join(experimentsDir, file));
    const id = path.basename(file, ".js");
    return {
      id,
      name: experiment.metadata?.name || id,
      description: experiment.metadata?.description || "Experiment ready to run",
      tags: experiment.metadata?.tags || [],
    };
  });

  res.json(experiments);
});

app.post("/api/experiments/:id/run", (req, res) => {
  const { id } = req.params;
  const experimentPath = safeResolve(experimentsDir, `${id}.js`);

  if (!experimentPath || !fs.existsSync(experimentPath)) {
    return res.status(404).json({ error: `Experiment ${id} not found` });
  }

  try {
    const experiment = require(experimentPath);
    if (typeof experiment.run !== "function") {
      return res.status(500).json({ error: `Experiment ${id} is missing a run() function` });
    }

    const result = experiment.run();
    res.json({ id, name: experiment.metadata?.name || id, result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/api/codex/entries", (req, res) => {
  if (!fs.existsSync(codexEntriesDir)) {
    return res.json([]);
  }

  const files = fs.readdirSync(codexEntriesDir).filter(file => file.endsWith(".json"));
  const entries = files.map(file => {
    const fullPath = path.join(codexEntriesDir, file);
    const content = JSON.parse(fs.readFileSync(fullPath, "utf-8"));
    return {
      id: path.basename(file, ".json"),
      title: content.title || content.name || file,
      description: content.summary || content.description || "Codex entry",
    };
  });

  res.json(entries);
});

app.get("/api/codex/entries/:id", (req, res) => {
  const { id } = req.params;
  const entryPath = safeResolve(codexEntriesDir, `${id}.json`);

  if (!entryPath || !fs.existsSync(entryPath)) {
    return res.status(404).json({ error: `Codex entry ${id} not found` });
  }

  try {
    const content = JSON.parse(fs.readFileSync(entryPath, "utf-8"));
    res.json(content);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/codex/list", (req, res) => {
  const files = fs.existsSync(codexEntriesDir)
    ? fs.readdirSync(codexEntriesDir).filter(file => file.endsWith(".json"))
    : [];
  res.json(files);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`NŊOB Universe UI: http://localhost:${port}/ui/index.html`);
});
