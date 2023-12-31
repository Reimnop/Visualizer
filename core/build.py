import bpy
import math

def copy_object(object, collection):
    new_obj = object.copy()
    new_obj.data = object.data.copy()
    new_obj.animation_data_clear()
    collection.objects.link(new_obj)
    return new_obj

def get_frequency_bands(min_freq, max_freq, bar_count):
    exponent = math.log2(max_freq / min_freq) / bar_count
    base = math.pow(2, exponent)
    bands = []
    for i in range(bar_count):
        bands.append(min_freq * math.pow(base, i))
    bands.append(max_freq)
    return bands

class VISUALIZER_OT_build(bpy.types.Operator):
    bl_idname = 'visualizer.build'
    bl_label = 'Build'
    bl_description = 'Build the visualizer'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.frame_current = 1 # start at frame 1

        # get user config
        audio_path = bpy.path.abspath(scene.v_audio_path)
        object = scene.v_object
        fcurve_path = scene.v_fcurve_path
        additional_object = scene.v_additional_object
        additional_fcurve = scene.v_additional_fcurve
        out_collection = scene.v_out_collection
        position = scene.v_position
        bar_count = scene.v_bar_count
        bar_spacing = scene.v_bar_spacing
        min_freq = scene.v_min_freq
        max_freq = scene.v_max_freq
        attack = scene.v_attack
        release = scene.v_release
        amplitude = scene.v_amplitude
        height_offset = scene.v_height_offset

        # add audio strip to scene
        scene.sequence_editor_create()
        sequence = scene.sequence_editor.sequences.new_sound(name='v_audio', filepath=audio_path, channel=1, frame_start=1)
        end_frame = sequence.frame_final_end

        # set scene length
        scene.frame_start = 1
        scene.frame_end = end_frame - 1

        # show progress bar
        should_bake_additional_fcurve = len(additional_fcurve) > 0 and additional_object is not None
        total_progress = bar_count + (1 if should_bake_additional_fcurve else 0)
        
        window_manager = context.window_manager
        window_manager.progress_begin(0, total_progress)
        
        # bake additional fcurve
        if should_bake_additional_fcurve:
            # select additional object
            additional_object.select_set(True)
            
            # change to graph editor
            area = bpy.context.area.type # cache old context are to restore later on
            bpy.context.area.type = 'GRAPH_EDITOR'
        
            # add fcurve
            additional_object.animation_data_create()
            additional_object.animation_data.action = bpy.data.actions.new(name=additional_object.name)
            fcurve = additional_object.animation_data.action.fcurves.new(data_path=additional_fcurve)
            
            # select fcurve
            fcurve.select = True
            
            # bake fcurves with audio data
            print(f"Baking additional object fcurve with frequency response range {min_freq} -> {max_freq}")
            bpy.ops.graph.sound_to_samples(filepath=audio_path, low=min_freq, high=max_freq, attack=attack, release=release)
            
            # reset area
            bpy.context.area.type = area
            
            # deselect additional object
            additional_object.select_set(False)
            
            # update progess
            total_progress += 1
            window_manager.progress_update(total_progress)

        # create bars
        bands = get_frequency_bands(min_freq, max_freq, bar_count)

        for i in range(bar_count):
            # use the object from the user config
            bar = copy_object(object, out_collection)
            bar.name = f'Bar {i}'
            bar.location = (i * bar_spacing + position[0], position[1], position[2])

            bar.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            # add fcurve
            bar.animation_data_create()
            bar.animation_data.action = bpy.data.actions.new(name=f'Bar {i}')
            fcurve = bar.animation_data.action.fcurves.new(data_path=fcurve_path)

            # select fcurve
            fcurve.select = True

            # change to graph editor
            area = bpy.context.area.type
            bpy.context.area.type = 'GRAPH_EDITOR'

            # bake fcurves with audio data
            print(f"Baking bar {i} with frequency response range {bands[i]} -> {bands[i + 1]}")
            bpy.ops.graph.sound_to_samples(filepath=audio_path, low=bands[i], high=bands[i + 1], attack=attack, release=release)

            # apply amplitude and height offset
            for keyframe in fcurve.sampled_points:
                keyframe.co[1] *= amplitude
                keyframe.co[1] = max(keyframe.co[1] + height_offset, 0.0)

            # restore
            bpy.context.area.type = area
            bar.select_set(False)

            # update progress bar
            total_progress += 1
            window_manager.progress_update(total_progress)

        # end progress bar
        window_manager.progress_end()
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VISUALIZER_OT_build)

def unregister():
    bpy.utils.unregister_class(VISUALIZER_OT_build)