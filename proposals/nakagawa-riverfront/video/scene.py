# NAKAGAWA RIVER NIGHTS - teaser background scene (Blender 4.0, Cycles CPU)
# Usage: blender -b -P scene.py -- <out_dir> [start end] [res_pct]
import bpy, math, random, sys
argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "/tmp/frames/"
START = int(argv[1]) if len(argv) > 1 else 1
END = int(argv[2]) if len(argv) > 2 else 450
PCT = int(argv[3]) if len(argv) > 3 else 100
FPS, BEAT = 30, 15            # 120 BPM -> beat every 15 frames
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
sc.eevee.taa_render_samples = 12
sc.eevee.use_bloom = True
sc.eevee.bloom_threshold = 1.2
sc.eevee.bloom_intensity = 0.06
sc.eevee.bloom_radius = 5.5
sc.eevee.use_ssr = True
sc.eevee.use_gtao = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, PCT
sc.render.fps = FPS
sc.frame_start, sc.frame_end = START, END
sc.render.filepath = OUT
sc.render.image_settings.file_format = 'PNG'
sc.view_settings.view_transform = 'AgX' if 'AgX' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
sc.view_settings.exposure = -0.4
sc.view_settings.look = 'AgX - Medium High Contrast' if sc.view_settings.view_transform=='AgX' else 'None'

# world: deep indigo night
w = bpy.data.worlds.new("night"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.004, 0.006, 0.022, 1); bg.inputs[1].default_value = 0.6

def emit(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e

# water: dark glossy with gentle waves
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 60, 0))
water = bpy.context.object
mw = bpy.data.materials.new("water"); mw.use_nodes = True
nt = mw.node_tree; bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.002, 0.006, 0.012, 1)
bsdf.inputs["Roughness"].default_value = 0.06
bsdf.inputs["Metallic"].default_value = 0.0
tex = nt.nodes.new("ShaderNodeTexWave"); tex.inputs["Scale"].default_value = 0.6; tex.inputs["Distortion"].default_value = 6
tex.wave_type = 'BANDS'; tex.bands_direction = 'X'
bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.08
nt.links.new(tex.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
mapn = nt.nodes.new("ShaderNodeMapping"); tc = nt.nodes.new("ShaderNodeTexCoord")
nt.links.new(tc.outputs["Object"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], tex.inputs["Vector"])
mapn.inputs["Location"].default_value = (0, 0, 0); mapn.inputs["Location"].keyframe_insert("default_value", frame=1)
mapn.inputs["Location"].default_value = (0, 6, 0); mapn.inputs["Location"].keyframe_insert("default_value", frame=450)
water.data.materials.append(mw)

# riverbanks: city blocks with lit windows (two rows)
mb = bpy.data.materials.new("bld"); mb.use_nodes = True
mb.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.01, 0.012, 0.02, 1)
win_cols = [(1.0, 0.62, 0.25), (1.0, 0.8, 0.5), (0.25, 0.75, 0.9), (1.0, 0.35, 0.4)]
win_mats = [emit(f"win{i}", c, 3)[0] for i, c in enumerate(win_cols)]
for side in (-1, 1):
    y = 6
    while y < 230:
        h = random.uniform(8, 38); wdt = random.uniform(5, 10); d = random.uniform(6, 12)
        x = side * (22 + d/2 + random.uniform(0, 4))
        bpy.ops.mesh.primitive_cube_add(location=(x, y, h/2)); b = bpy.context.object
        b.scale = (d/2, wdt/2, h/2); b.data.materials.append(mb)
        # windows as thin emissive strips on river-facing face
        for k in range(int(h // 3)):
            if random.random() < 0.55:
                bpy.ops.mesh.primitive_plane_add(size=1, location=(x - side*(d/2+0.05), y + random.uniform(-wdt/3, wdt/3), 2 + k*3))
                p = bpy.context.object; p.rotation_euler = (0, math.pi/2, 0); p.scale = (0.9, random.uniform(0.6, 1.6), 1)
                p.data.materials.append(random.choice(win_mats))
        y += wdt + random.uniform(0.5, 2.5)

# promenade light strips along both banks (the riverside lighting)
strip_mat, strip_em = emit("strip", (1.0, 0.62, 0.25), 6)
for side in (-1, 1):
    bpy.ops.mesh.primitive_cube_add(location=(side*21.5, 115, 0.6)); s = bpy.context.object
    s.scale = (0.12, 115, 0.12); s.data.materials.append(strip_mat)

# bridges: arcs of light that pulse on the beat
bridge_mats = []
for i, by in enumerate([45, 95, 150, 205]):
    m, e = emit(f"bridge{i}", (0.23, 0.72, 0.85) if i % 2 else (1.0, 0.6, 0.25), 4)
    bridge_mats.append(e)
    curve = bpy.data.curves.new(f"arc{i}", 'CURVE'); curve.dimensions = '3D'; curve.bevel_depth = 0.18
    sp = curve.splines.new('POLY'); n = 32; sp.points.add(n-1)
    for j in range(n):
        t = j/(n-1); x = -24 + 48*t; z = 4 + 3.2*math.sin(math.pi*t)
        sp.points[j].co = (x, by, z, 1)
    ob = bpy.data.objects.new(f"arc{i}", curve); sc.collection.objects.link(ob); ob.data.materials.append(m)
    # deck line
    bpy.ops.mesh.primitive_cube_add(location=(0, by, 3.6)); dk = bpy.context.object
    dk.scale = (24, 0.9, 0.25); dk.data.materials.append(mb)
    # beat pulse: base 6, flash 30 on each beat with offset per bridge
    for f in range(1, 451):
        if (f - 1 - i*4) % BEAT == 0:
            e.inputs[1].default_value = 14; e.inputs[1].keyframe_insert("default_value", frame=f)
            e.inputs[1].default_value = 3;  e.inputs[1].keyframe_insert("default_value", frame=f+8)

# floating light orbs over the water (lanterns / bokeh)
orb_cols = [(1.0, 0.62, 0.25), (0.23, 0.72, 0.85), (1.0, 0.35, 0.45)]
orb_mats = [emit(f"orb{i}", c, 8)[0] for i, c in enumerate(orb_cols)]
for k in range(70):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=random.uniform(0.12, 0.3), segments=12, ring_count=8,
                                         location=(random.uniform(-17, 17), random.uniform(10, 220), random.uniform(1, 9)))
    o = bpy.context.object; o.data.materials.append(random.choice(orb_mats))
    z0 = o.location.z
    o.keyframe_insert("location", frame=1)
    o.location.z = z0 + random.uniform(2, 6); o.keyframe_insert("location", frame=450)

# a barge stage (water stage) glowing ahead
stage_mat, stage_em = emit("stage", (1.0, 0.35, 0.4), 6)
bpy.ops.mesh.primitive_cube_add(location=(0, 175, 0.5)); st = bpy.context.object
st.scale = (7, 4, 0.5); st.data.materials.append(mb)
bpy.ops.mesh.primitive_cube_add(location=(0, 175, 1.05)); stl = bpy.context.object
stl.scale = (7.1, 4.1, 0.06); stl.data.materials.append(stage_mat)
for f in range(1, 451):
    if (f-1) % BEAT == 0:
        stage_em.inputs[1].default_value = 22; stage_em.inputs[1].keyframe_insert("default_value", frame=f)
        stage_em.inputs[1].default_value = 5; stage_em.inputs[1].keyframe_insert("default_value", frame=f+10)

# sweeping stage beams (thin emissive cones, additive look)
beam_mat = bpy.data.materials.new("beam"); beam_mat.use_nodes = True; beam_mat.blend_method = 'BLEND'
bn = beam_mat.node_tree; bn.nodes.clear()
bo = bn.nodes.new("ShaderNodeOutputMaterial"); be = bn.nodes.new("ShaderNodeEmission"); bt = bn.nodes.new("ShaderNodeBsdfTransparent")
bmix = bn.nodes.new("ShaderNodeMixShader"); btc = bn.nodes.new("ShaderNodeTexCoord"); bsep = bn.nodes.new("ShaderNodeSeparateXYZ")
bmr = bn.nodes.new("ShaderNodeMapRange"); bmr.inputs["From Min"].default_value = 0.0; bmr.inputs["From Max"].default_value = 1.0
bmr.inputs["To Min"].default_value = 0.28; bmr.inputs["To Max"].default_value = 0.0
be.inputs[0].default_value = (0.55, 0.85, 1.0, 1); be.inputs[1].default_value = 1.2
bn.links.new(btc.outputs["Generated"], bsep.inputs[0]); bn.links.new(bsep.outputs["Z"], bmr.inputs["Value"])
bn.links.new(bmr.outputs["Result"], bmix.inputs[0]); bn.links.new(bt.outputs[0], bmix.inputs[1]); bn.links.new(be.outputs[0], bmix.inputs[2])
bn.links.new(bmix.outputs[0], bo.inputs[0])
for k, x in enumerate([-5, -1.7, 1.7, 5]):
    bpy.ops.mesh.primitive_cone_add(radius1=0.05, radius2=2.4, depth=40, location=(x, 175, 21))
    c = bpy.context.object; c.data.materials.append(beam_mat)
    for f, ang in [(1, -0.25), (120, 0.25), (240, -0.25), (360, 0.25), (450, 0.0)]:
        c.rotation_euler = (0, ang * (1 if k % 2 else -1), 0); c.keyframe_insert("rotation_euler", frame=f)

# camera: low glide up the river, slight rise, ends framing the barge stage
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 28
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt)
con = cam.constraints.new('TRACK_TO'); con.target = tgt; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'
for f, cl, tl in [(1, (6, -10, 2.2), (-2, 60, 4)), (150, (-3, 30, 3.0), (2, 110, 5)),
                  (300, (2, 80, 5.5), (0, 170, 3)), (450, (0, 128, 7.5), (0, 176, 3))]:
    cam.location = cl; cam.keyframe_insert("location", frame=f)
    tgt.location = tl; tgt.keyframe_insert("location", frame=f)
for obj in (cam, tgt):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'; kp.easing = 'EASE_IN_OUT'
cam_d.dof.use_dof = False
bpy.ops.render.render(animation=True)
