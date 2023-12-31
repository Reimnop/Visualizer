import bpy

class VISUALIZER_PT_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_label = 'Visualizer'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, 'v_audio_path', text='Audio')
        layout.prop(scene, 'v_object', text='Object')
        layout.prop(scene, 'v_fcurve_path', text='FCurve')
        layout.prop(scene, 'v_additional_object', text='Additional object')
        layout.prop(scene, 'v_additional_fcurve', text='Additional FCurve')
        layout.prop(scene, 'v_out_collection', text='Collection')
        layout.prop(scene, 'v_position', text='Position')

        box = layout.box()
        box.label(text='Generator settings')

        row = box.row()
        row.prop(scene, 'v_bar_count', text='Count')
        row.prop(scene, 'v_bar_spacing', text='Spacing')
        
        split = box.split()
        col = split.column(align=True)
        col.prop(scene, 'v_min_freq', text='Min freq')
        col.prop(scene, 'v_max_freq', text='Max freq')
        col.prop(scene, 'v_amplitude', text='Amplitude')

        col = split.column(align=True)
        col.prop(scene, 'v_attack', text='Attack')
        col.prop(scene, 'v_release', text='Release')
        col.prop(scene, 'v_height_offset', text='Offset')

        layout.operator('visualizer.clean_and_rebuild', icon='FILE_REFRESH')
        
        row = layout.row()
        row.operator('visualizer.build', icon='MOD_BUILD')
        row.operator('visualizer.clean', icon='TRASH')

def register():
    bpy.utils.register_class(VISUALIZER_PT_panel)

    bpy.types.Scene.v_audio_path = bpy.props.StringProperty(
        name="Audio path",
        description="Path of the audio file",
        subtype="FILE_PATH")
    bpy.types.Scene.v_object = bpy.props.PointerProperty(
        name="Object",
        description="Template object to use for the visualizer",
        type=bpy.types.Object)
    bpy.types.Scene.v_additional_object = bpy.props.PointerProperty(
        name="Additional object",
        description="(Optional) Additional object to bake the FCurve into",
        type=bpy.types.Object)
    bpy.types.Scene.v_fcurve_path = bpy.props.StringProperty(
        name="FCurve path",
        description="FCurve path to use for the visualizer (relative to template object)")
    bpy.types.Scene.v_additional_fcurve = bpy.props.StringProperty(
        name="Additional FCurve path",
        description="(Optional) Additional FCurve to bake into for other purposes")
    bpy.types.Scene.v_out_collection = bpy.props.PointerProperty(
        name="Output collection",
        description="Collection to copy the template objects of the visualizer into",
        type=bpy.types.Collection)
    bpy.types.Scene.v_position = bpy.props.FloatVectorProperty(
        name="Position",
        description="First object of the visualizer",
        default=(0, 0, 0))
    
    bpy.types.Scene.v_bar_count = bpy.props.IntProperty(
        name="Bar count",
        description="Number of bars in the visualizer",
        default=10,
        min=1)
    bpy.types.Scene.v_bar_spacing = bpy.props.FloatProperty(
        name="Bar spacing",
        description="Spacing between the bars",
        default=0.5)

    bpy.types.Scene.v_min_freq = bpy.props.FloatProperty(
        name="Min frequency",
        description="Minimum frequency to analyze",
        default=80)
    bpy.types.Scene.v_max_freq = bpy.props.FloatProperty(
        name="Max frequency",
        description="Maximum frequency to analyze",
        default=22050)

    bpy.types.Scene.v_attack = bpy.props.FloatProperty(
        name="Attack",
        description="Attack time of the visualizer",
        default=0.1)
    bpy.types.Scene.v_release = bpy.props.FloatProperty(
        name="Release",
        description="Release time of the visualizer",
        default=0.1)
    bpy.types.Scene.v_amplitude = bpy.props.FloatProperty(
        name="Amplitude",
        description="Amplitude of the visualizer",
        default=12)
    bpy.types.Scene.v_height_offset = bpy.props.FloatProperty(
        name="Height offset",
        description="Height offset of the visualizer",
        default=0.1)

def unregister():
    bpy.utils.unregister_class(VISUALIZER_PT_panel)
    del bpy.types.Scene.v_audio_path
    del bpy.types.Scene.v_object
    del bpy.types.Scene.v_fcurve_path
    del bpy.types.Scene.v_additional_object
    del bpy.types.Scene.v_additional_fcurve
    del bpy.types.Scene.v_bar_count
    del bpy.types.Scene.v_bar_spacing
    del bpy.types.Scene.v_min_freq
    del bpy.types.Scene.v_max_freq
    del bpy.types.Scene.v_attack
    del bpy.types.Scene.v_release
    del bpy.types.Scene.v_amplitude
    del bpy.types.Scene.v_height_offset