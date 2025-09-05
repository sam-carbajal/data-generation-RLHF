import json
import streamlit as st
from st_draggable_list import DraggableList
from annotation_page import AnnotationSection
from startpage import DefaultSettings, InitializeSession

criteria = {
    "K_Bezug": "Aus kindlicher Perspektive mutmaßlich erkennbarer inhaltlicher Bezug zwischen "
                        "Prompt und Resultat",
    "K_konsistent": "Aus kindlicher Perspektive mutmaßlich schlüssige Handlung",
    "K_Stimulus": "Aus kindlicher Perspektive mutmaßlich stimulierende Erzählung "
                                "(z. B. lustig, spannend, immersiv)",
    "P_Idiomacy": "Aus pädagogischer Perspektive natürliche Gestalt der Sprache",
    "P_Cogn_Appr": "Aus pädagogischer Perspektive sprachlich fokussiert "
                                "(viele kurze, verständliche Sätze und viel einfaches Vokabular; "
                                "gezielt einzelne „Stepping Stones“, also herausfordernde Sätze und Vokabeln; "
                                "nur einfache Sprache oder zu schwere Sprache → niedriger Score, ausgewogene "
                                "Mischung → hoher Score)",
    "P_Ped_Appr": "Aus pädagogischer Perspektive ansprechende Handlung mit schlüssiger "
                                "Ereignisabfolge, angemessener Konfliktdarstellung, interessanten Wendungen"
}

n = 5 # Anzahl der Geschichten

DefaultSettings()

#prompt = ""

if st.session_state["page"] == "generator":
    st.session_state["prompt"] = InitializeSession(n)

elif st.session_state["page"] == "annotation":
    prompt = st.session_state.get("prompt", "")
    AnnotationSection(prompt, criteria)