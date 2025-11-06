bl_info = {
    "name": "Farm Render Pro",
    "author": "Hugo Ramos",
    "version": (2, 2),
    "blender": (4, 4, 0),
    "description": "Ferme de rendu locale avec gestion CPU/GPU automatique et options avancées",
    "category": "Render",
}

import bpy
import os
import subprocess
import threading
import concurrent.futures
from datetime import datetime
from bpy.props import StringProperty, IntProperty, EnumProperty


# --- 🔍 Détection automatique des GPU ---
def detect_render_devices(self, context):
    """Retourne la liste des périphériques de calcul disponibles (CPU, GPU, etc.)"""
    devices = []
    try:
        # Vérifie que Cycles est dispo
        if "cycles" not in bpy.context.preferences.addons:
            return [("CPU:CPU", "CPU (par défaut)", "")]

        prefs = bpy.context.preferences.addons["cycles"].preferences

        for device_type in ["OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"]:
            prefs.compute_device_type = device_type
            try:
                prefs.get_devices()
                for dev in prefs.devices:
                    if dev.type != "CPU":
                        devices.append((f"{device_type}:{dev.name}", f"{dev.name} ({device_type})", ""))
            except:
                continue

        # Ajouter le CPU toujours présent
        devices.append(("CPU:CPU", "CPU (Central Processing Unit)", ""))

        # Supprimer doublons
        unique_devices = []
        for d in devices:
            if d not in unique_devices:
                unique_devices.append(d)

        return unique_devices or [("CPU:CPU", "CPU (par défaut)", "")]
    except Exception as e:
        print(f"[FarmRender] ⚠️ Erreur détection GPU : {e}")
        return [("CPU:CPU", "CPU (par défaut)", "")]


# --- Fonction principale de rendu ---
def render_single_frame(blender_path, file_path, output_dir, frame_number, device_type):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "frame_####")

    command = [
        blender_path,
        "-b", file_path,
        "-o", output_path,
        "-f", str(frame_number)
    ]

    env = os.environ.copy()
    env["CYCLES_DEVICE"] = device_type.split(":")[0]  # Ex: OPTIX ou CPU

    try:
        subprocess.run(command, check=True, capture_output=True, text=True, env=env)
        print(f"[FarmRender] Frame {frame_number} OK ✅ ({device_type})")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FarmRender] Frame {frame_number} échouée ❌")
        print(e.stderr)
        return False


def apply_render_device(device_choice):
    """Configure Blender pour utiliser le bon périphérique (CPU ou GPU)"""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    device_type, device_name = device_choice.split(":")

    if device_type == "CPU":
        prefs.compute_device_type = "NONE"
        bpy.context.scene.cycles.device = "CPU"
        print("[FarmRender] Mode CPU activé.")
    else:
        prefs.compute_device_type = device_type
        bpy.context.scene.cycles.device = "GPU"

        # Activer le GPU sélectionné
        for d in prefs.devices:
            d.use = (d.name == device_name)
        print(f"[FarmRender] GPU {device_name} ({device_type}) activé.")


def launch_farm_render(start_frame, end_frame, output_dir, threads, device_choice, session_name):
    file_path = bpy.data.filepath
    if not file_path:
        print("[FarmRender] ⚠️ Sauvegarde ton fichier .blend avant de lancer le rendu.")
        return

    blender_path = bpy.app.binary_path
    frames = list(range(start_frame, end_frame + 1))

    # Crée un sous-dossier pour la session
    session_dir = os.path.join(output_dir, session_name)
    os.makedirs(session_dir, exist_ok=True)

    apply_render_device(device_choice)

    print(f"[FarmRender] Session : {session_name}")
    print(f"[FarmRender] Rendu sur {device_choice}")
    print(f"[FarmRender] Frames : {start_frame} à {end_frame}")
    print(f"[FarmRender] Threads : {threads}")
    print(f"[FarmRender] Dossier de sortie : {session_dir}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(
            lambda f: render_single_frame(blender_path, file_path, session_dir, f, device_choice),
            frames
        )

    print("[FarmRender] ✅ Tous les rendus sont terminés.")


# --- Classes Blender ---
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
    device_choice: EnumProperty(
        name="Périphérique de rendu",
        items=detect_render_devices,  # maintenant sous forme de callback
        description="Choisis le périphérique (GPU/CPU) pour le rendu"
)

    session_name: StringProperty(
        name="Nom de la session",
        default="session_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )


class FARMRENDER_OT_Run(bpy.types.Operator):
    bl_idname = "farmrender.run"
    bl_label = "Lancer le rendu"

    def execute(self, context):
        prefs = context.scene.farm_render_settings
        threading.Thread(
            target=launch_farm_render,
            args=(
                prefs.start_frame,
                prefs.end_frame,
                bpy.path.abspath(prefs.output_dir),
                prefs.thread_count,
                prefs.device_choice,
                prefs.session_name,
            ),
            daemon=True
        ).start()
        self.report({'INFO'}, f"Rendu sur {prefs.device_choice} lancé (voir console).")
        return {'FINISHED'}


class FARMRENDER_OT_OpenFolder(bpy.types.Operator):
    bl_idname = "farmrender.open_folder"
    bl_label = "Ouvrir le dossier de rendu"

    def execute(self, context):
        output_dir = bpy.path.abspath(context.scene.farm_render_settings.output_dir)
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            self.report({'WARNING'}, "Le dossier n'existe pas encore.")
        return {'FINISHED'}


class FARMRENDER_PT_Panel(bpy.types.Panel):
    bl_label = "Ferme de Rendu Pro"
    bl_idname = "FARMRENDER_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        prefs = context.scene.farm_render_settings

        # --- Section 1 : Configuration du rendu ---
        box = layout.box()
        box.label(text="⚙️ Configuration du rendu", icon="RENDER_STILL")
        box.prop(prefs, "output_dir")
        
        row = box.row()
        row.prop(prefs, "start_frame")
        row.prop(prefs, "end_frame")
        
        box.prop(prefs, "session_name")
        box.prop(prefs, "thread_count")
        box.prop(prefs, "device_choice")

        # Bouton pour rafraîchir la liste GPU
        row_refresh = box.row()
        row_refresh.operator("farmrender.refresh_devices", icon="FILE_REFRESH")

        layout.separator()

        # --- Section 2 : Contrôle ---
        box_control = layout.box()
        box_control.label(text="▶️ Contrôle du rendu", icon="RENDER_ANIMATION")
        box_control.operator("farmrender.run", icon="RENDER_ANIMATION")
        box_control.operator("farmrender.open_folder", icon="FILE_FOLDER")

        layout.separator()

        # --- Section 3 : Informations ---
        box_info = layout.box()
        box_info.label(text="ℹ️ Informations")
        total_frames = prefs.end_frame - prefs.start_frame + 1
        box_info.label(text=f"Frames à rendre : {total_frames}")
        box_info.label(text=f"Périphérique actif : {prefs.device_choice}")

class FARMRENDER_OT_RefreshDevices(bpy.types.Operator):
    bl_idname = "farmrender.refresh_devices"
    bl_label = "Rafraîchir GPU"

    def execute(self, context):
        prefs = context.scene.farm_render_settings
        # Force la mise à jour de l’EnumProperty
        prefs.device_choice = prefs.device_choice  # Réaffiche le menu
        self.report({'INFO'}, "Liste des périphériques mise à jour.")
        return {'FINISHED'}

# --- Register ---
classes = [
    FarmRenderSettings,
    FARMRENDER_OT_Run,
    FARMRENDER_OT_OpenFolder,
    FARMRENDER_OT_RefreshDevices,
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
