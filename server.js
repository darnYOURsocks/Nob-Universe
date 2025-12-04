import express from "express";
import path from "path";
import fs from "fs";
import { exec } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();

app.use(express.static(__dirname));

app.get("/run", (req, res) => {
  const exp = req.query.exp;
  exec(`node experiments/${exp}.js`, (err, stdout, stderr) => {
      if (err) return res.send(stderr);
      res.send(stdout);
  });
});

app.get("/codex/list", (req, res) => {
  const dir = path.join(__dirname, "codex/entries");
  const files = fs.readdirSync(dir);
  res.json(files);
});

app.listen(3000, () => {
    console.log("NŊOB Universe UI: http://localhost:3000/ui/index.html");
});

