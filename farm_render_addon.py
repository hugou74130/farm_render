bl_info = {
    "name": "Farm Render Launcher",
    "author": "Hugo Ramos",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "description": "Lance une ferme de rendu locale depuis Blender",
    "category": "Render",
}

import bpy
import subprocess
import os
import threading

# --- Configuration par défaut ---
BLENDER_EXE_PATH = bpy.app.binary_path  # le Blender actuel
OUTPUT_DIR = r"D:\animation\renders"
FRAMES_TO_RENDER = range(0, 5)

def render_single_frame(blender_path, file_path, frame_number):
    """Lance le rendu d'une seule image"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "frame_####")

    command = [
        blender_path,
        "-b", file_path,
        "-o", output_path,
        "-f", str(frame_number)
    ]

    print(f"[FarmRender] Lancement Frame {frame_number}...")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[FarmRender] Frame {frame_number} OK ✅")
    except subprocess.CalledProcessError as e:
        print(f"[FarmRender] Frame {frame_number} ÉCHEC ❌")
        print(e.stderr)


def launch_farm_render():
    """Lance la ferme en thread pour ne pas bloquer l’UI"""
    file_path = bpy.data.filepath
    if not file_path:
        print("[FarmRender] Sauvegarde ton fichier .blend avant de lancer le rendu.")
        return

    print("[FarmRender] --- Démarrage du rendu ---")
    print(f"[FarmRender] Fichier : {file_path}")
    print(f"[FarmRender] Frames : {list(FRAMES_TO_RENDER)}")

    for f in FRAMES_TO_RENDER:
        render_single_frame(BLENDER_EXE_PATH, file_path, f)

    print("[FarmRender] --- Tous les rendus sont terminés ---")


class FARMRENDER_OT_Run(bpy.types.Operator):
    """Opérateur pour exécuter la ferme de rendu"""
    bl_idname = "farmrender.run"
    bl_label = "Lancer la Ferme de Rendu"

    def execute(self, context):
        threading.Thread(target=launch_farm_render, daemon=True).start()
        self.report({'INFO'}, "Rendu en cours... Consulte la console Blender.")
        return {'FINISHED'}


class FARMRENDER_PT_Panel(bpy.types.Panel):
    """Interface dans Blender"""
    bl_label = "Ferme de Rendu Locale"
    bl_idname = "FARMRENDER_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        layout.operator("farmrender.run", icon='RENDER_ANIMATION')


def register():
    bpy.utils.register_class(FARMRENDER_OT_Run)
    bpy.utils.register_class(FARMRENDER_PT_Panel)


def unregister():
    bpy.utils.unregister_class(FARMRENDER_OT_Run)
    bpy.utils.unregister_class(FARMRENDER_PT_Panel)


if __name__ == "__main__":
    register()
