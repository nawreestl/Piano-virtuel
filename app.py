import streamlit as st
import os
import pygame
from io import BytesIO
import wave
import numpy as np

# Initialisation de pygame pour le son
pygame.mixer.init()

# 📁 Dossier contenant les fichiers audio
SOUNDS_DIR = "sounds"

# 🎹 Notes du piano (Deux octaves)
NOTES_WHITE = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2', 'c3']
DISPLAY_WHITE = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2', 'C3']

NOTES_BLACK = ['c_sharp', 'd_sharp', '', 'f_sharp', 'g_sharp', 'a_sharp', '', 'c2_sharp', 'd2_sharp', '', 'f2_sharp', 'g2_sharp', 'a2_sharp', '']
DISPLAY_BLACK = ['C#', 'D#', '', 'F#', 'G#', 'A#', '', 'C#2', 'D#2', '', 'F#2', 'G#2', 'A#2', '']

# 📀 Stockage des sons joués pour enregistrement
if "recording_active" not in st.session_state:
    st.session_state.recording_active = False

if "recorded_audio" not in st.session_state:
    st.session_state.recorded_audio = []

if "current_note" not in st.session_state:
    st.session_state.current_note = ""

# 🛠️ Fonction pour jouer un son
def play_sound(note):
    try:
        sound_file = os.path.join(SOUNDS_DIR, f"{note}.wav")
        pygame.mixer.Sound(sound_file).play()
        st.session_state.current_note = note.upper()
        if st.session_state.recording_active:
            st.session_state.recorded_audio.append(note)
    except Exception as e:
        st.error(f"Erreur : Impossible de jouer {note} - {e}")

# 🛠️ Fonction pour sauvegarder l'enregistrement
def save_recording():
    # Créer un fichier audio en mémoire avec les notes jouées
    audio_data = np.array([])  # Cela représente les données audio (simples exemples)
    
    # Transforme les notes jouées en sons simulés (simplifié)
    for note in st.session_state.recorded_audio:
        sound_file = os.path.join(SOUNDS_DIR, f"{note}.wav")
        sound = pygame.mixer.Sound(sound_file)
        # Ajouter chaque son dans l'enregistrement simulé
        audio_data = np.append(audio_data, np.array(sound.get_raw()))

    # Sauvegarder l'audio simulé dans un fichier WAV
    with wave.open("piano_recording.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes par échantillon (16 bits)
        wf.setframerate(44100)  # Fréquence d'échantillonnage
        wf.writeframes(audio_data.tobytes())  # Sauvegarder les données audio

    # Retourner le fichier sauvegardé
    return "piano_recording.wav"

# 🎨 CSS pour une belle interface
st.markdown("""
    <style>
    /* 🎀 Arrière-plan pastel rose */
    body { background: linear-gradient(135deg, #fce4ec, #f8bbd0); color: #4a4a4a; }
    .stApp { background: linear-gradient(135deg, #fce4ec, #f8bbd0); color: #4a4a4a; font-family: 'Arial', sans-serif; }

    /* 🎹 Boutons du piano */
    .piano-container { display: flex; justify-content: center; }
    .piano-button { width: 60px; height: 160px; margin: 3px; font-size: 16px; font-weight: bold; cursor: pointer; }
    
    .white { 
        background-color: #ffffff; /* Blanc pur */
        color: #4a4a4a; 
        border: 3px solid #d81b60; /* Rose foncé */
        border-radius: 5px; 
    }
    
    .black { 
        background-color: #d81b60; /* Rose foncé */
        color: white; 
        border: 3px solid #ad1457; /* Rose plus foncé */
        height: 110px; 
        margin-left: -30px; 
        z-index: 2; 
        position: relative; 
        border-radius: 5px; 
    }

    /* 🎤 Boutons d'action */
    .rec-btn {
        background-color: #f06292; /* Rose vif */
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .rec-btn:hover { background-color: #ec407a; } /* Rose plus intense au survol */

    .stop-btn {
        background-color: #f8bbd0; /* Rose pastel */
        color: black;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .stop-btn:hover { background-color: #f48fb1; } /* Rose plus chaud au survol */

    .download-btn {
        background-color: #d81b60; /* Rose foncé */
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .download-btn:hover { background-color: #c2185b; } /* Rose intense au survol */

    .reset-btn {
        background-color: #f06292; /* Rose vif */
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .reset-btn:hover { background-color: #e91e63; } /* Rose flash au survol */
    </style>
""", unsafe_allow_html=True)

# 🏠 Interface Streamlit
st.title("🎹 Piano Virtuel avec Enregistreur 🎶")
st.write("Cliquez sur une note pour jouer le son. 🎵")

# 🎼 Affichage de la note en cours
if st.session_state.current_note:
    st.subheader(f"🎶 Note en cours : {st.session_state.current_note}")

# 🎹 Piano (Touches Blanches)
white_keys = st.columns(len(NOTES_WHITE))
for i, note in enumerate(NOTES_WHITE):
    with white_keys[i]:
        if st.button(DISPLAY_WHITE[i], key=f"white_{note}", use_container_width=True):
            play_sound(note)

# 🎼 Piano (Touches Noires)
black_keys = st.columns(len(NOTES_BLACK))
for i, note in enumerate(NOTES_BLACK):
    with black_keys[i]:
        if note:  
            if st.button(DISPLAY_BLACK[i], key=f"black_{note}", use_container_width=True):
                play_sound(note)

# 🎤 Enregistrement
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🎙️ Enregistrement")
record_button = st.button("🎙️ Démarrer l'enregistrement", key="start_record", use_container_width=True)
if record_button:
    st.session_state.recording_active = True
    st.session_state.recorded_audio.clear()
    st.success("🎤 Enregistrement commencé !")

# ⏹ Stop & Téléchargement
stop_button = st.button("⏹ Stopper et sauvegarder l'enregistrement", key="stop_record", use_container_width=True)
if stop_button:
    st.session_state.recording_active = False
    st.success("✅ Enregistrement terminé ! Téléchargez votre musique ci-dessous :")
    audio_file = save_recording()
    if audio_file:
        st.download_button("📥 Télécharger l'enregistrement", audio_file, file_name="piano_recording.wav", mime="audio/wav")

# 🔄 Réinitialisation
if st.button("🔄 Réinitialiser", key="reset_piano", help="Réinitialiser l'enregistrement et les notes jouées", use_container_width=True):
    st.session_state.current_note = ""
    st.session_state.recorded_audio.clear()
    st.session_state.recording_active = False
    st.success("🔄 Réinitialisation complète !")
