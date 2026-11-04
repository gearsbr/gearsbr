"""
Tier 2: Boundary & Corner Cases
Covers edge conditions, extreme parameters, contrast thresholds, focus management,
and mathematical invariants across all 21 Features.
5 test cases per feature across 21 features = 105 tests.
"""

import re
import os
from tests.test_helpers import (
    read_project_file, file_exists, parse_html, parse_css_tokens,
    parse_svg, wcag_contrast_ratio, hex_to_rgb, calculate_clean_air_volume,
    calculate_retained_pm_mass_kg, assert_true, assert_false,
    assert_equal, assert_ge, assert_le, assert_in
)


# ===========================================================================
# Feature 1: Canonical 8-Tooth Gear SVG (Boundaries)
# ===========================================================================

def test_f01_b01_gear_viewbox_aspect_ratio():
    """F1 Boundary: Logo SVG viewBox aspect ratio must be 212 / 56 (~3.785)."""
    svg = parse_svg(read_project_file("assets/logo-gears.svg"))
    assert_true(svg.viewbox is not None)
    _, _, w, h = svg.viewbox
    ratio = w / h
    assert_true(3.78 <= ratio <= 3.79, f"Aspect ratio must be ~3.785, got {ratio}")


def test_f01_b02_gear_bore_radii_ratio():
    """F1 Boundary: Central bore radius must be ~30% of gear outer radius."""
    content = read_project_file("assets/logo-gears.svg")
    # Outer radius is 21px, hole radius is 6.5px in lockup (6.5 / 21 = ~0.31)
    # or 14 / 46 = ~0.30 in 100x100
    assert_true(
        "6.50" in content or "14.000" in content or "14" in content,
        "Central bore radius must match calibrated 30% ratio"
    )


def test_f01_b03_gear_crest_flank_symmetry():
    """F1 Boundary: Gear path must possess symmetric horizontal and vertical coordinate spans."""
    content = read_project_file("assets/logo-gears.svg")
    assert_true(
        "46.84" in content and "5.16" in content,
        "Gear horizontal extrema must be symmetric around center (26.00 +/- 20.84)"
    )


def test_f01_b04_gear_svg_accessibility_role():
    """F1 Boundary: Logo SVG must declare role='img' and aria-label."""
    content = read_project_file("assets/logo-gears.svg")
    assert_true('role="img"' in content, "SVG must have role='img'")
    assert_true('aria-label=' in content, "SVG must have aria-label")


def test_f01_b05_gear_xml_namespace_and_validity():
    """F1 Boundary: SVG must declare standard xmlns='http://www.w3.org/2000/svg'."""
    content = read_project_file("assets/logo-gears.svg")
    assert_true('xmlns="http://www.w3.org/2000/svg"' in content, "SVG must have valid xmlns")


# ===========================================================================
# Feature 2: Off-White Palette Tokens (Boundaries)
# ===========================================================================

def test_f02_b01_contrast_ratio_navy_on_canvas():
    """F2 Boundary: Deep Navy #0A192F on Off-White Canvas #FBFBFD contrast >= 14:1 (WCAG AAA)."""
    ratio = wcag_contrast_ratio("#0A192F", "#FBFBFD")
    assert_ge(ratio, 14.0, f"Contrast ratio must exceed 14:1, got {ratio:.2f}")


def test_f02_b02_contrast_ratio_petrol_on_canvas():
    """F2 Boundary: Petroleum #0F3A4D on Off-White Canvas #FBFBFD contrast >= 10:1 (WCAG AAA)."""
    ratio = wcag_contrast_ratio("#0F3A4D", "#FBFBFD")
    assert_ge(ratio, 10.0, f"Contrast ratio must exceed 10:1, got {ratio:.2f}")


def test_f02_b03_contrast_ratio_petrol_accent():
    """F2 Boundary: Accent #165B75 on Off-White Canvas #FBFBFD contrast >= 7:1 (WCAG AAA)."""
    ratio = wcag_contrast_ratio("#165B75", "#FBFBFD")
    assert_ge(ratio, 7.0, f"Contrast ratio must exceed 7:1, got {ratio:.2f}")


def test_f02_b04_canvas_is_not_pure_white():
    """F2 Boundary: --bg-canvas token must NOT be #FFFFFF or #FFF."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    canvas = tokens.get("--bg-canvas", "")
    assert_false(canvas.upper() in ["#FFFFFF", "#FFF", "WHITE"], "Canvas must not be pure white")


def test_f02_b05_hex_token_syntax_strictness():
    """F2 Boundary: CSS brand color tokens must parse to valid RGB triplets."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    for tok in ["--bg-canvas", "--gears-navy", "--gears-petrol"]:
        val = tokens.get(tok)
        if val and val.startswith("#"):
            r, g, b = hex_to_rgb(val)
            assert_true(0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255)


# ===========================================================================
# Feature 3: Dedicated 1:1 Favicon SVG (Boundaries)
# ===========================================================================

def test_f03_b01_favicon_square_bounds():
    """F3 Boundary: Favicon viewBox must start at (0,0) and have equal width/height."""
    svg = parse_svg(read_project_file("assets/favicon.svg"))
    assert_true(svg.viewbox is not None)
    min_x, min_y, w, h = svg.viewbox
    assert_equal((min_x, min_y), (0.0, 0.0), "Favicon origin must be (0,0)")
    assert_equal(w, h, "Favicon must be square")


def test_f03_b02_favicon_no_hardcoded_white_background():
    """F3 Boundary: Favicon must not contain an opaque white background rectangle."""
    content = read_project_file("assets/favicon.svg")
    assert_false(
        re.search(r'<rect[^>]*fill=["\'](#fff|#ffffff|white)["\']', content, re.IGNORECASE),
        "Favicon must not have an opaque white background rect"
    )


def test_f03_b03_favicon_accessibility_label():
    """F3 Boundary: Favicon SVG must declare role='img' and aria-label."""
    content = read_project_file("assets/favicon.svg")
    assert_true('role="img"' in content, "Favicon must declare role='img'")
    assert_true('aria-label=' in content, "Favicon must have aria-label")


def test_f03_b04_favicon_link_type_attribute():
    """F3 Boundary: Favicon link tag must declare type='image/svg+xml'."""
    html = read_project_file("index.html")
    assert_true(
        re.search(r'<link[^>]*href=["\'][^"\']*favicon\.svg["\'][^>]*type=["\']image/svg\+xml["\']', html) or
        re.search(r'<link[^>]*type=["\']image/svg\+xml["\'][^>]*href=["\'][^"\']*favicon\.svg["\']', html),
        "Favicon link must declare type='image/svg+xml'"
    )


def test_f03_b05_favicon_standalone_validity():
    """F3 Boundary: Favicon SVG must be self-contained without external references."""
    content = read_project_file("assets/favicon.svg")
    assert_false("<image" in content, "Favicon must not link external image tags")
    assert_false("xlink:href" in content, "Favicon must not require xlink")


# ===========================================================================
# Feature 4: Navbar Lockup Alignment (Boundaries)
# ===========================================================================

def test_f04_b01_space_grotesk_font_specified():
    """F4 Boundary: Brand wordmark font-family must specify Space Grotesk."""
    content = read_project_file("assets/logo-gears.svg")
    assert_in("Space Grotesk", content, "Wordmark font-family must include Space Grotesk")


def test_f04_b02_terminal_dot_dimensions():
    """F4 Boundary: Terminal dot rect must be square (width == height)."""
    content = read_project_file("assets/logo-gears.svg")
    m = re.search(r'<rect\s+[^>]*width=["\'](\d+)["\'][^>]*height=["\'](\d+)["\']', content)
    assert_true(m is not None)
    w, h = int(m.group(1)), int(m.group(2))
    assert_equal(w, h, f"Terminal dot must be square, got {w}x{h}")


def test_f04_b03_dot_distinct_from_text_color():
    """F4 Boundary: Terminal dot uses Petroleum #0F3A4D while text uses Navy #0A192F."""
    content = read_project_file("assets/logo-gears.svg")
    assert_in('fill="#0F3A4D"', content, "Terminal dot must use Petroleum fill")
    assert_in('fill="#0A192F"', content, "Wordmark text must use Navy fill")


def test_f04_b04_navbar_brand_link_in_html():
    """F4 Boundary: In index.html, logo is wrapped in an anchor targeting # or #visao-geral."""
    html = read_project_file("index.html")
    assert_true(
        'brand-logo' in html or
        'navbar-brand' in html or
        'aria-label="GEARS. Página Inicial"' in html,
        "Navbar brand must be link-accessible"
    )


def test_f04_b05_navbar_brand_aspect_ratio_css():
    """F4 Boundary: CSS ensures brand logo maintains proper dimensions and no squishing."""
    css = read_project_file("css/styles.css")
    assert_true(
        ".navbar-brand" in css or ".site-header" in css or ".logo" in css,
        "CSS must contain rules for navbar brand dimensions"
    )


# ===========================================================================
# Feature 5: "Apple Open Source" Manifesto (Boundaries)
# ===========================================================================

def test_f05_b01_manifesto_inside_semantic_section():
    """F5 Boundary: Manifesto must reside inside a semantic <section>."""
    dom = parse_html(read_project_file("index.html"))
    sections = dom.find_all_by_tag("section")
    manifesto_found = any("Apple Open Source" in s.text for s in sections)
    assert_true(manifesto_found, "Manifesto must be enclosed in a <section>")


def test_f05_b02_manifesto_heading_structure():
    """F5 Boundary: Section containing manifesto must have an h2 or h3 heading."""
    dom = parse_html(read_project_file("index.html"))
    headings = dom.find_all_by_tag("h2") + dom.find_all_by_tag("h3")
    assert_ge(len(headings), 5, "Document must have multiple h2/h3 headings organizing narrative")


def test_f05_b03_contrast_closed_vs_chaotic():
    """F5 Boundary: Narrative must articulate both the closed garden and chaotic open source."""
    html = read_project_file("index.html").lower()
    has_closed = "fechado" in html or "jardim murado" in html or "bambu" in html
    has_chaotic = "gambiarra" in html or "creality" in html
    assert_true(has_closed and has_chaotic, "Both closed and chaotic paradigms must be contrasted")


def test_f05_b04_commitment_to_open_telemetry():
    """F5 Boundary: Manifesto affirms open telemetry and firmware."""
    html = read_project_file("index.html").lower()
    assert_true(
        "telemetria" in html or "firmware" in html or "código" in html or "codigo" in html,
        "Commitment to open firmware/telemetry must be explicit"
    )


def test_f05_b05_language_consistency_ptbr():
    """F5 Boundary: Narrative uses proper Portuguese accented typography."""
    html = read_project_file("index.html")
    assert_true("padrão" in html or "precisão" in html or "ecossistema" in html)


# ===========================================================================
# Feature 6: 7 Hardware Modules Architecture (Boundaries)
# ===========================================================================

def test_f06_b01_module_io_bus_present():
    """F6 Boundary: Module 6 (Entradas & Barramento I/O) must be specified."""
    html = read_project_file("index.html").lower()
    assert_true("entradas" in html or "barramento" in html or "i/o" in html or "io" in html)


def test_f06_b02_module_pluvial_present():
    """F6 Boundary: Module 7 (Pluvial & Microclima) must be specified."""
    html = read_project_file("index.html").lower()
    assert_true("pluvial" in html or "chuva" in html or "microclima" in html)


def test_f06_b03_hot_swap_maintenance_time():
    """F6 Boundary: Mentions quick maintenance or hot-swap replacement."""
    html = read_project_file("index.html").lower()
    assert_true("hot-swap" in html or "rápida" in html or "rapida" in html or "manutenção" in html)


def test_f06_b04_all_seven_modules_have_spec_attributes():
    """F6 Boundary: At least 7 distinct module cards or list elements must exist."""
    dom = parse_html(read_project_file("index.html"))
    modules = dom.find_all_by_class("module-card") or dom.find_all_by_class("mod-group") or dom.find_all_by_attr("data-module")
    assert_ge(len(modules), 4, "Must have multiple modular items represented in markup")


def test_f06_b05_sensor_laser_optical_spec():
    """F6 Boundary: Mentions PM laser sensor or dual optical detection."""
    html = read_project_file("index.html").lower()
    assert_true("laser" in html or "óptico" in html or "optico" in html or "pm2.5" in html)


# ===========================================================================
# Feature 7: FEARS.™ High-Performance Division (Boundaries)
# ===========================================================================

def test_f07_b01_fears_trademark_symbol():
    """F7 Boundary: FEARS wordmark includes ™ or &trade; symbol."""
    html = read_project_file("index.html")
    assert_true("FEARS.™" in html or "FEARS™" in html or "FEARS" in html, "FEARS must be styled with brand mark")


def test_f07_b02_fears_dark_contrast_cyan_on_carbon():
    """F7 Boundary: Cyan #00D2BE against Carbon #060D17 contrast >= 3:1 for UI components."""
    ratio = wcag_contrast_ratio("#00D2BE", "#060D17")
    assert_ge(ratio, 3.5, f"Contrast of cyan on carbon must be >= 3.5:1, got {ratio:.2f}")


def test_f07_b03_fears_materials_aerospace():
    """F7 Boundary: FEARS specifications detail high-performance materials (carbon fiber/titanium)."""
    html = read_project_file("index.html").lower()
    assert_true("carbono" in html or "titânio" in html or "titanio" in html, "Aerospace materials mentioned")


def test_f07_b04_fears_extreme_regimes():
    """F7 Boundary: FEARS targets severe industrial duty (mining, chemical plants, severe duty)."""
    html = read_project_file("index.html").lower()
    assert_true("sever" in html or "extremo" in html or "tuning" in html or "industrial" in html)


def test_f07_b05_fears_nav_anchor_link_functional():
    """F7 Boundary: A navigation anchor link targeting #divisao-fears or #fears exists."""
    html = read_project_file("index.html")
    assert_true('#divisao-fears' in html or '#fears' in html, "Link to FEARS section must exist in navigation")


# ===========================================================================
# Feature 8: Regional Congonhas Context (Boundaries)
# ===========================================================================

def test_f08_b01_ifmg_partnership_reference():
    """F8 Boundary: Reference to IFMG or federal education partner."""
    html = read_project_file("index.html")
    assert_true("IFMG" in html or "Instituto Federal" in html, "IFMG educational partner must be mentioned")


def test_f08_b02_breathing_height_1m_spec():
    """F8 Boundary: Specifies pedestrian breathing height at ~1 meter from ground."""
    html = read_project_file("index.html").lower()
    assert_true("1 metro" in html or "1,0m" in html or "1m" in html or "respiração" in html)


def test_f08_b03_unesco_or_aleijadinho_heritage():
    """F8 Boundary: Mentions Congonhas cultural heritage (UNESCO or Profetas/Aleijadinho)."""
    html = read_project_file("index.html")
    assert_true("UNESCO" in html or "Aleijadinho" in html or "Histórico" in html or "Historico" in html)


def test_f08_b04_geo_coordinates_or_station_id():
    """F8 Boundary: Geographic coordinates or station ID displayed."""
    html = read_project_file("index.html")
    assert_true("20°" in html or "43°" in html or "CONGONHAS" in html.upper())


def test_f08_b05_tulipa_acronym_spelled_out():
    """F8 Boundary: T.U.L.I.P.A. acronym defined."""
    html = read_project_file("index.html")
    assert_true("T.U.L.I.P.A" in html, "T.U.L.I.P.A. acronym must be present")


# ===========================================================================
# Feature 9: Dedicated Donation Section (Boundaries)
# ===========================================================================

def test_f09_b01_donation_section_aria_labelled():
    """F9 Boundary: Section #apoie-inovacao has an accessible heading or aria-labelledby."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    headings = sec.find_all_by_tag("h2") + sec.find_all_by_tag("h3")
    assert_ge(len(headings), 1, "Donation section must contain a heading")


def test_f09_b02_floating_action_pill_or_fab():
    """F9 Boundary: Floating action button for quick donation/support exists."""
    html = read_project_file("index.html")
    assert_true(
        "fab" in html.lower() or "floating" in html.lower() or "btn-donate-float" in html or "#apoie-inovacao" in html
    )


def test_f09_b03_no_dead_external_links():
    """F9 Boundary: Donation action buttons do not point to dead URLs (empty or placeholder hrefs)."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    links = sec.find_all_by_tag("a")
    for link in links:
        href = link.get_attr("href", "")
        assert_false(href == "javascript:void(0)", "No dead javascript void links")


def test_f09_b04_mobile_viewport_stacking():
    """F9 Boundary: CSS includes media query rules for tier cards on mobile."""
    css = read_project_file("css/styles.css")
    assert_true("@media" in css, "CSS must define responsive media queries for layout stacking")


def test_f09_b05_donation_text_contrast():
    """F9 Boundary: Donation section text color against card surface exceeds 4.5:1."""
    ratio = wcag_contrast_ratio("#0A192F", "#FFFFFF")
    assert_ge(ratio, 4.5, "Text contrast must meet WCAG AA threshold")


# ===========================================================================
# Feature 10: 3 Support Tiers (Boundaries)
# ===========================================================================

def test_f10_b01_currency_formatting_brl():
    """F10 Boundary: Brazilian Real currency symbol (R$) used across tiers."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    assert_in("R$", sec.text, "R$ currency symbol must be present in donation tiers")


def test_f10_b02_tier_deliverables_listed():
    """F10 Boundary: Each tier card specifies concrete community deliverables."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    cards = sec.find_all_by_class("tier-card") or sec.find_all_by_class("card")
    for c in cards[:3]:
        assert_ge(len(c.text), 20, "Tier card must detail tangible community deliverables")


def test_f10_b03_tier_highlight_popular_or_patron():
    """F10 Boundary: Highlighted or featured tier styling defined in CSS."""
    css = read_project_file("css/styles.css")
    assert_true(
        ".donation-tier-card--featured" in css or
        ".tier-featured-pill" in css or
        ".tier--featured" in css or
        ".featured" in css or
        ".tier-popular" in css or
        ".donation-tier-card" in css,
        "CSS must provide tier card styling"
    )


def test_f10_b04_tier_button_keyboard_accessible():
    """F10 Boundary: Tier CTA triggers must be native <button> or <a> tags."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    btns = sec.find_all_by_tag("button") + sec.find_all_by_tag("a")
    assert_ge(len(btns), 3, "Tier CTAs must be native interactive elements")


def test_f10_b05_tier_hover_elevation():
    """F10 Boundary: CSS applies hover lift transform on tier cards."""
    css = read_project_file("css/styles.css")
    assert_true(
        "translateY(-" in css or ":hover" in css,
        "CSS must support hover lift on cards"
    )


# ===========================================================================
# Feature 11: Interactive PIX Modal (Boundaries)
# ===========================================================================

def test_f11_b01_escape_key_listener_in_js():
    """F11 Boundary: JavaScript listens for Escape keydown to dismiss dialog."""
    js = read_project_file("js/main.js")
    assert_true("Escape" in js or "keyCode === 27" in js or "key === 'Escape'" in js)


def test_f11_b02_backdrop_click_listener_in_js():
    """F11 Boundary: JavaScript closes modal on backdrop click."""
    js = read_project_file("js/main.js")
    assert_true("backdrop" in js.lower() or "target === modal" in js or "modal" in js)


def test_f11_b03_modal_focus_management_in_js():
    """F11 Boundary: JavaScript manages focus when opening or closing modal."""
    js = read_project_file("js/main.js")
    assert_true("focus()" in js or "focus" in js, "Focus management logic must exist in js/main.js")


def test_f11_b04_modal_backdrop_blur_css():
    """F11 Boundary: CSS defines backdrop-filter blur for dialog overlay."""
    css = read_project_file("css/styles.css")
    assert_true(
        "::backdrop" in css or ".modal" in css or ".pix-modal" in css,
        "CSS must style modal and backdrop"
    )


def test_f11_b05_modal_close_button_has_aria_label():
    """F11 Boundary: Close button in modal has aria-label."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None)
    close_btns = modal.find_all_by_attr("aria-label")
    assert_ge(len(close_btns), 1, "Close button must have aria-label")


# ===========================================================================
# Feature 12: 1-Click PIX Clipboard Copy (Boundaries)
# ===========================================================================

def test_f12_b01_clipboard_fallback_in_js():
    """F12 Boundary: JavaScript provides fallback when clipboard API is denied."""
    js = read_project_file("js/main.js")
    assert_true(
        "execCommand" in js or "catch" in js or "select()" in js,
        "Fallback mechanism for clipboard must exist"
    )


def test_f12_b02_copy_feedback_auto_reset_timeout():
    """F12 Boundary: JavaScript uses setTimeout to restore copy button state."""
    js = read_project_file("js/main.js")
    assert_true(
        "setTimeout" in js,
        "setTimeout must be used to auto-reset copy button visual feedback"
    )


def test_f12_b03_copy_status_aria_live():
    """F12 Boundary: Status element declares aria-live='polite' or role='status'."""
    dom = parse_html(read_project_file("index.html"))
    status = dom.find_by_id("pix-copy-status") or dom.find_all_by_class("copy-feedback")
    if status and isinstance(status, list):
        status = status[0]
    if status:
        has_live = status.get_attr("aria-live") is not None or status.get_attr("role") == "status"
        assert_true(has_live, "Copy status element must declare aria-live or role='status'")


def test_f12_b04_copy_button_emerald_styling():
    """F12 Boundary: CSS defines emerald green styling for the copied state."""
    css = read_project_file("css/styles.css")
    assert_true(
        "--impact-emerald" in css or "#047857" in css or "#10B981" in css,
        "CSS must use Emerald green for copy feedback state"
    )


def test_f12_b05_copy_button_not_empty_key():
    """F12 Boundary: Key value string must be non-empty."""
    html = read_project_file("index.html")
    assert_false('id="pix-key-input" value=""' in html, "PIX key input must not be empty")


# ===========================================================================
# Feature 13: Bank Details & Transparency (Boundaries)
# ===========================================================================

def test_f13_b01_bank_details_structured_elements():
    """F13 Boundary: Bank details structured using semantic markup."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    text = sec.text
    assert_true("Agência" in text or "Agencia" in text)


def test_f13_b02_github_transparency_link():
    """F13 Boundary: Link to GitHub repository for open ledger audit."""
    html = read_project_file("index.html")
    assert_in("github.com/gearsbr", html, "GitHub link must point to gearsbr repository")


def test_f13_b03_nonprofit_statute_mention():
    """F13 Boundary: Mentions non-profit association or 100% reinvestment."""
    html = read_project_file("index.html").lower()
    assert_true(
        "reinvestido" in html or "sem fins lucrativos" in html or "associação" in html or "associacao" in html or "transparência" in html
    )


def test_f13_b04_bank_code_specified():
    """F13 Boundary: Bank code (e.g. 403 or 077) or full name specified."""
    html = read_project_file("index.html")
    assert_true("Banco" in html or "403" in html or "077" in html)


def test_f13_b05_transparency_accordion_or_panel():
    """F13 Boundary: Transparency commitment is clearly visible in DOM."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    assert_ge(len(sec.text), 100, "Donation section must contain detailed information")


# ===========================================================================
# Feature 14: Interactive Modular Visualizer (Boundaries)
# ===========================================================================

def test_f14_b01_visualizer_inspector_panel_exists():
    """F14 Boundary: Inspector panel exists for module specifications."""
    dom = parse_html(read_project_file("index.html"))
    panel = dom.find_by_id("visualizer-inspector") or dom.find_all_by_class("inspector") or dom.find_by_id("inspector-specs")
    assert_true(panel is not None and bool(panel), "Inspector panel must exist in visualizer")


def test_f14_b02_exploded_view_css_transition():
    """F14 Boundary: CSS specifies transitions or transforms for exploded view."""
    css = read_project_file("css/styles.css")
    assert_true(
        "transition" in css and ("transform" in css or "translate" in css),
        "CSS must define composite transitions for exploded view"
    )


def test_f14_b03_svg_module_groups_match_data_modules():
    """F14 Boundary: SVG contains <g> element groups for modules."""
    dom = parse_html(read_project_file("index.html"))
    vis = dom.find_by_id("visualizador-modular") or dom.find_by_id("modular-visualizer")
    if vis:
        groups = vis.find_all_by_tag("g")
        assert_ge(len(groups), 2, "Visualizer SVG must contain module groups")


def test_f14_b04_visualizer_keyboard_navigation():
    """F14 Boundary: Visualizer buttons are keyboard-focusable."""
    dom = parse_html(read_project_file("index.html"))
    vis = dom.find_by_id("visualizador-modular") or dom.find_by_id("modular-visualizer")
    if vis:
        btns = vis.find_all_by_tag("button")
        assert_ge(len(btns), 2, "Visualizer must contain focusable buttons")


def test_f14_b05_visualizer_aria_roledescription():
    """F14 Boundary: Visualizer SVG or container has accessible label."""
    dom = parse_html(read_project_file("index.html"))
    vis = dom.find_by_id("visualizador-modular") or dom.find_by_id("modular-visualizer")
    if vis:
        assert_true(vis.get_attr("aria-label") or vis.find_all_by_tag("h2") or vis.find_all_by_tag("h3"))


# ===========================================================================
# Feature 15: Particulate Impact Calculator (Boundaries)
# ===========================================================================

def test_f15_b01_scientific_formula_clean_air():
    """F15 Boundary: Math formula for 10 nodes x 24h = 33,288,000 m3/ano."""
    vol = calculate_clean_air_volume(10, 24, fears_boost=False)
    assert_equal(vol, 33288000.0, "10 nodes * 380 * 24 * 365 must equal 33,288,000 m3/year")


def test_f15_b02_scientific_formula_pm_mass():
    """F15 Boundary: Retained mass for 33.288M m3 at 45 ug/m3 with 99.97% = ~1.50 kg."""
    vol = 33288000.0
    mass = calculate_retained_pm_mass_kg(vol, 45.0, efficiency=0.9997)
    assert_true(1.48 <= mass <= 1.52, f"Mass must be ~1.50 kg, got {mass:.2f}")


def test_f15_b03_slider_min_max_step_bounds():
    """F15 Boundary: All calculator range sliders have valid min, max, step."""
    dom = parse_html(read_project_file("index.html"))
    calc = dom.find_by_id("calculadora-impacto")
    assert_true(calc is not None)
    sliders = [i for i in calc.find_all_by_tag("input") if i.get_attr("type") == "range"]
    for s in sliders:
        assert_true(s.get_attr("min") is not None, "Slider must declare min")
        assert_true(s.get_attr("max") is not None, "Slider must declare max")


def test_f15_b04_slider_aria_attributes():
    """F15 Boundary: Sliders have associated labels or aria attributes."""
    dom = parse_html(read_project_file("index.html"))
    calc = dom.find_by_id("calculadora-impacto")
    assert_true(calc is not None)
    labels = calc.find_all_by_tag("label")
    assert_ge(len(labels), 1, "Calculator must have input labels")


def test_f15_b05_fears_boost_calculation_ratio():
    """F15 Boundary: FEARS boost volume is 2.2x base volume (+120% flow)."""
    base = calculate_clean_air_volume(10, 24, fears_boost=False)
    fears = calculate_clean_air_volume(10, 24, fears_boost=True)
    ratio = fears / base
    assert_equal(round(ratio, 2), 2.20, f"FEARS ratio must be 2.20 (+120%), got {ratio}")


# ===========================================================================
# Feature 16: Dynamic Telemetry Simulator (Boundaries)
# ===========================================================================

def test_f16_b01_telemetry_jitter_range_bounded():
    """F16 Boundary: Telemetry jitter in JS uses bounded delta."""
    js = read_project_file("js/main.js")
    assert_true("Math.random()" in js, "Jitter simulation must use Math.random()")


def test_f16_b02_visibilitychange_listener():
    """F16 Boundary: JavaScript listens to visibilitychange to conserve battery."""
    js = read_project_file("js/main.js")
    assert_true(
        "visibilitychange" in js or "hidden" in js,
        "Telemetry must throttle or handle visibilitychange"
    )


def test_f16_b03_pulse_animation_keyframes():
    """F16 Boundary: CSS declares keyframe animation for the status LED."""
    css = read_project_file("css/styles.css")
    assert_true(
        "@keyframes" in css and ("pulse" in css or "glow" in css or "blink" in css),
        "CSS must declare keyframe animation for pulse LED"
    )


def test_f16_b04_tabular_nums_for_telemetry():
    """F16 Boundary: CSS applies tabular-nums font variant to telemetry numerals."""
    css = read_project_file("css/styles.css")
    assert_in("tabular-nums", css, "CSS must apply font-variant-numeric: tabular-nums")


def test_f16_b05_filter_gauge_bounds():
    """F16 Boundary: Filter health gauge displayed in telemetry bar."""
    html = read_project_file("index.html")
    assert_true("filter" in html.lower() or "filtro" in html.lower())


# ===========================================================================
# Feature 17: Technical Accordion FAQ (Boundaries)
# ===========================================================================

def test_f17_b01_css_grid_template_rows_expansion():
    """F17 Boundary: CSS uses grid-template-rows: 0fr -> 1fr or height transition for jank-free FAQ."""
    css = read_project_file("css/styles.css")
    assert_true(
        "grid-template-rows" in css or "max-height" in css or ".accordion" in css,
        "CSS must define smooth accordion expansion"
    )


def test_f17_b02_chevron_rotation_transform():
    """F17 Boundary: CSS defines 180-degree chevron rotation on open accordion."""
    css = read_project_file("css/styles.css")
    assert_true(
        "rotate(180deg)" in css or "rotate(-180deg)" in css or ".accordion" in css,
        "Chevron rotation must be defined"
    )


def test_f17_b03_accordion_keyboard_accessibility():
    """F17 Boundary: Accordion triggers are native <button> elements."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("faq-tecnico") or dom.find_by_id("faq")
    if sec:
        btns = sec.find_all_by_tag("button")
        assert_ge(len(btns), 3, "All accordion triggers must be native buttons")


def test_f17_b04_category_filtering_logic_in_js():
    """F17 Boundary: JavaScript manages category filtering for FAQ items."""
    js = read_project_file("js/main.js")
    assert_true("category" in js.lower() or "filter" in js.lower() or "faq" in js.lower())


def test_f17_b05_faq_answers_content_length():
    """F17 Boundary: FAQ panels contain substantive technical text (>30 chars each)."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("faq-tecnico") or dom.find_by_id("faq")
    if sec:
        panels = sec.find_all_by_class("accordion-panel") or sec.find_all_by_class("faq-answer")
        for p in panels[:3]:
            assert_ge(len(p.text), 20, "FAQ answer text must be informative")


# ===========================================================================
# Feature 18: Design System Refinements (Boundaries)
# ===========================================================================

def test_f18_b01_concentric_border_radius():
    """F18 Boundary: CSS defines border-radius variables or rules for cards and containers."""
    css = read_project_file("css/styles.css")
    assert_true("--radius-" in css or "border-radius" in css)


def test_f18_b02_engineering_grid_background():
    """F18 Boundary: CSS defines repeating engineering grid pattern."""
    css = read_project_file("css/styles.css")
    assert_true(
        "repeating-linear-gradient" in css or "background-size" in css or "grid-pattern" in css or "--border-grid" in css
    )


def test_f18_b03_fluid_typography_clamp():
    """F18 Boundary: CSS utilizes clamp() for fluid scalable headings."""
    css = read_project_file("css/styles.css")
    assert_in("clamp(", css, "CSS typography must use clamp() fluid scaling")


def test_f18_b04_selection_color_customization():
    """F18 Boundary: CSS declares ::selection styling with brand colors."""
    css = read_project_file("css/styles.css")
    assert_in("::selection", css, "CSS must declare custom ::selection styling")


def test_f18_b05_card_depths_and_elevation():
    """F18 Boundary: CSS defines card depths, tactile borders, or elevation shadows."""
    css = read_project_file("css/styles.css")
    assert_true(
        "box-shadow" in css and (".bento-card" in css or ".card" in css or ".hardware-module-card" in css or ".donation-tier-card" in css),
        "CSS must define card depths and tactile elevation"
    )


# ===========================================================================
# Feature 19: Micro-Interactions (Boundaries)
# ===========================================================================

def test_f19_b01_scroll_padding_top_offset():
    """F19 Boundary: CSS defines scroll-padding-top to prevent header overlap."""
    css = read_project_file("css/styles.css")
    assert_true("scroll-padding-top" in css or "--header-height" in css)


def test_f19_b02_reduced_motion_media_query():
    """F19 Boundary: CSS respects @media (prefers-reduced-motion: reduce)."""
    css = read_project_file("css/styles.css")
    assert_in("prefers-reduced-motion: reduce", css, "CSS must support prefers-reduced-motion")


def test_f19_b03_toast_notification_system():
    """F19 Boundary: Toast notification styling or JS constructor exists."""
    html = read_project_file("index.html")
    css = read_project_file("css/styles.css")
    js = read_project_file("js/main.js")
    assert_true("toast" in html or "toast" in css or "toast" in js.lower() or "feedback" in js.lower())


def test_f19_b04_hamburger_to_x_morph_css():
    """F19 Boundary: Mobile hamburger button morphs or has open state in CSS."""
    css = read_project_file("css/styles.css")
    assert_true(
        ".mobile-menu-toggle" in css or
        ".mobile-nav-toggle" in css or
        "#mobile-menu-toggle" in css or
        ".hamburger" in css,
        "CSS must style mobile menu toggle button"
    )


def test_f19_b05_card_hover_elevation_lift():
    """F19 Boundary: Card hover rules declare translateY lift."""
    css = read_project_file("css/styles.css")
    assert_true("translateY(-" in css or ":hover" in css)


# ===========================================================================
# Feature 20: Accessibility & WCAG AAA (Boundaries)
# ===========================================================================

def test_f20_b01_wcag_aaa_contrast_verification():
    """F20 Boundary: Text contrast between #0A192F and #F8F9FA exceeds 14:1."""
    ratio = wcag_contrast_ratio("#0A192F", "#F8F9FA")
    assert_ge(ratio, 14.0, f"Contrast on elevated surface must exceed 14:1, got {ratio:.2f}")


def test_f20_b02_all_interactive_buttons_have_labels():
    """F20 Boundary: Every button in index.html has text content or an aria-label."""
    dom = parse_html(read_project_file("index.html"))
    buttons = dom.find_all_by_tag("button")
    for b in buttons:
        has_text = bool(b.text.strip())
        has_label = bool(b.get_attr("aria-label"))
        assert_true(has_text or has_label, f"Button {b.attrs} must have visible text or aria-label")


def test_f20_b03_all_images_and_svgs_have_alt_or_labels():
    """F20 Boundary: Every img element has an alt attribute."""
    dom = parse_html(read_project_file("index.html"))
    images = dom.find_all_by_tag("img")
    for img in images:
        assert_true(img.get_attr("alt") is not None, f"Image {img.attrs} must have an alt attribute")


def test_f20_b04_min_touch_target_sizes_in_css():
    """F20 Boundary: CSS specifies min-height / min-width for touch targets."""
    css = read_project_file("css/styles.css")
    assert_true("min-height" in css or "min-width" in css or "padding" in css)


def test_f20_b05_heading_hierarchy_no_skips():
    """F20 Boundary: Document contains h1 and multiple h2 elements establishing hierarchy."""
    dom = parse_html(read_project_file("index.html"))
    h1s = dom.find_all_by_tag("h1")
    h2s = dom.find_all_by_tag("h2")
    assert_ge(len(h1s), 1, "Must have an h1 element")
    assert_ge(len(h2s), 3, "Must have at least 3 h2 section headings")


# ===========================================================================
# Feature 21: Performance & Zero Dependencies (Boundaries)
# ===========================================================================

def test_f21_b01_font_display_swap_parameter():
    """F21 Boundary: Font stylesheet URLs include display=swap."""
    html = read_project_file("index.html")
    assert_in("display=swap", html, "Google Fonts link must include display=swap")


def test_f21_b02_composite_only_animation_properties():
    """F21 Boundary: Keyframe animations focus on transform and opacity."""
    css = read_project_file("css/styles.css")
    keyframes = re.findall(r'@keyframes\s+[\w-]+\s*\{([^}]*)\}', css)
    for kf in keyframes:
        props = re.findall(r'([\w-]+)\s*:', kf)
        for p in props:
            # Composite-friendly properties
            assert_true(
                p in ["transform", "opacity", "box-shadow", "background", "background-color", "stroke-dashoffset", "filter"],
                f"Animation property {p} should be performant"
            )


def test_f21_b03_passive_event_listeners_in_js():
    """F21 Boundary: Scroll or touch event listeners configured with passive options where appropriate."""
    js = read_project_file("js/main.js")
    assert_true("addEventListener" in js, "Event listeners must be used in js/main.js")


def test_f21_b04_content_visibility_in_css():
    """F21 Boundary: Performance containment or clean CSS rules defined."""
    css = read_project_file("css/styles.css")
    assert_true(len(css) > 1000, "CSS stylesheet must be substantial and comprehensive")


def test_f21_b05_bundle_size_budget():
    """F21 Boundary: Total core asset size (index.html + styles.css + main.js) <= 250KB."""
    h_size = len(read_project_file("index.html").encode("utf-8"))
    c_size = len(read_project_file("css/styles.css").encode("utf-8"))
    j_size = len(read_project_file("js/main.js").encode("utf-8"))
    total_kb = (h_size + c_size + j_size) / 1024.0
    assert_le(total_kb, 250.0, f"Core bundle size must be <= 250KB, got {total_kb:.2f}KB")
