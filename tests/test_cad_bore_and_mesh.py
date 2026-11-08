#!/usr/bin/env python3
"""
GEARS. Corporation — Monobloc Inductive Hotend Empirical Challenge Suite
================================================================================
Filament Path Probe Sweep & STL Mesh Manifoldness Stress Harness
Author: challenger_hotend_2 (Filament Path & Manifold Mesh Challenger)

This test suite empirically stress-tests:
1. Continuous internal bore clearance:
   - 1.75mm and 1.90mm filament cylinder probe sweeps from Z=83.5mm down to Z=1.5mm.
   - 0.38mm orifice probe through 0.40mm land from Z=-0.5mm to Z=0.5mm.
   - Full through-bore composite probe sweeps from Z=-0.5mm to Z=83.5mm.
   - Z-interval slice sweeps along the entire central axis.
2. STL Mesh quality, watertightness, and manifoldness:
   - Bico_Monobloco_Indutivo.stl in cad/ and GEARS_CAD/
   - MicroVentoinha_Lateral.stl in cad/ and GEARS_CAD/
   - Conjunto_Completo_Bico_GEARS.stl in cad/ and GEARS_CAD/
   - Verification of isSolid(), hasNonManifolds(), facet counts, degenerate triangles,
     and absence of isolated floating vertex shells.
================================================================================
"""

import sys
import os
import time

# Ensure FreeCAD library paths are loaded
for fc_lib in ['/usr/lib/freecad/lib', '/usr/lib/freecad-python3/lib']:
    if fc_lib not in sys.path:
        sys.path.append(fc_lib)

import FreeCAD as App
import Part
import Mesh
from FreeCAD import Vector

CAD_PATHS = [
    "/home/user/Documents/Antigravity/GEARS./cad",
    "/home/user/Documents/GEARS_CAD"
]


def test_filament_bore_175mm_clearance(cad_dir: str):
    """Test 1.75mm solid filament probe sweep from Z=83.5mm down to Z=1.5mm."""
    fcstd_path = os.path.join(cad_dir, "GEARS_Bico_DiamondBay_Piezo.FCStd")
    doc = App.openDocument(fcstd_path)
    hotend = doc.getObject("Bico_Monobloco_Indutivo").Shape

    # Cylinder dia = 1.75mm (r = 0.875mm), length = 82.0mm, from Z=1.5 to Z=83.5
    probe = Part.makeCylinder(0.875, 82.0, Vector(0, 0, 1.5), Vector(0, 0, 1))
    collision = hotend.common(probe)
    volume = collision.Volume

    App.closeDocument(doc.Name)
    assert volume < 1e-6, f"Collision detected for 1.75mm probe in {cad_dir}: volume = {volume:.8f} mm³"
    return volume


def test_filament_bore_190mm_clearance(cad_dir: str):
    """Test 1.90mm solid filament probe sweep from Z=83.5mm down to Z=1.5mm."""
    fcstd_path = os.path.join(cad_dir, "GEARS_Bico_DiamondBay_Piezo.FCStd")
    doc = App.openDocument(fcstd_path)
    hotend = doc.getObject("Bico_Monobloco_Indutivo").Shape

    # Cylinder dia = 1.90mm (r = 0.950mm), length = 82.0mm, from Z=1.5 to Z=83.5
    probe = Part.makeCylinder(0.950, 82.0, Vector(0, 0, 1.5), Vector(0, 0, 1))
    collision = hotend.common(probe)
    volume = collision.Volume

    App.closeDocument(doc.Name)
    assert volume < 1e-6, f"Collision detected for 1.90mm probe in {cad_dir}: volume = {volume:.8f} mm³"
    return volume


def test_orifice_land_038mm_clearance(cad_dir: str):
    """Test 0.38mm probe through 0.40mm orifice land from Z=-0.5mm to Z=0.5mm."""
    fcstd_path = os.path.join(cad_dir, "GEARS_Bico_DiamondBay_Piezo.FCStd")
    doc = App.openDocument(fcstd_path)
    hotend = doc.getObject("Bico_Monobloco_Indutivo").Shape

    # Cylinder dia = 0.38mm (r = 0.190mm), length = 1.0mm, from Z=-0.5 to Z=0.5
    probe = Part.makeCylinder(0.190, 1.0, Vector(0, 0, -0.5), Vector(0, 0, 1))
    collision = hotend.common(probe)
    volume = collision.Volume

    App.closeDocument(doc.Name)
    assert volume < 1e-6, f"Collision detected for 0.38mm probe in {cad_dir}: volume = {volume:.8f} mm³"
    return volume


def test_full_through_bore_continuity(cad_dir: str):
    """Test full through-bore composite probe sweeps from Z=-0.5mm to Z=83.5mm."""
    fcstd_path = os.path.join(cad_dir, "GEARS_Bico_DiamondBay_Piezo.FCStd")
    doc = App.openDocument(fcstd_path)
    hotend = doc.getObject("Bico_Monobloco_Indutivo").Shape

    # 1. Composite 1.75mm through probe
    p_ori = Part.makeCylinder(0.190, 1.0, Vector(0, 0, -0.5), Vector(0, 0, 1))
    p_fun = Part.makeCone(0.190, 0.875, 1.0, Vector(0, 0, 0.5), Vector(0, 0, 1))
    p_bore = Part.makeCylinder(0.875, 82.0, Vector(0, 0, 1.5), Vector(0, 0, 1))
    full_probe_175 = p_ori.fuse(p_fun).fuse(p_bore)
    vol_175 = hotend.common(full_probe_175).Volume

    # 2. Composite 1.90mm through probe
    p_fun_190 = Part.makeCone(0.190, 0.950, 1.0, Vector(0, 0, 0.5), Vector(0, 0, 1))
    p_bore_190 = Part.makeCylinder(0.950, 82.0, Vector(0, 0, 1.5), Vector(0, 0, 1))
    full_probe_190 = p_ori.fuse(p_fun_190).fuse(p_bore_190)
    vol_190 = hotend.common(full_probe_190).Volume

    # 3. Stepwise interval checks along Z from Z=0.5 to Z=83.5 (166 intervals)
    obstructed_intervals = 0
    for i in range(166):
        z1 = 0.5 + i * 0.5
        z2 = z1 + 0.5
        if z2 > 83.5:
            break
        if z2 <= 0.5:
            pr = Part.makeCylinder(0.190, z2 - z1, Vector(0, 0, z1), Vector(0, 0, 1))
        elif z1 >= 1.5:
            pr = Part.makeCylinder(0.875, z2 - z1, Vector(0, 0, z1), Vector(0, 0, 1))
        else:
            r_start = 0.190 + 0.685 * (z1 - 0.5)
            r_end = 0.190 + 0.685 * (z2 - 0.5)
            pr = Part.makeCone(r_start, r_end, z2 - z1, Vector(0, 0, z1), Vector(0, 0, 1))
        if hotend.common(pr).Volume > 1e-8:
            obstructed_intervals += 1

    App.closeDocument(doc.Name)
    assert vol_175 < 1e-6, f"Full 1.75mm probe collision: {vol_175:.8f} mm³"
    assert vol_190 < 1e-6, f"Full 1.90mm probe collision: {vol_190:.8f} mm³"
    assert obstructed_intervals == 0, f"Found {obstructed_intervals} obstructed intervals along bore!"
    return vol_175, vol_190, obstructed_intervals


def test_stl_bico_monobloco(cad_dir: str):
    """Test Bico_Monobloco_Indutivo.stl mesh manifoldness, watertightness, and facet count."""
    stl_path = os.path.join(cad_dir, "Bico_Monobloco_Indutivo.stl")
    assert os.path.exists(stl_path), f"Missing file: {stl_path}"

    m = Mesh.Mesh(stl_path)
    comps = m.getSeparateComponents()
    degen = [f for f in m.Facets if f.Area <= 1e-12]

    assert m.isSolid(), f"{stl_path} is not solid!"
    assert not m.hasNonManifolds(), f"{stl_path} has non-manifolds!"
    assert not m.hasSelfIntersections(), f"{stl_path} has self-intersections!"
    assert not m.hasCorruptedFacets(), f"{stl_path} has corrupted facets!"
    assert not m.hasInvalidPoints(), f"{stl_path} has invalid points!"
    assert m.CountFacets > 100000, f"{stl_path} facet count too low: {m.CountFacets}"
    assert len(comps) == 1, f"{stl_path} expected 1 shell component, got {len(comps)}"
    assert len(degen) == 0, f"{stl_path} has {len(degen)} degenerate facets!"

    return {
        "facets": m.CountFacets,
        "points": m.CountPoints,
        "is_solid": m.isSolid(),
        "has_non_manifolds": m.hasNonManifolds(),
        "has_self_intersections": m.hasSelfIntersections(),
        "components": len(comps),
        "degenerate_facets": len(degen),
        "volume": comps[0].Volume,
        "area": comps[0].Area,
    }


def test_stl_microventoinha(cad_dir: str):
    """Test MicroVentoinha_Lateral.stl mesh manifoldness, watertightness, and facet count."""
    stl_path = os.path.join(cad_dir, "MicroVentoinha_Lateral.stl")
    assert os.path.exists(stl_path), f"Missing file: {stl_path}"

    m = Mesh.Mesh(stl_path)
    comps = m.getSeparateComponents()
    degen = [f for f in m.Facets if f.Area <= 1e-12]

    assert m.isSolid(), f"{stl_path} is not solid!"
    assert not m.hasNonManifolds(), f"{stl_path} has non-manifolds!"
    assert not m.hasSelfIntersections(), f"{stl_path} has self-intersections!"
    assert not m.hasCorruptedFacets(), f"{stl_path} has corrupted facets!"
    assert not m.hasInvalidPoints(), f"{stl_path} has invalid points!"
    assert m.CountFacets > 5000, f"{stl_path} facet count too low: {m.CountFacets}"
    assert len(comps) == 3, f"{stl_path} expected 3 shell components, got {len(comps)}"
    assert len(degen) == 0, f"{stl_path} has {len(degen)} degenerate facets!"

    for i, c in enumerate(comps):
        assert c.isSolid(), f"Component {i} in {stl_path} is not solid!"
        assert not c.hasNonManifolds(), f"Component {i} in {stl_path} has non-manifolds!"
        assert c.Volume > 0, f"Component {i} in {stl_path} has non-positive volume!"

    return {
        "facets": m.CountFacets,
        "points": m.CountPoints,
        "is_solid": m.isSolid(),
        "has_non_manifolds": m.hasNonManifolds(),
        "has_self_intersections": m.hasSelfIntersections(),
        "components": len(comps),
        "degenerate_facets": len(degen),
        "component_volumes": [c.Volume for c in comps]
    }


def test_stl_conjunto_completo(cad_dir: str):
    """Test Conjunto_Completo_Bico_GEARS.stl assembly sub-components manifoldness and quality."""
    stl_path = os.path.join(cad_dir, "Conjunto_Completo_Bico_GEARS.stl")
    assert os.path.exists(stl_path), f"Missing file: {stl_path}"

    m = Mesh.Mesh(stl_path)
    comps = m.getSeparateComponents()
    degen = [f for f in m.Facets if f.Area <= 1e-12]

    assert not m.hasCorruptedFacets(), f"{stl_path} has corrupted facets!"
    assert not m.hasInvalidPoints(), f"{stl_path} has invalid points!"
    assert m.CountFacets > 130000, f"{stl_path} facet count too low: {m.CountFacets}"
    assert len(comps) == 8, f"{stl_path} expected 8 assembly components, got {len(comps)}"
    assert len(degen) == 0, f"{stl_path} has {len(degen)} degenerate facets!"

    comp_details = []
    for i, c in enumerate(comps):
        assert c.isSolid(), f"Assembly component {i} in {stl_path} is not solid!"
        assert not c.hasNonManifolds(), f"Assembly component {i} in {stl_path} has non-manifolds!"
        assert not c.hasSelfIntersections(), f"Assembly component {i} in {stl_path} has self-intersections!"
        assert c.Volume > 0, f"Assembly component {i} in {stl_path} has zero volume!"
        c_degen = [f for f in c.Facets if f.Area <= 1e-12]
        assert len(c_degen) == 0, f"Assembly component {i} has degenerate facets!"
        comp_details.append({
            "index": i,
            "facets": c.CountFacets,
            "points": c.CountPoints,
            "is_solid": c.isSolid(),
            "has_non_manifolds": c.hasNonManifolds(),
            "has_self_intersections": c.hasSelfIntersections(),
            "volume": c.Volume,
            "area": c.Area,
            "bb": (c.BoundBox.XMin, c.BoundBox.XMax, c.BoundBox.YMin, c.BoundBox.YMax, c.BoundBox.ZMin, c.BoundBox.ZMax)
        })

    return {
        "facets": m.CountFacets,
        "points": m.CountPoints,
        "components_count": len(comps),
        "degenerate_facets": len(degen),
        "components": comp_details
    }


def run_all_challenges():
    print("=" * 80)
    print("EMPIRICAL CHALLENGER 2: FILAMENT PATH & MESH MANIFOLD STRESS HARNESS")
    print("=" * 80)

    results = {}
    for cad_dir in CAD_PATHS:
        print(f"\n>>> Running stress tests on: {cad_dir}")
        t0 = time.time()

        print("  1. Testing 1.75mm bore probe clearance...")
        vol_175 = test_filament_bore_175mm_clearance(cad_dir)
        print(f"     [PASS] Probe 1.75mm intersection volume = {vol_175:.6f} mm³")

        print("  2. Testing 1.90mm bore probe clearance...")
        vol_190 = test_filament_bore_190mm_clearance(cad_dir)
        print(f"     [PASS] Probe 1.90mm intersection volume = {vol_190:.6f} mm³")

        print("  3. Testing 0.38mm orifice land probe clearance...")
        vol_038 = test_orifice_land_038mm_clearance(cad_dir)
        print(f"     [PASS] Probe 0.38mm intersection volume = {vol_038:.6f} mm³")

        print("  4. Testing 100% continuous through-bore probe sweeps...")
        c_175, c_190, obst = test_full_through_bore_continuity(cad_dir)
        print(f"     [PASS] Full 1.75mm probe volume = {c_175:.6f} mm³, 1.90mm = {c_190:.6f} mm³, obstructed intervals = {obst}")

        print("  5. Testing Bico_Monobloco_Indutivo.stl mesh quality...")
        res_hotend = test_stl_bico_monobloco(cad_dir)
        print(f"     [PASS] Facets={res_hotend['facets']:,}, isSolid={res_hotend['is_solid']}, NonManifold={res_hotend['has_non_manifolds']}, Degen={res_hotend['degenerate_facets']}")

        print("  6. Testing MicroVentoinha_Lateral.stl mesh quality...")
        res_fan = test_stl_microventoinha(cad_dir)
        print(f"     [PASS] Facets={res_fan['facets']:,}, isSolid={res_fan['is_solid']}, NonManifold={res_fan['has_non_manifolds']}, Components={res_fan['components']}")

        print("  7. Testing Conjunto_Completo_Bico_GEARS.stl assembly components...")
        res_assembly = test_stl_conjunto_completo(cad_dir)
        print(f"     [PASS] Total Facets={res_assembly['facets']:,}, 8 Subassembly Components All Watertight Solids!")
        for c in res_assembly['components']:
            print(f"       - Comp {c['index']}: Facets={c['facets']:,}, Vol={c['volume']:.2f} mm³, isSolid={c['is_solid']}, NonManifold={c['has_non_manifolds']}")

        results[cad_dir] = {
            "vol_175": vol_175,
            "vol_190": vol_190,
            "vol_038": vol_038,
            "c_175": c_175,
            "c_190": c_190,
            "obstructed_intervals": obst,
            "hotend_stl": res_hotend,
            "fan_stl": res_fan,
            "assembly_stl": res_assembly,
            "duration": time.time() - t0
        }

    print("\n" + "=" * 80)
    print("ALL EMPIRICAL CHALLENGES PASSED ACROSS BOTH DIRECTORIES WITH ZERO FAILURES!")
    print("=" * 80)
    return results


if __name__ == "__main__":
    run_all_challenges()
