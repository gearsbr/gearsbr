"""
Shared test utilities, parsers, and assertions for GEARS. E2E test suite.
Zero external dependencies - standard library only.
"""

import os
import re
import math
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_project_root() -> str:
    return PROJECT_ROOT


def file_exists(rel_path: str) -> bool:
    return os.path.exists(os.path.join(PROJECT_ROOT, rel_path))


def read_project_file(rel_path: str) -> str:
    full_path = os.path.join(PROJECT_ROOT, rel_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Project file not found: {rel_path} at {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# HTML DOM Node and Lightweight Parser
# ---------------------------------------------------------------------------

class DOMNode:
    def __init__(self, tag: str, attrs: Dict[str, str], parent: Optional['DOMNode'] = None):
        self.tag = tag.lower()
        self.attrs = attrs
        self.parent = parent
        self.children: List['DOMNode'] = []
        self.text_fragments: List[str] = []

    @property
    def text(self) -> str:
        all_text = list(self.text_fragments)
        for child in self.children:
            all_text.append(child.text)
        return " ".join(" ".join(all_text).split())

    def get_attr(self, name: str, default: Optional[str] = None) -> Optional[str]:
        return self.attrs.get(name.lower(), default)

    def has_class(self, class_name: str) -> bool:
        classes = self.get_attr("class", "").split()
        return class_name in classes

    def find_by_id(self, elem_id: str) -> Optional['DOMNode']:
        if self.get_attr("id") == elem_id:
            return self
        for child in self.children:
            res = child.find_by_id(elem_id)
            if res:
                return res
        return None

    def find_all_by_tag(self, tag_name: str) -> List['DOMNode']:
        results = []
        if self.tag == tag_name.lower():
            results.append(self)
        for child in self.children:
            results.extend(child.find_all_by_tag(tag_name))
        return results

    def find_all_by_class(self, class_name: str) -> List['DOMNode']:
        results = []
        if self.has_class(class_name):
            results.append(self)
        for child in self.children:
            results.extend(child.find_all_by_class(class_name))
        return results

    def find_all_by_attr(self, attr_name: str, attr_val: Optional[str] = None) -> List['DOMNode']:
        results = []
        val = self.get_attr(attr_name)
        if val is not None:
            if attr_val is None or val == attr_val:
                results.append(self)
        for child in self.children:
            results.extend(child.find_all_by_attr(attr_name, attr_val))
        return results


class HTMLTreeBuilder(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.root = DOMNode("document", {})
        self.current = self.root

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = {k.lower(): (v if v is not None else "") for k, v in attrs}
        node = DOMNode(tag, attr_dict, self.current)
        self.current.children.append(node)
        if tag.lower() not in self.VOID_TAGS:
            self.current = node

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        node = self.current
        while node is not None and node.tag != tag_lower and node != self.root:
            node = node.parent
        if node is not None and node != self.root and node.parent is not None:
            self.current = node.parent

    def handle_data(self, data: str):
        if data.strip():
            self.current.text_fragments.append(data)


def parse_html(html_str: str) -> DOMNode:
    builder = HTMLTreeBuilder()
    builder.feed(html_str)
    return builder.root


# ---------------------------------------------------------------------------
# CSS Tokens & WCAG Contrast Engine
# ---------------------------------------------------------------------------

def parse_css_tokens(css_text: str) -> Dict[str, str]:
    """Extracts CSS custom properties (--variable: value;) defined in :root or anywhere."""
    clean_css = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    token_pattern = re.compile(r'(--[\w-]+)\s*:\s*([^;]+);')
    tokens = {}
    for match in token_pattern.finditer(clean_css):
        name = match.group(1).strip()
        val = match.group(2).strip()
        tokens[name] = val
    return tokens


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    h = hex_str.strip().lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    elif len(h) == 4:
        h = "".join([c * 2 for c in h[:3]])
    elif len(h) == 8:
        h = h[:6]
    if len(h) != 6:
        raise ValueError(f"Invalid hex color string: {hex_str}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def srgb_channel_to_linear(c_byte: int) -> float:
    c = c_byte / 255.0
    if c <= 0.04045:
        return c / 12.92
    return math.pow((c + 0.055) / 1.055, 2.4)


def relative_luminance(hex_str: str) -> float:
    r, g, b = hex_to_rgb(hex_str)
    r_lin = srgb_channel_to_linear(r)
    g_lin = srgb_channel_to_linear(g)
    b_lin = srgb_channel_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def wcag_contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    l_max = max(l1, l2)
    l_min = min(l1, l2)
    return (l_max + 0.05) / (l_min + 0.05)


# ---------------------------------------------------------------------------
# SVG Path and Geometry Analyzer
# ---------------------------------------------------------------------------

class SVGInfo:
    def __init__(self, raw: str):
        self.raw = raw
        self.viewbox = self._extract_viewbox()
        self.paths = re.findall(r'<path\b([^>]*)/?>', raw, re.IGNORECASE)
        self.circles = re.findall(r'<circle\b([^>]*)/?>', raw, re.IGNORECASE)
        self.rects = re.findall(r'<rect\b([^>]*)/?>', raw, re.IGNORECASE)
        self.texts = re.findall(r'<text\b([^>]*)>(.*?)</text>', raw, re.IGNORECASE | re.DOTALL)

    def _extract_viewbox(self) -> Optional[Tuple[float, float, float, float]]:
        m = re.search(r'viewBox\s*=\s*["\']([-\d.\s]+)["\']', self.raw)
        if not m:
            return None
        parts = [float(x) for x in m.group(1).split()]
        if len(parts) == 4:
            return parts[0], parts[1], parts[2], parts[3]
        return None

    def has_evenodd_fill_rule(self) -> bool:
        return bool(re.search(r'fill-rule\s*=\s*["\']evenodd["\']', self.raw, re.IGNORECASE))

    def has_opaque_white_circles(self) -> bool:
        white_pattern = re.compile(r'fill\s*=\s*["\'](#[fF]{3,6}|white|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))["\']')
        for c in self.circles:
            if white_pattern.search(c):
                return True
        return False


def parse_svg(svg_content: str) -> SVGInfo:
    return SVGInfo(svg_content)


# ---------------------------------------------------------------------------
# Scientific Calculator Verification Formulas
# ---------------------------------------------------------------------------

def calculate_clean_air_volume(nodes: int, hours: int, fears_boost: bool = False) -> float:
    base_flow = 836.0 if fears_boost else 380.0  # m^3/h per node (836 with +120% boost)
    return nodes * base_flow * hours * 365.0


def calculate_retained_pm_mass_kg(volume_m3: float, pm_conc_ug: float, efficiency: float = 0.9997) -> float:
    # Mass in kg = Volume (m^3) * Concentration (ug/m^3) * efficiency * 1e-9 (ug to kg)
    return volume_m3 * pm_conc_ug * efficiency * 1e-9


def calculate_consultations_avoided(pm_mass_kg: float, exposed_pop: int = 15000) -> float:
    # WHO-derived epidemiological exposure factor: ~0.14 avoided visits per kg PM2.5 per 10k pop
    return pm_mass_kg * 0.14 * (exposed_pop / 10000.0)


# ---------------------------------------------------------------------------
# Assertion Helpers
# ---------------------------------------------------------------------------

def assert_true(condition: bool, msg: str = "Assertion failed: condition is not True"):
    if not condition:
        raise AssertionError(msg)


def assert_false(condition: bool, msg: str = "Assertion failed: condition is not False"):
    if condition:
        raise AssertionError(msg)


def assert_equal(actual: Any, expected: Any, msg: str = ""):
    if actual != expected:
        err = f"Expected {expected!r}, but got {actual!r}."
        if msg:
            err = f"{msg} — {err}"
        raise AssertionError(err)


def assert_in(needle: Any, haystack: Any, msg: str = ""):
    if needle not in haystack:
        err = f"Expected {needle!r} to be in container."
        if msg:
            err = f"{msg} — {err}"
        raise AssertionError(err)


def assert_not_in(needle: Any, haystack: Any, msg: str = ""):
    if needle in haystack:
        err = f"Expected {needle!r} to NOT be in container."
        if msg:
            err = f"{msg} — {err}"
        raise AssertionError(err)


def assert_ge(actual: Any, expected: Any, msg: str = ""):
    if actual < expected:
        err = f"Expected {actual!r} >= {expected!r}."
        if msg:
            err = f"{msg} — {err}"
        raise AssertionError(err)


def assert_le(actual: Any, expected: Any, msg: str = ""):
    if actual > expected:
        err = f"Expected {actual!r} <= {expected!r}."
        if msg:
            err = f"{msg} — {err}"
        raise AssertionError(err)


def assert_regex(pattern: str, text: str, msg: str = ""):
    if not re.search(pattern, text):
        err = f"Text did not match regex {pattern!r}."
        if msg:
            err = f"{msg} — {err}"
        raise AssertionError(err)
