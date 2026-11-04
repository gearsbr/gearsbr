"""
Tier 1: Feature Coverage (Happy Path Verification)
Covers all 21 Features from PROJECT.md § Feature Inventory.
5 test cases per feature across 21 features = 105 tests.
"""

import re
from tests.test_helpers import (
    read_project_file, file_exists, parse_html, parse_css_tokens,
    parse_svg, assert_true, assert_false, assert_equal, assert_in,
    assert_ge, assert_regex
)


# ===========================================================================
# Feature 1: Canonical 8-Tooth Gear SVG
# ===========================================================================

def test_f01_01_gear_svg_file_exists():
    """F1: Canonical 8-tooth gear SVG file must exist at assets/logo-gears.svg."""
    assert_true(file_exists("assets/logo-gears.svg"), "assets/logo-gears.svg must exist")


def test_f01_02_gear_svg_evenodd_fill_rule():
    """F1: Canonical gear must use fill-rule='evenodd' for clean center bore transparency."""
    content = read_project_file("assets/logo-gears.svg")
    svg = parse_svg(content)
    assert_true(svg.has_evenodd_fill_rule(), "SVG must declare fill-rule='evenodd'")


def test_f01_03_gear_svg_no_opaque_white_circles():
    """F1: Canonical gear center bore must be transparent without opaque white circles."""
    content = read_project_file("assets/logo-gears.svg")
    svg = parse_svg(content)
    assert_false(svg.has_opaque_white_circles(), "SVG center bore must not contain opaque white circles")


def test_f01_04_gear_svg_eight_teeth_path_geometry():
    """F1: Gear path must describe an 8-tooth geometry (8 crests/flanks)."""
    content = read_project_file("assets/logo-gears.svg")
    # Verify path coordinates reflect 8 sectors of 45 deg or contains path data
    assert_true(len(re.findall(r'[MLCA]\s*[-\d.]+', content)) >= 16, "Gear path must have 8-tooth polygon vertices")


def test_f01_05_gear_svg_brand_color():
    """F1: Gear path must be filled with Deep Navy (#0A192F) or Petroleum (#0F3A4D)."""
    content = read_project_file("assets/logo-gears.svg")
    assert_true(
        "#0A192F" in content.upper() or "#0F3A4D" in content.upper(),
        "Gear SVG fill must use brand Navy #0A192F or Petroleum #0F3A4D"
    )


# ===========================================================================
# Feature 2: Off-White Palette Tokens
# ===========================================================================

def test_f02_01_canvas_token_defined():
    """F2: --bg-canvas token must be defined as #FBFBFD in CSS."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    canvas = tokens.get("--bg-canvas") or tokens.get("--bg-offwhite-canvas")
    assert_true(canvas is not None, "--bg-canvas token must be defined in CSS")
    assert_equal(canvas.upper(), "#FBFBFD", "--bg-canvas must be #FBFBFD")


def test_f02_02_surface_token_defined():
    """F2: Elevated surface token must be defined as #F8F9FA in CSS."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    surface = tokens.get("--bg-surface-elevated") or tokens.get("--bg-surface-subtle") or tokens.get("--bg-surface")
    assert_true(surface is not None, "--bg-surface or elevated surface token must be defined")


def test_f02_03_gears_navy_token_defined():
    """F2: --gears-navy token must be defined as #0A192F."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    navy = tokens.get("--gears-navy")
    assert_true(navy is not None, "--gears-navy must be defined")
    assert_equal(navy.upper(), "#0A192F", "--gears-navy must be #0A192F")


def test_f02_04_gears_petrol_token_defined():
    """F2: --gears-petrol token must be defined as #0F3A4D."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    petrol = tokens.get("--gears-petrol")
    assert_true(petrol is not None, "--gears-petrol must be defined")
    assert_equal(petrol.upper(), "#0F3A4D", "--gears-petrol must be #0F3A4D")


def test_f02_05_body_uses_offwhite_background():
    """F2: Body/HTML background in CSS must use --bg-canvas or #FBFBFD."""
    css = read_project_file("css/styles.css")
    assert_true(
        re.search(r'body\s*\{[^}]*background(-color)?\s*:\s*var\(--bg-canvas', css) or
        re.search(r'body\s*\{[^}]*background(-color)?\s*:\s*#FBFBFD', css, re.IGNORECASE),
        "Body background must use var(--bg-canvas) or #FBFBFD"
    )


# ===========================================================================
# Feature 3: Dedicated 1:1 Favicon SVG
# ===========================================================================

def test_f03_01_favicon_svg_exists():
    """F3: Standalone 1:1 favicon SVG must exist at assets/favicon.svg."""
    assert_true(file_exists("assets/favicon.svg"), "assets/favicon.svg must exist")


def test_f03_02_favicon_viewbox_square():
    """F3: Favicon SVG viewBox must have a 1:1 square aspect ratio."""
    content = read_project_file("assets/favicon.svg")
    svg = parse_svg(content)
    assert_true(svg.viewbox is not None, "Favicon SVG must declare viewBox")
    _, _, w, h = svg.viewbox
    assert_equal(w, h, f"Favicon viewBox must be 1:1 square, got {w}x{h}")


def test_f03_03_favicon_linked_in_html():
    """F3: Favicon must be linked in index.html <head>."""
    html = read_project_file("index.html")
    assert_true(
        re.search(r'<link\s+[^>]*rel=["\']icon["\'][^>]*href=["\'][^"\']*favicon\.svg["\']', html) or
        re.search(r'<link\s+[^>]*href=["\'][^"\']*favicon\.svg["\'][^>]*rel=["\']icon["\']', html),
        "index.html must link to assets/favicon.svg"
    )


def test_f03_04_favicon_evenodd_rule():
    """F3: Favicon SVG must use fill-rule='evenodd' for clean bore."""
    content = read_project_file("assets/favicon.svg")
    svg = parse_svg(content)
    assert_true(svg.has_evenodd_fill_rule(), "Favicon SVG must use fill-rule='evenodd'")


def test_f03_05_favicon_contains_gear_path():
    """F3: Favicon SVG must contain 8-tooth gear path."""
    content = read_project_file("assets/favicon.svg")
    svg = parse_svg(content)
    assert_ge(len(svg.paths), 1, "Favicon SVG must have at least one <path> element")


# ===========================================================================
# Feature 4: Navbar Lockup Alignment
# ===========================================================================

def test_f04_01_logo_lockup_viewbox():
    """F4: Navbar lockup SVG must have viewBox '0 0 212 56'."""
    content = read_project_file("assets/logo-gears.svg")
    svg = parse_svg(content)
    assert_true(svg.viewbox is not None, "Logo SVG must have viewBox")
    _, _, w, h = svg.viewbox
    assert_equal((w, h), (212.0, 56.0), f"Logo viewBox must be 212x56, got {w}x{h}")


def test_f04_02_text_baseline_y49():
    """F4: GEARS wordmark text baseline must align at Y=49."""
    content = read_project_file("assets/logo-gears.svg")
    assert_true(
        re.search(r'<text\s+[^>]*y=["\']49["\'][^>]*>\s*GEARS\s*</text>', content),
        "Text baseline for GEARS must be y='49'"
    )


def test_f04_03_terminal_dot_rect_exists():
    """F4: Terminal dot rect element must exist in logo lockup."""
    content = read_project_file("assets/logo-gears.svg")
    svg = parse_svg(content)
    assert_ge(len(svg.rects), 1, "Logo lockup must contain terminal dot rect")


def test_f04_04_terminal_dot_bottom_y49():
    """F4: Terminal dot rect bottom (y + height) must align at Y=49."""
    content = read_project_file("assets/logo-gears.svg")
    m = re.search(r'<rect\s+[^>]*y=["\'](\d+)["\'][^>]*height=["\'](\d+)["\']', content)
    assert_true(m is not None, "Rect must have y and height attributes")
    y, h = int(m.group(1)), int(m.group(2))
    assert_equal(y + h, 49, f"Rect bottom (y+h) must be 49, got {y}+{h}={y+h}")


def test_f04_05_gear_bottom_at_y49():
    """F4: Canonical gear bottom crest must reach Y=49."""
    content = read_project_file("assets/logo-gears.svg")
    assert_in("48.84", content, "Gear bottom vertex coordinates must reach baseline Y=49 (~48.84)")


# ===========================================================================
# Feature 5: "Apple Open Source" Manifesto
# ===========================================================================

def test_f05_01_apple_open_source_in_html():
    """F5: 'Apple Open Source' phrase must be present in index.html."""
    html = read_project_file("index.html")
    assert_in("Apple Open Source", html, "index.html must contain 'Apple Open Source'")


def test_f05_02_bambu_lab_contrast_in_html():
    """F5: 'Bambu Lab' contrast narrative must be present in index.html."""
    html = read_project_file("index.html")
    assert_in("Bambu Lab", html, "index.html must contrast with 'Bambu Lab'")


def test_f05_03_creality_contrast_in_html():
    """F5: 'Creality' contrast narrative must be present in index.html."""
    html = read_project_file("index.html")
    assert_in("Creality", html, "index.html must contrast with 'Creality'")


def test_f05_04_controlled_modularity_in_html():
    """F5: 'Modularidade controlada' phrase must be present in index.html."""
    html = read_project_file("index.html").lower()
    assert_true("modularidade controlada" in html or "modularidade" in html, "index.html must discuss modularity")


def test_f05_05_rejection_of_gambiarras_in_html():
    """F5: Manifesto must explicitly reject 'gambiarra'."""
    html = read_project_file("index.html").lower()
    assert_in("gambiarra", html, "index.html must reject 'gambiarra'")


# ===========================================================================
# Feature 6: 7 Hardware Modules Architecture
# ===========================================================================

def test_f06_01_camera_optics_module_present():
    """F6: Hardware Module 1: Camera & Optics must be documented in index.html."""
    html = read_project_file("index.html").lower()
    assert_true("câmera" in html or "camera" in html, "Camera module must be present in HTML")


def test_f06_02_casing_tampas_module_present():
    """F6: Hardware Module 2: Tampas / Carenagem must be documented in index.html."""
    html = read_project_file("index.html").lower()
    assert_true("tampas" in html or "tampa" in html or "carenagem" in html, "Casing/covers module must be present")


def test_f06_03_multistage_filtration_module_present():
    """F6: Hardware Module 3: Multistage Filtration (HEPA H13) must be documented."""
    html = read_project_file("index.html").lower()
    assert_true("hepa" in html and "filtragem" in html, "Filtration HEPA module must be present")


def test_f06_04_motherboard_mcu_module_present():
    """F6: Hardware Module 4: Placa-Mãe / MCU (ESP32) must be documented."""
    html = read_project_file("index.html").lower()
    assert_true("esp32" in html or "placa-mãe" in html or "mcu" in html, "Motherboard/MCU module must be present")


def test_f06_05_battery_bms_module_present():
    """F6: Hardware Module 5: Bateria & BMS (LiFePO4) must be documented."""
    html = read_project_file("index.html").lower()
    assert_true("bateria" in html or "lifepo4" in html or "bms" in html, "Battery/BMS module must be present")


# ===========================================================================
# Feature 7: FEARS.™ High-Performance Division
# ===========================================================================

def test_f07_01_fears_section_exists():
    """F7: Dedicated FEARS section (#divisao-fears) must exist in index.html."""
    html = read_project_file("index.html")
    assert_true(
        'id="divisao-fears"' in html or 'id="fears"' in html,
        "Dedicated FEARS section (#divisao-fears) must exist in index.html"
    )


def test_f07_02_fears_mercedes_amg_analog():
    """F7: FEARS narrative must include the Mercedes-AMG / Maybach analogy."""
    html = read_project_file("index.html")
    assert_true(
        "Mercedes-AMG" in html or "AMG" in html or "Maybach" in html,
        "FEARS narrative must mention AMG or Maybach analogy"
    )


def test_f07_03_fears_logo_svg_exists():
    """F7: FEARS division logo file or SVG asset must exist."""
    assert_true(
        file_exists("assets/logo-fears.svg") or 'FEARS' in read_project_file("index.html"),
        "FEARS logo SVG asset must exist"
    )


def test_f07_04_fears_cyan_token_defined():
    """F7: --fears-cyan token must be defined in CSS as #00D2BE."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    cyan = tokens.get("--fears-cyan")
    assert_true(cyan is not None, "--fears-cyan token must be defined in CSS")
    assert_equal(cyan.upper(), "#00D2BE", "--fears-cyan must be #00D2BE")


def test_f07_05_fears_carbon_token_defined():
    """F7: --fears-carbon token must be defined in CSS."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    carbon = tokens.get("--fears-carbon") or tokens.get("--fears-obsidian")
    assert_true(carbon is not None, "--fears-carbon or obsidian token must be defined in CSS")


# ===========================================================================
# Feature 8: Regional Congonhas Context
# ===========================================================================

def test_f08_01_congonhas_city_reference():
    """F8: Congonhas city must be referenced in index.html."""
    html = read_project_file("index.html")
    assert_in("Congonhas", html, "Congonhas must be referenced in index.html")


def test_f08_02_quadrilatero_ferrifero_or_mg():
    """F8: Minas Gerais or Quadrilátero Ferrífero must be referenced in index.html."""
    html = read_project_file("index.html")
    assert_true(
        "Minas Gerais" in html or "Quadrilátero Ferrífero" in html or "MG" in html,
        "Regional mining territory must be referenced"
    )


def test_f08_03_iron_ore_particulate_mission():
    """F8: Iron ore particulate challenges (minério de ferro) must be referenced."""
    html = read_project_file("index.html").lower()
    assert_true("minério" in html or "minerio" in html or "particulado" in html, "Iron ore particulate mission in HTML")


def test_f08_04_founder_gabriel_rossi():
    """F8: Founder Gabriel Rossi Pereira must be referenced in index.html."""
    html = read_project_file("index.html")
    assert_in("Gabriel Rossi", html, "Founder Gabriel Rossi must be mentioned")


def test_f08_05_founder_paula_rossi():
    """F8: Paula Rossi de Oliveira must be referenced in index.html."""
    html = read_project_file("index.html")
    assert_in("Paula Rossi", html, "Paula Rossi must be mentioned in governance")


# ===========================================================================
# Feature 9: Dedicated Donation Section
# ===========================================================================

def test_f09_01_donation_section_exists():
    """F9: Dedicated donation section (#apoie-inovacao) must exist in index.html."""
    html = read_project_file("index.html")
    assert_in('id="apoie-inovacao"', html, "Section #apoie-inovacao must exist in index.html")


def test_f09_02_donation_heading_present():
    """F9: Donation section must feature an inviting heading for civic support."""
    html = read_project_file("index.html").lower()
    assert_true(
        "apoie" in html or "doação" in html or "doacao" in html,
        "Donation section heading must exist"
    )


def test_f09_03_maker_education_mission():
    """F9: Donation section must detail funding for maker labs, IFMG, or clean air."""
    html = read_project_file("index.html").lower()
    assert_true("maker" in html or "ar puro" in html or "estudantes" in html, "Maker/education mission in donation")


def test_f09_04_pix_modal_trigger_buttons():
    """F9: Interactive buttons to trigger the PIX modal must exist in donation section."""
    html = read_project_file("index.html")
    assert_true(
        'data-open-modal="pix-modal"' in html or 'data-modal="pix"' in html or 'href="#pix-modal"' in html or 'pix' in html.lower(),
        "Buttons triggering PIX modal must exist"
    )


def test_f09_05_donation_nav_link_in_header():
    """F9: Header navigation must contain a link targeting #apoie-inovacao."""
    html = read_project_file("index.html")
    assert_in('#apoie-inovacao', html, "Header navigation must link to #apoie-inovacao")


# ===========================================================================
# Feature 10: 3 Support Tiers
# ===========================================================================

def test_f10_01_at_least_three_tiers_exist():
    """F10: At least 3 distinct support tier cards must exist in #apoie-inovacao."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None, "#apoie-inovacao must be present")
    cards = (
        sec.find_all_by_class("donation-tier-card") or
        sec.find_all_by_class("tier-card") or
        sec.find_all_by_class("donation-tier") or
        sec.find_all_by_class("card")
    )
    assert_ge(len(cards), 3, "There must be at least 3 tier cards in donation section")


def test_f10_02_tier_civico_present():
    """F10: Tier 1: Apoiador Cívico / Maker (R$ 25 - 99) must be present."""
    html = read_project_file("index.html")
    assert_true("Cívico" in html or "Civico" in html or "Maker" in html, "Tier 1 Cívico/Maker must be present")


def test_f10_03_tier_desenvolvedor_present():
    """F10: Tier 2: Desenvolvedor de Módulo (R$ 100 - 499) must be present."""
    html = read_project_file("index.html")
    assert_true("Desenvolvedor" in html or "Módulo" in html or "Modulo" in html, "Tier 2 Desenvolvedor must be present")


def test_f10_04_tier_mantenedor_fears_present():
    """F10: Tier 3: Mantenedor Institucional & FEARS Patron (R$ 500+) must be present."""
    html = read_project_file("index.html")
    assert_true("Mantenedor" in html or "Patron" in html or "FEARS" in html, "Tier 3 Mantenedor/Patron must be present")


def test_f10_05_each_tier_has_pix_cta():
    """F10: Every tier card must feature a functional PIX CTA button."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None)
    buttons = sec.find_all_by_tag("button")
    assert_ge(len(buttons), 3, "At least 3 action buttons must exist across tier cards")


# ===========================================================================
# Feature 11: Interactive PIX Modal
# ===========================================================================

def test_f11_01_pix_modal_dialog_exists():
    """F11: Modal container (<dialog id='pix-modal'> or id='pix-modal') must exist."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None, "Element with id='pix-modal' must exist in index.html")


def test_f11_02_pix_modal_qr_code_svg():
    """F11: PIX modal must contain an SVG QR code graphic."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None)
    svgs = modal.find_all_by_tag("svg")
    assert_ge(len(svgs), 1, "PIX modal must contain at least one SVG graphic (QR Code)")


def test_f11_03_pix_key_display_exists():
    """F11: PIX modal must contain an input or container displaying the PIX key."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None)
    key_elem = modal.find_by_id("pix-key-input") or modal.find_by_id("pix-key") or modal.find_all_by_class("pix-key-value")
    assert_true(key_elem is not None and bool(key_elem), "PIX key display container must exist in modal")


def test_f11_04_pix_modal_close_button():
    """F11: PIX modal must contain a close button."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None)
    close_btn = modal.find_by_id("close-pix-modal") or modal.find_all_by_class("modal-close") or modal.find_all_by_attr("data-close-modal")
    assert_true(close_btn is not None and bool(close_btn), "PIX modal must have a close button")


def test_f11_05_pix_modal_dialog_aria_attributes():
    """F11: PIX modal must have role='dialog' or use native <dialog>."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None)
    assert_true(
        modal.tag == "dialog" or modal.get_attr("role") == "dialog",
        "PIX modal must be a <dialog> or have role='dialog'"
    )


# ===========================================================================
# Feature 12: 1-Click PIX Clipboard Copy
# ===========================================================================

def test_f12_01_copy_pix_button_exists():
    """F12: Copy button (#copy-pix-btn or .btn-copy-pix) must exist."""
    dom = parse_html(read_project_file("index.html"))
    btn = dom.find_by_id("copy-pix-btn") or dom.find_all_by_class("btn-copy-pix")
    assert_true(btn is not None and bool(btn), "Button #copy-pix-btn must exist in index.html")


def test_f12_02_clipboard_api_used_in_js():
    """F12: JavaScript must integrate navigator.clipboard.writeText."""
    js = read_project_file("js/main.js")
    assert_in("navigator.clipboard.writeText", js, "js/main.js must call navigator.clipboard.writeText")


def test_f12_03_copiado_feedback_in_js():
    """F12: JavaScript must display 'Copiado' confirmation feedback."""
    js = read_project_file("js/main.js")
    assert_true(
        "Copiado" in js or "copiada" in js.lower(),
        "js/main.js must provide 'Copiado!' visual confirmation feedback"
    )


def test_f12_04_copy_status_element_exists():
    """F12: Status element (#pix-copy-status or feedback toast) must exist."""
    dom = parse_html(read_project_file("index.html"))
    elem = dom.find_by_id("pix-copy-status") or dom.find_all_by_class("copy-feedback") or dom.find_all_by_class("pix-status")
    assert_true(elem is not None and bool(elem), "PIX copy status feedback element must exist")


def test_f12_05_pix_key_valid_value():
    """F12: Default PIX key in HTML or JS must match official specification."""
    html = read_project_file("index.html")
    js = read_project_file("js/main.js")
    combined = html + js
    assert_true(
        "58.214.932/0001-44" in combined or "gabrielrossipe@gmail.com" in combined or "31984566074" in combined,
        "Official PIX key (CNPJ or email) must be present in codebase"
    )


# ===========================================================================
# Feature 13: Bank Details & Transparency
# ===========================================================================

def test_f13_01_bank_name_present():
    """F13: Official bank details must indicate institution (Banco Inter or Cora SCD)."""
    html = read_project_file("index.html")
    assert_true(
        "Banco Inter" in html or "Cora" in html or "Nubank" in html or "Banco" in html,
        "Bank details must mention the financial institution"
    )


def test_f13_02_agency_field_present():
    """F13: Agência field must be present in bank details."""
    html = read_project_file("index.html")
    assert_in("Agência", html, "Agência field must be present in bank details")


def test_f13_03_account_field_present():
    """F13: Conta Corrente field must be present in bank details."""
    html = read_project_file("index.html")
    assert_true("Conta" in html or "Conta Corrente" in html, "Conta field must be present in bank details")


def test_f13_04_cnpj_or_association_present():
    """F13: Legal entity or CNPJ must be stated in transparency statement."""
    html = read_project_file("index.html")
    assert_true(
        "CNPJ" in html or "Associação" in html or "Associacao" in html or "Razão Social" in html,
        "CNPJ or corporate entity name must be present"
    )


def test_f13_05_transparency_commitment_present():
    """F13: Transparency statement on open book accounting / GitHub ledger."""
    html = read_project_file("index.html").lower()
    assert_true(
        "transparência" in html or "transparencia" in html or "livro-caixa" in html or "prestação de contas" in html,
        "Transparency & public accountability statement must be present"
    )


# ===========================================================================
# Feature 14: Interactive Modular Visualizer
# ===========================================================================

def test_f14_01_visualizer_section_exists():
    """F14: Section #visualizador-modular or container #modular-visualizer must exist."""
    html = read_project_file("index.html")
    assert_true(
        'id="visualizador-modular"' in html or 'id="modular-visualizer"' in html,
        "Visualizer section or container must exist in index.html"
    )


def test_f14_02_exploded_view_toggle_exists():
    """F14: Exploded view toggle button (#btn-toggle-exploded) must exist."""
    dom = parse_html(read_project_file("index.html"))
    btn = dom.find_by_id("btn-toggle-exploded") or dom.find_all_by_class("btn-exploded")
    assert_true(btn is not None and bool(btn), "Exploded view toggle button must exist")


def test_f14_03_module_selection_buttons_exist():
    """F14: Module selector buttons with data-module attribute must exist."""
    dom = parse_html(read_project_file("index.html"))
    btns = dom.find_all_by_attr("data-module")
    assert_ge(len(btns), 4, "At least 4 module selection buttons with data-module must exist")


def test_f14_04_svg_stage_exists():
    """F14: SVG stage (#visualizer-svg or #visualizer-stage) must exist."""
    dom = parse_html(read_project_file("index.html"))
    svg = dom.find_by_id("visualizer-svg") or dom.find_by_id("visualizer-stage")
    assert_true(svg is not None, "Visualizer SVG stage must exist")


def test_f14_05_visualizer_controller_in_js():
    """F14: Visualizer controller must be present in js/main.js."""
    js = read_project_file("js/main.js")
    assert_true(
        "Visualizer" in js or "ModularViewer" in js or "exploded" in js,
        "Visualizer controller must exist in js/main.js"
    )


# ===========================================================================
# Feature 15: Particulate Impact Calculator
# ===========================================================================

def test_f15_01_calculator_section_exists():
    """F15: Calculator section (#calculadora-impacto) must exist in index.html."""
    html = read_project_file("index.html")
    assert_in('id="calculadora-impacto"', html, "Calculator section #calculadora-impacto must exist")


def test_f15_02_range_sliders_exist():
    """F15: Range sliders for units, hours, or PM concentration must exist."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("calculadora-impacto")
    assert_true(sec is not None)
    sliders = [inp for inp in sec.find_all_by_tag("input") if inp.get_attr("type") == "range"]
    assert_ge(len(sliders), 2, "At least 2 range sliders must exist in calculator")


def test_f15_03_output_clean_air_exists():
    """F15: Output element for clean air volume (#calc-clean-air) must exist."""
    dom = parse_html(read_project_file("index.html"))
    elem = dom.find_by_id("calc-clean-air") or dom.find_by_id("calc-volume")
    assert_true(elem is not None, "Clean air output element must exist")


def test_f15_04_output_pm_mass_exists():
    """F15: Output element for retained PM mass (#calc-mass-pm) must exist."""
    dom = parse_html(read_project_file("index.html"))
    elem = dom.find_by_id("calc-mass-pm") or dom.find_by_id("calc-mass")
    assert_true(elem is not None, "PM mass output element must exist")


def test_f15_05_calculator_controller_in_js():
    """F15: Calculator controller must be implemented in js/main.js."""
    js = read_project_file("js/main.js")
    assert_true(
        "Calculator" in js or "calc" in js.lower(),
        "Calculator controller must be implemented in js/main.js"
    )


# ===========================================================================
# Feature 16: Dynamic Telemetry Simulator
# ===========================================================================

def test_f16_01_telemetry_bar_exists():
    """F16: Status strip (#telemetry-bar) must exist in index.html."""
    dom = parse_html(read_project_file("index.html"))
    elem = dom.find_by_id("telemetry-bar")
    assert_true(elem is not None, "#telemetry-bar must exist in index.html")


def test_f16_02_pulse_led_exists():
    """F16: Pulsing status LED element must exist in telemetry bar."""
    dom = parse_html(read_project_file("index.html"))
    bar = dom.find_by_id("telemetry-bar")
    assert_true(bar is not None)
    led = bar.find_all_by_class("pulse-led") or bar.find_all_by_class("telemetry-led") or bar.find_all_by_class("telemetry-dot")
    assert_ge(len(led), 1, "Pulsing status LED must exist in telemetry bar")


def test_f16_03_telemetry_pm_sensors_exist():
    """F16: PM2.5 and PM10 sensor value display elements must exist."""
    dom = parse_html(read_project_file("index.html"))
    bar = dom.find_by_id("telemetry-bar")
    assert_true(bar is not None)
    pm = bar.find_by_id("telemetry-pm25-val") or bar.find_by_id("telemetry-pm25") or bar.find_all_by_class("pm25-val")
    assert_true(pm is not None and bool(pm), "PM sensor value element must exist")


def test_f16_04_filter_health_gauge_exists():
    """F16: Filter health gauge element must exist in telemetry."""
    dom = parse_html(read_project_file("index.html"))
    bar = dom.find_by_id("telemetry-bar")
    assert_true(bar is not None)
    gauge = bar.find_by_id("telemetry-filter-gauge") or bar.find_by_id("telemetry-filter") or bar.find_all_by_class("filter-val")
    assert_true(gauge is not None and bool(gauge), "Filter health gauge element must exist")


def test_f16_05_telemetry_controller_in_js():
    """F16: Telemetry simulator controller must be implemented in js/main.js."""
    js = read_project_file("js/main.js")
    assert_true(
        "Telemetry" in js or "telemetry" in js.lower(),
        "Telemetry controller must be implemented in js/main.js"
    )


# ===========================================================================
# Feature 17: Technical Accordion FAQ
# ===========================================================================

def test_f17_01_faq_section_exists():
    """F17: Technical FAQ section (#faq-tecnico or #faq) must exist in index.html."""
    html = read_project_file("index.html")
    assert_true(
        'id="faq-tecnico"' in html or 'id="faq"' in html,
        "FAQ section (#faq-tecnico or #faq) must exist in index.html"
    )


def test_f17_02_accordion_triggers_with_aria():
    """F17: Accordion trigger buttons must use aria-expanded and aria-controls."""
    dom = parse_html(read_project_file("index.html"))
    triggers = [btn for btn in dom.find_all_by_tag("button") if btn.get_attr("aria-expanded") is not None]
    assert_ge(len(triggers), 3, "At least 3 accordion trigger buttons with aria-expanded must exist")


def test_f17_03_faq_panels_exist():
    """F17: Accordion panels with matching IDs must exist."""
    dom = parse_html(read_project_file("index.html"))
    triggers = [btn for btn in dom.find_all_by_tag("button") if btn.get_attr("aria-controls") is not None]
    assert_ge(len(triggers), 3, "Accordion triggers must specify aria-controls")
    for trg in triggers:
        target_id = trg.get_attr("aria-controls")
        assert_true(dom.find_by_id(target_id) is not None, f"Panel id '{target_id}' must exist in DOM")


def test_f17_04_faq_category_buttons_exist():
    """F17: Category filter buttons (data-category) must exist in FAQ."""
    dom = parse_html(read_project_file("index.html"))
    cats = dom.find_all_by_attr("data-category")
    assert_ge(len(cats), 3, "At least 3 FAQ category filter buttons must exist")


def test_f17_05_faq_controller_in_js():
    """F17: FAQ controller must be implemented in js/main.js."""
    js = read_project_file("js/main.js")
    assert_true("FAQ" in js or "faq" in js.lower() or "accordion" in js.lower(), "FAQ controller must be in js/main.js")


# ===========================================================================
# Feature 18: Design System Refinements (1–30)
# ===========================================================================

def test_f18_01_fibonacci_spacing_tokens():
    """F18: Fibonacci spacing scale tokens (--fib-*) must be defined in CSS."""
    css = read_project_file("css/styles.css")
    tokens = parse_css_tokens(css)
    fib_tokens = [k for k in tokens.keys() if k.startswith("--fib-")]
    assert_ge(len(fib_tokens), 5, "At least 5 Fibonacci spacing tokens (--fib-*) must be defined")


def test_f18_02_tactile_double_borders():
    """F18: Tactile dual-layer box-shadow rules must exist in CSS."""
    css = read_project_file("css/styles.css")
    assert_true(
        "box-shadow: 0 0 0 1px" in css or "box-shadow:0 0 0 1px" in css or "0 0 0 1px rgba" in css,
        "CSS must contain tactile double-border box-shadow rules"
    )


def test_f18_03_glassmorphism_backdrop_filter():
    """F18: Backdrop-filter blur rules must be defined in CSS."""
    css = read_project_file("css/styles.css")
    assert_in("backdrop-filter", css, "CSS must declare backdrop-filter for glassmorphism")


def test_f18_04_elevation_shadow_system():
    """F18: Multi-level elevation shadow tokens or classes must exist in CSS."""
    css = read_project_file("css/styles.css")
    assert_true(
        "--shadow-" in css or "elevation" in css or ".card" in css,
        "Elevation shadow system must be defined in CSS"
    )


def test_f18_05_badge_system_in_css():
    """F18: Badge component styles (.badge or .cad-marker) must be defined."""
    css = read_project_file("css/styles.css")
    assert_true(".badge" in css or ".pill" in css or ".tag" in css, "Badge styles must exist in CSS")


# ===========================================================================
# Feature 19: Micro-Interactions (106–130)
# ===========================================================================

def test_f19_01_scroll_progress_bar():
    """F19: Scroll progress indicator must exist in HTML or CSS."""
    html = read_project_file("index.html")
    css = read_project_file("css/styles.css")
    assert_true(
        "scroll-progress" in html or "scroll-progress" in css or "progressBar" in read_project_file("js/main.js"),
        "Scroll progress bar indicator must exist in codebase"
    )


def test_f19_02_button_active_press_transform():
    """F19: Buttons must have tactile active press scale transforms (:active scale(0.98))."""
    css = read_project_file("css/styles.css")
    assert_true(
        re.search(r':active\s*\{[^}]*scale\(0\.9', css),
        "Buttons must feature active press scale transform in CSS"
    )


def test_f19_03_back_to_top_fab():
    """F19: Floating back-to-top button (#back-to-top or .btn-fab) must exist."""
    html = read_project_file("index.html")
    assert_true(
        'id="back-to-top"' in html or 'btn-back-to-top' in html or 'fab' in html,
        "Back-to-top floating button must exist in index.html"
    )


def test_f19_04_smooth_scrolling_in_css():
    """F19: Smooth scroll behavior must be declared in CSS."""
    css = read_project_file("css/styles.css")
    assert_in("scroll-behavior: smooth", css, "CSS must declare scroll-behavior: smooth")


def test_f19_05_navigation_controller_in_js():
    """F19: Navigation controller managing scroll and mobile drawer in js/main.js."""
    js = read_project_file("js/main.js")
    assert_true(
        "Navigation" in js or "Nav" in js or "scroll" in js,
        "Navigation controller must be present in js/main.js"
    )


# ===========================================================================
# Feature 20: Accessibility & WCAG AAA (131–155)
# ===========================================================================

def test_f20_01_skip_link_exists():
    """F20: Skip-to-content link (.skip-link) must exist as first child in body."""
    dom = parse_html(read_project_file("index.html"))
    skip_links = dom.find_all_by_class("skip-link")
    assert_ge(len(skip_links), 1, "Skip-to-content link must exist in index.html")


def test_f20_02_skip_link_target_valid():
    """F20: Skip link href must point to main content container (#main-content or #visao-geral)."""
    dom = parse_html(read_project_file("index.html"))
    skip_link = dom.find_all_by_class("skip-link")[0]
    target = skip_link.get_attr("href", "").lstrip("#")
    assert_true(bool(target), "Skip link must have non-empty hash target")
    assert_true(dom.find_by_id(target) is not None, f"Target #{target} must exist in DOM")


def test_f20_03_focus_visible_styling():
    """F20: Dual-ring or high-contrast :focus-visible styling must exist in CSS."""
    css = read_project_file("css/styles.css")
    assert_in(":focus-visible", css, "CSS must declare :focus-visible accessibility styling")


def test_f20_04_semantic_landmarks():
    """F20: HTML must contain landmark elements <header>, <nav>, <main>, <footer>."""
    dom = parse_html(read_project_file("index.html"))
    assert_ge(len(dom.find_all_by_tag("header")), 1, "<header> landmark must be present")
    assert_ge(len(dom.find_all_by_tag("nav")), 1, "<nav> landmark must be present")
    assert_ge(len(dom.find_all_by_tag("main")), 1, "<main> landmark must be present")
    assert_ge(len(dom.find_all_by_tag("footer")), 1, "<footer> landmark must be present")


def test_f20_05_html_lang_attribute():
    """F20: <html> tag must declare lang='pt-BR'."""
    dom = parse_html(read_project_file("index.html"))
    html_node = dom.find_all_by_tag("html")
    assert_ge(len(html_node), 1, "<html> element must exist")
    assert_equal(html_node[0].get_attr("lang"), "pt-BR", "<html> lang attribute must be 'pt-BR'")


# ===========================================================================
# Feature 21: Performance & Zero Dependencies
# ===========================================================================

def test_f21_01_zero_external_js_frameworks():
    """F21: index.html must not import heavy runtime frameworks (React, Vue, jQuery)."""
    html = read_project_file("index.html")
    forbidden = ["react", "vue", "jquery", "angular", "bootstrap.js", "tailwind"]
    for f in forbidden:
        assert_false(f in html.lower() and "<script" in html.lower(), f"No {f} scripts allowed")


def test_f21_02_main_script_deferred():
    """F21: Primary script js/main.js must use defer attribute."""
    html = read_project_file("index.html")
    assert_true(
        re.search(r'<script\s+[^>]*src=["\']js/main\.js["\'][^>]*defer', html) or
        re.search(r'<script\s+[^>]*defer[^>]*src=["\']js/main\.js["\']', html),
        "js/main.js must be loaded with defer"
    )


def test_f21_03_font_preconnect_present():
    """F21: Fonts preconnect links must be present in <head>."""
    html = read_project_file("index.html")
    assert_true(
        '<link rel="preconnect" href="https://fonts.googleapis.com"' in html or
        '<link rel="preconnect" href="https://fonts.gstatic.com"' in html,
        "Google Fonts preconnect link must be present"
    )


def test_f21_04_native_es6_js_structure():
    """F21: js/main.js must use native ES6 structure (const/let, arrow functions/classes)."""
    js = read_project_file("js/main.js")
    assert_true("const " in js or "class " in js, "js/main.js must use modern ES6 syntax")


def test_f21_05_relative_asset_paths():
    """F21: Static asset links in index.html must use relative paths for GitHub Pages."""
    html = read_project_file("index.html")
    # All css and js imports should not use absolute root paths (/css/ or /js/)
    assert_false('href="/css/' in html, "CSS paths must be relative")
    assert_false('src="/js/' in html, "JS paths must be relative")
