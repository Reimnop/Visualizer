import bpy

class VISUALIZER_OT_clean(bpy.types.Operator):
    bl_idname = 'visualizer.clean'
    bl_label = 'Clean'
    bl_description = 'Remove all visualizer objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        out_collection = scene.v_out_collection

        # remove all objects from output collection
        for obj in out_collection.objects:
            out_collection.objects.unlink(obj)
            bpy.data.objects.remove(obj)

        # remove audio strip
        if scene.sequence_editor:
            for sequence in scene.sequence_editor.sequences:
                if sequence.name == 'v_audio':
                    scene.sequence_editor.sequences.remove(sequence)
                    break
        
        # remove additional object fcurve
        additional_object = scene.v_additional_object
        additional_fcurve = scene.v_additional_fcurve
        if len(additional_fcurve) > 0 and additional_object is not None:
            # change to graph editor
            area = bpy.context.area.type
            bpy.context.area.type = 'GRAPH_EDITOR'
            
            # select additional_object
            additional_object.select_set(True)
            
            if additional_object.animation_data is not None and additional_object.animation_data.action is not None and additional_object.animation_data.action.fcurves is not None:
                for fcurve in additional_object.animation_data.action.fcurves:
                    if fcurve.data_path == additional_fcurve:
                        additional_object.animation_data.action.fcurves.remove(fcurve)
                        break
            
            # deselect it
            additional_object.select_set(False)
                    
            # restore context
            bpy.context.area.type = area

        return {'FINISHED'}

def register():
    bpy.utils.register_class(VISUALIZER_OT_clean)

def unregister():
    bpy.utils.unregister_class(VISUALIZER_OT_clean)