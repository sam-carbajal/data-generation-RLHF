import json
import streamlit as st
from st_draggable_list import DraggableList
from annotation_page import AnnotationSection
from startpage import DefaultSettings, InitializeSession

criteria = {
    "Clarity_of_Moral": "How clearly does the story express its moral or lesson?",
    "Age_Appropriateness": "Is the story suitable for the target age group?",
    "Emotional_Resonance": "Does the story engage emotions in a positive, age-appropriate way?",
    "Engagement_Creativity": "Is the story creative and fun for children?",
    "Potential_for_Harm": "Does the story contain harmful or inappropriate elements?"
}

n = 2 # Anzahl der Geschichten

DefaultSettings()

prompt = ""

if st.session_state["page"] == "generator":
    InitializeSession(n)

elif st.session_state["page"] == "annotation":
    AnnotationSection(prompt, criteria)