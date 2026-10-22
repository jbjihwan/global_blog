# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_cover_image(out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100) # 1200 x 630 px
    
    # Background
    fig.patch.set_facecolor('#0F172A') # Dark slate navy
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 63)
    ax.axis('off')
    
    # Stanford accent badge
    badge = patches.FancyBboxPatch((8, 48), 34, 7, boxstyle="round,pad=0.5", ec="#E11D48", fc="#881337", lw=1.5)
    ax.add_patch(badge)
    ax.text(25, 51.5, "STANFORD CS146S CURRICULUM", color="#FECDD3", fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Title
    ax.text(8, 41, "The Modern Software Developer", color="#F8FAFC", fontsize=24, fontweight='bold', ha='left', va='center')
    ax.text(8, 34, "The Paradigm Shift: From Code Typist to Agent Conductor", color="#38BDF8", fontsize=15, fontweight='semibold', ha='left', va='center')
    
    # Subtitle / Concepts
    ax.text(8, 27, "Spec-Driven Development (SDD) • Agentic Workflows • Model Context Protocol (MCP) • Loop Engineering", 
            color="#94A3B8", fontsize=11, ha='left', va='center')
    
    # Architecture Pipeline Boxes (Visual diagram)
    # Box 1: Human Architect
    box1 = patches.FancyBboxPatch((8, 6), 28, 14, boxstyle="round,pad=0.8", ec="#38BDF8", fc="#1E293B", lw=1.5)
    ax.add_patch(box1)
    ax.text(22, 16.5, "Human Architect", color="#38BDF8", fontsize=13, fontweight='bold', ha='center', va='center')
    ax.text(22, 12.5, "• Spec Formulation (What)\n• Threat Modeling & Security\n• Architectural Review", 
            color="#E2E8F0", fontsize=9.5, ha='center', va='center')
    
    # Arrow 1 -> 2
    ax.annotate('', xy=(42, 13), xytext=(38, 13), arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=2))
    
    # Box 2: Autonomous Agent Loop
    box2 = patches.FancyBboxPatch((44, 6), 34, 14, boxstyle="round,pad=0.8", ec="#A855F7", fc="#1E293B", lw=1.5)
    ax.add_patch(box2)
    ax.text(61, 16.5, "Agentic Workflow Loop", color="#C084FC", fontsize=13, fontweight='bold', ha='center', va='center')
    ax.text(61, 12.5, "• Multi-File Context Graph\n• Autonomous Tool Calling (MCP)\n• Test-Driven Self-Correction", 
            color="#E2E8F0", fontsize=9.5, ha='center', va='center')
    
    # Arrow 2 -> 3
    ax.annotate('', xy=(84, 13), xytext=(80, 13), arrowprops=dict(arrowstyle="->", color="#A855F7", lw=2))
    
    # Box 3: Production Pipeline
    box3 = patches.FancyBboxPatch((86, 6), 26, 14, boxstyle="round,pad=0.8", ec="#10B981", fc="#1E293B", lw=1.5)
    ax.add_patch(box3)
    ax.text(99, 16.5, "Verified System", color="#34D399", fontsize=13, fontweight='bold', ha='center', va='center')
    ax.text(99, 12.5, "• Deterministic CI/CD Gate\n• Zero-Hallucination Delivery\n• 10x Scaled Engineering", 
            color="#E2E8F0", fontsize=9.5, ha='center', va='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=100, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    target_img = r"D:\ai\antigravity\global_blog\blog\2026-10-22-stanford-cs146s-1\images\01_cs146s_human_agent_orchestration.png"
    generate_cover_image(target_img)
