import streamlit as st
import pandas as pd
import re
import time

# Dummy API Call for Relation Extraction
def dummy_relation_extraction(text):
    """Simulates relation extraction and returns all possible relations."""
    time.sleep(2)  # Simulate processing delay
    all_relations = [
        ("GeneA", "interacts with", "ProteinB"),
        ("DrugX", "treats", "DiseaseY"),
        ("ProteinC", "associated with", "DiseaseZ"),
        ("GeneA", "expressed in", "TissueY"),
        ("DrugX", "inhibits", "ProteinB"),
    ]
    return all_relations

# Function to filter relations based on selected entities
def filter_relations(relations, selected_entities):
    """Filters relations to show only those involving selected entities."""
    if not selected_entities:
        return relations  # No filtering if no entities are selected
    
    filtered = []
    
    # Singularize the selected entities for better matching
    singular_entities = [sel.rstrip('s').lower() for sel in selected_entities]

    for relation in relations:
        entity1, _, entity2 = relation
        
        # Check if either entity1 or entity2 partially/fully matches selected entities
        if any(singular in entity1.lower() or singular in entity2.lower() for singular in singular_entities):
            filtered.append(relation)
    
    return filtered

# Initialize Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "loading" not in st.session_state:
    st.session_state.loading = False

# Layout and Title
st.title("Biomedical Relation Extraction")

# Input Field for Biomedical Text
input_text = st.text_area("Enter Biomedical Text:", placeholder="Type or paste text here...")

# Multi-select Dropdown for Entity Types
entity_options = ["Genes", "Proteins", "Diseases", "Drugs", "Tissues"]
selected_entities = st.multiselect(
    "Select Entities to display Relations for (Choose nothing to extract all Relations by Default):",
    entity_options,
    default=[]
)

# Extract Relations Button
if st.button("Extract Relations"):
    if input_text.strip():  # Check if input is not empty
        st.session_state.loading = True
        st.session_state.chat_history.append({
            "text": input_text,
            "selected_entities": selected_entities,
            "relations": None
        })
        st.rerun()  # Refresh to display the input immediately
    else:
        st.warning("Please enter some biomedical text.")


# If loading, simulate the API call and update the last entry with relations
if st.session_state.loading:
    with st.spinner("Extracting relations..."):
        # Get the last input details
        last_input = st.session_state.chat_history[-1]
        
        # Dummy API Call for Relation Extraction
        relations = dummy_relation_extraction(last_input["text"])
        
        # Update the last chat history item with the extracted relations
        st.session_state.chat_history[-1]["relations"] = relations
    
    # Stop loading and refresh to show the relations
    st.session_state.loading = False
    st.rerun()


# Display Chat History
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**Input Text:** {chat['text']}")
    # st.markdown(f"**Selected Entities:** {', '.join(chat['selected_entities']) if chat['selected_entities'] else 'All'}")
    st.markdown(f"**Selected Entities:** {', '.join(chat.get('selected_entities', [])) or 'All'}")


    # Display Extracted Relations
    if chat["relations"] is not None:
        # st.markdown("**Filtered Relations:**")
        # filtered_relations = filter_relations(chat["relations"], chat["selected_entities"])
        filtered_relations = filter_relations(chat["relations"], chat.get("selected_entities", []))

        
        if filtered_relations:
            # for relation in filtered_relations:
            #     st.markdown(f"- {relation[0]} **{relation[1]}** {relation[2]}")
            st.markdown("#### Extracted Relations")

            # Prepare table data
            table_data = []
            for relation in filtered_relations:
                entity1 = relation[0]
                entity2 = relation[2]
                relation_type = relation[1]
                table_data.append([entity1, entity2, relation_type])

            df = pd.DataFrame(table_data, columns=['Entity 1', 'Entity 2', 'Relation Type'])
            df.index = df.index + 1
            
            # Display the table
            st.table(df)
        else:
            st.markdown("_No matching relations found for the selected entities._")
    else:
        st.markdown("_Processing..._")

    st.divider()
