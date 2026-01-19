"""
Typhoid HDT v3.0+: Interactive Discovery Dashboard
Professional interface for exploring host-directed therapy targets.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Page Config
st.set_page_config(page_title="Typhoid HDT v3.0+ Mastery", layout="wide", page_icon="🧬")

@st.cache_data
def load_mastery_data():
    path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_v4_mastery.csv'
    if path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_drug_data():
    path = BASE_DIR / 'outputs' / 'tables' / 'compounds_from_chembl.csv'
    if path.exists():
        return pd.read_csv(path)
    return None

df_targets = load_mastery_data()
df_drugs = load_drug_data()

# HEADER
st.title("🧬 Typhoid HDT Discovery Dashboard v3.0+")
st.markdown("### Convergent Evidence-Based Drug Repurposing Explorer")
st.sidebar.image("https://img.icons8.com/plasticine/200/dna-helix.png", width=100)
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Main Menu", ["🏆 Discovery Leaderboard", "🕸️ Host Interactome", "🧪 Target Deep-Dive", "💊 ChEMBL Drug Library"])

if df_targets is not None:
    if menu == "🏆 Discovery Leaderboard":
        st.subheader("Final v4.0 Master Prioritization List")
        st.info("Consolidating: Transcriptomics, Network Medicine, Structural Fit, Single-Cell, and Causal Inference.")
        
        # Dashboard Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Analyzed Targets", len(df_targets))
        col2.metric("Causal Verified", len(df_targets[df_targets['Causal_Evidence'] == 'Verified (GWAS)']))
        col3.metric("Structural Fit (Mean)", f"{df_targets['V3_Score'].mean():.2f}")
        col4.metric("Top Hit", df_targets.iloc[0]['Symbol'])
        
        st.dataframe(df_targets[['Final_Rank', 'Symbol', 'Final_Mastery_Score', 'Causal_Evidence', 'Pathway', 'Druggability']].style.background_gradient(subset=['Final_Mastery_Score'], cmap='viridis'), use_container_width=True)
        
        fig = px.scatter(df_targets, x='Network_Hub_Score', y='Log2FC_Thompson', size='Cellular_Specificity_Score', hue='Causal_Evidence', hover_name='Symbol', title="The Convergent Evidence Matrix")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "🕸️ Host Interactome":
        st.subheader("The Typhoid Host Interactome (Network)")
        st.markdown("Mapping essential bottlenecks in the Salmonella host response.")
        
        fig = px.bar(df_targets.head(15), x='Symbol', y='Network_Hub_Score', color='Network_Hub_Score', title="Interactome Centrality (Hub Support)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.image(str(BASE_DIR / 'outputs' / 'figures' / 'figure6_interactome.png'))

    elif menu == "🧪 Target Deep-Dive":
        st.subheader("Target Dimensionality Analysis")
        selected_gene = st.selectbox("Select a target to inspect:", df_targets['Symbol'].tolist())
        
        target_row = df_targets[df_targets['Symbol'] == selected_gene].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write(f"**Target:** {selected_gene}")
            st.write(f"**Pathway:** {target_row['Pathway']}")
            st.write(f"**Druggability:** {target_row['Druggability']}")
            st.success(f"**Causal Evidence:** {target_row['Causal_Evidence']}")
            
            # Radar Plot
            categories = ['Transcriptomics', 'Network Hub', 'Cellular Spec', 'Genetic Support']
            values = [
                abs(target_row['Log2FC_Thompson']) / 5, 
                target_row['Network_Hub_Score'], 
                target_row['Cellular_Specificity_Score'],
                target_row['Genetic_Support_Score']
            ]
            
            fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False, title=f"{selected_gene} Evidence Profile")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader(f"Repurposing Candidates for {selected_gene}")
            if df_drugs is not None:
                gene_drugs = df_drugs[df_drugs['Gene'] == selected_gene].sort_values('pChEMBL', ascending=False)
                if not gene_drugs.empty:
                    st.dataframe(gene_drugs[['Drug_Name', 'pChEMBL', 'Max_Phase']])
                else:
                    st.warning("No compounds found for this target in ChEMBL snapshot.")

    elif menu == "💊 ChEMBL Drug Library":
        st.subheader("Repurposing Library Explorer")
        if df_drugs is not None:
            st.write(f"Total Compounds Mined: {len(df_drugs)}")
            phase_filter = st.multiselect("Filter by Clinical Phase:", [0, 1, 2, 3, 4], default=[4])
            
            filtered_drugs = df_drugs[df_drugs['Max_Phase'].isin(phase_filter)]
            st.dataframe(filtered_drugs.sort_values('pChEMBL', ascending=False), use_container_width=True)
            
            fig = px.histogram(df_drugs, x='pChEMBL', color='Max_Phase', title="Potency Distribution (pChEMBL)")
            st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Mastery data not found. Please run the v3.0+ pipeline scripts first.")

st.sidebar.markdown("---")
st.sidebar.info("Developed by Dr. Siddalingaiah H S | Typhoid HDT Discovery v3.0")
