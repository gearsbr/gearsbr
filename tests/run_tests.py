#!/usr/bin/env python3
"""
GEARS. Corporation — E2E Test Suite Runner
Dual Track Protocol: Independent Opaque-Box Requirements Verification
Standard library only: zero external dependencies.
"""

import sys
import os
import time
import argparse
import inspect
import urllib.request
import urllib.error
from typing import List, Tuple, Dict, Any, Callable

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import tests.test_tier1_features as tier1_module
import tests.test_tier2_boundaries as tier2_module
import tests.test_tier3_combinations as tier3_module
import tests.test_tier4_workflows as tier4_module

# ANSI Colors
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_CYAN = "\033[36m"
COLOR_BLUE = "\033[34m"
COLOR_GRAY = "\033[90m"


class TestCaseResult:
    def __init__(self, name: str, doc: str, tier: str, status: str, message: str = "", duration_ms: float = 0.0):
        self.name = name
        self.doc = doc.strip().split("\n")[0] if doc else name
        self.tier = tier
        self.status = status  # 'PASS', 'FAIL', 'SKIP'
        self.message = message
        self.duration_ms = duration_ms


def discover_tests(module: Any, prefix: str) -> List[Tuple[str, Callable, str]]:
    tests_list = []
    for attr_name in sorted(dir(module)):
        if attr_name.startswith(prefix):
            fn = getattr(module, attr_name)
            if callable(fn):
                doc = inspect.getdoc(fn) or attr_name
                tests_list.append((attr_name, fn, doc))
    return tests_list


def run_test_case(name: str, fn: Callable, doc: str, tier: str) -> TestCaseResult:
    t0 = time.perf_counter()
    try:
        fn()
        duration = (time.perf_counter() - t0) * 1000.0
        return TestCaseResult(name, doc, tier, "PASS", "", duration)
    except AssertionError as e:
        duration = (time.perf_counter() - t0) * 1000.0
        return TestCaseResult(name, doc, tier, "FAIL", str(e), duration)
    except Exception as e:
        duration = (time.perf_counter() - t0) * 1000.0
        return TestCaseResult(name, doc, tier, "FAIL", f"Unhandled Exception: {type(e).__name__}: {e}", duration)


def run_tier(tier_name: str, tests: List[Tuple[str, Callable, str]], verbose: bool = False) -> List[TestCaseResult]:
    print(f"\n{COLOR_BOLD}{COLOR_CYAN}▶ Running {tier_name} ({len(tests)} tests)...{COLOR_RESET}")
    results = []
    for name, fn, doc in tests:
        res = run_test_case(name, fn, doc, tier_name)
        results.append(res)
        if verbose:
            if res.status == "PASS":
                print(f"  {COLOR_GREEN}✓ PASS{COLOR_RESET} {res.name} {COLOR_GRAY}({res.duration_ms:.1f}ms){COLOR_RESET}: {res.doc}")
            else:
                print(f"  {COLOR_RED}✗ FAIL{COLOR_RESET} {res.name}: {res.doc}")
                print(f"    {COLOR_RED}Error: {res.message}{COLOR_RESET}")
        else:
            if res.status == "PASS":
                sys.stdout.write(f"{COLOR_GREEN}.{COLOR_RESET}")
            else:
                sys.stdout.write(f"{COLOR_RED}F{COLOR_RESET}")
            sys.stdout.flush()
    if not verbose:
        print()
    return results


def check_local_server(server_url: str) -> Tuple[bool, str]:
    endpoints = ["/", "/css/styles.css", "/js/main.js", "/assets/logo-gears.svg", "/assets/favicon.svg"]
    try:
        for ep in endpoints:
            url = server_url.rstrip("/") + ep
            req = urllib.request.Request(url, headers={"User-Agent": "GEARS-E2E-Runner/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status != 200:
                    return False, f"Endpoint {ep} returned status {resp.status}"
        return True, "All HTTP endpoints returned HTTP 200 OK"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="GEARS. Corporation E2E Test Suite Runner")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all", help="Execute specific test tier")
    parser.add_argument("--server", type=str, default=None, help="Check local server (e.g. http://localhost:8000)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose per-test output")
    args = parser.parse_args()

    start_time = time.perf_counter()

    print(f"{COLOR_BOLD}{COLOR_BLUE}======================================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_BLUE}    GEARS. Corporation — Opaque-Box E2E Test Suite Runner             {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_BLUE}    Dual Track Protocol // Standards & Requirements Verification       {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_BLUE}======================================================================={COLOR_RESET}")
    print(f"Working Directory: {PROJECT_ROOT}")

    all_results: List[TestCaseResult] = []
    tier_stats: Dict[str, Dict[str, int]] = {}

    # Optional Server Check
    if args.server:
        print(f"\n{COLOR_CYAN}Testing HTTP server connectivity at {args.server}...{COLOR_RESET}")
        ok, msg = check_local_server(args.server)
        if ok:
            print(f"  {COLOR_GREEN}✓ Server check passed: {msg}{COLOR_RESET}")
        else:
            print(f"  {COLOR_YELLOW}⚠ Server check warning: {msg} (Static checks will continue){COLOR_RESET}")

    # Tier 1: Feature Coverage
    if args.tier in ["1", "all"]:
        t1_tests = discover_tests(tier1_module, "test_f")
        t1_results = run_tier("Tier 1: Feature Coverage (Features 1–21)", t1_tests, args.verbose)
        all_results.extend(t1_results)
        tier_stats["Tier 1: Feature Coverage"] = {
            "pass": sum(1 for r in t1_results if r.status == "PASS"),
            "fail": sum(1 for r in t1_results if r.status == "FAIL"),
            "total": len(t1_results)
        }

    # Tier 2: Boundary & Corner Cases
    if args.tier in ["2", "all"]:
        t2_tests = discover_tests(tier2_module, "test_f")
        t2_results = run_tier("Tier 2: Boundary & Corner Cases (Features 1–21)", t2_tests, args.verbose)
        all_results.extend(t2_results)
        tier_stats["Tier 2: Boundaries & Corners"] = {
            "pass": sum(1 for r in t2_results if r.status == "PASS"),
            "fail": sum(1 for r in t2_results if r.status == "FAIL"),
            "total": len(t2_results)
        }

    # Tier 3: Cross-Feature Combinations
    if args.tier in ["3", "all"]:
        t3_tests = discover_tests(tier3_module, "test_t3_")
        t3_results = run_tier("Tier 3: Cross-Feature Combinations", t3_tests, args.verbose)
        all_results.extend(t3_results)
        tier_stats["Tier 3: Pairwise Combinations"] = {
            "pass": sum(1 for r in t3_results if r.status == "PASS"),
            "fail": sum(1 for r in t3_results if r.status == "FAIL"),
            "total": len(t3_results)
        }

    # Tier 4: Real-World Application Workflows
    if args.tier in ["4", "all"]:
        t4_tests = discover_tests(tier4_module, "test_t4_")
        t4_results = run_tier("Tier 4: Real-World Workflows", t4_tests, args.verbose)
        all_results.extend(t4_results)
        tier_stats["Tier 4: User Journeys"] = {
            "pass": sum(1 for r in t4_results if r.status == "PASS"),
            "fail": sum(1 for r in t4_results if r.status == "FAIL"),
            "total": len(t4_results)
        }

    total_duration = time.perf_counter() - start_time
    total_passed = sum(1 for r in all_results if r.status == "PASS")
    total_failed = sum(1 for r in all_results if r.status == "FAIL")
    total_count = len(all_results)

    # Print Summary Table
    print(f"\n{COLOR_BOLD}{COLOR_BLUE}======================================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_BLUE}                         TEST EXECUTION SUMMARY                        {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_BLUE}======================================================================={COLOR_RESET}")
    print(f"{'Tier / Subsystem':<38} | {'Pass':<8} | {'Fail':<8} | {'Total':<8} | {'Status':<10}")
    print("-" * 79)

    for tier_name, stats in tier_stats.items():
        st_color = COLOR_GREEN if stats["fail"] == 0 else COLOR_RED
        st_text = "PASS" if stats["fail"] == 0 else "FAIL"
        print(f"{tier_name:<38} | {stats['pass']:<8} | {stats['fail']:<8} | {stats['total']:<8} | {st_color}{st_text:<10}{COLOR_RESET}")

    print("-" * 79)
    total_color = COLOR_GREEN if total_failed == 0 else COLOR_RED
    total_status = "PASS" if total_failed == 0 else "FAIL"
    print(f"{'OVERALL SUITE':<38} | {total_passed:<8} | {total_failed:<8} | {total_count:<8} | {total_color}{COLOR_BOLD}{total_status:<10}{COLOR_RESET}")
    print(f"Elapsed Time: {total_duration:.2f}s")
    print(f"{COLOR_BOLD}{COLOR_BLUE}======================================================================={COLOR_RESET}")

    # Print Failure Details if any
    if total_failed > 0:
        print(f"\n{COLOR_BOLD}{COLOR_RED}FAILED TESTS SUMMARY ({total_failed}):{COLOR_RESET}")
        for r in all_results:
            if r.status == "FAIL":
                print(f"  {COLOR_RED}✗ [{r.tier}] {r.name}{COLOR_RESET}")
                print(f"    {COLOR_GRAY}{r.doc}{COLOR_RESET}")
                print(f"    {COLOR_YELLOW}Reason: {r.message}{COLOR_RESET}\n")
        sys.exit(1)
    else:
        print(f"\n{COLOR_BOLD}{COLOR_GREEN}✓ ALL {total_count} TEST ASSERTIONS PASSED PERFECTLY!{COLOR_RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
