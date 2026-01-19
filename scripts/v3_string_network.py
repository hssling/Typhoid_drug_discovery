"""
HDT v3.0: Network Medicine Layer
Queries STRING-db API for Protein-Protein Interactions (PPI) and calculates centrality.
"""

import pandas as pd
import requests
import networkx as nx
from pathlib import Path
import time
import json

BASE_DIR = Path(__file__).parent.parent
STRING_API_URL = "https://string-db.org/api"
OUTPUT_FORMAT = "json"
METHOD = "network"

def get_string_network(genes, species=9606):
    """
    Fetch interaction network from STRING-db for a list of human genes.
    """
    print(f"Querying STRING-db for {len(genes)} genes...")
    
    params = {
        "identifiers": "%0d".join(genes), # expect newline separated
        "species": species,
        "caller_identity": "Typhoid_HDT_Pipeline_v3",
        "required_score": 700 # High confidence
    }
    
    request_url = f"{STRING_API_URL}/{OUTPUT_FORMAT}/{METHOD}"
    
    try:
        response = requests.post(request_url, data=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error querying STRING-db: {e}")
        return None

def main():
    print("="*50)
    print("PHASE 1: NETWORK MEDICINE (INTERACTOME ANALYSIS)")
    print("="*50)
    
    # Load authentic gene signature (v2.0 results)
    input_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked_authentic.csv'
    if not input_path.exists():
        input_path = BASE_DIR / 'data' / 'gene_signature_verified.csv'
        genes_df = pd.read_csv(input_path, comment='#')
    else:
        genes_df = pd.read_csv(input_path)
    
    # Get top 50 genes for network analysis
    genes = genes_df['Symbol'].head(50).tolist()
    
    # Fetch network from STRING
    network_data = get_string_network(genes)
    
    if not network_data:
        print("Failed to retrieve network data.")
        return

    # Build NetworkX graph
    G = nx.Graph()
    for edge in network_data:
        G.add_edge(edge['preferredName_A'], edge['preferredName_B'], weight=edge['score'])
    
    print(f"Built interactome graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Calculate Centrality Metrics
    degree_centrality = nx.degree_centrality(G)
    try:
        betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
    except:
        betweenness_centrality = nx.betweenness_centrality(G)
        
    # Scale to 0-1
    def scale_dict(d):
        if not d: return {}
        max_val = max(d.values())
        if max_val == 0: return {k: 0 for k in d}
        return {k: v / max_val for k, v in d.items()}

    scaled_degree = scale_dict(degree_centrality)
    scaled_betweenness = scale_dict(betweenness_centrality)
    
    # Compile scores for our query genes
    results = []
    for gene in genes:
        results.append({
            'Symbol': gene,
            'Degree_Centrality': scaled_degree.get(gene, 0),
            'Betweenness_Centrality': scaled_betweenness.get(gene, 0),
            'Network_Hub_Score': (scaled_degree.get(gene, 0) * 0.5 + scaled_betweenness.get(gene, 0) * 0.5)
        })
    
    results_df = pd.DataFrame(results)
    output_path = BASE_DIR / 'outputs' / 'tables' / 'v3_network_scores.csv'
    results_df.to_csv(output_path, index=False)
    
    print(f"Network analysis complete. Results saved to {output_path.name}")
    print("\nTop Network Hubs:")
    print(results_df.sort_values('Network_Hub_Score', ascending=False).head(10))

if __name__ == "__main__":
    main()
