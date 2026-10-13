"""3D試作：『東口の改札を出て、時計の下』の静止画（Blender / Cycles）。

おもちゃのジオラマ風。形はすべてこのスクリプトで作るオリジナルの簡略形で、
特定の駅・機種の再現ではない。

使い方: python scene_still.py [出力PNG] [サンプル数]
  （pip install bpy した Python で実行。bpy 5.2.2 で確認）
"""
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "NotoSansJP-Bold.otf")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "out", "3d-still-east-exit.png")
SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 128

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
font = bpy.data.fonts.load(FONT)
NOLINE = bpy.data.collections.new("NoLine")  # 輪郭線を描かないもの（文字・壁）
scene.collection.children.link(NOLINE)


# ---------------------------------------------------------------------------
# 材質
# ---------------------------------------------------------------------------
def hexcol(h, a=1.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]  # sRGB → linear
    return (*c, a)


_mats = {}


def mat(name, color, rough=0.55, emit=0.0, metal=0.0, coat=0.0):
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexcol(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = hexcol(color)
        b.inputs["Emission Strength"].default_value = emit
    _mats[name] = m
    return m


def tile_mat():
    """広場の石畳（ゆるい格子）。"""
    m = bpy.data.materials.new("tiles")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.8
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 0.9
    br.inputs["Mortar Size"].default_value = 0.012
    br.inputs["Color1"].default_value = hexcol("#D9CDB6")
    br.inputs["Color2"].default_value = hexcol("#CFC1A7")
    br.inputs["Mortar"].default_value = hexcol("#B9AA8E")
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return m


# ---------------------------------------------------------------------------
# 形
# ---------------------------------------------------------------------------
def finish(o, m, bevel=0.0, segs=3, smooth=True):
    o.data.materials.append(m)
    if bevel:
        bv = o.modifiers.new("bevel", "BEVEL")
        bv.width = bevel
        bv.segments = segs
        bv.limit_method = "ANGLE"
    if smooth:
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.shade_auto_smooth()
    return o


def box(name, loc, size, m, bevel=0.03, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    return finish(o, m, bevel)


def cyl(name, loc, r, depth, m, rot=(0, 0, 0), bevel=0.01, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    return finish(o, m, bevel)


def sphere(name, loc, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(m)
    return o


def capsule(name, p0, p1, r, m):
    """p0→p1 を結ぶ丸い棒（腕・脚）。"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    c = cyl(name, (p0 + p1) / 2, r, d.length, m, bevel=0, verts=24)
    c.rotation_mode = "QUATERNION"
    c.rotation_quaternion = d.to_track_quat("Z", "Y")
    return [c, sphere(name + "_a", p0, r, m), sphere(name + "_b", p1, r, m)]


def text(body, loc, size, m, rot=(math.radians(90), 0, 0), align="CENTER", extrude=0.004):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object
    for col in list(o.users_collection):
        col.objects.unlink(o)
    NOLINE.objects.link(o)
    o.data.body = body
    o.data.font = font
    o.data.size = size
    o.data.align_x = align
    o.data.align_y = "CENTER"
    o.data.extrude = extrude
    o.data.materials.append(m)
    return o


def parent(children, name, loc=(0, 0, 0), rot_z=0.0, lean=0.0):
    e = bpy.data.objects.new(name, None)
    scene.collection.objects.link(e)
    for c in children:
        c.parent = e
    e.location = loc
    e.rotation_mode = "ZXY"
    e.rotation_euler = (lean, 0, rot_z)
    return e


# ---------------------------------------------------------------------------
# 人物（おもちゃの人形風）。ローカル座標で作り、最後に置く
# ---------------------------------------------------------------------------
SKIN = mat("skin", "#F3D2B5", 0.5)
HAIR = mat("hair", "#2A2522", 0.45)
EYE = mat("eye", "#1E1B19", 0.2)
PANTS = mat("pants", "#3E4A63", 0.6)
SHOE = mat("shoe", "#3A302A", 0.5)


def person(name, shirt, pose="stand", hair="bob", loc=(0, 0, 0), rot_z=0.0, look=0.0, bag=None, lean=0.0):
    s = mat("shirt_" + name, shirt, 0.6)
    parts = []
    run = pose == "run"
    # 脚
    if run:
        parts += [*capsule(name + "_legL", (-0.09, 0.0, 0.78), (-0.12, 0.36, 0.30), 0.075, PANTS),
                  *capsule(name + "_legR", (0.09, 0.0, 0.78), (0.11, -0.30, 0.12), 0.075, PANTS)]
        parts += [sphere(name + "_shoeL", (-0.12, 0.42, 0.26), 0.1, SHOE, (0.9, 1.4, 0.7)),
                  sphere(name + "_shoeR", (0.11, -0.36, 0.08), 0.1, SHOE, (0.9, 1.4, 0.7))]
    else:
        parts += [*capsule(name + "_legL", (-0.1, 0, 0.78), (-0.11, 0, 0.12), 0.078, PANTS),
                  *capsule(name + "_legR", (0.1, 0, 0.78), (0.11, 0, 0.12), 0.078, PANTS)]
        parts += [sphere(name + "_shoeL", (-0.11, -0.06, 0.07), 0.1, SHOE, (0.95, 1.5, 0.7)),
                  sphere(name + "_shoeR", (0.11, -0.06, 0.07), 0.1, SHOE, (0.95, 1.5, 0.7))]
    # 胴（丸みのある円柱）
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.62, location=(0, 0, 1.08), vertices=48)
    torso = bpy.context.object
    torso.name = name + "_torso"
    torso.scale = (1.0, 0.72, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    finish(torso, s, bevel=0.09, segs=5)
    parts.append(torso)
    # 腕
    if run:
        parts += [*capsule(name + "_armL", (-0.24, 0, 1.32), (-0.32, -0.26, 1.14), 0.06, s),
                  *capsule(name + "_armR", (0.24, 0, 1.32), (0.33, 0.24, 1.04), 0.06, s)]
        parts += [sphere(name + "_handL", (-0.32, -0.30, 1.12), 0.065, SKIN),
                  sphere(name + "_handR", (0.33, 0.27, 1.0), 0.065, SKIN)]
        # 汗のしずく
        parts.append(sphere(name + "_sweat", (0.24, -0.05, 1.86), 0.04, mat("sweat", "#8FD3F5", 0.05), (0.8, 0.8, 1.3)))
    else:
        # 左手首を前に出して腕時計を見る
        parts += [*capsule(name + "_armL", (-0.24, 0, 1.32), (-0.30, -0.06, 1.04), 0.06, s),
                  *capsule(name + "_armL2", (-0.30, -0.06, 1.04), (-0.12, -0.30, 1.16), 0.055, s),
                  *capsule(name + "_armR", (0.24, 0, 1.32), (0.29, 0.0, 0.94), 0.06, s)]
        parts += [sphere(name + "_handL", (-0.09, -0.33, 1.17), 0.062, SKIN),
                  sphere(name + "_handR", (0.29, 0.0, 0.88), 0.065, SKIN)]
        parts.append(cyl(name + "_watch", (-0.15, -0.28, 1.15), 0.045, 0.03, mat("watch", "#E9E4D8", 0.3, metal=0.2),
                         rot=(math.radians(60), 0, math.radians(-40)), verts=24))
    # 首と頭
    parts.append(cyl(name + "_neck", (0, 0, 1.44), 0.07, 0.1, SKIN, bevel=0, verts=24))
    hz = 1.66
    head = sphere(name + "_head", (0, 0, hz), 0.2, SKIN, (1, 0.96, 1.04))
    parts.append(head)
    # 髪
    if hair == "bob":
        h = sphere(name + "_hair", (0, 0.02, hz + 0.04), 0.215, HAIR, (1.07, 1.05, 0.98))
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        for v in h.data.vertices:  # 顔の前側を切り抜く
            v.select = v.co.y < -0.06 and v.co.z < 0.05
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.delete(type="VERT")
        bpy.ops.object.mode_set(mode="OBJECT")
        parts.append(h)
    else:
        h = sphere(name + "_hair", (0, 0.03, hz + 0.07), 0.205, HAIR, (1.03, 1.03, 0.8))
        parts.append(h)
    # 目と口（look で視線を横へ）
    for sx in (-0.07, 0.07):
        parts.append(sphere(name + "_eye%+.2f" % sx, (sx + look * 0.04, -0.188, hz + 0.0), 0.024, EYE, (1, 0.6, 1.25)))
    parts.append(sphere(name + "_cheekL", (-0.11 + look * 0.03, -0.165, hz - 0.06), 0.028, mat("cheek", "#F2A7A0", 0.6), (1, 0.4, 0.7)))
    parts.append(sphere(name + "_cheekR", (0.11 + look * 0.03, -0.165, hz - 0.06), 0.028, mat("cheek", "#F2A7A0", 0.6), (1, 0.4, 0.7)))
    parts.append(sphere(name + "_mouth", (look * 0.04, -0.192, hz - 0.085), 0.022, mat("mouth", "#9C4A3E", 0.5), (1.3, 0.5, 0.55)))
    if bag:
        parts.append(box(name + "_bag", (0.3, 0.05, 0.98), (0.08, 0.26, 0.3), mat("bag_" + name, bag, 0.6), bevel=0.03))
        parts += capsule(name + "_strap", (0.22, 0.0, 1.38), (0.31, 0.05, 1.12), 0.015, mat("bag_" + name, bag, 0.6))
    return parent(parts, name, loc, rot_z, lean)


# ---------------------------------------------------------------------------
# 場面：駅の東口
# ---------------------------------------------------------------------------
WALL = mat("wall", "#F1E9DA", 0.7)
WALL2 = mat("wall2", "#E3D7C2", 0.7)
NAVY = mat("navy", "#2F4E73", 0.45)
ROOF = mat("roof", "#5B7FA6", 0.5)
WHITE = mat("white", "#FBF8F1", 0.35)
INKM = mat("ink", "#2A2A2A", 0.4)
RED = mat("red", "#D9483A", 0.45)
YEL = mat("yellow", "#F2C14E", 0.4)
GATE = mat("gate", "#D3D9E2", 0.35, metal=0.1)
BOARD = mat("board", "#2E4A3B", 0.85)
WOOD = mat("wood", "#9B6B43", 0.6)
CHALK = mat("chalk", "#F4F1E6", 0.9)
GREEN = mat("phone", "#5FA874", 0.35, coat=0.3)
GLASS = mat("warmglow", "#F7C98A", 0.5, emit=0.9)
POLE = mat("pole", "#4A4F57", 0.35, metal=0.6)
LEAF = mat("leaf", "#6E9E5B", 0.7)
POT = mat("pot", "#C9734E", 0.6)

# 地面
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, -6, 0))
ground = bpy.context.object
ground.data.materials.append(tile_mat())

# 駅舎（正面の壁に出口の開口）
FY = 4.0  # 正面の y
for w in (box("wall_left", (-12.45, FY + 0.6, 2.4), (19.1, 1.2, 4.8), WALL),
          box("wall_right", (4.6, FY + 0.6, 2.4), (9.0, 1.2, 4.8), WALL),
          box("wall_top", (-1.6, FY + 0.6, 4.2), (2.8, 1.2, 1.2), WALL)):
    for col in list(w.users_collection):
        col.objects.unlink(w)
    NOLINE.objects.link(w)
box("base_band", (0, FY - 0.02, 0.25), (20, 0.1, 0.5), WALL2, bevel=0.01)
box("inner_floor", (-1.6, FY + 3.0, 0.02), (6, 6, 0.04), mat("innerfloor", "#E8DFCF", 0.6), bevel=0)
box("inner_back", (-1.6, FY + 5.5, 2.4), (6, 0.3, 4.8), mat("innerwall", "#F6E7CC", 0.8, emit=0.35), bevel=0)
for x in (-4.5, 1.3):
    box("inner_side", (x, FY + 3.0, 2.4), (0.2, 5.2, 4.8), mat("innerwall", "#F6E7CC", 0.8, emit=0.35), bevel=0)
box("inner_ceiling", (-1.6, FY + 3.0, 4.6), (6, 5.2, 0.2), mat("innerceil", "#EFE4D0", 0.8), bevel=0)
for i in range(3):
    box("ceil_light%d" % i, (-1.6, FY + 1.5 + i * 1.4, 4.48), (2.4, 0.18, 0.04), GLASS, bevel=0)
# 左右に続く町並み（遠景）
for i, (x, y, w, h, c) in enumerate(((-14, 9, 6, 7, "#E9D9C3"), (-19, 12, 5, 10, "#D8C9B4"),
                                     (15, 9, 6, 8, "#E4D3BC"), (20, 12, 6, 11, "#D2C3AF"))):
    box("bldg%d" % i, (x, y, h / 2), (w, 4, h), mat("bldg%d" % i, c, 0.85), bevel=0.05)
for i, x in enumerate((-11.5, 11.0)):
    cyl("trunk%d" % i, (x, 3.6, 1.0), 0.14, 2.0, WOOD)
    sphere("crown%d" % i, (x, 3.6, 2.7), 1.25, LEAF, (1, 1, 1.15))
box("roof_slab", (-6.0, FY + 0.6, 4.95), (32.4, 2.0, 0.35), ROOF, bevel=0.06)
# 庇（ひさし）
box("canopy", (-1.6, FY - 0.8, 3.15), (4.4, 1.8, 0.16), ROOF, bevel=0.05)
for x in (-3.5, 0.3):
    cyl("canopy_post", (x, FY - 1.55, 1.55), 0.06, 3.1, POLE)
# 窓（温かい光）
for i, x in enumerate((2.6, 4.6, 6.6)):
    box("win%d" % i, (x, FY - 0.03, 2.2), (1.4, 0.08, 1.7), GLASS, bevel=0.02)
    box("winframe%d" % i, (x, FY - 0.05, 2.2), (1.55, 0.04, 1.85), WHITE, bevel=0.01)
    box("winbar%d" % i, (x, FY - 0.09, 2.2), (0.05, 0.03, 1.7), WHITE, bevel=0)
    box("winbarh%d" % i, (x, FY - 0.09, 2.45), (1.4, 0.03, 0.05), WHITE, bevel=0)
for i, x in enumerate((-8.0, -6.0)):
    box("winL%d" % i, (x, FY - 0.03, 2.2), (1.4, 0.08, 1.7), GLASS, bevel=0.02)
    box("winLframe%d" % i, (x, FY - 0.05, 2.2), (1.55, 0.04, 1.85), WHITE, bevel=0.01)
    box("winLbar%d" % i, (x, FY - 0.09, 2.2), (0.05, 0.03, 1.7), WHITE, bevel=0)
    box("winLbarh%d" % i, (x, FY - 0.09, 2.45), (1.4, 0.03, 0.05), WHITE, bevel=0)

# 「東口」の看板
box("sign_east", (-1.6, FY - 0.1, 3.95), (2.3, 0.12, 0.72), NAVY, bevel=0.03)
text("東口", (-1.6, FY - 0.17, 3.95), 0.48, WHITE)
# 駅名板（架空の駅名ではなく「駅」だけ）
# 壁のポスター（色だけの図案。文字なし）
for i, (x, c1, c2) in enumerate(((-10.0, "#F2C14E", "#D9483A"), (0.95, "#8FC1E3", "#F2C14E"))):
    box("poster%d" % i, (x, FY - 0.04, 2.05), (0.9, 0.04, 1.25), mat("poster%d" % i, c1, 0.5), bevel=0.01)
    sphere("poster_dot%d" % i, (x, FY - 0.07, 2.2), 0.26, mat("posterdot%d" % i, c2, 0.5), (1, 0.15, 1))

# 改札（開口の奥）
for i in range(4):
    gx = -3.2 + i * 1.05
    box("gate%d" % i, (gx, FY + 1.6, 0.5), (0.32, 1.1, 1.0), GATE, bevel=0.05)
    box("gate_slot%d" % i, (gx, FY + 1.05, 0.92), (0.2, 0.06, 0.08), YEL, bevel=0.01)
box("gate_sign", (-1.6, FY + 1.6, 2.6), (2.0, 0.1, 0.45), NAVY, bevel=0.03)
text("改札", (-1.6, FY + 1.54, 2.6), 0.3, WHITE)

# 伝言板（改札横）
BX, BY = -4.6, 3.35
box("board_frame", (BX, BY, 1.55), (2.3, 0.1, 1.35), WOOD, bevel=0.03)
box("board", (BX, BY - 0.055, 1.55), (2.12, 0.02, 1.17), BOARD, bevel=0.0)
box("board_tray", (BX, BY - 0.12, 0.9), (2.2, 0.14, 0.05), WOOD, bevel=0.01)
for x in (-1.05, 1.05):
    box("board_leg", (BX + x, BY, 0.5), (0.08, 0.08, 1.0), WOOD, bevel=0.01)
box("board_label", (BX, BY - 0.02, 2.38), (1.0, 0.06, 0.32), WHITE, bevel=0.02)
text("伝言板", (BX, BY - 0.06, 2.38), 0.2, INKM)
text("東口で待っています", (BX - 0.95, BY - 0.075, 1.8), 0.23, CHALK, align="LEFT", extrude=0.001)
text("先に喫茶店へ行きます", (BX - 0.95, BY - 0.075, 1.36), 0.2, CHALK, align="LEFT", extrude=0.001)
box("chalk_piece", (BX + 0.6, BY - 0.15, 0.935), (0.12, 0.03, 0.03), CHALK, bevel=0.01)

# 公衆電話（簡略形・壁ぎわ）
PX, PY = 6.0, 3.45
box("phone_stand", (PX, PY, 0.5), (0.7, 0.55, 1.0), WALL2, bevel=0.04)
box("phone_body", (PX, PY - 0.02, 1.33), (0.52, 0.36, 0.66), GREEN, bevel=0.06)
box("phone_handset", (PX - 0.3, PY - 0.08, 1.38), (0.1, 0.14, 0.5), GREEN, bevel=0.04)
box("phone_window", (PX + 0.04, PY - 0.21, 1.53), (0.3, 0.02, 0.1), WHITE, bevel=0.01)
box("phone_hood", (PX, PY - 0.05, 1.92), (0.86, 0.6, 0.06), mat("hood", "#E7E1D5", 0.4), bevel=0.02)

# 時計の柱（約束の場所）
CX, CY = 1.2, 1.1
cyl("clock_base", (CX, CY, 0.06), 0.32, 0.12, POLE)
cyl("clock_pole", (CX, CY, 1.6), 0.07, 3.2, POLE)
CZ = 3.42
cyl("clock_rim", (CX, CY, CZ), 0.44, 0.16, POLE, rot=(math.radians(90), 0, 0), bevel=0.02, verts=64)
cyl("clock_face", (CX, CY - 0.085, CZ), 0.39, 0.02, WHITE, rot=(math.radians(90), 0, 0), bevel=0, verts=64)
for i in range(12):
    a = i / 12 * 2 * math.pi
    r = 0.33
    big = i % 3 == 0
    box("tick%d" % i, (CX + math.sin(a) * r, CY - 0.1, CZ + math.cos(a) * r),
        (0.03 if big else 0.018, 0.01, 0.08 if big else 0.05), INKM, bevel=0, rot=(0, a, 0))
# 2時20分
for nm, ang, L, w in (("hour", (2 + 20 / 60) / 12 * 2 * math.pi, 0.2, 0.035),
                      ("minute", 20 / 60 * 2 * math.pi, 0.3, 0.022)):
    box("hand_" + nm, (CX + math.sin(ang) * L / 2, CY - 0.11, CZ + math.cos(ang) * L / 2), (w, 0.01, L), INKM,
        bevel=0, rot=(0, ang, 0))
cyl("clock_pin", (CX, CY - 0.12, CZ), 0.025, 0.02, RED, rot=(math.radians(90), 0, 0), bevel=0)

# 植木とベンチ
for x in (-7.2, 8.4):
    cyl("pot", (x, 2.6, 0.3), 0.38, 0.6, POT, bevel=0.03)
    sphere("bush", (x, 2.6, 0.95), 0.55, LEAF, (1, 1, 0.9))
box("bench_seat", (3.8, 2.4, 0.45), (1.8, 0.45, 0.08), WOOD, bevel=0.02)
for x in (3.1, 4.5):
    box("bench_leg", (x, 2.4, 0.22), (0.08, 0.4, 0.44), POLE, bevel=0.01)

# 人物
person("waiter", "#3FA66B", "stand", "bob", loc=(1.75, 0.75, 0), rot_z=math.radians(-28), look=-0.6, bag="#C96E3B")
person("late", "#E07B39", "run", "short", loc=(-1.9, 3.1, 0.0), rot_z=math.radians(52), lean=math.radians(12))
# 鳩
for i, (x, y, r) in enumerate(((-0.6, -1.4, 30), (-1.15, -1.05, -70))):
    b1 = sphere("pigeon_body%d" % i, (0, 0, 0.13), 0.13, mat("pigeon", "#8C93A3", 0.6), (0.8, 1.3, 0.8))
    b2 = sphere("pigeon_head%d" % i, (0, -0.17, 0.27), 0.07, mat("pigeon", "#8C93A3", 0.6))
    b3 = sphere("pigeon_neck%d" % i, (0, -0.12, 0.2), 0.06, mat("pigeon_neck", "#6E8F86", 0.4))
    b4 = sphere("pigeon_beak%d" % i, (0, -0.24, 0.26), 0.022, mat("beak", "#E2A64B", 0.5), (0.8, 1.6, 0.8))
    b5 = sphere("pigeon_tail%d" % i, (0, 0.2, 0.15), 0.07, mat("pigeon", "#8C93A3", 0.6), (0.7, 1.4, 0.4))
    parent([b1, b2, b3, b4, b5], "pigeon%d" % i, (x, y, 0), math.radians(r))

# ---------------------------------------------------------------------------
# 光とカメラ
# ---------------------------------------------------------------------------
world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
wn = world.node_tree.nodes
sky = wn.new("ShaderNodeTexSky")
try:
    sky.sky_type = "MULTIPLE_SCATTERING"
except TypeError:
    sky.sky_type = "NISHITA"
sky.sun_elevation = math.radians(7)
sky.sun_rotation = math.radians(-125)
world.node_tree.links.new(sky.outputs["Color"], wn["Background"].inputs["Color"])
wn["Background"].inputs["Strength"].default_value = 0.14

bpy.ops.object.light_add(type="SUN", rotation=(math.radians(72), 0, math.radians(-128)))
sun = bpy.context.object
sun.data.energy = 3.0
sun.data.color = (1.0, 0.76, 0.52)
sun.data.angle = math.radians(3)

bpy.ops.object.light_add(type="AREA", location=(-3, -8, 6))
fill = bpy.context.object
fill.data.energy = 450
fill.data.size = 8
fill.data.color = (0.82, 0.88, 1.0)
fill.rotation_euler = (Vector((0.5, 2.5, 1.5)) - fill.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(4.9, -6.6, 1.35))
cam = bpy.context.object
scene.camera = cam
target = Vector((-0.7, 2.0, 2.05))
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.lens = 30
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = (Vector((1.75, 0.75, 1.4)) - cam.location).length
cam.data.dof.aperture_fstop = 2.8

# ---------------------------------------------------------------------------
# 描画設定
# ---------------------------------------------------------------------------
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Punchy"
scene.view_settings.exposure = -0.35
# 線画チャンネルらしさを残すため、薄い輪郭線（Freestyle）
scene.render.use_freestyle = True
scene.render.line_thickness_mode = "ABSOLUTE"
scene.render.line_thickness = 1.3
fs = bpy.context.view_layer.freestyle_settings
ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("lines")
if ls.linestyle is None:
    ls.linestyle = bpy.data.linestyles.new("lines")
ls.linestyle.color = (0.16, 0.15, 0.14)
ls.linestyle.alpha = 0.55
ls.select_by_visibility = True
ls.select_by_collection = True
ls.collection = NOLINE
ls.collection_negation = "EXCLUSIVE"
ls.select_crease = False
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("->", OUT)
