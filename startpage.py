import streamlit as st
from ai_models import GenerateResponse, ClientKey

def DefaultSettings():
    left, middle, m2, right = st.columns(4)
    if right.button("Session neustarten"):
        for key in ["story_pool", "prompt", "selected_indices", "rankings"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state["page"] = "generator"
        st.rerun()

    # Initialize session state defaults
    if "story_pool" not in st.session_state:
        st.session_state["story_pool"] = []

    if "page" not in st.session_state:
        st.session_state["page"] = "generator"

    if "selected_indices" not in st.session_state:
        st.session_state["selected_indices"] = []

    if "rankings" not in st.session_state:
        st.session_state["rankings"] = {}

def GenerationButton(anfang_text, num_stories, client_key, model, prompt, temperature):
    if st.button(f"{anfang_text}"):
        with st.spinner("Geschichten werden generiert..."):
            new_items = []
            for i in range(num_stories):
                response = GenerateResponse(client_key, model, prompt, temperature)
                new_items.append({"text": response, "model": model})
                #return st.session_state["story_pool"].append({
                #    "text": response,
                #    "model": model
                #})
            st.session_state["story_pool"].extend(new_items)
        st.success(f"{len(new_items)} Geschichten generiert.")
        st.rerun()

def InitializeSession(n):
    st.title("KI Generator + Annotationen")
    model = st.selectbox(
        "Wähle ein Modell:",
        ["gemini-2.5-pro", "gpt-4o-mini", "gpt-4o", "gpt-5", "deepseek", "grok"],
        index=0  # Standard: Gemini
    )
    client_key = ClientKey(model)
    temperature = st.slider("Kreativität der Antworten (Temperature)", 0.0, 0.5, 0.7, 1.0, 1.3, 1.5, 2.0)
    prompt = ""
    prompt = st.text_input("Prompt eingeben")
    if len(st.session_state["story_pool"]) == 0:
        num_stories = st.slider("Anzahl der zu generierenden Geschichten", 1, 10, 2)
        GenerationButton("Generiere Geschichten", num_stories, client_key, model, prompt, temperature)
    else:
        num_new_stories = st.slider("Anzahl der zu generierenden neuen Stories", 1, 5, 1)
        GenerationButton("Generiere eine neue Geschichte", num_new_stories, client_key, model, prompt, temperature)
        AnnotationSelection(n)
    return prompt

def AnnotationSelection(n):
    if st.session_state["story_pool"]:
            st.subheader("Erstellte Geschichten:")
            for idx, s in enumerate(st.session_state["story_pool"]):
                with st.expander(f"Story {idx+1} - {s['model']}"):
                    st.write(s['text'])

            selected_indices = st.multiselect(
                f"Wähle bis zu {n} Geschichten für Annotationen aus.", 
                options=list(range(len(st.session_state["story_pool"]))),
                format_func=lambda i: f"Story {i+1}",
                default=st.session_state["selected_indices"],  # bisherige Auswahl beibehalten
                key="story_selector"
            )

            st.session_state["selected_indices"] = selected_indices

            if "show_annotation" not in st.session_state:
                st.session_state["show_annotation"] = False
    
            if len(selected_indices) == n:
                l, m, m2, m3, m4, m5, r = st.columns(7)
                if r.button("Weiter", key="go_annotation"):
                    if len(selected_indices) != n:
                        st.warning(f"Bitte wähle genau {n} Geschichten für die Annotation aus!")
                    else:
                        st.session_state["page"] = "annotation"
