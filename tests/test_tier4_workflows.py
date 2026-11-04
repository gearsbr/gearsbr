"""
Tier 4: Real-World Application Workflows (End-to-End User Journeys)
Simulates realistic end-to-end user journeys through the application:
1. Congonhas Municipal Environmental Technician evaluating T.U.L.I.P.A.
2. Civic Maker & Donor supporting IFMG student lab via PIX
3. Performance Engineer reviewing FEARS.™ high-output modular specs
4. Accessibility Auditor validating WCAG AAA compliance and keyboard navigation
"""

import re
from tests.test_helpers import (
    read_project_file, parse_html, parse_css_tokens, parse_svg,
    wcag_contrast_ratio, calculate_clean_air_volume, calculate_retained_pm_mass_kg,
    calculate_consultations_avoided, assert_true, assert_equal, assert_ge, assert_in
)


# ===========================================================================
# Journey 1: Congonhas Municipal Environmental Technician
# ===========================================================================

def test_t4_journey1_step1_congonhas_regional_context():
    """J1 Step 1: Technician reviews territorial mining particulate context."""
    html = read_project_file("index.html")
    assert_in("Congonhas", html, "Must prominently display Congonhas territorial context")
    assert_true(
        "minério" in html.lower() or "minerio" in html.lower() or "particulado" in html.lower(),
        "Must highlight particulate challenges from iron ore extraction"
    )


def test_t4_journey1_step2_hardware_modules_inspection():
    """J1 Step 2: Technician inspects HEPA H13 multistage filtration specs."""
    html = read_project_file("index.html")
    assert_in("HEPA", html, "Must display HEPA filtration technical data")
    assert_true("99.97%" in html or "99,97%" in html, "Must verify 99.97% particulate retention rating")


def test_t4_journey1_step3_calculator_corridor_evaluation():
    """J1 Step 3: Technician evaluates Av. Júlia Kubitschek corridor in calculator."""
    # Simulation: 15 nodes, 24 hours, 55 ug/m3 PM concentration
    vol = calculate_clean_air_volume(15, 24, fears_boost=False)
    assert_equal(vol, 49932000.0)  # 15 * 380 * 24 * 365 = 49,932,000 m3/ano
    mass_kg = calculate_retained_pm_mass_kg(vol, 55.0)
    assert_true(2.70 <= mass_kg <= 2.80, f"Mass must be ~2.75 kg, got {mass_kg:.2f}")
    consultations = calculate_consultations_avoided(mass_kg, exposed_pop=20000)
    assert_true(consultations > 0.5, f"Avoided consultations must be positive, got {consultations:.2f}")


def test_t4_journey1_step4_faq_municipal_deployment():
    """J1 Step 4: Technician reviews municipal deployment and public standards in FAQ."""
    html = read_project_file("index.html")
    assert_true(
        "faq" in html.lower() or "perguntas" in html.lower() or "dúvidas" in html.lower(),
        "Technical FAQ must address deployment inquiries"
    )


# ===========================================================================
# Journey 2: Civic Maker & Community Donor (PIX Flow)
# ===========================================================================

def test_t4_journey2_step1_navigate_to_donation_section():
    """J2 Step 1: Donor navigates to #apoie-inovacao via header navigation CTA."""
    dom = parse_html(read_project_file("index.html"))
    sec = dom.find_by_id("apoie-inovacao")
    assert_true(sec is not None, "Donation section must exist and be targetable by ID")


def test_t4_journey2_step2_select_support_tier():
    """J2 Step 2: Donor inspects support tiers and selects Apoiador Cívico."""
    html = read_project_file("index.html")
    assert_true("Cívico" in html or "Civico" in html or "Maker" in html, "Tier 1 must be available")
    assert_in("R$", html, "Currency amounts must be formatted in BRL")


def test_t4_journey2_step3_open_pix_modal_and_view_qr():
    """J2 Step 3: Donor launches PIX modal dialog and views dynamic vector QR code."""
    dom = parse_html(read_project_file("index.html"))
    modal = dom.find_by_id("pix-modal")
    assert_true(modal is not None, "PIX modal dialog must exist")
    svgs = modal.find_all_by_tag("svg")
    assert_ge(len(svgs), 1, "PIX modal must contain SVG QR code")


def test_t4_journey2_step4_copy_pix_key_and_verify_feedback():
    """J2 Step 4: Donor clicks copy button and receives visual confirmation."""
    js = read_project_file("js/main.js")
    assert_in("navigator.clipboard.writeText", js, "Clipboard API must be invoked on click")
    assert_true("Copiado" in js or "copiada" in js.lower(), "Visual feedback must confirm copy action")


# ===========================================================================
# Journey 3: Mining Fleet Performance Engineer (FEARS.™ Division)
# ===========================================================================

def test_t4_journey3_step1_jump_to_fears_division():
    """J3 Step 1: Engineer navigates to #divisao-fears high-performance section."""
    html = read_project_file("index.html")
    assert_true(
        'id="divisao-fears"' in html or 'id="fears"' in html,
        "FEARS high-performance section must exist"
    )


def test_t4_journey3_step2_review_amg_tuning_philosophy():
    """J3 Step 2: Engineer reviews Mercedes-AMG / Maybach tuning comparison."""
    html = read_project_file("index.html")
    assert_true(
        "AMG" in html or "Mercedes" in html or "Maybach" in html,
        "Must detail Mercedes-AMG / Maybach tuning parallel"
    )


def test_t4_journey3_step3_fears_modular_boost_inspection():
    """J3 Step 3: Engineer inspects FEARS twin-turbine and carbon-fiber hardware modules."""
    html = read_project_file("index.html").lower()
    assert_true("carbono" in html or "titânio" in html or "titanio" in html or "turbo" in html)


def test_t4_journey3_step4_industrial_filtration_capacity_calculation():
    """J3 Step 4: Engineer evaluates boosted mine buffer capacity (+120% flow)."""
    # 25 units in FEARS mode, 24h continuous operation
    fears_vol = calculate_clean_air_volume(25, 24, fears_boost=True)
    # 25 * 836 * 24 * 365 = 183,084,000 m3/year
    assert_equal(fears_vol, 183084000.0)
    # Heavy dust mining corridor: 120 ug/m3
    fears_mass = calculate_retained_pm_mass_kg(fears_vol, 120.0)
    assert_true(21.8 <= fears_mass <= 22.2, f"Mass must be ~21.96 kg/ano, got {fears_mass:.2f}")


# ===========================================================================
# Journey 4: Accessibility Auditor (WCAG AAA & Keyboard Traversal)
# ===========================================================================

def test_t4_journey4_step1_skip_link_activation():
    """J4 Step 1: Auditor activates skip-to-content link on initial keyboard navigation."""
    dom = parse_html(read_project_file("index.html"))
    skip_link = dom.find_all_by_class("skip-link")
    assert_ge(len(skip_link), 1, "Skip link must be present for keyboard users")


def test_t4_journey4_step2_semantic_landmark_structure():
    """J4 Step 2: Auditor verifies standard semantic landmark elements."""
    dom = parse_html(read_project_file("index.html"))
    landmarks = ["header", "nav", "main", "footer"]
    for lm in landmarks:
        assert_ge(len(dom.find_all_by_tag(lm)), 1, f"Semantic landmark <{lm}> must be present")


def test_t4_journey4_step3_keyboard_focus_indicators():
    """J4 Step 3: Auditor verifies high-contrast :focus-visible styling in CSS."""
    css = read_project_file("css/styles.css")
    assert_in(":focus-visible", css, ":focus-visible rules must be declared for keyboard navigation")


def test_t4_journey4_step4_wcag_aaa_contrast_validation():
    """J4 Step 4: Auditor verifies WCAG AAA contrast ratio >= 7:1 for text."""
    # Navy #0A192F on Off-White #FBFBFD
    ratio1 = wcag_contrast_ratio("#0A192F", "#FBFBFD")
    assert_ge(ratio1, 7.0, f"Text contrast must satisfy WCAG AAA (>= 7.0:1), got {ratio1:.2f}")
    # Petrol #0F3A4D on Off-White #FBFBFD
    ratio2 = wcag_contrast_ratio("#0F3A4D", "#FBFBFD")
    assert_ge(ratio2, 7.0, f"Petrol contrast must satisfy WCAG AAA (>= 7.0:1), got {ratio2:.2f}")
