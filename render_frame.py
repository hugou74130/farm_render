import subprocess
import os
import sys

# --- À CONFIGURER PAR VOUS ---
BLENDER_EXE_PATH = r"C:\Users\Hugor\Desktop\blender-4.4.0-windows-x64\blender.exe"
BLEND_FILE_PATH = r"D:\animation\testrender.blend"

# Définir la plage que vous voulez rendre
# range(10, 21) signifie : de 10 jusqu'à 21 (exclu),
# donc 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.
FRAMES_TO_RENDER = range(0, 5)
# --- FIN DE LA CONFIGURATION ---


def render_single_frame(blender_path, file_path, frame_number):
    """
    Lance le rendu d'une seule image avec un dossier de sortie personnalisé.
    """
    print(f"--- Lancement Tâche : Image {frame_number} ---")

    # Dossier où tu veux stocker les frames rendues
    OUTPUT_DIR = r"D:\animation\renders"

    # Crée le dossier s'il n'existe pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Chemin de sortie (Blender utilise # pour le numéro de frame)
    output_path = os.path.join(OUTPUT_DIR, "frame_####")

    command = [
        blender_path,
        "-b", file_path,
        "-o", output_path,  # <- dossier de sortie
        "-f", str(frame_number)
    ]

    print(f"Commande : {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"--- Tâche Terminée : Image {frame_number} (Succès) ---")
        return True
    except subprocess.CalledProcessError as e:
        print(f"!!! ERREUR Tâche : Image {frame_number} (Échec) !!!")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        return False
    
# --- Point d'entrée principal ---
if __name__ == "__main__":
    print(f"--- Démarrage du Simulateur de Ferme ---")
    print(f"Fichier : {BLEND_FILE_PATH}")
    print(f"Images à rendre : {list(FRAMES_TO_RENDER)}")

    # Vérifier les chemins une seule fois au début
    if not os.path.exists(BLENDER_EXE_PATH) or not os.path.exists(BLEND_FILE_PATH):
        print("ERREUR : Vérifiez BLENDER_EXE_PATH et BLEND_FILE_PATH en haut du script.")
        sys.exit(1)

    successful_frames = 0
    failed_frames = []

    # C'est ce que votre SERVEUR fera :
    # distribuer les tâches une par une.
    for frame in FRAMES_TO_RENDER:

        # Sur une vraie ferme, le serveur enverrait "frame"
        # au prochain worker disponible.
        # Ici, on exécute la tâche localement.

        success = render_single_frame(BLENDER_EXE_PATH, BLEND_FILE_PATH, frame)

        if success:
            successful_frames += 1
        else:
            failed_frames.append(frame)
            # Optionnel : arrêter tout s'il y a une erreur
            # print("Arrêt du script à cause d'une erreur.")
            # break

    print("\n--- Rapport Final ---")
    print(f"Rendus terminés : {successful_frames}")
    print(f"Rendus échoués  : {len(failed_frames)}")
    if failed_frames:
        print(f"Images échouées : {failed_frames}")
        sys.exit(1)

    print("Tous les rendus ont été complétés avec succès.")
    sys.exit(0)
