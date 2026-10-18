import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Output directory for images in default blog and all 3 localized folders
IMAGE_DIRS = [
    r"D:\ai\antigravity\global_blog\blog\2026-10-18-static-site-security-hardening\images",
    r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-10-18-static-site-security-hardening\images",
    r"D:\ai\antigravity\global_blog\i18n\ja\docusaurus-plugin-content-blog\2026-10-18-static-site-security-hardening\images",
    r"D:\ai\antigravity\global_blog\i18n\es\docusaurus-plugin-content-blog\2026-10-18-static-site-security-hardening\images",
]

for d in IMAGE_DIRS:
    os.makedirs(d, exist_ok=True)

def generate_threat_model_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    # Left box: Traditional Dynamic Web Server
    rect1 = patches.FancyBboxPatch((0.5, 1.0), 3.8, 3.5, boxstyle="round,pad=0.2", 
                                   linewidth=2, edgecolor='#ef4444', facecolor='#1e293b')
    ax.add_patch(rect1)
    ax.text(2.4, 4.1, "Dynamic Server (Node/Django)", color='#f87171', fontsize=12, fontweight='bold', ha='center')
    ax.text(2.4, 3.4, "- Active Listening Daemon (Port 80/443)\n- Database Connection (SQLi, Auth)\n- Dynamic Template Execution (RCE)\n- Server Memory Exploitation\n- npm Vulnerabilities = LIVE THREAT", 
            color='#cbd5e1', fontsize=9, ha='center', va='center')
    
    # Right box: Static Site Generator (Docusaurus + GitHub Pages)
    rect2 = patches.FancyBboxPatch((5.7, 1.0), 3.8, 3.5, boxstyle="round,pad=0.2", 
                                   linewidth=2, edgecolor='#10b981', facecolor='#1e293b')
    ax.add_patch(rect2)
    ax.text(7.6, 4.1, "Static Site (GitHub Pages CDN)", color='#34d399', fontsize=12, fontweight='bold', ha='center')
    ax.text(7.6, 3.4, "- Pre-compiled Pure HTML/CSS/JS\n- NO Running Node Server in Prod\n- NO Database / Backend Ports\n- Immune to Server-Side RCE / DoS\n- npm audit in Bundler = ZERO RUNTIME RISK", 
            color='#cbd5e1', fontsize=9, ha='center', va='center')
    
    # Title
    ax.text(5.0, 4.8, "Threat Modeling: Dynamic Server vs Static Site Generation (SSG)", color='#ffffff', fontsize=13, fontweight='bold', ha='center')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 5.2)
    ax.axis('off')
    plt.tight_layout()
    
    out_name = "01_threat_model.png"
    for d in IMAGE_DIRS:
        fig.savefig(os.path.join(d, out_name), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated 01_threat_model.png")

def generate_security_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    steps = [
        ("1. Git Secret Scanning", "Regex detection for API keys,\nPAT tokens & certs", "#38bdf8"),
        ("2. PII Protection", "Phone & Resident Number\nRegex validation", "#818cf8"),
        ("3. Supply Chain Audit", "Rational triage of npm audit\nwithout breaking builds", "#fbbf24"),
        ("4. Client Privacy", "Referrer Policy, Giscus iframe\n& Strict .gitignore", "#34d399"),
    ]
    
    for i, (title, desc, col) in enumerate(steps):
        x = 0.5 + i * 2.35
        rect = patches.FancyBboxPatch((x, 1.0), 2.1, 2.5, boxstyle="round,pad=0.15",
                                      linewidth=2, edgecolor=col, facecolor='#1e293b')
        ax.add_patch(rect)
        ax.text(x + 1.05, 3.1, title, color=col, fontsize=10, fontweight='bold', ha='center')
        ax.text(x + 1.05, 2.0, desc, color='#e2e8f0', fontsize=8.5, ha='center', va='center')
        
        if i < 3:
            arrow = patches.FancyArrowPatch((x + 2.2, 2.25), (x + 2.45, 2.25),
                                           arrowstyle='->', mutation_scale=15, color='#94a3b8', linewidth=2)
            ax.add_patch(arrow)
            
    ax.text(5.0, 4.2, "Comprehensive 4-Layer Static Blog Security Hardening Pipeline", color='#ffffff', fontsize=13, fontweight='bold', ha='center')
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 4.6)
    ax.axis('off')
    plt.tight_layout()
    
    out_name = "02_security_pipeline.png"
    for d in IMAGE_DIRS:
        fig.savefig(os.path.join(d, out_name), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated 02_security_pipeline.png")

if __name__ == "__main__":
    generate_threat_model_diagram()
    generate_security_pipeline_diagram()
