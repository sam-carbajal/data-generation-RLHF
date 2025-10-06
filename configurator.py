import json
import streamlit as st
from st_draggable_list import DraggableList
from annotation_page import AnnotationSection
from startpage import DefaultSettings, InitializeSession

criteria = {
    "Werte": "Entspricht den moralischen Anforderungen?",
    "Spannung": "Werden sprachliche Bilder, Methafern, etc. verwendet; gibt es unerwartete " 
                            "Wendungen; Einzigartigkeit, ungewöhnliche Settings, Geschehnisse?",
    "Struktur": "Hat die Geschichte eine veständliche und schlüssige Erzählform? Ist sie dem "
                            "Alter des Kindes angepasst (Themen, Wortschatz, Komplexität)? Ist sie "
                            "gut strukturiert: Einleitung, Hauptteil, Schluss?",
}

n = 5 # Anzahl der Geschichten

DefaultSettings()


if st.session_state["page"] == "generator":
    st.session_state["prompt"] = InitializeSession(n)

elif st.session_state["page"] == "annotation":
    prompt = st.session_state.get("prompt", "")
    AnnotationSection(prompt, criteria)