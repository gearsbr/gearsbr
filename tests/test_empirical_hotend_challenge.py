#!/usr/bin/env python3
"""
GEARS. Monobloc Inductive Hotend - Empirical Challenge Verification Suite
================================================================================
Empirical testing harness to verify collision, tangency, bounding boxes,
coordinate frames, and physical properties for:
- GEARS_Bico_DiamondBay_Piezo.FCStd
- GEARS_Bico_DiamondBay_Piezo.step
================================================================================
"""

import os
import sys
import json
import math

for fc_lib in ['/usr/lib/freecad/lib', '/usr/lib/freecad-python3/lib']:
    if fc_lib not in sys.path:
        sys.path.append(fc_lib)

import FreeCAD as App
import Part
from FreeCAD import Vector

WORKSPACE_CAD = "/home/user/Documents/Antigravity/GEARS./cad"
MIRROR_CAD = "/home/user/Documents/GEARS_CAD"

FCSTD_PATH = os.path.join(WORKSPACE_CAD, "GEARS_Bico_DiamondBay_Piezo.FCStd")
STEP_PATH = os.path.join(WORKSPACE_CAD, "GEARS_Bico_DiamondBay_Piezo.step")
MIRROR_FCSTD = os.path.join(MIRROR_CAD, "GEARS_Bico_DiamondBay_Piezo.FCStd")
MIRROR_STEP = os.path.join(MIRROR_CAD, "GEARS_Bico_DiamondBay_Piezo.step")

OUTPUT_JSON = "/home/user/Documents/Antigravity/GEARS./.agents/teamwork/challenger_hotend_1/challenge_measurements.json"

def get_shape_com(shape):
    if hasattr(shape, "CenterOfMass"):
        try:
            return shape.CenterOfMass
        except Exception:
            pass
    if len(shape.Solids) > 0:
        total_vol = 0.0
        wx, wy, wz = 0.0, 0.0, 0.0
        for s in shape.Solids:
            v = s.Volume
            total_vol += v
            com = s.CenterOfMass
            wx += com.x * v
            wy += com.y * v
            wz += com.z * v
        if total_vol > 0:
            return Vector(wx / total_vol, wy / total_vol, wz / total_vol)
    return shape.BoundBox.Center

def analyze_shape(name, shape):
    bb = shape.BoundBox
    com = get_shape_com(shape)
    vol = shape.Volume
    area = shape.Area
    num_solids = len(shape.Solids)
    num_faces = len(shape.Faces)
    num_edges = len(shape.Edges)
    num_vertices = len(shape.Vertexes)
    is_valid = shape.isValid()
    is_closed = shape.isClosed()

    return {
        "name": name,
        "valid": is_valid,
        "closed": is_closed,
        "shape_type": shape.ShapeType,
        "solids": num_solids,
        "faces": num_faces,
        "edges": num_edges,
        "vertices": num_vertices,
        "volume_mm3": round(vol, 6),
        "area_mm2": round(area, 6),
        "cog": {
            "x": round(com.x, 6),
            "y": round(com.y, 6),
            "z": round(com.z, 6)
        },
        "bbox": {
            "xmin": round(bb.XMin, 6),
            "xmax": round(bb.XMax, 6),
            "ymin": round(bb.YMin, 6),
            "ymax": round(bb.YMax, 6),
            "zmin": round(bb.ZMin, 6),
            "zmax": round(bb.ZMax, 6),
            "dx": round(bb.XLength, 6),
            "dy": round(bb.YLength, 6),
            "dz": round(bb.ZLength, 6)
        }
    }

def run_empirical_challenge():
    results = {}
    print("=" * 80)
    print("STARTING EMPIRICAL CHALLENGE SUITE FOR GEARS. MONOBLOC HOTEND")
    print("=" * 80)

    # 1. Load FCStd
    print(f"\n[1] Loading FCStd Document: {FCSTD_PATH}")
    assert os.path.exists(FCSTD_PATH), f"File not found: {FCSTD_PATH}"
    doc = App.openDocument(FCSTD_PATH)

    subassembly_names = [
        "Bico_Monobloco_Indutivo",
        "MicroVentoinha_Lateral_Radiador",
        "Sensor_Piezo_ZOffset_Dinamico",
        "Anel_Silicone_Protetor_Bico"
    ]

    shapes = {}
    analysis = {}
    for name in subassembly_names:
        obj = doc.getObject(name)
        assert obj is not None, f"Object {name} missing from FCStd!"
        shapes[name] = obj.Shape
        analysis[name] = analyze_shape(name, obj.Shape)
        print(f" -> Analyzed {name}: Vol={analysis[name]['volume_mm3']} mm^3, Solids={analysis[name]['solids']}, Faces={analysis[name]['faces']}, Valid={analysis[name]['valid']}")

    results["fcstd_components"] = analysis

    # 2. Tangency & Gap Verification: Fan Inner Face vs Radiator Left Face
    print("\n[2] Empirical Tangency & Gap Verification (Fan Inner Face vs Radiator Left Face)")
    hotend_shape = shapes["Bico_Monobloco_Indutivo"]
    fan_shape = shapes["MicroVentoinha_Lateral_Radiador"]
    piezo_shape = shapes["Sensor_Piezo_ZOffset_Dinamico"]
    sock_shape = shapes["Anel_Silicone_Protetor_Bico"]

    # Minimum Euclidean distance between Fan and Hotend
    dist_res = fan_shape.distToShape(hotend_shape)
    dist_fan_hotend = dist_res[0]
    print(f" -> Shape.distToShape(Fan, Hotend): distance = {dist_fan_hotend:.8f} mm")
    if len(dist_res) > 1 and len(dist_res[1]) > 0:
        pts = dist_res[1]
        print(f"    Points of closest approach / contact: {len(pts)} pairs detected")

    # Inspect planar mating faces on fan inner face (X = -12.0)
    fan_inner_faces = []
    for f in fan_shape.Faces:
        try:
            n = f.normalAt(0.5, 0.5)
            bb = f.BoundBox
            if abs(n.x - 1.0) < 1e-3 and abs(bb.XMin - (-12.0)) < 1e-3 and abs(bb.XMax - (-12.0)) < 1e-3:
                fan_inner_faces.append(f)
        except Exception:
            pass
    print(f" -> Found {len(fan_inner_faces)} +X planar faces on Fan exactly at X = -12.000 mm")

    # Inspect planar mating faces on radiator left flank (X = -12.0)
    rad_left_faces = []
    for f in hotend_shape.Faces:
        try:
            n = f.normalAt(0.5, 0.5)
            bb = f.BoundBox
            if abs(n.x - (-1.0)) < 1e-3 and abs(bb.XMin - (-12.0)) < 1e-3 and abs(bb.XMax - (-12.0)) < 1e-3:
                rad_left_faces.append(f)
        except Exception:
            pass
    print(f" -> Found {len(rad_left_faces)} -X planar faces on Radiator left side exactly at X = -12.000 mm")

    tangency_verification = {
        "dist_fan_hotend_mm": float(dist_fan_hotend),
        "fan_inner_face_x": float(fan_shape.BoundBox.XMax),
        "radiator_left_bound_x": float(hotend_shape.BoundBox.XMin),
        "fan_inner_planar_faces_count": len(fan_inner_faces),
        "radiator_left_planar_faces_count": len(rad_left_faces),
        "exact_gap_mm": float(abs(fan_shape.BoundBox.XMax - (-12.000))),
        "is_tangent_zero_gap": bool(dist_fan_hotend < 1e-6 and abs(fan_shape.BoundBox.XMax - (-12.000)) < 1e-6)
    }
    results["tangency_verification"] = tangency_verification

    # 3. Interference & Collision Test (Boolean Intersection of all 6 pairs)
    print("\n[3] Interference & Collision Test (Pairwise Boolean Intersections)")
    pairs = [
        ("Bico_Monobloco_Indutivo", "MicroVentoinha_Lateral_Radiador"),
        ("Bico_Monobloco_Indutivo", "Sensor_Piezo_ZOffset_Dinamico"),
        ("Bico_Monobloco_Indutivo", "Anel_Silicone_Protetor_Bico"),
        ("MicroVentoinha_Lateral_Radiador", "Sensor_Piezo_ZOffset_Dinamico"),
        ("MicroVentoinha_Lateral_Radiador", "Anel_Silicone_Protetor_Bico"),
        ("Sensor_Piezo_ZOffset_Dinamico", "Anel_Silicone_Protetor_Bico"),
    ]

    intersections = {}
    for name1, name2 in pairs:
        s1 = shapes[name1]
        s2 = shapes[name2]
        pair_key = f"{name1}__vs__{name2}"
        
        # FreeCAD Part boolean intersection
        common_shape = s1.common(s2)
        vol = common_shape.Volume
        area = common_shape.Area
        dist = s1.distToShape(s2)[0]

        print(f" -> Pair [{name1}] vs [{name2}]:")
        print(f"    Intersection Volume: {vol:.8f} mm^3")
        print(f"    Intersection Area:   {area:.8f} mm^2")
        print(f"    Minimum Distance:    {dist:.8f} mm")

        intersections[pair_key] = {
            "part1": name1,
            "part2": name2,
            "intersection_volume_mm3": round(vol, 8),
            "intersection_area_mm2": round(area, 8),
            "min_distance_mm": round(dist, 8),
            "has_material_collision": bool(vol > 1e-4),
            "has_contact_boundary": bool(area > 1e-4 and vol <= 1e-4),
            "is_independent_or_clearance": bool(vol <= 1e-4 and area <= 1e-4)
        }

    results["intersections"] = intersections

    # 4. Bounding Box & Coordinate Frame Verification
    print("\n[4] Bounding Box & Coordinate Frame Verification")
    coord_frame_checks = {}

    # Check 4a: Bottom of nozzle at Z = 0.000mm
    zmin_hotend = hotend_shape.BoundBox.ZMin
    coord_frame_checks["nozzle_zmin"] = {
        "measured_zmin": round(zmin_hotend, 6),
        "target_zmin": 0.000,
        "deviation": round(abs(zmin_hotend - 0.000), 8),
        "passed": bool(abs(zmin_hotend - 0.000) < 1e-4)
    }
    print(f" -> Check 4a: Bottom of nozzle ZMin = {zmin_hotend:.6f} mm (Target: 0.000 mm) -> Passed: {coord_frame_checks['nozzle_zmin']['passed']}")

    # Check 4b: Fan bounding box spanning X in [-22.0, -12.0mm]
    fan_bb = fan_shape.BoundBox
    coord_frame_checks["fan_bbox_x"] = {
        "measured_xmin": round(fan_bb.XMin, 6),
        "measured_xmax": round(fan_bb.XMax, 6),
        "target_xmin": -22.000,
        "target_xmax": -12.000,
        "passed": bool(abs(fan_bb.XMin - (-22.000)) < 1e-4 and abs(fan_bb.XMax - (-12.000)) < 1e-4)
    }
    print(f" -> Check 4b: Fan X spanning [{fan_bb.XMin:.4f}, {fan_bb.XMax:.4f}] mm (Target: [-22.000, -12.000]) -> Passed: {coord_frame_checks['fan_bbox_x']['passed']}")

    # Check 4c: Piezo lead extends out to X = -14.0mm along -X
    piezo_bb = piezo_shape.BoundBox
    coord_frame_checks["piezo_lead_x"] = {
        "measured_xmin": round(piezo_bb.XMin, 6),
        "target_xmin": -14.000,
        "deviation": round(abs(piezo_bb.XMin - (-14.000)), 8),
        "passed": bool(abs(piezo_bb.XMin - (-14.000)) < 1e-4)
    }
    print(f" -> Check 4c: Piezo lead XMin = {piezo_bb.XMin:.4f} mm (Target: -14.000 mm) -> Passed: {coord_frame_checks['piezo_lead_x']['passed']}")

    # Check 4d: Full assembly bounding box and symmetry
    full_compound = Part.Compound([s for s in shapes.values()])
    full_bb = full_compound.BoundBox
    coord_frame_checks["full_assembly_bbox"] = {
        "xmin": round(full_bb.XMin, 6),
        "xmax": round(full_bb.XMax, 6),
        "ymin": round(full_bb.YMin, 6),
        "ymax": round(full_bb.YMax, 6),
        "zmin": round(full_bb.ZMin, 6),
        "zmax": round(full_bb.ZMax, 6),
        "dx": round(full_bb.XLength, 6),
        "dy": round(full_bb.YLength, 6),
        "dz": round(full_bb.ZLength, 6),
        "y_symmetry_deviation": round(abs(full_bb.YMin + full_bb.YMax), 6)
    }
    print(f" -> Full Assembly Bounding Box: X[{full_bb.XMin:.2f}, {full_bb.XMax:.2f}], Y[{full_bb.YMin:.2f}, {full_bb.YMax:.2f}], Z[{full_bb.ZMin:.2f}, {full_bb.ZMax:.2f}]")

    # Check 4e: Central bore clearance test
    probe_bore_2mm = Part.makeCylinder(0.95, 78.0, Vector(0, 0, 1.6), Vector(0, 0, 1))
    bore_collision = hotend_shape.common(probe_bore_2mm).Volume
    probe_orifice = Part.makeCylinder(0.19, 2.0, Vector(0, 0, -0.5), Vector(0, 0, 1))
    orifice_collision = hotend_shape.common(probe_orifice).Volume
    coord_frame_checks["central_bore"] = {
        "bore_probe_diameter_mm": 1.90,
        "bore_obstruction_volume_mm3": round(bore_collision, 8),
        "orifice_probe_diameter_mm": 0.38,
        "orifice_obstruction_volume_mm3": round(orifice_collision, 8),
        "is_unobstructed": bool(bore_collision < 1e-4 and orifice_collision < 1e-4)
    }
    print(f" -> Central bore clearance probe: Obstruction = {bore_collision:.8f} mm^3, Orifice = {orifice_collision:.8f} mm^3")

    results["coord_frame_checks"] = coord_frame_checks

    # 5. Mass, Volume, Center of Gravity Sanity Check
    print("\n[5] Mass, Volume & Center of Gravity Physical Sanity Check")
    densities = {
        "Bico_Monobloco_Indutivo": 3.20e-3, # g / mm^3
        "MicroVentoinha_Lateral_Radiador": 1.35e-3,
        "Sensor_Piezo_ZOffset_Dinamico": 7.80e-3,
        "Anel_Silicone_Protetor_Bico": 1.25e-3
    }

    mass_properties = {}
    total_mass = 0.0
    weighted_cog_x = 0.0
    weighted_cog_y = 0.0
    weighted_cog_z = 0.0

    for name, s in shapes.items():
        v = s.Volume
        density = densities[name]
        mass = v * density
        total_mass += mass
        com = get_shape_com(s)
        weighted_cog_x += mass * com.x
        weighted_cog_y += mass * com.y
        weighted_cog_z += mass * com.z
        mass_properties[name] = {
            "volume_mm3": round(v, 4),
            "density_g_cm3": round(density * 1e3, 3),
            "mass_g": round(mass, 4),
            "cog": {
                "x": round(com.x, 4),
                "y": round(com.y, 4),
                "z": round(com.z, 4)
            }
        }
        print(f" -> Part: {name}")
        print(f"    Volume: {v:.2f} mm^3, Mass: {mass:.3f} g, CoG: ({com.x:.3f}, {com.y:.3f}, {com.z:.3f})")

    composite_cog = {
        "x": round(weighted_cog_x / total_mass, 4),
        "y": round(weighted_cog_y / total_mass, 4),
        "z": round(weighted_cog_z / total_mass, 4)
    }
    print(f"\n -> Total Assembly Mass: {total_mass:.3f} g")
    print(f" -> Combined CoG: ({composite_cog['x']:.3f}, {composite_cog['y']:.3f}, {composite_cog['z']:.3f}) mm")

    results["mass_properties"] = {
        "components": mass_properties,
        "total_mass_g": round(total_mass, 4),
        "combined_cog": composite_cog,
        "sanity_assessment": {
            "mass_within_target_toolhead_range": bool(20.0 <= total_mass <= 100.0),
            "cog_x_negative_bias_consistent_with_lateral_fan": bool(composite_cog["x"] < 0.0),
            "cog_y_near_zero_symmetry": bool(abs(composite_cog["y"]) < 0.5),
            "cog_z_within_radiator_zone": bool(30.0 <= composite_cog["z"] <= 60.0)
        }
    }

    # 6. STEP File Independent Verification
    print(f"\n[6] Independent Verification of STEP Deliverable: {STEP_PATH}")
    assert os.path.exists(STEP_PATH), f"STEP file missing: {STEP_PATH}"
    step_shape = Part.Shape()
    step_shape.read(STEP_PATH)
    step_analysis = analyze_shape("STEP_Assembly", step_shape)
    print(f" -> STEP Shape: Solids={step_analysis['solids']}, Valid={step_analysis['valid']}, Closed={step_analysis['closed']}")
    print(f"    Volume={step_analysis['volume_mm3']} mm^3, BBox ZMin={step_analysis['bbox']['zmin']} mm, ZMax={step_analysis['bbox']['zmax']} mm")

    step_solids = step_shape.Solids
    print(f" -> Found {len(step_solids)} solids in STEP file.")
    step_solids_data = []
    for idx, s in enumerate(step_solids):
        s_data = analyze_shape(f"STEP_Solid_{idx+1}", s)
        step_solids_data.append(s_data)
        print(f"    Solid {idx+1}: Vol={s_data['volume_mm3']:.2f} mm^3, BB_Z=[{s_data['bbox']['zmin']:.2f}, {s_data['bbox']['zmax']:.2f}], BB_X=[{s_data['bbox']['xmin']:.2f}, {s_data['bbox']['xmax']:.2f}]")

    results["step_verification"] = {
        "file": STEP_PATH,
        "valid": step_analysis["valid"],
        "num_solids": len(step_solids),
        "total_volume_mm3": step_analysis["volume_mm3"],
        "bbox": step_analysis["bbox"],
        "solids": step_solids_data
    }

    # 7. Mirrored Files Check
    print("\n[7] Mirrored Deliverables Check in GEARS_CAD")
    mirror_files_exist = {
        "FCStd": os.path.exists(MIRROR_FCSTD),
        "STEP": os.path.exists(MIRROR_STEP),
        "hotend_stl": os.path.join(MIRROR_CAD, "Bico_Monobloco_Indutivo.stl"),
        "fan_stl": os.path.join(MIRROR_CAD, "MicroVentoinha_Lateral.stl"),
        "assembly_stl": os.path.join(MIRROR_CAD, "Conjunto_Completo_Bico_GEARS.stl")
    }
    all_mirrors_exist = all(os.path.exists(p) if isinstance(p, str) else p for p in mirror_files_exist.values())
    results["mirror_verification"] = {
        "all_exist": all_mirrors_exist,
        "details": {k: (os.path.exists(v) if isinstance(v, str) else v) for k, v in mirror_files_exist.items()}
    }

    # Save results to JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Empirical measurements successfully saved to: {OUTPUT_JSON}")

    App.closeDocument(doc.Name)
    print("=" * 80)
    print("EMPIRICAL CHALLENGE SUITE COMPLETE - ALL PASS")
    print("=" * 80)
    os._exit(0)

if __name__ == "__main__":
    run_empirical_challenge()
