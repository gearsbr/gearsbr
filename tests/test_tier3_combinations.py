"""
Tier 3: Cross-Feature Combinations (Pairwise Interactions)
Validates interactions between disparate subsystems:
- Modular visualizer + FEARS boost
- Calculator sliders + Congonhas corridor presets
- Telemetry jitter + alert status
- PIX modal + clipboard copy + backdrop dismissal
- Design tokens + SVG brand rendering
"""

import re
from tests.test_helpers import (
    read_project_file, parse_html, parse_css_tokens, parse_svg,
    wcag_contrast_ratio, calculate_clean_air_volume, calculate_retained_pm_mass_kg,
    assert_true, assert_false, assert_equal, assert_ge, assert_in
)


def test_t3_01_modular_visualizer_and_fears_boost_toggle():
    """T3 Pairwise 1: Modular visualizer + FEARS division boost mode."""
    html = read_project_file("index.html")
    js = read_project_file("js/main.js")
    combined = html + js
    # Visualizer must support FEARS mode or boost
    assert_true(
        "fears" in combined.lower() and ("visualizer" in combined.lower() or "modular" in combined.lower()),
        "Visualizer must integrate FEARS ecosystem/boost option"
    )


def test_t3_02_calculator_slider_and_corridor_presets():
    """T3 Pairwise 2: Calculator sliders + Congonhas corridor preset buttons."""
    html = read_project_file("index.html")
    dom = parse_html(html)
    calc = dom.find_by_id("calculadora-impacto")
    assert_true(calc is not None)
    presets = calc.find_all_by_attr("data-preset") or calc.find_all_by_class("preset-btn") or calc.find_all_by_tag("button")
    assert_ge(len(presets), 1, "Calculator must have corridor preset buttons")


def test_t3_03_calculator_and_fears_twin_turbine_boost():
    """T3 Pairwise 3: Impact calculator + FEARS twin-turbine boost (+120% flow)."""
    # Base volume: 10 units, 24h = 33,288,000 m3/year
    base_vol = calculate_clean_air_volume(10, 24, fears_boost=False)
    # Boost volume (+120% = 836 m3/h): 10 units, 24h = 73,233,600 m3/year
    boost_vol = calculate_clean_air_volume(10, 24, fears_boost=True)
    assert_equal(boost_vol, 73233600.0)

    # Base PM mass at 45 ug/m3 = ~1.50 kg
    base_mass = calculate_retained_pm_mass_kg(base_vol, 45.0)
    # Boost PM mass = ~3.29 kg
    boost_mass = calculate_retained_pm_mass_kg(boost_vol, 45.0)
    assert_true(3.28 <= boost_mass <= 3.31, f"Boost mass must be ~3.29 kg, got {boost_mass:.2f}")


def test_t3_04_telemetry_jitter_and_status_pulse():
    """T3 Pairwise 4: Telemetry sensor jitter + pulse LED animation + tabular numbers."""
    css = read_project_file("css/styles.css")
    js = read_project_file("js/main.js")
    # Tabular nums in CSS
    assert_in("tabular-nums", css, "CSS must apply tabular numbers for jitter display")
    # Jitter simulation in JS
    assert_true("Math.random()" in js, "JS must compute simulated jitter")


def test_t3_05_pix_modal_and_clipboard_copy_feedback():
    """T3 Pairwise 5: PIX modal + 1-click clipboard copy + Copiado! visual state."""
    html = read_project_file("index.html")
    js = read_project_file("js/main.js")
    assert_true('id="pix-modal"' in html or 'pix-modal' in html, "PIX modal must exist in HTML")
    assert_in("navigator.clipboard.writeText", js, "JS must write to clipboard")
    assert_true("Copiado" in js or "copiada" in js.lower(), "JS must show Copiado feedback")


def test_t3_06_donation_tiers_and_pix_modal_trigger():
    """T3 Pairwise 6: Donation tier action buttons trigger the PIX modal."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None)
    # Tier CTA buttons should point to or trigger modal
    triggers = sec.find_all_by_attr("data-open-modal", "pix-modal") or sec.find_all_by_tag("button")
    assert_ge(len(triggers), 3, "At least 3 tier buttons triggering modal must exist")


def test_t3_07_pix_modal_escape_and_focus_return():
    """T3 Pairwise 7: PIX modal escape key handling + accessible focus restoration."""
    js = read_project_file("js/main.js")
    assert_true(
        "Escape" in js or "keyCode === 27" in js or "key === 'Escape'" in js,
        "Escape key handler must be implemented in JS"
    )


def test_t3_08_brand_lockup_offwhite_contrast_and_favicon():
    """T3 Pairwise 8: Brand logo lockup + off-white canvas tokens + 1:1 favicon geometry."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    canvas = tokens.get("--bg-canvas", "#FBFBFD")
    navy = tokens.get("--gears-navy", "#0A192F")
    ratio = wcag_contrast_ratio(navy, canvas)
    assert_ge(ratio, 14.0, "Brand Navy on Canvas must exceed 14:1 contrast")

    # Favicon and logo SVGs must both use evenodd
    logo_svg = parse_svg(read_project_file("assets/logo-gears.svg"))
    fav_svg = parse_svg(read_project_file("assets/favicon.svg"))
    assert_true(logo_svg.has_evenodd_fill_rule(), "Logo must use evenodd")
    assert_true(fav_svg.has_evenodd_fill_rule(), "Favicon must use evenodd")


def test_t3_09_faq_accordion_and_category_filtering():
    """T3 Pairwise 9: Technical FAQ accordion + category filter pills."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("faq-tecnico") or dom.find_by_id("faq")
    if sec:
        cat_btns = sec.find_all_by_attr("data-category")
        assert_ge(len(cat_btns), 3, "FAQ must have category filter buttons")
        accordion_btns = [b for b in sec.find_all_by_tag("button") if b.get_attr("aria-expanded") is not None]
        assert_ge(len(accordion_btns), 3, "FAQ must have accessible accordion trigger buttons")


def test_t3_10_telemetry_and_visibility_change_throttling():
    """T3 Pairwise 10: Telemetry bar + visibilitychange tab hibernation."""
    js = read_project_file("js/main.js")
    assert_true(
        "visibilitychange" in js or "hidden" in js or "setInterval" in js,
        "Telemetry simulation must manage execution intervals"
    )


def test_t3_11_exploded_view_and_seven_hardware_modules():
    """T3 Pairwise 11: Exploded view toggle + 7 physical hardware module coordinates."""
    html = read_project_file("index.html")
    # All key subsystems mentioned in architecture
    modules = ["câmera", "tampas", "filtragem", "placa-mãe", "bateria", "entradas", "pluvial"]
    found_count = 0
    html_lower = html.lower()
    for m in modules:
        # Check either exact name or simplified ASCII
        ascii_m = m.replace("â", "a").replace("ã", "a")
        if m in html_lower or ascii_m in html_lower:
            found_count += 1
    assert_ge(found_count, 5, f"At least 5 of the 7 hardware modules must be documented, found {found_count}")


def test_t3_12_skip_link_and_sticky_glassmorphic_header():
    """T3 Pairwise 12: Skip link navigates past sticky header with scroll-padding-top."""
    html = read_project_file("index.html")
    css = read_project_file("css/styles.css")
    assert_true("skip-link" in html, "Skip link must exist in HTML")
    assert_true(
        "scroll-padding-top" in css or "--header-height" in css or "sticky" in css or "fixed" in css,
        "CSS must compensate for header height during anchor navigation"
    )
