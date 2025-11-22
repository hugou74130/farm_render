#include <stdio.h>	// pour printf, scanf
#include <stdlib.h> // pour system et fonctions utilitaires
#include <string.h> // pour strcmp

int main()
{
	char fichier[256];		  // variable pour stocker le chemin du fichier .blend
	char mode[10];			  // variable pour stocker le mode de rendu choisi (EEVEE ou CYCLES)
	char device[10];		  // variable pour stocker le device (CPU ou GPU) si Cycles est choisi
	int frameDebut, frameFin; // variables pour stocker le numéro de la frame de début et de fin
	char sortie[256];		  // variable pour stocker le chemin du dossier de sortie

	// Demande à l'utilisateur le chemin du fichier .blend
	printf("Chemin du fichier .blend : ");
	scanf("%255s", fichier); // lit au maximum 255 caractères pour éviter de dépasser la taille de la variable

	// Demande le mode de rendu
	printf("Mode de rendu (EEVEE ou CYCLES) : ");
	scanf("%9s", mode); // lit au maximum 9 caractères pour éviter le dépassement du buffer

	// Si l'utilisateur choisit CYCLES, demander CPU ou GPU
	if (strcmp(mode, "CYCLES") == 0) // strcmp compare deux chaînes, retourne 0 si elles sont identiques
	{
		printf("Device (CPU ou GPU) : ");
		scanf("%9s", device); // lit au maximum 9 caractères pour le choix du device
	}
	else
	{
		device[0] = '\0'; // si Eevee est choisi, la variable device reste vide
	}

	// Demande la frame de début
	printf("Frame de début : ");
	scanf("%d", &frameDebut); // lit un entier pour la frame de début

	// Demande la frame de fin
	printf("Frame de fin : ");
	scanf("%d", &frameFin); // lit un entier pour la frame de fin

	// Demande le dossier de sortie
	printf("Dossier de sortie : ");
	scanf("%255s", sortie); // lit au maximum 255 caractères pour le chemin du dossier de sortie

	// Construction de la commande Blender
	char commande[1024]; // buffer pour stocker la commande complète

	if (strcmp(mode, "CYCLES") == 0) // si le moteur est Cycles
	{
		snprintf(commande, sizeof(commande),
				 "blender -b \"%s\" -s %d -e %d -a --render-engine %s --cycles-device %s -o \"%s/frame_\"",
				 fichier, frameDebut, frameFin, mode, device, sortie);
		// snprintf construit une chaîne de caractères avec les paramètres pour le rendu
	}
	else // sinon le moteur est Eevee
	{
		snprintf(commande, sizeof(commande),
				 "blender -b \"%s\" -s %d -e %d -a --render-engine %s -o \"%s/frame_\"",
				 fichier, frameDebut, frameFin, mode, sortie);
		// même chose mais sans le device, car Eevee n'a pas besoin de CPU/GPU
	}

	// Affiche la commande qui sera exécutée
	printf("\nCommande à exécuter :\n%s\n", commande);

	// Optionnel : exécuter la commande directement
	// system(commande);  // décommente cette ligne pour lancer Blender automatiquement

	return 0; // fin du programme
}
