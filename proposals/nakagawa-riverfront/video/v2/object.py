# Abstract 3D element: a glossy ring (bridge / stage / ripple as one form), transparent background.
# Usage: blender -b -P object.py -- <out_prefix> [start end]
import bpy, math, sys
argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "/tmp/obj_"; S = int(argv[1]) if len(argv) > 1 else 1; E = int(argv[2]) if len(argv) > 2 else 450
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 8
sc.eevee.use_bloom = True; sc.eevee.bloom_intensity = 0.04; sc.eevee.use_ssr = True
sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = 760
sc.render.fps = 30; sc.frame_start, sc.frame_end = S, E
sc.render.filepath = OUT; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'AgX'
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.03, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.3
# ring = torus, slightly squashed like an arch reflected in water
bpy.ops.mesh.primitive_torus_add(major_radius=1.6, minor_radius=0.22, major_segments=160, minor_segments=40)
ring = bpy.context.object; bpy.ops.object.shade_smooth()
m = bpy.data.materials.new("chrome"); m.use_nodes = True
p = m.node_tree.nodes["Principled BSDF"]
p.inputs["Base Color"].default_value = (0.9, 0.92, 0.95, 1); p.inputs["Metallic"].default_value = 1.0; p.inputs["Roughness"].default_value = 0.12
ring.data.materials.append(m)
# inner thin emissive ring (the "light-up")
bpy.ops.mesh.primitive_torus_add(major_radius=1.95, minor_radius=0.012, major_segments=160, minor_segments=12)
glow = bpy.context.object
gm = bpy.data.materials.new("glow"); gm.use_nodes = True; nt = gm.node_tree; nt.nodes.clear()
o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission")
e.inputs[0].default_value = (1.0, 0.62, 0.25, 1); e.inputs[1].default_value = 6
nt.links.new(e.outputs[0], o.inputs[0]); glow.data.materials.append(gm)
glow.parent = ring
# colored area lights -> teal / coral / amber reflections on chrome
for loc, col, en in [((-4, -2, 3), (0.23, 0.72, 0.85), 900), ((4, -2, -1), (1.0, 0.35, 0.4), 700), ((0, -4, -3), (1.0, 0.6, 0.25), 500), ((0, 3, 4), (0.6, 0.7, 1.0), 300)]:
    ld = bpy.data.lights.new("l", 'AREA'); ld.size = 3; ld.color = col; ld.energy = en
    lo = bpy.data.objects.new("l", ld); lo.location = loc; sc.collection.objects.link(lo)
    c = lo.constraints.new('TRACK_TO'); c.target = ring; c.track_axis = 'TRACK_NEGATIVE_Z'
# animation: slow turn + tilt, beat breathing (120 BPM = 15 frames)
for f in range(S, E + 1, 1):
    t = (f - 1) / 30
    ring.rotation_euler = (math.radians(70 + 12 * math.sin(t * 0.8)), math.radians(18 * math.sin(t * 0.5)), math.radians(t * 24))
    ring.keyframe_insert("rotation_euler", frame=f)
    ph = ((f - 1) % 15) / 15
    s = 1.0 + 0.05 * math.exp(-ph * 6)
    ring.scale = (s, s, s); ring.keyframe_insert("scale", frame=f)
    e.inputs[1].default_value = 4 + 14 * math.exp(-ph * 5); e.inputs[1].keyframe_insert("default_value", frame=f)
cam_d = bpy.data.cameras.new("c"); cam_d.lens = 60
cam = bpy.data.objects.new("c", cam_d); cam.location = (0, -9.5, 0); cam.rotation_euler = (math.radians(90), 0, 0)
sc.collection.objects.link(cam); sc.camera = cam
bpy.ops.render.render(animation=True)
