import bpy

class VISUALIZER_OT_clean_and_rebuild(bpy.types.Operator):
    bl_idname = 'visualizer.clean_and_rebuild'
    bl_label = 'Clean and Rebuild'
    bl_description = 'Clean and rebuild the visualizer'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.visualizer.clean()
        bpy.ops.visualizer.build()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VISUALIZER_OT_clean_and_rebuild)

def unregister():
    bpy.utils.unregister_class(VISUALIZER_OT_clean_and_rebuild)