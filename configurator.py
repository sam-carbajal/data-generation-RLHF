import json
import streamlit as st
from st_draggable_list import DraggableList
from annotation_page import AnnotationSection
from startpage import DefaultSettings, InitializeSession

criteria = {
    "Inhaltliche Passung": "Aus kindlicher Perspektive mutmaßlich erkennbarer inhaltlicher Bezug zwischen "
                        "Prompt und Resultat",
    "Schlüssige Handlung": "Aus kindlicher Perspektive mutmaßlich schlüssige Handlung",
    "Stimulation & Immersion": "Aus kindlicher Perspektive mutmaßlich stimulierende Erzählung "
                                "(z. B. lustig, spannend, immersiv)",
    "Natürliche Sprache": "Aus pädagogischer Perspektive natürliche Gestalt der Sprache",
    "Sprachliche Fokussierung": "Aus pädagogischer Perspektive sprachlich fokussiert "
                                "(viele kurze, verständliche Sätze und viel einfaches Vokabular; "
                                "gezielt einzelne „Stepping Stones“, also herausfordernde Sätze und Vokabeln; "
                                "nur einfache Sprache oder zu schwere Sprache → niedriger Score, ausgewogene "
                                "Mischung → hoher Score)",
    "Pädagogisch schlüssige Handlung": "Aus pädagogischer Perspektive ansprechende Handlung mit schlüssiger "
                                "Ereignisabfolge, angemessener Konfliktdarstellung, interessanten Wendungen"
}

n = 5 # Anzahl der Geschichten

DefaultSettings()

prompt = ""

if st.session_state["page"] == "generator":
    InitializeSession(n)

elif st.session_state["page"] == "annotation":
    AnnotationSection(prompt, criteria)