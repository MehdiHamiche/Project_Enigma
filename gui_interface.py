import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk 
from enigma import MachineEnigma
from rotor import Rotor
from reflector import Reflector
from config.config_manager import save_configuration, load_configuration
import random
import string

# Charger la configuration pour les options de rotors et réflecteurs
config = load_configuration("config/default_config.json")

# Variable to store the key used for encryption
encryption_key = None

# Fonction pour générer une clé 3-lettre
def generate_random_key():
    return ''.join(random.choices(string.ascii_uppercase, k=3))

# Fonction pour afficher une infobulle (tooltip)
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    tooltip_label = tk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1, font=("Arial", 8))
    tooltip_label.pack()

    def show_tooltip(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def hide_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

def chiffrer_message():
    global encryption_key  # Access the global encryption_key variable
    message = message_entry.get().upper()
    operation = operation_var.get()

    # Pour chiffrement, générer une clé
    if operation == "Chiffrer":
        encryption_key = generate_random_key()
        key_entry.delete(0, tk.END)  # Clear previous key
        key_entry.insert(0, encryption_key)  # Display the key used for encryption

    # Use the stored encryption key for decryption
    key = encryption_key if operation == "Déchiffrer" else key_entry.get().upper()

    # Vérifie que la clé et le message ne sont pas vides
    if not key:
        messagebox.showwarning("Erreur", "Le champ de la clé est vide.")
        return
    if not message:
        messagebox.showwarning("Erreur", "Le champ du message est vide.")
        return
    if len(message) > 100000:
        messagebox.showwarning("Erreur", "Le message est trop long (max 100000 caractères).")
        return

    # Obtenir les choix de rotors et de réflecteur de l'utilisateur
    rotor1_choice = rotor1_combo.get()
    rotor2_choice = rotor2_combo.get()
    rotor3_choice = rotor3_combo.get()
    reflector_choice = reflector_combo.get()

    # Initialiser les rotors et le réflecteur selon les choix de l'utilisateur
    rotor1 = Rotor(config['rotors'][rotor1_choice]['wiring'], config['rotors'][rotor1_choice]['notch'])
    rotor2 = Rotor(config['rotors'][rotor2_choice]['wiring'], config['rotors'][rotor2_choice]['notch'])
    rotor3 = Rotor(config['rotors'][rotor3_choice]['wiring'], config['rotors'][rotor3_choice]['notch'])
    reflector = Reflector(config['reflectors'][reflector_choice])

    # Initialize the Enigma machine with selected rotors and reflector
    machine = MachineEnigma([rotor1, rotor2, rotor3], reflector)
    machine.set_rotor_positions(key)

    verbose = verbose_var.get() == 1

    if operation == "Chiffrer":
        encrypted_message = machine.encrypt(message, verbose=verbose)
        result_label.config(text=f"Message chiffré : {encrypted_message}")
    elif operation == "Déchiffrer":
        decrypted_message = machine.decrypt(message, verbose=verbose)
        result_label.config(text=f"Message déchiffré : {decrypted_message}")

def sauvegarder_configuration():
    # Obtenir les choix de rotors et de réflecteur
    rotor1_choice = rotor1_combo.get()
    rotor2_choice = rotor2_combo.get()
    rotor3_choice = rotor3_combo.get()
    reflector_choice = reflector_combo.get()

    # Initialiser les rotors et le réflecteur selon les choix de l'utilisateur
    rotor1 = Rotor(config['rotors'][rotor1_choice]['wiring'], config['rotors'][rotor1_choice]['notch'])
    rotor2 = Rotor(config['rotors'][rotor2_choice]['wiring'], config['rotors'][rotor2_choice]['notch'])
    rotor3 = Rotor(config['rotors'][rotor3_choice]['wiring'], config['rotors'][rotor3_choice]['notch'])
    reflector = Reflector(config['reflectors'][reflector_choice])

    # Sauvegarder la configuration dans custom_config.json
    save_configuration([rotor1, rotor2, rotor3], reflector, "config/custom_config.json")
    result_label.config(text="Configuration sauvegardée dans config/custom_config.json")

def traiter_fichier():
    """
    Permet de chiffrer ou déchiffrer un fichier texte sélectionné par l'utilisateur.
    """
    # Ouvre une boîte de dialogue pour sélectionner le fichier
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return  # Annule si aucun fichier n'est sélectionné

    # Récupère la clé et l'opération
    key = key_entry.get().upper()
    operation = operation_var.get()

    # Obtenir les choix de rotors et de réflecteur
    rotor1_choice = rotor1_combo.get()
    rotor2_choice = rotor2_combo.get()
    rotor3_choice = rotor3_combo.get()
    reflector_choice = reflector_combo.get()

    # Initialiser les rotors et le réflecteur
    rotor1 = Rotor(config['rotors'][rotor1_choice]['wiring'], config['rotors'][rotor1_choice]['notch'])
    rotor2 = Rotor(config['rotors'][rotor2_choice]['wiring'], config['rotors'][rotor2_choice]['notch'])
    rotor3 = Rotor(config['rotors'][rotor3_choice]['wiring'], config['rotors'][rotor3_choice]['notch'])
    reflector = Reflector(config['reflectors'][reflector_choice])

    machine = MachineEnigma([rotor1, rotor2, rotor3], reflector)
    machine.set_rotor_positions(key)

    verbose = verbose_var.get() == 1

    try:
        # Chiffrement/Déchiffrement du fichier
        with open(file_path, 'r') as file:
            text = file.read()

        if operation == "Chiffrer":
            processed_text = machine.encrypt(text, verbose=verbose)
            output_filename = f"{file_path}_encrypted.txt"
        elif operation == "Déchiffrer":
            processed_text = machine.decrypt(text, verbose=verbose)
            output_filename = f"{file_path}_decrypted.txt"

        # Sauvegarde du résultat
        with open(output_filename, 'w') as file:
            file.write(processed_text)

        result_label.config(text=f"Fichier traité et sauvegardé sous : {output_filename}")
    
    except Exception as e:
        result_label.config(text=f"Erreur lors du traitement : {e}")

# Interface Tkinter
window = tk.Tk()
window.title("Emulateur Enigma")
window.geometry("1000x1000")  # Ajuste la taille de la fenêtre

# Create a frame for main controls
main_frame = ttk.Frame(window)
main_frame.pack(pady=10)

# Ajouter le titre
titre_label = tk.Label(window, text="Simulateur de la Machine Enigma", font=("Arial", 16, "bold"))
titre_label.pack(pady=10)

# Charger et afficher l'image
image_path = "enigma_image.png"  # Remplacez par le chemin de votre image Enigma
image = Image.open(image_path)
image = image.resize((100, 100), Image.LANCZOS)  # Ajuste la taille de l'image
enigma_image = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image=enigma_image)
image_label.pack(pady=30)

# Utiliser ttk pour les widgets modernes
style = ttk.Style(window)
style.theme_use("default")

# Entrée pour la clé
tk.Label(window, text="Clé initiale (ex: ABC) :").pack(pady=5)
key_entry = ttk.Entry(window, width=10)
key_entry.pack(pady=5)

# Entrée pour le message
tk.Label(window, text="Message à traiter :").pack(pady=5)
message_entry = ttk.Entry(window, width=50)
message_entry.pack(pady=(5,30))

# Ajout des Tooltips
# Menus déroulants pour les rotors et le réflecteur
tk.Label(window, text="Sélectionner le Rotor 1 :").pack(pady=5)
rotor1_combo = ttk.Combobox(window, values=list(config['rotors'].keys()))
rotor1_combo.set("I")  # Valeur par défaut
rotor1_combo.pack(pady=5)
create_tooltip(rotor1_combo, "Rotor 1: Permet de sélectionner la permutation de câblage du premier rotor.")

tk.Label(window, text="Sélectionner le Rotor 2 :").pack(pady=5)
rotor2_combo = ttk.Combobox(window, values=list(config['rotors'].keys()))
rotor2_combo.set("II")  # Valeur par défaut
rotor2_combo.pack(pady=5)
create_tooltip(rotor2_combo, "Rotor 2: Permet de sélectionner la permutation de câblage du deuxième rotor.")

tk.Label(window, text="Sélectionner le Rotor 3 :").pack(pady=5)
rotor3_combo = ttk.Combobox(window, values=list(config['rotors'].keys()))
rotor3_combo.set("III")  # Valeur par défaut
rotor3_combo.pack(pady=5)
create_tooltip(rotor3_combo, "Rotor 3: Permet de sélectionner la permutation de câblage du troisième rotor.")

tk.Label(window, text="Sélectionner le Réflecteur :").pack(pady=5)
reflector_combo = ttk.Combobox(window, values=list(config['reflectors'].keys()))
reflector_combo.set("B")  # Valeur par défaut
reflector_combo.pack(pady=(5,10))
create_tooltip(reflector_combo, "Réflecteur: Redirige le signal électrique pour compléter la permutation.")

# Options de traitement (Chiffrer ou Déchiffrer)
operation_var = tk.StringVar(value="Chiffrer")
operation_frame = ttk.Frame(window)
operation_frame.pack(pady=10)
ttk.Radiobutton(operation_frame, text="Chiffrer", variable=operation_var, value="Chiffrer").pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(operation_frame, text="Déchiffrer", variable=operation_var, value="Déchiffrer").pack(side=tk.LEFT, padx=10)

# Option pour activer le mode verbose
verbose_var = tk.IntVar()
tk.Checkbutton(window, text="Activer le mode verbose", variable=verbose_var).pack(pady=5)

# Bouton pour sauvegarder la configuration
ttk.Button(window, text="Sauvegarder Configuration", command=sauvegarder_configuration).pack(pady=(5,35))

# Bouton pour traiter le message
ttk.Button(window, text="Traiter", command=chiffrer_message).pack(pady=(5,25))

# Bouton pour traiter un fichier
ttk.Button(window, text="Traiter un Fichier", command=traiter_fichier).pack(pady=(5,25))

# Label pour afficher le résultat
result_label = tk.Label(window, text="Message traité :", font=("Arial", 12))
result_label.pack(pady=(5,15))

# Bouton pour copier le résultat
def copier_resultat():
    result_text = result_label.cget("text")
    if result_text:
        window.clipboard_clear()
        window.clipboard_append(result_text)
        messagebox.showinfo("Copie", "Le message a été copié dans le presse-papier.")
    else:
        messagebox.showwarning("Erreur", "Aucun message à copier.")

copy_button = tk.Button(window, text="Copier", command=copier_resultat)
copy_button.pack(pady=5)

# Bouton Réinitialiser sans fonction dédiée
reset_button = tk.Button(
    window,
    text="Réinitialiser",
    command=lambda: (
        key_entry.delete(0, tk.END),
        message_entry.delete(0, tk.END),
        rotor1_combo.set("I"),
        rotor2_combo.set("II"),
        rotor3_combo.set("III"),
        reflector_combo.set("B"),
        operation_var.set("Chiffrer"),
        verbose_var.set(0),
        result_label.config(text="")
    ),
)
reset_button.pack(pady=5)

# Pied de page
footer_label = tk.Label(window, text="© 2024 Emulateur Enigma - Tous droits réservés", font=("Arial", 8))
footer_label.pack(side="bottom", pady=10)

# Barre de menu
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Menu Fichier
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

def charger_configuration():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
    if file_path:
        load_configuration(file_path)
        messagebox.showinfo("Chargement", f"Configuration chargée depuis {file_path}")

file_menu.add_command(label="Charger une configuration", command=charger_configuration)

def enregistrer_resultat():
    result_text = result_label.cget("text")
    if result_text:
        # Enlève le préfixe "Message chiffré : " ou "Message déchiffré : " pour enregistrer uniquement le message
        if "Message chiffré : " in result_text:
            result_text = result_text.replace("Message chiffré : ", "")
        elif "Message déchiffré : " in result_text:
            result_text = result_text.replace("Message déchiffré : ", "")
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(result_text)
            messagebox.showinfo("Enregistrement", f"Résultat enregistré dans {file_path}")
    else:
        messagebox.showwarning("Erreur", "Aucun message à enregistrer.")

file_menu.add_command(label="Enregistrer le résultat", command=enregistrer_resultat)

# Menu À propos
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="À propos", menu=help_menu)

def afficher_a_propos():
    messagebox.showinfo("À propos", "Simulateur de la Machine Enigma\nVersion 1.0\nDéveloppé par Mehdi Hamiche")

help_menu.add_command(label="À propos", command=afficher_a_propos)

window.mainloop()