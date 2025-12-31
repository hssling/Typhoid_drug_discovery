"""
Generate publication-quality figures for Typhoid HDT Pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
plt.style.use('seaborn-v0_8-whitegrid')

def figure1_target_prioritization():
    """Figure 1: Top 20 Target Prioritization with Phase Coloring"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'targets_ranked.csv')
    top20 = df.head(20)
    
    def get_color(phase):
        if phase == 'Acute':
            return '#E74C3C'  # Red - acute infection
        elif phase == 'Carrier':
            return '#3498DB'  # Blue - chronic carrier
        else:
            return '#9B59B6'  # Purple - both phases
    
    colors = [get_color(p) for p in top20['Phase_Relevance']]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(range(len(top20)), top20['Composite_Score'], color=colors, edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(range(len(top20)))
    ax.set_yticklabels(top20['Symbol'], fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    
    ax.set_xlabel('Composite Score', fontsize=12, fontweight='bold')
    ax.set_title('Top 20 Host-Directed Therapy Targets for Typhoid Fever\n(Addressing MDR/XDR Salmonella Typhi)', fontsize=14, fontweight='bold')
    
    for i, (bar, val) in enumerate(zip(bars, top20['Composite_Score'])):
        ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=9)
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='Acute Infection'),
        Patch(facecolor='#3498DB', label='Chronic Carrier'),
        Patch(facecolor='#9B59B6', label='Both Phases')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure1_target_prioritization.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure1_target_prioritization.png")

def figure2_compound_distribution():
    """Figure 2: Compound Distribution"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'compounds_ranked.csv')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    phase_counts = df['Phase'].value_counts().sort_index(ascending=False)
    phase_labels = {4: 'FDA Approved', 3: 'Phase III', 2: 'Phase II', 1: 'Phase I/Preclinical'}
    
    colors = ['#27AE60', '#F1C40F', '#E67E22', '#E74C3C']
    wedges, texts, autotexts = axes[0].pie(
        phase_counts.values, 
        labels=[phase_labels.get(p, f'Phase {p}') for p in phase_counts.index],
        autopct='%1.1f%%',
        colors=colors[:len(phase_counts)],
        explode=[0.05 if p == 4 else 0 for p in phase_counts.index],
        shadow=True
    )
    axes[0].set_title('A. Clinical Development Phase\n(n={})'.format(len(df)), fontsize=12, fontweight='bold')
    
    target_counts = df.groupby('Related_Gene').size().sort_values(ascending=True).tail(10)
    axes[1].barh(range(len(target_counts)), target_counts.values, color='teal', edgecolor='black')
    axes[1].set_yticks(range(len(target_counts)))
    axes[1].set_yticklabels(target_counts.index, fontsize=10)
    axes[1].set_xlabel('Number of Compounds', fontsize=11)
    axes[1].set_title('B. Compounds per Target Gene', fontsize=12, fontweight='bold')
    
    for i, v in enumerate(target_counts.values):
        axes[1].text(v + 0.1, i, str(v), va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure2_compound_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure2_compound_distribution.png")

def figure3_potency_by_target():
    """Figure 3: Compound Potency by Target"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'compounds_ranked.csv')
    
    potency_by_gene = df.groupby('Related_Gene')['pChEMBL'].agg(['mean', 'max', 'count'])
    potency_by_gene = potency_by_gene.sort_values('max', ascending=False).head(15)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(potency_by_gene)))
    
    bars = ax.barh(range(len(potency_by_gene)), potency_by_gene['max'], color=colors, edgecolor='black')
    
    ax.set_yticks(range(len(potency_by_gene)))
    ax.set_yticklabels(potency_by_gene.index, fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    
    ax.set_xlabel('Maximum pChEMBL (Higher = More Potent)', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Typhoid Targets by Compound Potency', fontsize=14, fontweight='bold')
    
    ax.axvline(x=6.0, color='red', linestyle='--', alpha=0.7, label='1 µM threshold')
    ax.axvline(x=8.0, color='green', linestyle='--', alpha=0.7, label='10 nM threshold')
    
    for i, (idx, row) in enumerate(potency_by_gene.iterrows()):
        ax.text(row['max'] + 0.1, i, f'{row["max"]:.1f}', va='center', fontsize=9)
    
    ax.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure3_target_potency.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure3_target_potency.png")

def figure4_pathway_heatmap():
    """Figure 4: Pathway Analysis"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'targets_ranked.csv')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    
    pathway_counts = df.groupby('Pathway').size().sort_values(ascending=True)
    pathway_scores = df.groupby('Pathway')['Composite_Score'].mean().sort_values(ascending=True)
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(pathway_counts)))
    axes[0].barh(range(len(pathway_counts)), pathway_counts.values, color=colors, edgecolor='black')
    axes[0].set_yticks(range(len(pathway_counts)))
    axes[0].set_yticklabels([p.replace('_', ' ').title() for p in pathway_counts.index], fontsize=10)
    axes[0].set_xlabel('Number of Targets', fontsize=11)
    axes[0].set_title('A. Targets per Pathway', fontsize=12, fontweight='bold')
    
    for i, v in enumerate(pathway_counts.values):
        axes[0].text(v + 0.1, i, str(v), va='center', fontsize=9)
    
    colors2 = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(pathway_scores)))
    axes[1].barh(range(len(pathway_scores)), pathway_scores.values, color=colors2, edgecolor='black')
    axes[1].set_yticks(range(len(pathway_scores)))
    axes[1].set_yticklabels([p.replace('_', ' ').title() for p in pathway_scores.index], fontsize=10)
    axes[1].set_xlabel('Mean Composite Score', fontsize=11)
    axes[1].set_title('B. Mean Score by Pathway', fontsize=12, fontweight='bold')
    
    for i, v in enumerate(pathway_scores.values):
        axes[1].text(v + 0.01, i, f'{v:.3f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure4_pathway_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure4_pathway_heatmap.png")

def figure5_typhoid_timeline():
    """Figure 5: Typhoid Infection Timeline and HDT Opportunities"""
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # Timeline (weeks)
    x = np.linspace(0, 8, 500)
    
    # Bacterial load curve
    bacterial = 100 * np.exp(-0.3 * (x - 2)**2) * (1 + 0.2 * np.sin(x*2))
    bacterial[x < 0.5] = bacterial[x < 0.5] * (x[x < 0.5] / 0.5)
    
    # Immune response curve
    immune = 80 * (1 - np.exp(-0.5 * x)) * np.exp(-0.1 * x)
    
    # Carrier persistence
    carrier = 30 * (1 - np.exp(-0.2 * x)) * (x > 4)
    
    ax.fill_between(x, 0, bacterial, alpha=0.3, color='red', label='Bacterial Burden')
    ax.fill_between(x, 0, immune, alpha=0.3, color='blue', label='Immune Response')
    ax.fill_between(x, 0, carrier, alpha=0.3, color='orange', label='Chronic Carriage')
    ax.plot(x, bacterial, 'r-', linewidth=2)
    ax.plot(x, immune, 'b-', linewidth=2)
    ax.plot(x, carrier, 'orange', linewidth=2)
    
    # Phase labels
    ax.annotate('INCUBATION\n& INVASION', xy=(1, 75), fontsize=10, fontweight='bold', color='darkred', ha='center')
    ax.annotate('ACUTE\nFEVER', xy=(2.5, 85), fontsize=10, fontweight='bold', color='darkred', ha='center')
    ax.annotate('RESOLUTION', xy=(4.5, 50), fontsize=10, fontweight='bold', color='darkblue', ha='center')
    ax.annotate('CARRIER\nSTATE', xy=(6.5, 35), fontsize=10, fontweight='bold', color='darkorange', ha='center')
    
    # HDT interventions
    ax.annotate('', xy=(2, 85), xytext=(2, 100),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(2, 103, 'Autophagy enhancers\nmTOR inhibitors\nIron chelators', ha='center', fontsize=9, color='green')
    
    ax.annotate('', xy=(4, 55), xytext=(4, 75),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))
    ax.text(4, 78, 'Inflammasome\nmodulators\nMacrophage activators', ha='center', fontsize=9, color='purple')
    
    ax.annotate('', xy=(6.5, 25), xytext=(6.5, 45),
                arrowprops=dict(arrowstyle='->', color='brown', lw=2))
    ax.text(6.5, 48, 'Bile acid modulators\nBiofilm disruption', ha='center', fontsize=9, color='brown')
    
    ax.set_xlabel('Weeks After Infection', fontsize=12, fontweight='bold')
    ax.set_ylabel('Disease Activity / Response', fontsize=12, fontweight='bold')
    ax.set_title('Typhoid Fever Timeline and Host-Directed Therapy Intervention Windows', fontsize=14, fontweight='bold', pad=15)
    
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=4, color='gray', linestyle='--', alpha=0.5)
    
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right')
    
    plt.tight_layout(pad=2.0)
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure5_typhoid_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure5_typhoid_timeline.png")

if __name__ == '__main__':
    print("Generating figures...")
    print("="*50)
    
    figure1_target_prioritization()
    figure2_compound_distribution()
    figure3_potency_by_target()
    figure4_pathway_heatmap()
    figure5_typhoid_timeline()
    
    print("="*50)
    print("All figures generated successfully!")
