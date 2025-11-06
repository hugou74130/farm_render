bl_info = {
    "name": "Farm Render Pro",
    "author": "Hugo Ramos",
    "version": (2, 0),
    "blender": (4, 4, 0),
    "description": "Lance une ferme de rendu locale avec options avancées",
    "category": "Render",
}

import bpy
import os
import subprocess
import threading
import concurrent.futures
from bpy.props import StringProperty, IntProperty, BoolProperty

# --- Fonctions de rendu ---
def render_single_frame(blender_path, file_path, output_dir, frame_number):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "frame_####")

    command = [
        blender_path,
        "-b", file_path,
        "-o", output_path,
        "-f", str(frame_number)
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[FarmRender] Frame {frame_number} OK ✅")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FarmRender] Frame {frame_number} échouée ❌")
        print(e.stderr)
        return False


def launch_farm_render(start_frame, end_frame, output_dir, threads):
    file_path = bpy.data.filepath
    if not file_path:
        print("[FarmRender] ⚠️ Sauvegarde ton fichier .blend avant de lancer le rendu.")
        return

    blender_path = bpy.app.binary_path
    frames = list(range(start_frame, end_frame + 1))
    print(f"[FarmRender] Lancement du rendu pour frames {start_frame} → {end_frame}")
    print(f"[FarmRender] Dossier de sortie : {output_dir}")
    print(f"[FarmRender] Threads : {threads}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda f: render_single_frame(blender_path, file_path, output_dir, f), frames)

    print("[FarmRender] ✅ Tous les rendus sont terminés.")


# --- Classes Blender ---
class FARMRENDER_OT_Run(bpy.types.Operator):
    bl_idname = "farmrender.run"
    bl_label = "Lancer le rendu"

    def execute(self, context):
        prefs = context.scene.farm_render_settings
        threading.Thread(
            target=launch_farm_render,
            args=(prefs.start_frame, prefs.end_frame, prefs.output_dir, prefs.thread_count),
            daemon=True
        ).start()
        self.report({'INFO'}, "Rendu lancé (voir console pour les logs)")
        return {'FINISHED'}


class FARMRENDER_OT_OpenFolder(bpy.types.Operator):
    bl_idname = "farmrender.open_folder"
    bl_label = "Ouvrir le dossier de rendu"

    def execute(self, context):
        output_dir = context.scene.farm_render_settings.output_dir
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            self.report({'WARNING'}, "Le dossier n'existe pas encore")
        return {'FINISHED'}


class FarmRenderSettings(bpy.types.PropertyGroup):
    output_dir: StringProperty(
        name="Dossier de sortie",
        subtype='DIR_PATH',
        default="//renders/"
    )
    start_frame: IntProperty(
        name="Frame début",
        default=0,
        min=0
    )
    end_frame: IntProperty(
        name="Frame fin",
        default=10,
        min=1
    )
    thread_count: IntProperty(
        name="Threads (CPU)",
        default=2,
        min=1,
        max=16
    )


class FARMRENDER_PT_Panel(bpy.types.Panel):
    bl_label = "Ferme de Rendu Pro"
    bl_idname = "FARMRENDER_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        prefs = context.scene.farm_render_settings

        layout.prop(prefs, "output_dir")
        layout.prop(prefs, "start_frame")
        layout.prop(prefs, "end_frame")
        layout.prop(prefs, "thread_count")

        layout.separator()
        layout.operator("farmrender.run", icon="RENDER_ANIMATION")
        layout.operator("farmrender.open_folder", icon="FILE_FOLDER")


# --- Register ---
classes = [
    FarmRenderSettings,
    FARMRENDER_OT_Run,
    FARMRENDER_OT_OpenFolder,
    FARMRENDER_PT_Panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.farm_render_settings = bpy.props.PointerProperty(type=FarmRenderSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.farm_render_settings

if __name__ == "__main__":
    register()
