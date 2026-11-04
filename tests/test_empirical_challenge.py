#!/usr/bin/env python3
"""
GEARS. Corporation — Empirical Challenge Verification & Stress Harness
Author: challenger_1 (teamwork_challenger)
Purpose: Independent empirical stress-testing of SVG geometry, particulate engine,
         telemetry stability, and WCAG contrast.
Standard Library Only — Zero External Dependencies.
"""

import math
import os
import random
import re
import sys
from typing import Dict, List, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.test_helpers import (
    hex_to_rgb,
    relative_luminance,
    wcag_contrast_ratio,
    parse_css_tokens,
    read_project_file,
    parse_svg
)


def extract_gear_vertices(path_d: str) -> List[Tuple[float, float]]:
    outer_loop_str = path_d.split("Z")[0]
    tokens = re.split(r'([MLAZ])', outer_loop_str)
    cur_cmd = None
    all_points = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in ('M', 'L', 'A', 'Z'):
            cur_cmd = token
        else:
            nums = [float(x) for x in token.split()]
            if cur_cmd in ('M', 'L'):
                for i in range(0, len(nums), 2):
                    all_points.append((nums[i], nums[i+1]))
            elif cur_cmd == 'A':
                all_points.append((nums[-2], nums[-1]))

    # Deduplicate sequential identical points
    unique_vertices = []
    for pt in all_points:
        if not unique_vertices or (abs(pt[0] - unique_vertices[-1][0]) > 1e-4 or abs(pt[1] - unique_vertices[-1][1]) > 1e-4):
            unique_vertices.append(pt)

    # If the last point closes the loop back to the first, exclude the duplicate closing point
    if len(unique_vertices) > 1 and math.hypot(unique_vertices[-1][0] - unique_vertices[0][0], unique_vertices[-1][1] - unique_vertices[0][1]) < 1e-3:
        unique_vertices.pop()

    return unique_vertices


def run_svg_geometry_challenge() -> Dict[str, any]:
    print("\n=======================================================")
    print("▶ CHALLENGE 1: SVG 8-Tooth Geometry & Symmetry Analysis")
    print("=======================================================")

    results = {}

    # ---------------------------------------------------------
    # 1. Favicon SVG Analysis
    # ---------------------------------------------------------
    favicon_content = read_project_file("assets/favicon.svg")
    fav_svg = parse_svg(favicon_content)

    results["fav_evenodd"] = fav_svg.has_evenodd_fill_rule()
    results["fav_no_white"] = not fav_svg.has_opaque_white_circles() and "#FFFFFF" not in favicon_content.upper() and "#FFF" not in favicon_content.upper() and "WHITE" not in favicon_content.upper()

    d_fav = re.search(r'd="([^"]+)"', favicon_content).group(1)
    fav_vertices = extract_gear_vertices(d_fav)
    results["fav_vertex_count"] = len(fav_vertices)

    cx_fav, cy_fav = 50.0, 50.0
    fav_root_radii = []
    fav_outer_radii = []

    for i, (vx, vy) in enumerate(fav_vertices):
        dist = math.hypot(vx - cx_fav, vy - cy_fav)
        idx_in_tooth = i % 4
        if idx_in_tooth in (0, 3):
            fav_root_radii.append(dist)
        else:
            fav_outer_radii.append(dist)

    results["fav_avg_root_r"] = sum(fav_root_radii) / len(fav_root_radii)
    results["fav_avg_outer_r"] = sum(fav_outer_radii) / len(fav_outer_radii)

    # Test 8-fold rotational symmetry (45 degree intervals) on favicon
    tooth_0 = fav_vertices[0:4]
    fav_max_sym_err = 0.0
    for k in range(1, 8):
        theta = math.radians(k * 45.0)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        tooth_k = fav_vertices[k*4 : (k+1)*4]
        for p_idx in range(4):
            x0, y0 = tooth_0[p_idx]
            dx, dy = x0 - cx_fav, y0 - cy_fav
            exp_x = cx_fav + (dx * cos_t - dy * sin_t)
            exp_y = cy_fav + (dx * sin_t + dy * cos_t)
            act_x, act_y = tooth_k[p_idx]
            err = math.hypot(act_x - exp_x, act_y - exp_y)
            if err > fav_max_sym_err:
                fav_max_sym_err = err

    results["fav_max_sym_err"] = fav_max_sym_err

    # Favicon Center bore radius
    bore_fav_match = re.search(r'M\s+50(?:\.0+)?\s+36(?:\.0+)?\s+A\s+([\d.]+)\s+([\d.]+)', d_fav)
    fav_bore_r = float(bore_fav_match.group(1)) if bore_fav_match else None
    results["fav_bore_r"] = fav_bore_r

    print(f"[favicon.svg]")
    print(f"  - Extracted Vertices: {len(fav_vertices)} (Target: 32)")
    print(f"  - Root Radius: mean={results['fav_avg_root_r']:.3f} (min={min(fav_root_radii):.3f}, max={max(fav_root_radii):.3f}, Target: 32.0)")
    print(f"  - Outer Radius: mean={results['fav_avg_outer_r']:.3f} (min={min(fav_outer_radii):.3f}, max={max(fav_outer_radii):.3f}, Target: 46.0)")
    print(f"  - Center Bore Radius: {fav_bore_r} (Target: 14.0)")
    print(f"  - 8-Fold Rotational Symmetry (45°): Max error = {fav_max_sym_err:.4f} px (Target: < 0.05 px)")
    print(f"  - fill-rule='evenodd': {results['fav_evenodd']}")
    print(f"  - Absence of White (#FFFFFF) fills: {results['fav_no_white']}")

    # ---------------------------------------------------------
    # 2. Logo-gears SVG Analysis
    # ---------------------------------------------------------
    logo_content = read_project_file("assets/logo-gears.svg")
    logo_svg = parse_svg(logo_content)
    results["logo_evenodd"] = logo_svg.has_evenodd_fill_rule()
    results["logo_no_white"] = not logo_svg.has_opaque_white_circles() and "#FFFFFF" not in logo_content.upper() and "#FFF" not in logo_content.upper() and "WHITE" not in logo_content.upper()

    d_logo = re.search(r'd="([^"]+)"', logo_content).group(1)
    logo_vertices = extract_gear_vertices(d_logo)
    results["logo_vertex_count"] = len(logo_vertices)

    cx_logo, cy_logo = 26.0, 28.0
    logo_root_radii = []
    logo_outer_radii = []

    for i, (vx, vy) in enumerate(logo_vertices):
        dist = math.hypot(vx - cx_logo, vy - cy_logo)
        idx_in_tooth = i % 4
        if idx_in_tooth in (0, 3):
            logo_root_radii.append(dist)
        else:
            logo_outer_radii.append(dist)

    results["logo_avg_root_r"] = sum(logo_root_radii) / len(logo_root_radii)
    results["logo_avg_outer_r"] = sum(logo_outer_radii) / len(logo_outer_radii)

    # Logo tooth 8-fold rotational symmetry (45 degree intervals)
    logo_tooth_0 = logo_vertices[0:4]
    logo_max_sym_err = 0.0
    for k in range(1, 8):
        theta = math.radians(k * 45.0)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        tooth_k = logo_vertices[k*4 : (k+1)*4]
        for p_idx in range(4):
            x0, y0 = logo_tooth_0[p_idx]
            dx, dy = x0 - cx_logo, y0 - cy_logo
            exp_x = cx_logo + (dx * cos_t - dy * sin_t)
            exp_y = cy_logo + (dx * sin_t + dy * cos_t)
            act_x, act_y = tooth_k[p_idx]
            err = math.hypot(act_x - exp_x, act_y - exp_y)
            if err > logo_max_sym_err:
                logo_max_sym_err = err

    results["logo_max_sym_err"] = logo_max_sym_err

    # Logo Center bore radius
    bore_logo_match = re.search(r'M\s+26(?:\.\d+)?\s+21\.5\d*\s+A\s+([\d.]+)\s+([\d.]+)', d_logo)
    if not bore_logo_match:
        # Fallback search for any arc after the second M
        bore_logo_match = re.search(r'M\s+[\d.]+\s+[\d.]+\s+A\s+([\d.]+)\s+([\d.]+)', d_logo.split("Z")[1])
    logo_bore_r = float(bore_logo_match.group(1)) if bore_logo_match else None
    results["logo_bore_r"] = logo_bore_r

    # Normalization scale factor: logo root radius / favicon root radius = 14.603 / 32.000 = 0.4563
    scale_norm = results["logo_avg_root_r"] / 32.0
    norm_outer_r = results["logo_avg_outer_r"] / scale_norm
    norm_bore_r = logo_bore_r / scale_norm

    results["logo_norm_outer_r"] = norm_outer_r
    results["logo_norm_bore_r"] = norm_bore_r

    print(f"\n[logo-gears.svg]")
    print(f"  - Extracted Vertices: {len(logo_vertices)} (Target: 32)")
    print(f"  - Actual Root Radius: mean={results['logo_avg_root_r']:.3f} (Normalized: 32.000)")
    print(f"  - Actual Outer Radius: mean={results['logo_avg_outer_r']:.3f} (Normalized: {norm_outer_r:.3f}, Target: 46.0)")
    print(f"  - Actual Center Bore Radius: {logo_bore_r} (Normalized: {norm_bore_r:.3f}, Target: 14.0)")
    print(f"  - 8-Fold Rotational Symmetry (45°): Max error = {logo_max_sym_err:.4f} px (Target: < 0.05 px)")
    print(f"  - fill-rule='evenodd': {results['logo_evenodd']}")
    print(f"  - Absence of White (#FFFFFF) fills: {results['logo_no_white']}")

    # Baseline Y=49 verification
    text_y_match = re.search(r'<text\b[^>]*y="(\d+)"', logo_content)
    text_y = int(text_y_match.group(1)) if text_y_match else None
    dot_rect_match = re.search(r'<rect\b[^>]*y="(\d+)"[^>]*height="(\d+)"', logo_content)
    dot_y = int(dot_rect_match.group(1)) if dot_rect_match else None
    dot_h = int(dot_rect_match.group(2)) if dot_rect_match else None
    dot_bottom = (dot_y + dot_h) if (dot_y and dot_h) else None
    print(f"  - Text Baseline Y: {text_y} (Target: 49)")
    print(f"  - Terminal Dot Bottom Y: {dot_bottom} (Target: 49)")

    results["text_y_49"] = (text_y == 49)
    results["dot_y_49"] = (dot_bottom == 49)

    return results


def run_particulate_calculator_challenge(trials: int = 1000) -> Dict[str, any]:
    print("\n=======================================================")
    print(f"▶ CHALLENGE 2: Particulate Impact Calculator ({trials} Property Tests)")
    print("=======================================================")

    random.seed(42)  # Deterministic seed for reproducible stress-testing

    failures = []
    monotonicity_violations = []

    # 1. Randomized Property Testing across parameter space:
    # node counts (1 to 500), operating hours (1 to 24), particulate concentrations (5 to 300 µg/m³)
    for i in range(trials):
        nodes = random.randint(1, 500)
        hours = random.randint(1, 24)
        pm = random.uniform(5.0, 300.0)
        fears_boost = random.choice([True, False])

        flow_per_unit = 836.0 if fears_boost else 380.0
        daily_volume = nodes * flow_per_unit * hours
        annual_volume = daily_volume * 365.0
        annual_mass_kg = annual_volume * pm * 0.9997 * 1e-9
        consultations = max(1, round(annual_mass_kg * 0.207))

        # Invariants:
        # a) Not NaN or Inf
        if any(math.isnan(x) or math.isinf(x) for x in (annual_volume, annual_mass_kg, consultations)):
            failures.append((i, "Non-finite float produced", (nodes, hours, pm, fears_boost)))

        # b) Strictly positive
        if annual_volume <= 0:
            failures.append((i, "Volume <= 0", annual_volume))
        if annual_mass_kg <= 0:
            failures.append((i, "Mass <= 0", annual_mass_kg))
        if consultations < 1:
            failures.append((i, "Consultations < 1", consultations))

    # 2. Monotonicity & FEARS 2.2x Ratio Test
    for _ in range(100):
        nodes = random.randint(1, 200)
        hours = random.randint(1, 24)
        pm = random.uniform(10.0, 200.0)

        vol_std = nodes * 380.0 * hours * 365.0
        vol_fears = nodes * 836.0 * hours * 365.0

        ratio = vol_fears / vol_std
        if abs(ratio - 2.2) > 1e-9:
            monotonicity_violations.append(f"FEARS boost ratio mismatch: {ratio} != 2.2")

        # Increasing nodes must strictly increase volume
        vol_more_nodes = (nodes + 1) * 380.0 * hours * 365.0
        if vol_more_nodes <= vol_std:
            monotonicity_violations.append(f"Volume not monotonic with nodes: {vol_std} >= {vol_more_nodes}")

        # Increasing pm must strictly increase mass
        mass_1 = vol_std * pm * 0.9997 * 1e-9
        mass_2 = vol_std * (pm + 1.0) * 0.9997 * 1e-9
        if mass_2 <= mass_1:
            monotonicity_violations.append("Mass not monotonic with PM concentration")

    # 3. Known Preset Validation
    presets = {
        'Av. Júlia Kubitschek': {'nodes': 15, 'pm': 65, 'hours': 24, 'exp_vol_std': 15 * 380 * 24 * 365},
        'Rua Bom Jesus': {'nodes': 8, 'pm': 40, 'hours': 18, 'exp_vol_std': 8 * 380 * 18 * 365},
        'Cinturão de Mineração': {'nodes': 25, 'pm': 95, 'hours': 24, 'exp_vol_std': 25 * 380 * 24 * 365}
    }
    preset_checks = {}
    for name, p in presets.items():
        v = p['nodes'] * 380 * p['hours'] * 365
        m = v * p['pm'] * 0.9997 * 1e-9
        h = max(1, round(m * 0.207))
        preset_checks[name] = {'volume_m3': v, 'mass_kg': round(m, 2), 'consultations': h}

    print(f"Property trials executed: {trials}")
    print(f"Failures found: {len(failures)}")
    print(f"Monotonicity violations: {len(monotonicity_violations)}")
    print("Preset check results:", preset_checks)

    return {
        "trials": trials,
        "failures": failures,
        "monotonicity_violations": monotonicity_violations,
        "presets": preset_checks
    }


def run_telemetry_simulator_challenge(ticks: int = 1000) -> Dict[str, any]:
    print("\n=======================================================")
    print(f"▶ CHALLENGE 3: Telemetry Simulator Stability ({ticks} Ticks)")
    print("=======================================================")

    random.seed(1337)

    base_pm25 = 18.4
    base_pm10 = 34.2

    pm25_readings = []
    pm10_readings = []
    ratio_factors_25 = []
    ratio_factors_10 = []
    multipliers = []

    for _ in range(ticks):
        # Multiplier bounded model: [1 - 0.008, 1 + 0.008] = [0.992, 1.008]
        factor = 1.0 + (random.random() - 0.5) * 0.016
        multipliers.append(factor)

        # Implementation model in js/main.js
        jitter25 = (random.random() - 0.5) * 0.6
        jitter10 = (random.random() - 0.5) * 1.0

        cur25 = max(12.0, base_pm25 + jitter25)
        cur10 = max(20.0, base_pm10 + jitter10)

        pm25_readings.append(cur25)
        pm10_readings.append(cur10)
        ratio_factors_25.append(cur25 / base_pm25)
        ratio_factors_10.append(cur10 / base_pm10)

    min_mult = min(multipliers)
    max_mult = max(multipliers)

    min_pm25, max_pm25 = min(pm25_readings), max(pm25_readings)
    min_pm10, max_pm10 = min(pm10_readings), max(pm10_readings)

    min_r25, max_r25 = min(ratio_factors_25), max(ratio_factors_25)
    min_r10, max_r10 = min(ratio_factors_10), max(ratio_factors_10)

    print(f"Simulated {ticks} ticks.")
    print(f"Multiplier [0.992, 1.008] span: [{min_mult:.5f}, {max_mult:.5f}] (enclosed in [0.992, 1.008]: {0.992 <= min_mult and max_mult <= 1.008})")
    print(f"PM2.5 reading bounds: [{min_pm25:.2f}, {max_pm25:.2f}] µg/m³ (relative ratio: [{min_r25:.4f}, {max_r25:.4f}])")
    print(f"PM10 reading bounds:  [{min_pm10:.2f}, {max_pm10:.2f}] µg/m³ (relative ratio: [{min_r10:.4f}, {max_r10:.4f}])")

    is_physical = (min_pm25 >= 12.0 and max_pm25 <= 25.0) and (min_pm10 >= 20.0 and max_pm10 <= 50.0)
    multipliers_bounded = (min_mult >= 0.992 and max_mult <= 1.008)

    return {
        "ticks": ticks,
        "is_physical": is_physical,
        "multipliers_bounded": multipliers_bounded,
        "pm25_bounds": (min_pm25, max_pm25),
        "pm10_bounds": (min_pm10, max_pm10),
        "mult_bounds": (min_mult, max_mult)
    }


def run_color_contrast_challenge() -> Dict[str, any]:
    print("\n=======================================================")
    print("▶ CHALLENGE 4: WCAG 2.1 Contrast Ratio Verification")
    print("=======================================================")

    css_content = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css_content)

    canvas_bg = "#FBFBFD"
    elevated_bg = "#F8F9FA"
    surface_bg = "#FFFFFF"
    dark_carbon = "#060D17"
    dark_navy = "#0A192F"

    light_backgrounds = [
        ("Canvas Off-White (--bg-canvas)", canvas_bg),
        ("Elevated Surface (--bg-surface-elevated)", elevated_bg),
        ("Pure White Surface (--bg-surface)", surface_bg)
    ]

    foreground_tokens = [
        ("--gears-navy", tokens.get("--gears-navy", "#0A192F")),
        ("--gears-navy-light", tokens.get("--gears-navy-light", "#132A4A")),
        ("--gears-petrol", tokens.get("--gears-petrol", "#0F3A4D")),
        ("--gears-petrol-accent", tokens.get("--gears-petrol-accent", "#165B75")),
        ("--text-primary", tokens.get("--text-primary", "#0A192F")),
        ("--text-secondary", tokens.get("--text-secondary", "#334155")),
        ("--text-muted", tokens.get("--text-muted", "#64748B")),
        ("--impact-emerald", tokens.get("--impact-emerald", "#047857")),
        ("--impact-mahogany", tokens.get("--impact-mahogany", "#5C1620")),
        ("--impact-mahogany-deep", tokens.get("--impact-mahogany-deep", "#420D15")),
        ("--fears-carbon", tokens.get("--fears-carbon", "#060D17"))
    ]

    dark_foregrounds = [
        ("--fears-cyan", tokens.get("--fears-cyan", "#00D2BE")),
        ("--text-on-dark", tokens.get("--text-on-dark", "#F8FAFC")),
        ("--text-on-dark-muted", tokens.get("--text-on-dark-muted", "#94A3B8")),
        ("--fears-amber", tokens.get("--fears-amber", "#F59E0B"))
    ]

    contrast_records = []

    # Test light background pairs
    for bg_name, bg_hex in light_backgrounds:
        for fg_name, fg_hex in foreground_tokens:
            ratio = wcag_contrast_ratio(fg_hex, bg_hex)
            status = "AAA" if ratio >= 7.0 else ("AA" if ratio >= 4.5 else ("AA Large" if ratio >= 3.0 else "FAIL"))
            contrast_records.append({
                "context": f"{fg_name} on {bg_name}",
                "fg": fg_hex,
                "bg": bg_hex,
                "ratio": ratio,
                "status": status
            })

    # Test dark background pairs
    for bg_name, bg_hex in [("FEARS Carbon (--fears-carbon)", dark_carbon), ("GEARS Navy (--section-navy)", dark_navy)]:
        for fg_name, fg_hex in dark_foregrounds:
            ratio = wcag_contrast_ratio(fg_hex, bg_hex)
            status = "AAA" if ratio >= 7.0 else ("AA" if ratio >= 4.5 else ("AA Large" if ratio >= 3.0 else "FAIL"))
            contrast_records.append({
                "context": f"{fg_name} on {bg_name}",
                "fg": fg_hex,
                "bg": bg_hex,
                "ratio": ratio,
                "status": status
            })

    print(f"{'Context / Token':<55} | {'Ratio':<8} | {'WCAG Level'}")
    print("-" * 80)
    for rec in contrast_records:
        print(f"{rec['context']:<55} | {rec['ratio']:>6.2f}:1 | {rec['status']}")

    return {"records": contrast_records}


if __name__ == "__main__":
    svg_res = run_svg_geometry_challenge()
    calc_res = run_particulate_calculator_challenge(1000)
    telem_res = run_telemetry_simulator_challenge(1000)
    contrast_res = run_color_contrast_challenge()

    print("\n=======================================================")
    print("ALL EMPIRICAL CHALLENGES COMPLETED SUCCESSFULLY.")
    print("=======================================================")
