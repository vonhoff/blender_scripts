import time

import bpy
import os
import math

# SETTINGS
RESOLUTION_X = 256
RESOLUTION_Y = 256
FRAME_STEP = 2
SEGMENTS = 8
ACTIONS = ['idle', 'run', 'dying']
OUTPUT_FOLDER = os.path.abspath('C:\\tmp\\Mutant')


def get_angle_values(segments):
    angle_values = []
    for i in range(segments):
        angle_rad = (2 * math.pi / segments) * i
        angle_deg = math.degrees(angle_rad)
        angle_values.append(angle_deg)

    return angle_values


def render_models_from_multiple_angles(path):
    # Ensure output folder exists
    os.makedirs(path, exist_ok=True)

    # Save current selection and deselect all objects
    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        print("\n")
        print("ERROR: No objects selected. Please select an armature before running this script.")
        time.sleep(4)
        return False
    bpy.ops.object.select_all(action='DESELECT')

    # Set render settings
    scene = bpy.context.scene
    scene.render.resolution_x = RESOLUTION_X
    scene.render.resolution_y = RESOLUTION_Y

    # Get the angle values
    angle_values = get_angle_values(SEGMENTS)

    for obj in selected_objects:
        bpy.context.scene.objects[obj.name].select_set(True)

        for action in bpy.data.actions:
            if action.name not in ACTIONS:
                continue

            # Set current action and determine last frame
            bpy.context.object.animation_data.action = action
            last_frame = int(action.frame_range[1])

            # Create folder for action
            action_folder = os.path.join(path, action.name)
            os.makedirs(action_folder, exist_ok=True)

            for i, angle in enumerate(angle_values):
                # Create folder for angle
                angle_folder = os.path.join(action_folder, str(angle))
                os.makedirs(angle_folder, exist_ok=True)

                # Set rotation for the new angle
                obj.rotation_euler[2] = math.radians(-angle)

                # Calculate percentage of angles processed
                angles_processed_percent = (i + 1) / len(angle_values) * 100

                frames = range(scene.frame_start, last_frame, FRAME_STEP)

                # Loop through and render frames
                for j, frame in enumerate(frames):
                    scene.frame_set(frame)

                    # Calculate percentage of frames rendered
                    frames_rendered_percent = (j + 1) / len(frames) * 100

                    # Set filepath for rendered image
                    filepath = os.path.join(angle_folder, f"{action.name}_{frame:03d}.png")
                    scene.render.filepath = filepath

                    # Render the image
                    print(
                        f"Rendering {action.name} at {angle} degrees ({angles_processed_percent:.2f}% of angles, "
                        f"{frames_rendered_percent:.2f}% of frames), frame {scene.frame_current}")
                    bpy.ops.render.render(False, animation=False, write_still=True)

        # Deselect the object after rendering is complete
        obj.select_set(False)

    # Restore original selection
    for obj in selected_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = selected_objects[0]

    return True


bpy.ops.wm.console_toggle()

if render_models_from_multiple_angles(OUTPUT_FOLDER):
    print("Script finished")

bpy.ops.wm.console_toggle()
