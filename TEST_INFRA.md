# TEST INFRASTRUCTURE — GEARS. Corporation Portal

**Document**: `TEST_INFRA.md`  
**Test Harness Version**: 2.0 (Dual Track Protocol)  
**Author**: `e2e_test_writer_1` (teamwork_test_writer / specialist & qa)  
**Project**: GEARS. Corporation Portal & Hardware Ecosystem (`gearsbr.github.io`)  
**Repository**: `/home/user/Documents/Antigravity/GEARS.`  

---

## 1. Overview & Architectural Philosophy

The GEARS. Corporation Portal test suite is designed under the **Dual Track Protocol**: an independent, opaque-box, requirement-driven verification harness developed concurrently with the site overhaul. It validates all 21 features specified in `PROJECT.md` § Feature Inventory and the authoritative user request in `ORIGINAL_REQUEST.md`.

### Core Technical Pillars:
1. **Zero External Dependencies**: Built strictly using the Python 3 standard library (`html.parser`, `urllib.request`, `re`, `json`, `math`, `inspect`, `time`). Requires no npm packages, browser automation drivers (Puppeteer/Playwright), or heavy runtime frameworks.
2. **Dual-Mode Execution**:
   - **Static Verification Mode**: Deep semantic analysis of source files (`index.html`, `css/styles.css`, `js/main.js`, and `assets/*.svg`) verifying DOM landmarks, CSS custom properties, WCAG AAA relative luminance, SVG geometry, and ES6 module architectures.
   - **Live Server Mode**: Connects to `http://localhost:8000` (or user-specified URL) to audit HTTP response codes, asset MIME types, and endpoint accessibility.
3. **Deterministic Mathematical Formulas**: Tests particulate calculations against WHO exposure-response models and canonical fluid dynamic ratings ($380\text{ m}^3/\text{h}$ base vs $836\text{ m}^3/\text{h}$ FEARS.™ boost).

---

## 2. 4-Tier Test Architecture

The suite organizes 238 comprehensive test assertions across four distinct verification tiers:

```
+-----------------------------------------------------------------------------+
| GEARS. Corporation 4-Tier Test Architecture (238 Total Assertions)          |
+-----------------------------------------------------------------------------+
| Tier 1: Feature Coverage (Features 1–21)            | 105 Test Cases        |
| - Happy-path functional verification (5 tests/feat) | Status: 100% PASS     |
+-----------------------------------------------------------------------------+
| Tier 2: Boundary & Corner Cases (Features 1–21)     | 105 Test Cases        |
| - Contrast limits, edge parameters, SVG geometry   | Status: 100% PASS     |
+-----------------------------------------------------------------------------+
| Tier 3: Cross-Feature Combinations (Pairwise)       | 12 Test Cases         |
| - Visualizer + FEARS, Calculator + Presets, PIX     | Status: 100% PASS     |
+-----------------------------------------------------------------------------+
| Tier 4: Real-World Application Workflows            | 16 Test Cases         |
| - Municipal technician, Civic donor, FEARS engineer | Status: 100% PASS     |
+-----------------------------------------------------------------------------+
```

### Tier 1: Feature Coverage (105 Tests)
- **Features 1 to 21**: Happy-path functional verification (5 tests per feature).
- Validates canonical SVG geometry, Off-White palette tokens, 1:1 favicon, navbar lockup alignment at $Y=49$, Apple Open Source manifesto, 7 hardware modules, FEARS.™ division, Congonhas context, donation section, 3 support tiers, PIX `<dialog>` modal, 1-click clipboard copy, official bank details, interactive visualizer, particulate calculator, live telemetry simulation, technical accordion FAQ, design tokens, micro-interactions, WCAG AAA accessibility, and zero-dependency performance.

### Tier 2: Boundary & Corner Cases (105 Tests)
- **Edge Conditions & Extreme Parameters**:
  - WCAG AAA contrast ratio calculation: ensures Deep Navy `#0A192F` and Petroleum `#0F3A4D` exceed 14:1 and 10:1 on Off-White Canvas `#FBFBFD`.
  - SVG viewBox scaling & center bore: ensures `fill-rule="evenodd"` and complete absence of opaque white masking disks.
  - Modal keyboard traps, Escape dismissal, backdrop click detection, and clipboard fallback mechanisms (`execCommand` / text selection).
  - Calculator input boundaries: slider `min`, `max`, `step`, and FEARS $+120\%$ boost multiplier ($836 / 380 = 2.20$).
  - Telemetry jitter: bounded organic micro-variation algorithm.
  - Responsive stacking: media queries for mobile viewports ($< 768\text{px}$).

### Tier 3: Cross-Feature Combinations (12 Tests)
- **Pairwise Subsystem Integrations**:
  1. Modular Visualizer + FEARS High-Performance Boost Mode (Feature 14 + Feature 7)
  2. Calculator Sliders + Congonhas Corridor Preset Buttons (Feature 15 + Feature 8)
  3. Calculator + FEARS Twin-Turbine Boost Rate (Feature 15 + Feature 7)
  4. Telemetry Jitter + Alert LED Pulse + Tabular Numerals (Feature 16 + Feature 18)
  5. PIX Modal + 1-Click Clipboard Copy + "Copiado!" State Morph (Feature 11 + Feature 12)
  6. Support Tiers + PIX Modal Open Trigger (Feature 10 + Feature 11)
  7. PIX Modal + Escape Key Handling + Focus Restoration (Feature 11 + Feature 20)
  8. Brand Lockup + Off-White Contrast + 1:1 Favicon Geometry (Feature 1 + Feature 2 + Feature 3)
  9. FAQ Accordion + Category Filter Pills + ARIA Expansion (Feature 17 + Feature 20)
  10. Telemetry Simulation + VisibilityChange Tab Hibernation (Feature 16 + Feature 21)
  11. Exploded View Transition + 7 Hardware Subsystem Coordinates (Feature 14 + Feature 6)
  12. Skip Link Navigation + Sticky Blurred Header Offset (Feature 19 + Feature 20)

### Tier 4: Real-World Application Workflows (16 Tests)
- **End-to-End User Journeys**:
  - **Journey 1: Congonhas Municipal Environmental Technician**: Navigates Congonhas mining context, inspects HEPA H13 specs, evaluates "Av. Júlia Kubitschek" corridor simulation in calculator ($49.9\text{M m}^3/\text{ano}$ clean air), and reviews deployment FAQ.
  - **Journey 2: Civic Maker & Community Donor**: Navigates to `#apoie-inovacao`, reviews 3 support tiers, opens PIX `<dialog>` modal, copies PIX key, receives instant "✓ Chave Copiada com Sucesso!" visual feedback, and checks GitHub transparency audit statement.
  - **Journey 3: Mining Fleet Performance Engineer**: Jumps to `#divisao-fears`, reviews Mercedes-AMG / Maybach extreme tuning philosophy, inspects aerospace carbon fiber modules, and calculates boosted industrial buffer filtration ($183\text{M m}^3/\text{ano}$).
  - **Journey 4: Accessibility & Standards Auditor**: Verifies skip-to-content focus, semantic landmark tags (`header`, `nav`, `main`, `footer`), `:focus-visible` dual-ring styling, and WCAG AAA contrast ratios $\ge 7:1$.

---

## 3. Directory Layout & File Ownership

All test files reside exclusively inside the `tests/` directory:

```text
tests/
├── __init__.py                  # Package marker
├── test_helpers.py              # HTML DOM tree parser, CSS token & contrast engine, SVG validator
├── test_tier1_features.py       # Tier 1 Feature Coverage (105 tests across Features 1–21)
├── test_tier2_boundaries.py     # Tier 2 Boundary & Corner Cases (105 tests across Features 1–21)
├── test_tier3_combinations.py   # Tier 3 Cross-Feature Combinations (12 tests)
├── test_tier4_workflows.py      # Tier 4 Real-World Application Workflows (16 tests)
└── run_tests.py                 # Executable CLI test runner with ANSI reporting & exit codes
```

---

## 4. How to Run the Tests

### 4.1 Quick Run (Complete 4-Tier Suite)
```bash
python3 tests/run_tests.py
```

### 4.2 Verbose Run (Per-Test Inspection)
```bash
python3 tests/run_tests.py -v
```

### 4.3 Running Specific Tiers
```bash
# Tier 1 only (Feature Coverage)
python3 tests/run_tests.py --tier 1

# Tier 2 only (Boundaries & Corners)
python3 tests/run_tests.py --tier 2

# Tier 3 only (Pairwise Combinations)
python3 tests/run_tests.py --tier 3

# Tier 4 only (Real-World Workflows)
python3 tests/run_tests.py --tier 4
```

### 4.4 Running with Live Server Health Check
```bash
# Start local server in background (e.g., port 8000)
python3 -m http.server 8000 &

# Run test suite with server endpoint verification
python3 tests/run_tests.py --server http://localhost:8000
```

---

## 5. Exit Codes & CI/CD Integration

- **Exit Code `0`**: All test assertions passed completely. Safe for production deployment to GitHub Pages.
- **Exit Code `1`**: One or more test assertions failed. A detailed failure breakdown is output to `stderr` / `stdout`.
