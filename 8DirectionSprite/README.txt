This blender script and template is based on the following sources:

https://foozlecc.itch.io/render-4-or-8-direction-sprites-from-blender
https://github.com/FoozleCC/blender_scripts/blob/main/render_8_direction_sprites


Main differences:

The render_models_from_multiple_angles function has been modified to include an additional check for whether any objects are selected. If no objects are selected, an error message is printed and the script exits.

The get_angle_values function has been added to generate a list of angle values based on the SEGMENTS variable. This list of angle values is used to rotate the objects in the scene.

The render_models_from_multiple_angles function now loops through each selected object and renders it from multiple angles. For each object, it loops through each action in the ACTIONS list, sets the current action, and renders the frames for that action from multiple angles.

The console is toggled on and off at the beginning and end of the script using bpy.ops.wm.console_toggle(). This allows the script to print messages to the console.