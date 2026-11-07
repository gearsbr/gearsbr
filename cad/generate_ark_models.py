import os
import math
import FreeCAD
import Part
from FreeCAD import Base, Vector

doc = FreeCAD.newDocument("GEARS_Ark_Models")

# 1. ARK CHASSIS MONOBLOCO (380 x 380 x 480 mm)
width, depth, height = 380.0, 380.0, 480.0
wall_thickness = 16.0

outer_box = Part.makeBox(width, depth, height, Vector(-width/2, -depth/2, 0))
# Câmara Interna Oca
inner_box = Part.makeBox(width - 2*wall_thickness, depth - 2*wall_thickness, height - 60.0,
                         Vector(-width/2 + wall_thickness, -depth/2 + wall_thickness, 40.0))

# Janela Frontal de Acesso / Porta de Vidro
door_cut = Part.makeBox(280.0, 40.0, 360.0, Vector(-140.0, -depth/2 - 10.0, 60.0))

chassis = outer_box.cut(inner_box).cut(door_cut)

# Relevo Voxel Wave nas laterais (painéis biomiméticos acústicos)
for i in range(5):
    z_pos = 100.0 + i * 65.0
    cut_r = Part.makeCylinder(6.0, 260.0, Vector(width/2 - 5.0, -130.0, z_pos), Vector(0, 1, 0))
    cut_l = Part.makeCylinder(6.0, 260.0, Vector(-width/2 + 5.0, -130.0, z_pos), Vector(0, 1, 0))
    chassis = chassis.cut(cut_r).cut(cut_l)

chassis_obj = doc.addObject("Part::Feature", "Chassi_Ark_VoxelWave")
chassis_obj.Shape = chassis

# 2. MESA DE IMPRESSÃO AQUECIDA (260 x 260 x 8 mm)
bed = Part.makeBox(260.0, 260.0, 8.0, Vector(-130.0, -130.0, 80.0))
bed_obj = doc.addObject("Part::Feature", "Mesa_Impressao_250")
bed_obj.Shape = bed

# 3. CABEÇOTE UNIVERSAL MODULAR (TOOLHEAD 7 SEÇÕES)
toolhead_box = Part.makeBox(64.0, 72.0, 85.0, Vector(-32.0, -36.0, 320.0))
heater_block = Part.makeCylinder(9.0, 25.0, Vector(0, 0, 295.0), Vector(0, 0, 1))
nozzle_cone = Part.makeCone(6.0, 1.0, 8.0, Vector(0, 0, 287.0), Vector(0, 0, 1))
blower_r = Part.makeBox(18.0, 36.0, 45.0, Vector(32.0, -18.0, 335.0))
blower_l = Part.makeBox(18.0, 36.0, 45.0, Vector(-50.0, -18.0, 335.0))
cutter_box = Part.makeBox(26.0, 16.0, 30.0, Vector(-13.0, -48.0, 345.0))
display_disc = Part.makeCylinder(16.0, 6.0, Vector(width/2 - 14.0, -depth/2 + 65.0, 430.0), Vector(0, -1, 0))

toolhead_total = toolhead_box.fuse(heater_block).fuse(nozzle_cone).fuse(blower_r).fuse(blower_l).fuse(cutter_box)
toolhead_obj = doc.addObject("Part::Feature", "Toolhead_Universal_7Secoes")
toolhead_obj.Shape = toolhead_total

dial_obj = doc.addObject("Part::Feature", "Display_OLED_Circular")
dial_obj.Shape = display_disc

# 4. SISTEMA T.U.L.I.P.A.™ (PULMÃO URBANO BIOMIMÉTICO)
duto_inferior = Part.makeCylinder(35.0, 350.0, Vector(0, 0, 0), Vector(0, 0, 1))
corpo_filtro = Part.makeCylinder(90.0, 220.0, Vector(0, 0, 350.0), Vector(0, 0, 1))
coifa_cone = Part.makeCone(90.0, 140.0, 180.0, Vector(0, 0, 570.0), Vector(0, 0, 1))
coifa_hollow = Part.makeCone(82.0, 132.0, 185.0, Vector(0, 0, 572.0), Vector(0, 0, 1))
petalas = coifa_cone.cut(coifa_hollow)
duto_pluvial = Part.makeCylinder(14.0, 380.0, Vector(0, 0, 420.0), Vector(0, 0, 1))

tulipa_shape = duto_inferior.fuse(corpo_filtro).fuse(petalas).fuse(duto_pluvial)
tulipa_obj = doc.addObject("Part::Feature", "Sistema_TULIPA_Biomimetico")
tulipa_obj.Shape = tulipa_shape
tulipa_obj.Placement.Base = Vector(600.0, 0, 0)

doc.recompute()

output_fcstd = "/home/user/Documents/Antigravity/GEARS./cad/GEARS_Ark_Tulipa_Monobloco.FCStd"
output_step = "/home/user/Documents/Antigravity/GEARS./cad/GEARS_Ark_Tulipa_Monobloco.step"
output_stl_ark = "/home/user/Documents/Antigravity/GEARS./cad/Ark_Chassis_VoxelWave.stl"
output_stl_toolhead = "/home/user/Documents/Antigravity/GEARS./cad/Toolhead_7Secoes.stl"
output_stl_tulipa = "/home/user/Documents/Antigravity/GEARS./cad/Sistema_TULIPA.stl"

doc.saveAs(output_fcstd)
print("Salvo arquivo nativo FreeCAD:", output_fcstd)

Part.export([chassis_obj, bed_obj, toolhead_obj, dial_obj, tulipa_obj], output_step)
print("Salvo arquivo industrial STEP:", output_step)

chassis.exportStl(output_stl_ark)
toolhead_total.exportStl(output_stl_toolhead)
tulipa_shape.exportStl(output_stl_tulipa)
print("Salvos arquivos STL para impressao 3D!")
