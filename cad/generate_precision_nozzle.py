import FreeCAD
import Part
from FreeCAD import Base, Vector

doc = FreeCAD.newDocument("GEARS_Hotend_Nozzle_Assembly")

# ==============================================================================
# BICO DE ALTA PRECISÃO GEARS. (HOTEND MONOBLOCO INDUTIVO)
# Modelagem anatômica detalhada de cima para baixo
# ==============================================================================

# Coordenada Z de montagem descendente
z_current = 90.0

# ------------------------------------------------------------------------------
# 1. ENTRADA EM FORMA DE DONUT (GUIA SUPERIOR DO FILAMENTO)
# ------------------------------------------------------------------------------
# Toroide suave (Donut) no topo para guiar o filamento de 1.75mm
donut_major_r = 5.5
donut_minor_r = 2.0
donut_torus = Part.makeTorus(donut_major_r, donut_minor_r, Vector(0, 0, z_current), Vector(0, 0, 1))

# Tubo interno central (canal de passagem do filamento de 2.0mm de diâmetro)
filament_channel = Part.makeCylinder(1.05, 120.0, Vector(0, 0, -20.0), Vector(0, 0, 1))

# Tubo pescoço de entrada conectado ao donut
entry_tube = Part.makeCylinder(4.2, 8.0, Vector(0, 0, z_current - 8.0), Vector(0, 0, 1))
top_entry = donut_torus.fuse(entry_tube)

z_current -= 8.0

# ------------------------------------------------------------------------------
# 2. SEÇÃO DA PLACA NFC & COMUNICAÇÃO SMART
# Aloja a antena e chip NFC para leitura de tipo de bico, diâmetro e horas de uso
# ------------------------------------------------------------------------------
nfc_height = 10.0
nfc_body = Part.makeCylinder(7.5, nfc_height, Vector(0, 0, z_current - nfc_height), Vector(0, 0, 1))

# Rebaixo estilizado da placa NFC (face plana para contato e leitura com o toolhead)
nfc_flat_cut = Part.makeBox(6.0, 16.0, nfc_height + 2.0, Vector(5.5, -8.0, z_current - nfc_height - 1.0))
nfc_section = nfc_body.cut(nfc_flat_cut)

# Pequena ranhura de trava mecânica de posicionamento
keyway = Part.makeBox(3.0, 3.0, nfc_height, Vector(-7.5, -1.5, z_current - nfc_height))
nfc_section = nfc_section.cut(keyway)

z_current -= nfc_height

# ------------------------------------------------------------------------------
# 3. RADIADOR DE RESFRIAMENTO (DISSIPADOR COM ALETAS CIRCULARES)
# ------------------------------------------------------------------------------
heatsink_height = 28.0
heatsink_core = Part.makeCylinder(4.0, heatsink_height, Vector(0, 0, z_current - heatsink_height), Vector(0, 0, 1))

# Aletas de refrigeração
num_fins = 8
fin_thick = 1.0
fin_spacing = (heatsink_height - 4.0) / num_fins
fin_outer_r = 10.5

heatsink_full = heatsink_core
for i in range(num_fins):
    fin_z = z_current - heatsink_height + 2.0 + i * fin_spacing
    fin = Part.makeCylinder(fin_outer_r, fin_thick, Vector(0, 0, fin_z), Vector(0, 0, 1))
    heatsink_full = heatsink_full.fuse(fin)

# ------------------------------------------------------------------------------
# 4. MICRO-VENTOINHA ACOPLADA DO LADO ESQUERDO DO RADIADOR
# Quadrada com bordas arredondadas (fillet), grade e carcaça
# ------------------------------------------------------------------------------
fan_size = 22.0
fan_thick = 8.0
fan_z_pos = z_current - heatsink_height + 4.0
fan_x_pos = -fin_outer_r - fan_thick - 1.0

# Bloco base da carcaça da ventoinha
fan_base = Part.makeBox(fan_thick, fan_size, fan_size, Vector(fan_x_pos, -fan_size/2, fan_z_pos))
fan_box = fan_base.makeFillet(3.0, fan_base.Edges)

# Abertura circular da hélice (furo central)
fan_hole = Part.makeCylinder(9.0, fan_thick + 2.0, Vector(fan_x_pos - 1.0, 0, fan_z_pos + fan_size/2), Vector(1, 0, 0))

# Cubo central do motor da ventoinha
fan_hub = Part.makeCylinder(4.2, fan_thick, Vector(fan_x_pos, 0, fan_z_pos + fan_size/2), Vector(1, 0, 0))

# 4 furos de fixação nos cantos
for dx in [-fan_size/2 + 3.0, fan_size/2 - 3.0]:
    for dz in [3.0, fan_size - 3.0]:
        bolt_hole = Part.makeCylinder(1.0, fan_thick + 4.0, Vector(fan_x_pos - 2.0, dx, fan_z_pos + dz), Vector(1, 0, 0))
        fan_box = fan_box.cut(bolt_hole)

fan_assembly = fan_box.cut(fan_hole).fuse(fan_hub)

# Brackets de suporte acoplando a ventoinha ao radiador
bracket_top = Part.makeBox(5.0, 4.0, 2.5, Vector(-fin_outer_r - 2.0, -2.0, fan_z_pos + fan_size - 3.0))
bracket_bot = Part.makeBox(5.0, 4.0, 2.5, Vector(-fin_outer_r - 2.0, -2.0, fan_z_pos + 1.0))
fan_mounted = fan_assembly.fuse(bracket_top).fuse(bracket_bot)

z_current -= heatsink_height

# ------------------------------------------------------------------------------
# 5. DISCO / SENSOR PIEZOELÉTRICO NA EXTREMIDADE INFERIOR DO RADIADOR
# Mede a calibração dinâmica e o Z-offset direto no contato físico do bico
# ------------------------------------------------------------------------------
piezo_height = 2.5
piezo_outer_r = 9.0
piezo_disc = Part.makeCylinder(piezo_outer_r, piezo_height, Vector(0, 0, z_current - piezo_height), Vector(0, 0, 1))

# Fio / Conector de sinal piezoelétrico lateral
piezo_lead = Part.makeBox(4.0, 3.0, piezo_height, Vector(piezo_outer_r - 1.0, -1.5, z_current - piezo_height))
piezo_sensor = piezo_disc.fuse(piezo_lead)

z_current -= piezo_height

# ------------------------------------------------------------------------------
# 6. GARGALTA TÉRMICA (HEATBREAK BI-METÁLICO)
# Isolamento térmico de titânio entre o radiador frio e a zona quente
# ------------------------------------------------------------------------------
heatbreak_height = 6.0
heatbreak = Part.makeCylinder(2.6, heatbreak_height, Vector(0, 0, z_current - heatbreak_height), Vector(0, 0, 1))

z_current -= heatbreak_height

# ------------------------------------------------------------------------------
# 7. CILINDRO AQUECIDO POR INDUÇÃO + TERMOSTATO INTEGRADO
# Cilindro receptor de calor por correntes parasitas (indução eletromagnética)
# ------------------------------------------------------------------------------
inductor_cyl_height = 16.0
inductor_cyl_r = 6.8
heater_cyl = Part.makeCylinder(inductor_cyl_r, inductor_cyl_height, Vector(0, 0, z_current - inductor_cyl_height), Vector(0, 0, 1))

# Alojamento do termostato / sensor de temperatura embutido na parede do cilindro
thermostat_well = Part.makeCylinder(1.6, 12.0, Vector(3.8, 0, z_current - inductor_cyl_height + 2.0), Vector(0, 0, 1))

z_current -= inductor_cyl_height

# ------------------------------------------------------------------------------
# 8. ANEL / BORRACHA DE SILICONE PROTETORA ANTI-ADERENTE
# Cria o anel de vedação evitando que plástico e impurezas subam para o corpo
# ------------------------------------------------------------------------------
silicone_sock_h = 7.0
silicone_sock_outer_r = 7.8
silicone_sock = Part.makeCylinder(silicone_sock_outer_r, silicone_sock_h, Vector(0, 0, z_current - silicone_sock_h), Vector(0, 0, 1))

z_current -= silicone_sock_h

# ------------------------------------------------------------------------------
# 9. DIAMOND BAY & BICO INTEGRADO (NÃO REMOVÍVEL)
# Bico de precisão de diamante/carboneto montado na ponta com geometria chanfrada
# ------------------------------------------------------------------------------
# Base cônica do Diamond Bay
cone_height = 7.0
diamond_bay = Part.makeCone(6.0, 2.8, cone_height, Vector(0, 0, z_current - cone_height), Vector(0, 0, 1))

# Ponta final do bico de extrusão com saída de 0.4mm
nozzle_tip_h = 3.5
nozzle_tip = Part.makeCone(2.8, 0.8, nozzle_tip_h, Vector(0, 0, z_current - cone_height - nozzle_tip_h), Vector(0, 0, 1))

# Orifício de saída do filamento (0.4mm de diâmetro)
nozzle_orifice = Part.makeCylinder(0.2, 10.0, Vector(0, 0, z_current - cone_height - nozzle_tip_h - 1.0), Vector(0, 0, 1))

nozzle_unit = diamond_bay.fuse(nozzle_tip).cut(nozzle_orifice)

# ==============================================================================
# MONTAGEM FINAL E SUBTRAÇÃO DO CANAL DO FILAMENTO
# ==============================================================================
hotend_body = (
    top_entry
    .fuse(nfc_section)
    .fuse(heatsink_full)
    .fuse(heatbreak)
    .fuse(heater_cyl)
    .cut(thermostat_well)
    .fuse(diamond_bay)
    .fuse(nozzle_tip)
)

# Cortar o canal central contínuo de 2.1mm para o filamento descer até a ponta
hotend_body = hotend_body.cut(filament_channel).cut(nozzle_orifice)

# Adicionar componentes individuais com propriedades visuais e técnicas no FreeCAD
obj_hotend = doc.addObject("Part::Feature", "Bico_Monobloco_Indutivo")
obj_hotend.Shape = hotend_body

obj_fan = doc.addObject("Part::Feature", "MicroVentoinha_Lateral_Radiador")
obj_fan.Shape = fan_mounted

obj_piezo = doc.addObject("Part::Feature", "Sensor_Piezo_ZOffset_Dinamico")
obj_piezo.Shape = piezo_sensor

obj_silicone = doc.addObject("Part::Feature", "Anel_Silicone_Protetor_Bico")
obj_silicone.Shape = silicone_sock.cut(Part.makeCylinder(5.8, silicone_sock_h + 1.0, Vector(0, 0, z_current - 0.5), Vector(0, 0, 1)))

doc.recompute()

# Caminhos de exportação nas duas pastas (projeto e Documents/GEARS_CAD)
paths = [
    "/home/user/Documents/Antigravity/GEARS./cad",
    "/home/user/Documents/GEARS_CAD"
]

for p in paths:
    fcstd_file = f"{p}/GEARS_Bico_DiamondBay_Piezo.FCStd"
    step_file = f"{p}/GEARS_Bico_DiamondBay_Piezo.step"
    stl_hotend = f"{p}/Bico_Monobloco_Indutivo.stl"
    stl_fan = f"{p}/MicroVentoinha_Lateral.stl"
    stl_full = f"{p}/Conjunto_Completo_Bico_GEARS.stl"

    doc.saveAs(fcstd_file)
    Part.export([obj_hotend, obj_fan, obj_piezo, obj_silicone], step_file)
    hotend_body.exportStl(stl_hotend)
    fan_mounted.exportStl(stl_fan)
    
    assembly_full = hotend_body.fuse(fan_mounted).fuse(piezo_sensor).fuse(obj_silicone.Shape)
    assembly_full.exportStl(stl_full)
    print(f"Arquivos gerados em: {p}")

print("Modelagem do Bico GEARS. concluída com sucesso absoluto!")
