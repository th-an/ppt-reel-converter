# PPT Reel Converter

Convert landscape PowerPoint presentations to Instagram Reel (9:16) portrait scenes with AI-assisted layout and per-slide validation.

## Architecture

### 4-Gate Pipeline (Per Slide, Sequential Approval)

```
Gate 1: SCAN     → Parse PPTX, extract all elements (title, bullets, images, numbers)
Gate 2: PLAN     → AI/Rule engine decides how to split into reel scenes
Gate 3: RENDER   → Generate 9:16 PPTX using template placeholders
Gate 4: VERIFY   → Validate content integrity, typography, whitespace (score 0-100)

Slide N+1 does NOT start until Slide N is approved, retried, or skipped.
```

### Tech Stack

- **Backend**: Python 3.11+, `python-pptx`, `httpx`, `pydantic`, `Pillow`
- **AI**: OpenCode Go API (`deepseek-v4-flash` or `glm-5`) for layout decisions
- **Frontend**: Electron 30 + React 18 + TypeScript + Vite + TailwindCSS
- **Template**: 9:16 portrait `.pptx` with slide master layouts

## Quick Start

### 1. Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r python/requirements.txt
```

### 2. Install Node.js Dependencies

```bash
npm install
```

### 3. Create Template (Optional)

```bash
python scripts/create_template.py
```

### 4. Run CLI

```bash
python -m reel_converter.cli tests/fixtures/simple_test.pptx --template reel_clean
```

### 5. Run Electron App (Development)

```bash
npm run electron:dev
```

## Project Structure

```
ppt-reel-converter/
├── python/reel_converter/          # Python backend
│   ├── gate1_scan/                 # PPTX parser, shape classifier
│   ├── gate2_plan/                 # AI agent + rule engine
│   ├── gate3_render/               # PPTX generator, content fitter
│   ├── gate4_verify/               # Content integrity + scoring
│   ├── pipeline/                   # Orchestrator + approval manager
│   ├── schemas/                    # Pydantic models
│   └── templates/                  # 9:16 portrait templates
├── electron/                       # Electron main process
├── src/                            # React frontend
├── tests/fixtures/                 # Test PPTX files
└── scripts/                        # Utility scripts
```

## Validation Scoring

| Category | Weight | Checks |
|----------|--------|--------|
| Content Integrity | 40% | Title, bullets, numbers, images preserved |
| Text Readability | 25% | No overflow, font sizes ≥ 14pt, hierarchy |
| Visual Quality | 20% | Safe zones, whitespace balance |
| Theme Consistency | 15% | Colors, fonts match original |

**Pass threshold**: 80/100

## Templates

- `reel_clean` — Dark background, clean typography
- `reel_modern` — Bold colors, gradient backgrounds
- `reel_bold` — Heavy typography, high contrast
- `reel_minimal` — Light, lots of whitespace
- `reel_corporate` — Professional, structured

## License

MIT
