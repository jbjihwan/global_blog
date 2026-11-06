import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set dark theme style for technical avionics look
plt.style.use('dark_background')

OUT_DIRS = [
    r"D:\ai\antigravity\global_blog\배포대기\2026-12-04-sdc-02-stack-spike-doctrine-hypotheses\blog\images",
    r"D:\ai\antigravity\global_blog\배포대기\2026-12-04-sdc-02-stack-spike-doctrine-hypotheses\i18n\ko\images"
]

def save_fig(fig, filename):
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, filename)
        fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"[+] Saved {filename}")

# ==========================================
# FIGURE 1: 01_cover.png (1200x630 Dark Mode)
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
ax.set_facecolor('#0B0F19')
fig.patch.set_facecolor('#0B0F19')

# Grid pattern background
for x in np.linspace(0, 12, 25):
    ax.axvline(x, color='#1E293B', lw=0.5, alpha=0.5)
for y in np.linspace(0, 6.3, 14):
    ax.axhline(y, color='#1E293B', lw=0.5, alpha=0.5)

# Radar / Avionics circle overlay
circle = plt.Circle((9.8, 3.15), 2.2, color='#0EA5E9', fill=False, lw=1.5, ls='--', alpha=0.4)
ax.add_patch(circle)
circle2 = plt.Circle((9.8, 3.15), 1.2, color='#0EA5E9', fill=False, lw=1.0, ls=':', alpha=0.6)
ax.add_patch(circle2)
ax.plot([7.6, 12.0], [3.15, 3.15], color='#0EA5E9', lw=1.0, alpha=0.4)
ax.plot([9.8, 9.8], [0.95, 5.35], color='#0EA5E9', lw=1.0, alpha=0.4)

# Heading Badge
ax.text(0.8, 5.4, "AIR COMBAT MISSION REPLANNING // EPISODE 02", 
        fontsize=12, fontweight='bold', color='#38BDF8', family='monospace')

# Title
ax.text(0.8, 4.3, "Stack Spike (a) & Doctrine Hypotheses", 
        fontsize=24, fontweight='heavy', color='#F8FAFC', family='sans-serif')

# Subtitle
ax.text(0.8, 3.5, "MapLibre WebGL 165Hz · Ed25519 Delta Roundtrip · ROK 2022 Threat Matrix T1~T12", 
        fontsize=12, color='#94A3B8', family='sans-serif')

# Badges (Technical specs)
badges = [
    ("6/6 Criteria Passed", "#10B981"),
    ("Path Search 196ms (Grid 1000x1000)", "#0EA5E9"),
    ("Ed25519 Latency 1.6~23ms", "#6366F1"),
    ("MND White Paper T1~T12", "#F59E0B"),
    ("FalconView/JMPS Baseline", "#EC4899")
]

start_x = 0.8
for text, color in badges:
    bbox = dict(boxstyle="round,pad=0.4", facecolor=color, alpha=0.15, edgecolor=color, lw=1.2)
    ax.text(start_x, 2.5, text, fontsize=9.5, fontweight='bold', color=color, 
            family='monospace', bbox=bbox)
    start_x += 2.15

# Architecture micro-code box
code_text = (
    "// SPIKE (a) INVARIANTS VERIFICATION\n"
    "assert webgl_fps >= 30.0            # Actual: 164.2 fps (p95 6.2ms)\n"
    "assert mcp_latency_ms < 2000.0      # Actual: 196.4 ms (1000x1000)\n"
    "assert delta_ack.status == 'APPLIED'# Ed25519 Sig Verified in 1.6ms\n"
    "assert doctrine.grounding == 'MND22'# Threat T1~T12 Verified"
)
bbox_code = dict(boxstyle="round,pad=0.6", facecolor='#111827', edgecolor='#334155', lw=1.5)
ax.text(0.8, 0.7, code_text, fontsize=9, color='#CBD5E1', family='monospace', bbox=bbox_code)

ax.set_xlim(0, 12)
ax.set_ylim(0, 6.3)
ax.axis('off')
save_fig(fig, "01_cover.png")


# ==========================================
# FIGURE 2: 02_spike_a_benchmarks.png
# ==========================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=200)
fig.patch.set_facecolor('#0F172A')

for ax in axes:
    ax.set_facecolor('#1E293B')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#475569')
    ax.spines['bottom'].set_color('#475569')
    ax.tick_params(colors='#94A3B8')

# Panel A: MapLibre WebGL UI Pan/Zoom (FPS & Frame Time)
ax_a = axes[0]
bars = ax_a.bar(['Target\nMin Spec', 'Spike (a)\nRun 1 (Avg)', 'Spike (a)\nRun 2 (Avg)'], 
               [30.0, 164.2, 159.2], 
               color=['#EF4444', '#10B981', '#059669'], width=0.55)
ax_a.axhline(30.0, color='#F87171', ls='--', lw=1.5, label='Min SLA Threshold (30 FPS)')
ax_a.set_ylabel('Frame Rate (FPS)', color='#F1F5F9', fontsize=10, fontweight='bold')
ax_a.set_title('Criterion 1: WebGL Pan/Zoom (165Hz)', color='#F8FAFC', fontsize=11, fontweight='bold')
for bar in bars:
    y = bar.get_height()
    ax_a.text(bar.get_x() + bar.get_width()/2, y + 3, f"{y:.1f} FPS", 
              ha='center', va='bottom', color='#F8FAFC', fontsize=9, fontweight='bold')
ax_a.text(0.5, 0.45, "p95 Frame Time: 6.2 ms\nMax Frame Time: 24.4 ms\nRenderer: Radeon 610M D3D11\nFrames Dropped (>33ms): 0",
          transform=ax_a.transAxes, ha='center', fontsize=8.5, family='monospace',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#0B0F19', edgecolor='#38BDF8', lw=1),
          color='#38BDF8')
ax_a.set_ylim(0, 200)

# Panel B: 1000x1000 Grid MCP Path Search Latency
ax_b = axes[1]
runs = ['Run 1', 'Run 2', 'Run 3', 'Run 4', 'Run 5', 'Browser\nUI Call']
latencies = [196.2, 198.5, 201.1, 203.4, 199.0, 246.0]
colors = ['#0EA5E9']*5 + ['#F59E0B']
bars_b = ax_b.bar(runs, latencies, color=colors, width=0.6)
ax_b.axhline(2000.0, color='#EF4444', ls='--', lw=1.5, label='Budget Limit (2000 ms)')
ax_b.set_ylabel('Execution Latency (ms)', color='#F1F5F9', fontsize=10, fontweight='bold')
ax_b.set_title('Criterion 6: 1000x1000 MCP Path Search', color='#F8FAFC', fontsize=11, fontweight='bold')
for bar in bars_b:
    y = bar.get_height()
    ax_b.text(bar.get_x() + bar.get_width()/2, y + 10, f"{y:.1f}ms", 
              ha='center', va='bottom', color='#F8FAFC', fontsize=8, fontweight='bold')
ax_b.text(0.5, 0.70, "Budget: 2,000 ms\nActual Avg: 199.6 ms\nSpeed Margin: 10.0x Headroom\nCost Prep: 129~137 ms",
          transform=ax_b.transAxes, ha='center', fontsize=8.5, family='monospace',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#0B0F19', edgecolor='#10B981', lw=1),
          color='#34D399')
ax_b.set_ylim(0, 450)

# Panel C: Ed25519 Sign/Verify & IPC Roundtrip Latency
ax_c = axes[2]
components = ['Sign (Ed25519)', 'HTTP IPC Post', 'Verify Sig', 'Apply Delta', 'Sign ACK']
times = [0.42, 1.15, 0.58, 0.35, 0.40]
bars_c = ax_c.barh(components, times, color=['#818CF8', '#38BDF8', '#818CF8', '#34D399', '#818CF8'], height=0.55)
ax_c.set_xlabel('Component Time (ms)', color='#F1F5F9', fontsize=10, fontweight='bold')
ax_c.set_title('Criterion 2 & 3: IPC Roundtrip & Classifier', color='#F8FAFC', fontsize=11, fontweight='bold')
for bar in bars_c:
    x = bar.get_width()
    ax_c.text(x + 0.03, bar.get_y() + bar.get_height()/2, f"{x:.2f}ms", 
              ha='left', va='center', color='#F8FAFC', fontsize=8.5, fontweight='bold')
ax_c.text(0.5, 0.25, "Roundtrip Total: 1.6 ~ 23 ms\nRF Classifier Inference: 2.1 ms\nGPU VRAM: 0 MB (Pure CPU)\nAutomated Tests: 5/5 (5.1s)",
          transform=ax_c.transAxes, ha='center', fontsize=8.5, family='monospace',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#0B0F19', edgecolor='#A855F7', lw=1),
          color='#C084FC')
ax_c.set_xlim(0, 2.0)

plt.tight_layout()
save_fig(fig, "02_spike_a_benchmarks.png")


# ==========================================
# FIGURE 3: 03_doctrine_threat_matrix.png
# ==========================================
fig, ax = plt.subplots(figsize=(14, 7.5), dpi=200)
ax.set_facecolor('#0B0F19')
fig.patch.set_facecolor('#0B0F19')

# Draw 3 vertical tiers
ax.text(0.5, 7.0, "OPERATIONAL THREAT SITUATIONS (T1~T12) TO BOTTLENECK HYPOTHESES (H1~H9)", 
        fontsize=13, fontweight='bold', color='#38BDF8', family='monospace')

# Col 1: Threats (MND 2022 Defense White Paper)
rect1 = patches.FancyBboxPatch((0.4, 0.5), 4.0, 6.2, boxstyle="round,pad=0.2", 
                               facecolor='#1E293B', edgecolor='#3B82F6', lw=1.5)
ax.add_patch(rect1)
ax.text(2.4, 6.3, "2022 Defense White Paper Threats", color='#60A5FA', fontsize=10.5, 
        fontweight='bold', ha='center', family='sans-serif')

threats = [
    ("T1", "Ballistic Missile Launch / TEL Move (p.30-31, 98)", "Grade A, C | Min Pressure"),
    ("T2", "Nuclear Doctrine Posture / KMPR (p.23, 31, 57)", "Grade C, D | Batch Swarm"),
    ("T3", "Forward Air Raid / 12-Ship Flight (p.28-29)", "Grade B, C | ACO Reroute"),
    ("T4", "Small UAV Infiltration (p.23, 29, 98)", "Grade B, C | Civil Airspace"),
    ("T5", "GPS & Electronic Warfare Jamming (p.29)", "All Grades | RF Drop / Stale"),
    ("T6", "Coastal / Long-range Artillery Provocation (p.25, 28)", "Grade A, B | Narrow Corridor"),
    ("T10", "Airbase / Runway Bombing Damage (p.28, 55)", "Grade B, C, D | Divert Base"),
    ("T12", "Combined Hybrid Provocation (p.25)", "All Grades | High Stress Queue")
]

y_pos = 5.7
for tid, desc, meta in threats:
    ax.text(0.6, y_pos, f"[{tid}] {desc}", color='#F8FAFC', fontsize=8.2, fontweight='bold')
    ax.text(0.6, y_pos - 0.22, f"  -> {meta}", color='#94A3B8', fontsize=7.5, family='monospace')
    y_pos -= 0.62

# Purged T13 Notice
ax.text(2.4, 0.75, "[PURGED] T13 (Friendly Breakdown): Purged due to lack of doctrinal justification", 
        color='#EF4444', fontsize=7.5, ha='center', family='monospace')

# Col 2: Bottleneck Hypotheses & RAND Validation
rect2 = patches.FancyBboxPatch((4.9, 0.5), 4.3, 6.2, boxstyle="round,pad=0.2", 
                               facecolor='#1E293B', edgecolor='#10B981', lw=1.5)
ax.add_patch(rect2)
ax.text(7.05, 6.3, "Bottleneck Hypotheses & RAND Status", color='#34D399', fontsize=10.5, 
        fontweight='bold', ha='center', family='sans-serif')

hypos = [
    ("H1", "In-flight Voice/Manual Relay Delay", "VERIFIED (RAND MG-166 p.254, MR-1365)"),
    ("H2", "Ground-Cockpit Plan Version Desync", "STRUCTURAL (No direct empirical case)"),
    ("H3", "Pre-flight Total Plan Rewrite", "STRUCTURAL (Addressed by Delta in S5)"),
    ("H4", "Ground Approval Latency Bottleneck", "VERIFIED (RAND MG-166 p.294, JP 3-60)"),
    ("H5", "Concurrent Change Request HOL Queue", "NEW FROM T2/T3 (Head-of-Line Block)"),
    ("H6", "Civil Airspace Multi-Rule Delay", "NEW FROM T4/T6 (Dynamic Rule Matrix)"),
    ("H7", "Noisy / Jammed Channel Missing ACK", "NEW FROM T5 (Idempotent Resync)"),
    ("H8", "C2 Command Authority Delegation Risk", "NEW FROM T11 (Signed Token Transfer)"),
    ("H9", "Divert Base Re-route Delta Limit", "NEW FROM T10 (Full Replace Cut-line)")
]

y_pos = 5.7
for hid, desc, status in hypos:
    stat_col = '#10B981' if 'VERIFIED' in status else ('#38BDF8' if 'NEW' in status else '#F59E0B')
    ax.text(5.1, y_pos, f"[{hid}] {desc}", color='#F8FAFC', fontsize=8.2, fontweight='bold')
    ax.text(5.1, y_pos - 0.22, f"  -> {status}", color=stat_col, fontsize=7.5, family='monospace')
    y_pos -= 0.56

# Col 3: Operational Replanning Delta Architecture
rect3 = patches.FancyBboxPatch((9.7, 0.5), 3.9, 6.2, boxstyle="round,pad=0.2", 
                               facecolor='#1E293B', edgecolor='#F59E0B', lw=1.5)
ax.add_patch(rect3)
ax.text(11.65, 6.3, "Mission Delta Grades & Baseline", color='#FBBF24', fontsize=10.5, 
        fontweight='bold', ha='center', family='sans-serif')

grades = [
    ("Grade A: Target Coordinate Update", "Delta < 1.0 KB | Auth: Tactical Controller\nStrict 1-click Cockpit ACK | Latency: Seconds"),
    ("Grade B: Route & Leg Modification", "Delta 1~5 KB | Auth: Air Operations Center\nTurn Feasibility + Minimum Fuel Verification"),
    ("Grade C: Mission Reassignment", "Delta 5~20 KB | Auth: AOC Mission Director\nTarget Reallocation + Weapon Clearance"),
    ("Grade D: Total Plan Replacement", "Delta > 20 KB | Full Mission Package Reload\nDivert Airbase / Threat Library Overhaul")
]

y_pos = 5.6
for g_title, g_desc in grades:
    ax.text(9.9, y_pos, g_title, color='#FDE047', fontsize=8.2, fontweight='bold')
    ax.text(9.9, y_pos - 0.45, g_desc, color='#CBD5E1', fontsize=7.5, family='sans-serif')
    y_pos -= 1.1

# Baseline comparison badge
base_box = dict(boxstyle='round,pad=0.4', facecolor='#0F172A', edgecolor='#EC4899', lw=1.2)
ax.text(11.65, 0.9, "Baseline Pre-flight Latency (FalconView/JMPS)\nA-01 Single Flight: 0.94 hr (56 min)\nA-02 Mission Package: 7.30 hr", 
        color='#F472B6', fontsize=7.5, ha='center', family='monospace', bbox=base_box)

# Connection arrows
for y in [5.7, 4.46, 3.22, 1.98]:
    ax.annotate('', xy=(4.9, y), xytext=(4.4, y),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2))
    ax.annotate('', xy=(9.7, y), xytext=(9.2, y),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2))

ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis('off')
save_fig(fig, "03_doctrine_threat_matrix.png")


# ==========================================
# FIGURE 4: 04_replay_rejection_fix.png
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)
fig.patch.set_facecolor('#0B0F19')

for ax in [ax1, ax2]:
    ax.set_facecolor('#1E293B')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

# Left Panel: Bug B-04
ax1.set_title("FLAWED DESIGN (B-04): Naive Version Mismatch Rejection", 
              color='#F87171', fontsize=10.5, fontweight='bold', pad=15)

# Lifelines
ax1.plot([2.5, 2.5], [1.0, 9.0], color='#475569', lw=1.5, ls='--')
ax1.plot([7.5, 7.5], [1.0, 9.0], color='#475569', lw=1.5, ls='--')
ax1.text(2.5, 9.2, "Ground C2 (M2)", color='#38BDF8', fontsize=9.5, fontweight='bold', ha='center')
ax1.text(7.5, 9.2, "Aircraft Avionics (M4)", color='#34D399', fontsize=9.5, fontweight='bold', ha='center')

# Step 1: Send Change
ax1.annotate('', xy=(7.4, 8.0), xytext=(2.6, 8.4),
             arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=1.5))
ax1.text(5.0, 8.4, "1. POST /change (msg_id=42, v1->v2)", color='#F8FAFC', fontsize=8, ha='center')

# Step 2: Apply & ACK
ax1.text(7.7, 7.8, "[Applied: v1->v2]", color='#10B981', fontsize=7.5, family='monospace')
ax1.annotate('', xy=(4.5, 6.8), xytext=(7.4, 7.2),
             arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.5, ls=':'))
ax1.text(5.5, 7.2, "2. ACK (APPLIED, v2)", color='#CBD5E1', fontsize=8, ha='center')
ax1.text(4.2, 6.6, "[X] PACKET LOST (Jamming T5)", color='#EF4444', fontsize=8, fontweight='bold')

# Step 3: Timeout & Retransmit
ax1.text(2.3, 5.8, "[Timeout 30s: No ACK]", color='#F59E0B', fontsize=7.5, ha='right', family='monospace')
ax1.annotate('', xy=(7.4, 5.0), xytext=(2.6, 5.4),
             arrowprops=dict(arrowstyle="->", color='#F59E0B', lw=1.5))
ax1.text(5.0, 5.4, "3. Retransmit /change (msg_id=42, v1->v2)", color='#F8FAFC', fontsize=8, ha='center')

# Step 4: Rejection & Desync!
ax1.text(7.7, 4.8, "[Check: current=v2 != base=v1]", color='#EF4444', fontsize=7.5, family='monospace')
ax1.annotate('', xy=(2.6, 3.8), xytext=(7.4, 4.2),
             arrowprops=dict(arrowstyle="->", color='#EF4444', lw=2))
ax1.text(5.0, 4.2, "4. REJECTED: VERSION_MISMATCH", color='#EF4444', fontsize=8.5, fontweight='bold', ha='center')

# Result box
fail_box = dict(boxstyle='round,pad=0.5', facecolor='#450A0A', edgecolor='#EF4444', lw=1.5)
ax1.text(5.0, 2.0, "FATAL DESYNCHRONIZATION:\nAircraft is on v2, Ground thinks Aircraft rejected v2.\nGround rolls back to v1 while Aircraft executes v2!", 
         color='#FCA5A5', fontsize=8, ha='center', family='sans-serif', bbox=fail_box)


# Right Panel: Fixed Idempotent Architecture
ax2.set_title("CLEAN FIX: Idempotent Transaction Cache & Plan Hash Verification", 
              color='#34D399', fontsize=10.5, fontweight='bold', pad=15)

# Lifelines
ax2.plot([2.5, 2.5], [1.0, 9.0], color='#475569', lw=1.5, ls='--')
ax2.plot([7.5, 7.5], [1.0, 9.0], color='#475569', lw=1.5, ls='--')
ax2.text(2.5, 9.2, "Ground C2 (M2)", color='#38BDF8', fontsize=9.5, fontweight='bold', ha='center')
ax2.text(7.5, 9.2, "Aircraft Avionics (M4)", color='#34D399', fontsize=9.5, fontweight='bold', ha='center')

# Step 1: Send Change
ax2.annotate('', xy=(7.4, 8.0), xytext=(2.6, 8.4),
             arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=1.5))
ax2.text(5.0, 8.4, "1. POST /change (msg_id=42, v1->v2)", color='#F8FAFC', fontsize=8, ha='center')

# Step 2: Apply, Cache & ACK
ax2.text(7.7, 7.8, "[Applied: v1->v2]\n[Cache: 42 -> Signed ACK]", color='#10B981', fontsize=7.5, family='monospace')
ax2.annotate('', xy=(4.5, 6.8), xytext=(7.4, 7.2),
             arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.5, ls=':'))
ax2.text(5.5, 7.2, "2. ACK (APPLIED, v2)", color='#CBD5E1', fontsize=8, ha='center')
ax2.text(4.2, 6.6, "[X] PACKET LOST (Jamming T5)", color='#EF4444', fontsize=8, fontweight='bold')

# Step 3: Retransmit
ax2.text(2.3, 5.8, "[Timeout 30s: No ACK]", color='#F59E0B', fontsize=7.5, ha='right', family='monospace')
ax2.annotate('', xy=(7.4, 5.0), xytext=(2.6, 5.4),
             arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=1.5))
ax2.text(5.0, 5.4, "3. Retransmit /change (msg_id=42, v1->v2)", color='#F8FAFC', fontsize=8, ha='center')

# Step 4: Idempotent Cache Return
ax2.text(7.7, 4.8, "[Found in Cache: msg_id=42]\n[Hash Matches Plan v2]", color='#38BDF8', fontsize=7.5, family='monospace')
ax2.annotate('', xy=(2.6, 3.8), xytext=(7.4, 4.2),
             arrowprops=dict(arrowstyle="->", color='#10B981', lw=2))
ax2.text(5.0, 4.2, "4. RETURN CACHED ACK: APPLIED (v2)", color='#34D399', fontsize=8.5, fontweight='bold', ha='center')

# Result box
success_box = dict(boxstyle='round,pad=0.5', facecolor='#064E3B', edgecolor='#10B981', lw=1.5)
ax2.text(5.0, 2.0, "IDEMPOTENT SAFE CONVERGENCE:\nGround receives cached ACK and confirms Aircraft is on v2.\nZero false rejections, zero state divergence under jamming!", 
         color='#A7F3D0', fontsize=8, ha='center', family='sans-serif', bbox=success_box)

plt.tight_layout()
save_fig(fig, "04_replay_rejection_fix.png")

print("[+] All EP 02 figures generated successfully!")
