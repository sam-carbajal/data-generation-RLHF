import json
import streamlit as st
from datetime import datetime
from st_draggable_list import DraggableList


def AnnotationSection(prompt, criteria):
    st.title("Annotation Abschnitt")
    st.markdown("Bitte bewerte die Geschichten anhand der Kriterien.")

    tab_names = list(criteria.keys())
    tab_criteria = list(criteria.values())
    tabs = st.tabs(tab_names)

    rankings, justifs = Ranking(tabs, tab_names, tab_criteria)
    annotation = AnnotationFormat(rankings, prompt,justifs)

    DownloadJSON(annotation, tab_names)

    if st.button("Zurück", key="generator"):
        st.session_state["page"] = "generator"


def Ranking(tabs, tab_names, tab_criteria):
    rankings = st.session_state.setdefault("rankings", {})
    justifs = st.session_state.setdefault("justifications", {})

    for t_idx, (tab, name) in enumerate(zip(tabs, tab_criteria)):
        with tab:
            st.write(f"Beschreibung: **{tab_criteria[t_idx]}**")
            st.text("Zum Lesen der Geschichten:")

            stories = []
            for pos, idx in enumerate(st.session_state["selected_indices"], start=1):
                raw = st.session_state["story_pool"][idx]
                text = raw["text"] if isinstance(raw, dict) else str(raw)
                with st.expander(f"Story {idx+1}", expanded=False):
                    st.write(text)
                stories.append({
                    "id": idx,
                    "order": pos,
                    "name": f"Story {idx+1}",
                    "story": text,
                })

            st.write("Bitte die Geschichten einordnen:")
            slist = DraggableList(stories, key=f"drag_{name}_{t_idx}")

            ordered_items = slist if isinstance(slist, list) and slist else stories

            rankings[name] = [f"Story_{it['id']+1}" for it in ordered_items]

            st.markdown("**Kurze Begründung** (1–5 Sätze): ")
            justification = st.text_area("Erläutern Sie Ihre Reihenfolge der Geschichten. " \
                            "Bitte auf den Hauptgrund konzentrieren. **Zum Beispiel:** " \
                            "Story 3 stellt die Moral am deutlichsten heraus, " \
                            "während Story 1 die Lehre noch erkennbar macht, aber weniger klar formuliert. " \
                            "Die anderen Geschichten enthalten entweder keine klare Moral (Story 2 und 4) " \
                            "oder verpacken sie zu kompliziert (Story 5).   ",
                            key=f"just_{name}_{t_idx}")
            justifs[name] = justification

    return rankings, justifs


def AnnotationFormat(rankings, prompt, just_annot):
    
    criteria_annot = {}

    for crit, rank_list in rankings.items():
        if isinstance(rank_list, dict):
            rank_list = [v for _, v in sorted(rank_list.items())]
        else:
            rank_list = list(rank_list)

        criteria_annot[crit] = {
            "ranking": rank_list,
            "justification": just_annot.get(crit, "") or ""
        }

    annotation = {
        "prompt": prompt,
        "stories": {
            f"Story_{i+1}": (
                st.session_state["story_pool"][i]["text"]
                if isinstance(st.session_state["story_pool"][i], dict)
                else str(st.session_state["story_pool"][i])
            )
            for i in st.session_state["selected_indices"]
        },
        "criteria": criteria_annot,
    }
    return annotation


def DownloadJSON(annotation, tab_names):
    if st.button("See JSON File"):
        justifs = st.session_state.get("justifications", {})
        missing = [crit for crit in tab_names if not justifs.get(crit, "").strip()]

        if missing:
            st.warning(
                "Bitte geben Sie für alle Kriterien eine Begründung an.\n\n"
                "Fehlend: " + ", ".join(missing)
            )
        else:
            # Pretty code block with copy button
            json_str = json.dumps(annotation, indent=2, ensure_ascii=False)
            st.code(json_str, language="json")

            # Download
            filename = f"annotation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            downloaded = st.download_button(
                "⬇ Download JSON",
                json_str,
                file_name=filename,
                mime="application/json",
                key="download_annotation",
            )
            if downloaded:
                st.success("Annotation saved!")
