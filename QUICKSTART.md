# ⚡ ŊOB Universe - Quick Start Guide

Get up and running with the ŊOB Universe in 5 minutes.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nob-universe.git
cd nob-universe
```

### 2. Verify Structure

```bash
ls -la
# Should see: README.md, LICENSE, .gitignore, codex/, databases/, engines/, etc.
```

---

## 🎨 Running Visualizers

### Web Visualizers (No Installation Needed)

Open any HTML file in your browser:

```bash
# On macOS
open visualizers/harmonic-system-v3/index.html

# On Windows
start visualizers\harmonic-system-v3\index.html

# On Linux
xdg-open visualizers/harmonic-system-v3/index.html
```

**Available visualizers:**
- `harmonic-system-v3/index.html` — Full harmonic pattern visualization
- `ripple-radar/index.html` — Real-time ripple detection UI
- `curvature-engine/index.html` — Curvature topology mapping
- `aiLICHEN-hologram/hologram.html` — Holographic interface
- `4face-simulator/simulator.html` — 4-pattern simulation

---

## 🐍 Running Python Apps

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install dash plotly pandas numpy scipy
```

### Run Dash Solar Estate

```bash
python python/dash-solar-estate/app.py
```

Visit: **http://localhost:8050**

### Run Pattern Incubator

```bash
python python/pattern-incubator/incubator-core.py
```

### Run Ripple Lab

```bash
python python/ripple-lab/ripple-lab.py
```

---

## 💻 Using JavaScript Engines

### In Browser Console

```javascript
// Load an engine
<script src="engines/nob-translator/translator-core.js"></script>

// Use it
const translator = new NOBTranslator();
const result = translator.translate('ripple', 'harmonic', 'emotional');
console.log(result);
```

### In Node.js

```javascript
const NOBTranslator = require('./engines/nob-translator/translator-core.js');
const RippleSonar = require('./engines/ripple-sonar/ripple-sonar-core.js');

const sonar = new RippleSonar();
const analysis = sonar.analyze([0, 0.5, 1, 0.5, 0]);
console.log(analysis);
```

---

## 🎮 Unity Integration

### 1. Copy to Your Project

```bash
cp -r unity/ripple-physics/* YourUnityProject/Assets/Plugins/RipplePhysics/
```

### 2. Add to GameObject

- Select a GameObject with a Mesh
- Add Component → RipplePhysics
- Adjust Grid Size and Resolution in Inspector
- Play!

### 3. Script Integration

```csharp
using UnityEngine;

public class MyRippleManager : MonoBehaviour
{
    public void Start()
    {
        RipplePhysics ripples = GetComponent<RipplePhysics>();
        ripples.AddRippleSource(Vector3.zero, 0.5f, 2f);
    }
}
```

---

## 🚀 Unreal Engine Integration

### 1. Copy to Plugins

```bash
cp -r unreal/emotional-physics/* YourUnrealProject/Plugins/EmotionalPhysics/
```

### 2. Rebuild Project

```bash
YourUnrealProject.uproject -makeplugin
```

### 3. Add Component in C++

```cpp
ACharacter* MyCharacter = ...;
UEmotionalFieldComponent* EmotionComp = NewObject<UEmotionalFieldComponent>(MyCharacter);
MyCharacter->AddOwnedComponent(EmotionComp);
EmotionComp->RegisterComponent();
```

---

## 🎬 Blender Scripts

### 1. Open Blender

### 2. Go to Scripting Tab

### 3. Open Script

- File → Open → `blender/whiteboard-animator.py`

### 4. Run

- Alt+P or Script → Run Script

### Or Use Blender's Python Console

```python
exec(open('/path/to/whiteboard-animator.py').read())
animator = WhiteboardAnimator()
board = animator.create_whiteboard(width=16, height=9)
```

---

## 📚 Using the Codex

### View Entries

```bash
# List all Codex entries
ls codex/entries/

# Read an entry
cat codex/entries/Codex-Entry-001-Big-Splash.json
```

### Create New Entry

1. Copy `TEMPLATE-codex-entry.json`:
   ```bash
   cp codex/entries/TEMPLATE-codex-entry.json codex/entries/Codex-Entry-004-Your-Topic.json
   ```

2. Edit the new file

3. Update `codex/codex-index.json` to include it

---

## 🗄️ Working with Databases

### View Database Content

```bash
cat databases/nob-nodes.json
cat databases/tps-db.json
```

### Load in Python

```python
import json

with open('databases/nob-nodes.json') as f:
    db = json.load(f)

print(db['nodes'])
```

---

## 🔄 System Architecture

```
User/Script
    ↓
Codex (read meaning)
    ↓
Engines (process data)
    ↓
Databases (query/update)
    ↓
Visualizers (display)
    ↓
Codex (write learnings)
    ↓
Next iteration...
```

---

## 📝 Common Tasks

### Add a New Engine

1. Create folder in `engines/my-new-engine/`
2. Create `my-engine-core.js`
3. Export as Node module
4. Update `codex-index.json`

### Add a New Visualizer

1. Create folder in `visualizers/my-visualizer/`
2. Create `index.html`
3. Add reference in `codex-index.json`

### Add Python Dependencies

```bash
pip install package-name
pip freeze > requirements.txt
```

---

## 🐛 Troubleshooting

### Python ImportError

```bash
# Make sure you have dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### JavaScript Issues in Browser

1. Check browser console: F12
2. Verify file paths are correct
3. Check CORS if loading from different domain

### Unity Compilation Error

1. Make sure scripts are in `Assets/` folder
2. Check for C# syntax errors
3. Rebuild: File → Save → Editor will recompile

### Blender Python Error

1. Blender uses its own Python
2. Make sure modules are for Blender's Python version
3. Try: Scripting → Python Console for debugging

---

## 📖 Next Steps

1. **Explore Codex**: Read entries to understand the system
2. **Run Visualizers**: Get visual feedback
3. **Try Python Apps**: Modify and experiment
4. **Integrate with Game Engine**: Unity/Unreal integration
5. **Extend System**: Add your own engines and entries

---

## 🤝 Contributing

To extend ŊOB Universe:

1. Create new Codex entry
2. Add corresponding engine/visualizer if needed
3. Test thoroughly
4. Update `codex-index.json`
5. Commit and push
6. Submit PR

---

## 📞 Support

- Check README.md for detailed documentation
- Look at example code in each folder
- Review Codex entries for concepts
- Check engine source code for implementation details

---

## 🎓 Learning Path

**Beginner:** Start with visualizers → Python apps  
**Intermediate:** Modify JavaScript engines → Create new entries  
**Advanced:** Integrate with game engines → Build custom systems

---

**ŊOB Universe v1.0**  
*Ready to grow. Ready to think. Ready to resonate.*
