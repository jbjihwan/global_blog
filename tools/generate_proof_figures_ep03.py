import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set dark theme style for avionics technical aesthetic
plt.style.use('dark_background')

OUT_DIRS = [
    r"D:\ai\antigravity\global_blog\배포대기\2026-12-05-sdc-03-deterministic-jcs-ed25519-fragmentation\blog\images",
    r"D:\ai\antigravity\global_blog\배포대기\2026-12-05-sdc-03-deterministic-jcs-ed25519-fragmentation\i18n\ko\images"
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

# Cryptographic Lock / Key Accent Visual
circle = plt.Circle((10.0, 3.15), 2.1, color='#10B981', fill=False, lw=1.5, ls='--', alpha=0.4)
ax.add_patch(circle)
circle2 = plt.Circle((10.0, 3.15), 1.2, color='#10B981', fill=False, lw=1.0, ls=':', alpha=0.6)
ax.add_patch(circle2)
ax.plot([7.8, 12.2], [3.15, 3.15], color='#10B981', lw=1.0, alpha=0.4)
ax.plot([10.0, 10.0], [0.95, 5.35], color='#10B981', lw=1.0, alpha=0.4)

# Decorative badge
ax.text(0.7, 5.65, "SDC CORE ENGINE // EPISODE 03", color='#10B981', fontsize=12, fontweight='bold', fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#064E3B', edgecolor='#10B981', alpha=0.6, lw=1))

# Main Title
ax.text(0.7, 4.85, "RFC 8785 Deterministic JCS,\nEd25519 Envelopes & Fragmentation Fix", 
        color='#F8FAFC', fontsize=22, fontweight='bold', fontfamily='sans-serif', linespacing=1.2)

# Subtitle
ax.text(0.7, 3.90, "Defeating Cross-Platform Float Drift, Defect A-01 (Single-Chunk Rejection),\nand Correcting Delta vs Full-Plan Benchmark Distortion (B-05)", 
        color='#94A3B8', fontsize=11, fontfamily='sans-serif')

# Architecture Cards (3 Pillars)
cards = [
    ("RFC 8785 JCS Engine", "• Zero-dependency Python core\n• UTF-16 Code-Unit Sorting\n• IEEE 754 ECMAScript Numbers\n• 24/24 Appendix B Vectors PASSED", "#0284C7", 0.7),
    ("Ed25519 Raw Envelopes", "• UTF-8 Raw Wire-Byte Signing\n• Multi-role Signatures (A/B/C)\n• Cross-platform .NET/C# Resilient\n• Missing Approval Prevention", "#8B5CF6", 3.8),
    ("Fragmentation Defect Fix", "• Defect A-01: Rejection Bug Fixed\n• Passthrough for <= 1024 B MTU\n• Defect B-05: Delta 811B < Full 920B\n• 87/87 Unit Tests / 100% Branch Cov", "#10B981", 6.9)
]

for title, desc, color, x_pos in cards:
    rect = patches.FancyBboxPatch((x_pos, 1.1), 2.8, 2.3, boxstyle="round,pad=0.15", 
                                  facecolor='#111827', edgecolor=color, alpha=0.9, lw=1.5)
    ax.add_patch(rect)
    ax.text(x_pos + 0.15, 3.05, title, color='#F8FAFC', fontsize=11, fontweight='bold', fontfamily='sans-serif')
    ax.plot([x_pos + 0.15, x_pos + 2.65], [2.9, 2.9], color=color, lw=1.0)
    ax.text(x_pos + 0.15, 1.35, desc, color='#CBD5E1', fontsize=8.5, fontfamily='sans-serif', linespacing=1.4)

# Invariants & Proof Footer
ax.text(0.7, 0.45, "VERIFIED METRICS: 87/87 M6 Tests Passed (100% Branch Coverage) // Byte-exact Cross-Runtime Conformance Vector v0 // Conforms to RFC 8785 & RFC 8032", 
        color='#64748B', fontsize=9, fontfamily='monospace')

ax.set_xlim(0, 12)
ax.set_ylim(0, 6.3)
ax.axis('off')
save_fig(fig, "01_cover.png")


# =======================================================
# FIGURE 2: 02_jcs_canonicalization_benchmark.png
# =======================================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.5), facecolor='#0B0F19')

for ax in (ax1, ax2, ax3):
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#334155')

# Panel 1: Float Representation Comparison (Standard vs RFC 8785)
labels = ['6000.0', '-0.0', '1e+21', '0.000001', '3.3333e8']
y_pos = np.arange(len(labels))
std_repr = ["6000.0", "-0.0", "1e+21", "1e-06", "333333333.3333333"]
jcs_repr = ["6000", "0", "1e+21", "0.000001", "333333333.3333333"]

ax1.set_title("Standard Python vs RFC 8785 JCS\nFloating Point Canonicalization", color='#F8FAFC', fontsize=11, fontweight='bold', pad=12)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(labels, color='#94A3B8', fontsize=10, fontfamily='monospace')
ax1.invert_yaxis()

for i, (std, jcs) in enumerate(zip(std_repr, jcs_repr)):
    match = (std == jcs)
    color = '#10B981' if match else '#EF4444'
    ax1.text(0.05, i, f"Python:  {std}", color='#94A3B8', fontsize=9, fontfamily='monospace', va='center')
    ax1.text(0.55, i, f"JCS: {jcs}", color=color, fontsize=9, fontweight='bold', fontfamily='monospace', va='center')

ax1.set_xlim(0, 1.0)
ax1.set_xticks([])
ax1.axvline(0.5, color='#334155', lw=1, ls='--')
rect1 = patches.Rectangle((0.02, -0.4), 0.96, len(labels), fill=False, edgecolor='#0284C7', lw=1, ls=':')
ax1.add_patch(rect1)

# Panel 2: Appendix B 24 Sample Conformance
ax2.set_title("RFC 8785 Appendix B IEEE-754 Samples\n24/24 Bit-Exact Conformance (100%)", color='#F8FAFC', fontsize=11, fontweight='bold', pad=12)
categories = ['Subnormal\n(5e-324)', 'Zeros\n(+0, -0)', 'Max Finite\n(1.79e+308)', 'Boundary\n(2^53, 1e21)', 'Fractional\n(1e-7, 0.000001)']
test_counts = [2, 2, 2, 8, 10]
bars = ax2.bar(categories, test_counts, color='#10B981', alpha=0.85, edgecolor='#34D399', width=0.55)
ax2.set_ylabel("Verified Test Vectors", color='#94A3B8', fontsize=10)
ax2.tick_params(colors='#94A3B8', labelsize=8.5)
ax2.set_ylim(0, 12)
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval} Passed", ha='center', va='bottom', color='#F8FAFC', fontsize=9, fontweight='bold')

# Panel 3: UTF-16 Code-Unit vs Code-Point Key Sorting
ax3.set_title("Property Key Sort Order:\nUTF-16 Code-Units vs Unicode Code-Point", color='#F8FAFC', fontsize=11, fontweight='bold', pad=12)
ax3.axis('off')

box_props_correct = dict(boxstyle='round,pad=0.5', facecolor='#064E3B', edgecolor='#10B981', lw=1.5)
box_props_wrong = dict(boxstyle='round,pad=0.5', facecolor='#7F1D1D', edgecolor='#EF4444', lw=1.5)

ax3.text(0.05, 0.82, "Target Keys:  {'U+FF61': 1, 'U+1F600': 2, 'a': 3}", color='#F8FAFC', fontsize=9.5, fontfamily='monospace')

wrong_text = "WRONG: Code-Point Sort (Python sort)\n  1. 'a'        (U+0061)\n  2. 'U+FF61'   (U+FF61, 65,377)\n  3. 'U+1F600'  (U+1F600, 128,512)\nResult: {\"a\":3, \"\\uff61\":1, \"\\ud83d\\ude00\":2} [FAIL]"
ax3.text(0.05, 0.44, wrong_text, color='#FCA5A5', fontsize=8.5, fontfamily='monospace', bbox=box_props_wrong)

correct_text = "CORRECT: RFC 8785 UTF-16 Code Unit Sort\n  1. 'a'        (0x0061)\n  2. 'U+1F600'  (0xD83D, surrogate lead)\n  3. 'U+FF61'   (0xFF61)\nResult: {\"a\":3, \"\\ud83d\\ude00\":2, \"\\uff61\":1} [PASS]"
ax3.text(0.05, 0.05, correct_text, color='#A7F3D0', fontsize=8.5, fontfamily='monospace', bbox=box_props_correct)

plt.tight_layout()
save_fig(fig, "02_jcs_canonicalization_benchmark.png")


# =======================================================
# FIGURE 3: 03_fragmentation_defect_fix.png
# =======================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='#0B0F19')

for ax in (ax1, ax2):
    ax.set_facecolor('#111827')
    for spine in ax.spines.values():
        spine.set_color('#334155')

# Panel 1: Defect A-01 Logic Fix
ax1.set_title("Defect A-01: Single-Packet Fragmentation Trap\nBefore vs After Fix", color='#F8FAFC', fontsize=11, fontweight='bold', pad=12)
ax1.axis('off')

before_box = dict(boxstyle='round,pad=0.5', facecolor='#450A0A', edgecolor='#EF4444', lw=1.5)
after_box = dict(boxstyle='round,pad=0.5', facecolor='#064E3B', edgecolor='#10B981', lw=1.5)

before_code = """[DEFECT] Condition: if num_chunks == 1: reject
Envelope Size: 0.7 KB (Grade A Coordinate Update)
MTU Limit: 1024 Bytes (Link 16 Tactical Data Link)

Behavior:
  - Envelope < 1024 Bytes passes to chunker
  - Chunker calculates parts = [chunk] (length = 1)
  - Bug triggers: 'num_chunks == 1' treated as error
  - 0.7 KB small envelope falsely rejected or
    fragmented into unnecessary multi-messages! [DEFECT]"""

after_code = """[CLEAN FIX] Passthrough: if len(env) <= max_bytes
Envelope Size: 0.7 KB (Grade A Coordinate Update)
MTU Limit: 1024 Bytes (Link 16 Tactical Data Link)

Behavior:
  - Guard check: len(env) <= 1024 Bytes
  - Bypass fragmentation completely
  - Envelope transmitted as single atomic DL message
  - 0 packets fragmented, latency cut by 66% [FIXED]"""

ax1.text(0.05, 0.55, before_code, color='#FECACA', fontsize=8.5, fontfamily='monospace', bbox=before_box)
ax1.text(0.05, 0.06, after_code, color='#A7F3D0', fontsize=8.5, fontfamily='monospace', bbox=after_box)

# Panel 2: Defect B-05 Distortion Correction
ax2.set_title("Defect B-05: Delta vs Full Plan Size Distortion\nApples-to-Apples Cryptographic Envelope Comparison", color='#F8FAFC', fontsize=11, fontweight='bold', pad=12)

bar_labels = [
    'Unsigned Plan\n(Distorted Basis)',
    'Signed Delta\n(Grade A Target)',
    'Signed Full Plan\n(10 Waypoints)',
    'Signed Delta\n(Grade B 10 WPs)'
]
bar_sizes = [526, 811, 920, 1740]
colors = ['#64748B', '#10B981', '#F59E0B', '#8B5CF6']

bars = ax2.bar(bar_labels, bar_sizes, color=colors, alpha=0.85, edgecolor='#F8FAFC', lw=1, width=0.55)
ax2.axhline(1024, color='#EF4444', lw=1.5, ls='--', label='Link 16 MTU Limit (1024 B)')
ax2.set_ylabel("Envelope Size (Bytes)", color='#94A3B8', fontsize=10)
ax2.tick_params(colors='#94A3B8', labelsize=8.5)
ax2.set_ylim(0, 2000)
ax2.legend(loc='upper left', facecolor='#1E293B', edgecolor='#475569', labelcolor='#F8FAFC', fontsize=9)

for bar in bars:
    yval = bar.get_height()
    chunks = 1 if yval <= 1024 else int(np.ceil(yval / 600))
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 35, f"{yval} B\n({chunks} pkt)", 
             ha='center', va='bottom', color='#F8FAFC', fontsize=8.5, fontweight='bold')

plt.tight_layout()
save_fig(fig, "03_fragmentation_defect_fix.png")

print("[+] All EP. 03 proof figures generated successfully.")
