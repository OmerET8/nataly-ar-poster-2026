import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("assets", exist_ok=True)

# Set high DPI for crisp feature extraction
DPI = 150
WIDTH_PX, HEIGHT_PX = 1280, 720
FIGSIZE = (WIDTH_PX / DPI, HEIGHT_PX / DPI)

print("Generating Graph 1...")
# -------------------------------------------------------------
# GRAPH 1: Temporal Signal Dynamics
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#f8fafc')

t = np.linspace(0, 10, 300)
signal = np.sin(1.8 * t) * np.exp(-0.15 * t) + 0.3 * np.cos(4.5 * t) * np.exp(-0.4 * t)
noise_upper = signal + 0.25 * (1 + 0.2 * np.sin(0.8 * t))
noise_lower = signal - 0.25 * (1 + 0.2 * np.sin(0.8 * t))

ax.fill_between(t, noise_lower, noise_upper, color='#60a5fa', alpha=0.35, label='95% Confidence Interval')
ax.plot(t, signal, color='#1d4ed8', lw=3.2, label='Model Trajectory: S(t)')

# Marker points for feature density
peak_idx = [13, 45, 80, 115, 160]
ax.scatter(t[peak_idx], signal[peak_idx], color='#dc2626', s=80, zorder=5, edgecolors='black', lw=1.5, label='Critical Invariants')
for idx in peak_idx:
    ax.annotate(f'P_{idx}', xy=(t[idx], signal[idx]), xytext=(t[idx]+0.15, signal[idx]+0.2),
                arrowprops=dict(facecolor='#1e293b', arrowstyle='->', lw=1.2),
                fontweight='bold', fontsize=10, color='#0f172a')

# Threshold line & grid
ax.axhline(0.65, color='#e11d48', linestyle='--', lw=2, label='Threshold θ = 0.65')
ax.grid(True, linestyle=':', alpha=0.7, color='#94a3b8', lw=1.2)
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.8)

# Stylized academic header
ax.set_title("FIGURE 1: Temporal Signal Dynamics & Spectral Response", fontsize=15, fontweight='bold', pad=18, color='#0f172a')
ax.set_xlabel("Normalized Time (τ / ms)", fontsize=12, fontweight='semibold', labelpad=8)
ax.set_ylabel("Amplitude Response (mV)", fontsize=12, fontweight='semibold', labelpad=8)
ax.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1', fontsize=10)

# Add distinct decorative corner badges to ensure rich corner features
fig.text(0.02, 0.95, "[EXP-01 #4892]", fontsize=11, fontweight='black', color='#1e3a8a')
fig.text(0.85, 0.03, "λ = 1.84 | SNR = 24.2 dB", fontsize=10, fontweight='bold', color='#475569')

plt.tight_layout()
graph1_path = os.path.join("assets", "graph1.png")
fig.savefig(graph1_path, dpi=DPI)
plt.close(fig)
print(f"Graph 1 saved: {graph1_path}")

# -------------------------------------------------------------
# GRAPH 2: Multi-Agent Convergence & Loss Landscape
# -------------------------------------------------------------
print("Generating Graph 2...")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
fig.patch.set_facecolor('#ffffff')

# Contour background
x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = 0.5 * (X**2 + Y**2) - 0.4 * np.cos(3*X) * np.cos(3*Y) + 0.3 * np.sin(2*X + Y)

cp = ax.contourf(X, Y, Z, levels=18, cmap='viridis', alpha=0.85)
cbar = fig.colorbar(cp, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Loss Potential Φ(θ)', fontsize=11, fontweight='semibold')
ax.contour(X, Y, Z, levels=12, colors='white', alpha=0.4, linewidths=0.8)

# Trajectories
np.random.seed(42)
t_steps = np.linspace(0, 1, 40)
path1_x = 2.4 * np.exp(-2.5 * t_steps) * np.cos(5 * t_steps)
path1_y = 2.2 * np.exp(-2.5 * t_steps) * np.sin(5 * t_steps)
path2_x = -2.2 * np.exp(-2.0 * t_steps) + 0.1 * np.sin(10 * t_steps)
path2_y = 2.0 * np.exp(-2.0 * t_steps) + 0.1 * np.cos(10 * t_steps)

ax.plot(path1_x, path1_y, color='#ef4444', lw=3, marker='o', markersize=4, label='Optimizer A (AdamW)')
ax.plot(path2_x, path2_y, color='#38bdf8', lw=3, marker='^', markersize=4, label='Optimizer B (SGD-M)')

# Minima star
ax.plot(0, 0, marker='*', markersize=18, color='#fbbf24', markeredgecolor='black', markeredgewidth=1.5, label='Global Optimum θ*')
ax.annotate('Optimum (0, 0)', xy=(0, 0), xytext=(0.4, -0.6),
            arrowprops=dict(facecolor='yellow', arrowstyle='->', lw=1.5),
            fontweight='bold', fontsize=11, color='white',
            bbox=dict(boxstyle="round,pad=0.3", fc="#0f172a", ec="white", lw=1))

ax.set_title("FIGURE 2: Stochastic Optimization Trajectories in Loss Landscape", fontsize=15, fontweight='bold', pad=18, color='#0f172a')
ax.set_xlabel("Parameter Vector Dimension θ_1", fontsize=12, fontweight='semibold', labelpad=8)
ax.set_ylabel("Parameter Vector Dimension θ_2", fontsize=12, fontweight='semibold', labelpad=8)
ax.legend(loc='upper left', framealpha=0.92, edgecolor='#cbd5e1', fontsize=10)

fig.text(0.02, 0.95, "[EXP-02 #8819]", fontsize=11, fontweight='black', color='#065f46')
fig.text(0.80, 0.03, "Epochs = 500 | Loss = 0.0031", fontsize=10, fontweight='bold', color='#334155')

plt.tight_layout()
graph2_path = os.path.join("assets", "graph2.png")
fig.savefig(graph2_path, dpi=DPI)
plt.close(fig)
print(f"Graph 2 saved: {graph2_path}")

# -------------------------------------------------------------
# Generate Video 1 (Animation of Signal Dynamics)
# -------------------------------------------------------------
print("Generating Video 1 frames and encoding H.264 MP4...")
frames_dir_1 = "scratch_frames_1"
os.makedirs(frames_dir_1, exist_ok=True)
total_frames = 60
fps = 20

for f in range(total_frames):
    phase = 2 * np.pi * (f / total_frames)
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')
    
    t_full = np.linspace(0, 10, 300)
    # Dynamic traveling wave
    sig_f = np.sin(1.8 * t_full - phase) * np.exp(-0.15 * t_full) + 0.3 * np.cos(4.5 * t_full - 2 * phase) * np.exp(-0.4 * t_full)
    upper_f = sig_f + 0.25 * (1 + 0.2 * np.sin(0.8 * t_full + phase))
    lower_f = sig_f - 0.25 * (1 + 0.2 * np.sin(0.8 * t_full + phase))
    
    ax.fill_between(t_full, lower_f, upper_f, color='#60a5fa', alpha=0.35, label='95% Confidence Interval')
    ax.plot(t_full, sig_f, color='#1d4ed8', lw=3.2, label='Model Trajectory: S(t)')
    
    # Animated scanning vertical line
    scan_x = (f / total_frames) * 10
    ax.axvline(scan_x, color='#10b981', linestyle='-', lw=2.5, alpha=0.8, label=f'Scan: t = {scan_x:.1f}ms')
    
    # Pulsing peak markers
    pulse = 1.0 + 0.3 * np.sin(phase * 2)
    ax.scatter(t[peak_idx], sig_f[peak_idx], color='#dc2626', s=80 * pulse, zorder=5, edgecolors='black', lw=1.5)
    
    ax.axhline(0.65, color='#e11d48', linestyle='--', lw=2)
    ax.grid(True, linestyle=':', alpha=0.7, color='#94a3b8', lw=1.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.5, 1.8)
    
    ax.set_title("FIGURE 1: Temporal Signal Dynamics [LIVE AR SIMULATION]", fontsize=15, fontweight='bold', pad=18, color='#0f172a')
    ax.set_xlabel("Normalized Time (τ / ms)", fontsize=12, fontweight='semibold', labelpad=8)
    ax.set_ylabel("Amplitude Response (mV)", fontsize=12, fontweight='semibold', labelpad=8)
    ax.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1', fontsize=10)
    
    fig.text(0.02, 0.95, "[LIVE AR #4892]", fontsize=11, fontweight='black', color='#1e3a8a')
    fig.text(0.78, 0.03, f"Phase = {phase:.2f} rad | Frame {f+1}/{total_frames}", fontsize=10, fontweight='bold', color='#475569')
    
    plt.tight_layout()
    frame_path = os.path.join(frames_dir_1, f"frame_{f:04d}.png")
    fig.savefig(frame_path, dpi=DPI)
    plt.close(fig)

video1_path = os.path.join("assets", "video1.mp4")
cmd1 = [
    "ffmpeg", "-y", "-framerate", str(fps),
    "-i", os.path.join(frames_dir_1, "frame_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    video1_path
]
subprocess.run(cmd1, check=True)
print(f"Video 1 encoded: {video1_path}")

# Clean frame images
for f in os.listdir(frames_dir_1):
    os.remove(os.path.join(frames_dir_1, f))
os.rmdir(frames_dir_1)

# -------------------------------------------------------------
# Generate Video 2 (Animation of Optimization Landscape)
# -------------------------------------------------------------
print("Generating Video 2 frames and encoding H.264 MP4...")
frames_dir_2 = "scratch_frames_2"
os.makedirs(frames_dir_2, exist_ok=True)

for f in range(total_frames):
    phase = 2 * np.pi * (f / total_frames)
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_facecolor('#ffffff')
    
    # Pulsing contour levels
    Z_f = 0.5 * (X**2 + Y**2) - 0.4 * np.cos(3*X + phase) * np.cos(3*Y + phase) + 0.3 * np.sin(2*X + Y + 0.5*phase)
    cp = ax.contourf(X, Y, Z_f, levels=18, cmap='viridis', alpha=0.85)
    cbar = fig.colorbar(cp, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Loss Potential Φ(θ)', fontsize=11, fontweight='semibold')
    ax.contour(X, Y, Z_f, levels=12, colors='white', alpha=0.4, linewidths=0.8)
    
    # Step-by-step moving agents
    step_frac = (f + 1) / total_frames
    idx_now = int(len(path1_x) * step_frac)
    ax.plot(path1_x[:idx_now], path1_y[:idx_now], color='#ef4444', lw=3.2, marker='o', markersize=4, label='Optimizer A (AdamW)')
    ax.scatter(path1_x[max(0, idx_now-1)], path1_y[max(0, idx_now-1)], color='#fca5a5', s=160, edgecolors='white', lw=2, zorder=6)
    
    ax.plot(path2_x[:idx_now], path2_y[:idx_now], color='#38bdf8', lw=3.2, marker='^', markersize=4, label='Optimizer B (SGD-M)')
    ax.scatter(path2_x[max(0, idx_now-1)], path2_y[max(0, idx_now-1)], color='#bae6fd', s=160, edgecolors='white', lw=2, zorder=6)
    
    ax.plot(0, 0, marker='*', markersize=18, color='#fbbf24', markeredgecolor='black', markeredgewidth=1.5, label='Global Optimum θ*')
    
    ax.set_title("FIGURE 2: Stochastic Optimization [LIVE DYNAMICS]", fontsize=15, fontweight='bold', pad=18, color='#0f172a')
    ax.set_xlabel("Parameter Vector Dimension θ_1", fontsize=12, fontweight='semibold', labelpad=8)
    ax.set_ylabel("Parameter Vector Dimension θ_2", fontsize=12, fontweight='semibold', labelpad=8)
    ax.legend(loc='upper left', framealpha=0.92, edgecolor='#cbd5e1', fontsize=10)
    
    fig.text(0.02, 0.95, "[LIVE AR #8819]", fontsize=11, fontweight='black', color='#065f46')
    fig.text(0.75, 0.03, f"Step: {int(step_frac*500)} / 500 | Loss: {0.0031/(step_frac+0.1):.4f}", fontsize=10, fontweight='bold', color='#334155')
    
    plt.tight_layout()
    frame_path = os.path.join(frames_dir_2, f"frame_{f:04d}.png")
    fig.savefig(frame_path, dpi=DPI)
    plt.close(fig)

video2_path = os.path.join("assets", "video2.mp4")
cmd2 = [
    "ffmpeg", "-y", "-framerate", str(fps),
    "-i", os.path.join(frames_dir_2, "frame_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    video2_path
]
subprocess.run(cmd2, check=True)
print(f"Video 2 encoded: {video2_path}")

for f in os.listdir(frames_dir_2):
    os.remove(os.path.join(frames_dir_2, f))
os.rmdir(frames_dir_2)

print("All sample assets generated successfully!")
