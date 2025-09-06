import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# Configure font
try:
    # This path would be used inside the Docker container
    fm.fontManager.addfont('/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf')
    plt.rcParams['font.family'] = 'Times New Roman'
    print("Times New Roman font configured successfully")
except Exception as e:
    print(f"Font configuration error: {e}")
    print("Continuing with default font...")

# Models: Proposed + 6 existing baselines 
models = ["APDC", "K-Means", "GMM", "Neural-Only", "OMP", "Lasso", "DeepMIMO-Baseline"] 

# Using the real experimental improvements for APDC 
# Assume baseline average NMSE = 0.25, precoding gain = 10, recovery time = 0.8s 
nmse_baseline = 0.25 
precoding_baseline = 10 
recovery_baseline = 0.8 

# APDC improvements 
nmse_apdc = nmse_baseline * (1 - 0.20)  # 20% average improvement 
precoding_apdc = precoding_baseline * (1 + 0.135)  # 13.5% average improvement 
recovery_apdc = recovery_baseline * (1 - 0.25)  # 25% faster recovery 

# Assign dummy values for other baselines 
nmse = np.array([nmse_apdc, 0.27, 0.28, 0.26, 0.29, 0.28, 0.27]) 
precoding_gain = np.array([precoding_apdc, 9.2, 9.0, 9.5, 8.8, 9.1, 9.3]) 
recovery_time = np.array([recovery_apdc, 0.85, 0.87, 0.83, 0.88, 0.86, 0.84]) 

# --- Plot 1: Radar Chart --- 
metrics = ["NMSE (↓)", "Precoding Gain (↑)", "Recovery Time (↓)"] 
data = np.vstack([nmse / nmse.max(), precoding_gain / precoding_gain.max(), recovery_time / recovery_time.max()]).T 

angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist() 
angles += angles[:1] 

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True)) 
for i, model in enumerate(models): 
    values = data[i].tolist() 
    values += values[:1] 
    ax.plot(angles, values, label=model, linewidth=2) 
    ax.fill(angles, values, alpha=0.15) 

ax.set_xticks(angles[:-1]) 
ax.set_xticklabels(metrics, fontsize=12) 

ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1)) 

# Save the plot
fig.savefig('test_radar_chart.png', dpi=300, bbox_inches='tight')
print("Saved radar chart to test_radar_chart.png")

# --- Plot 2: Grouped Bar Plot --- 
x = np.arange(len(models)) 
width = 0.25 

fig2, ax2 = plt.subplots(figsize=(10, 6)) 
ax2.bar(x - width, nmse, width, label="NMSE (↓)") 
ax2.bar(x, precoding_gain, width, label="Precoding Gain (↑)") 
ax2.bar(x + width, recovery_time, width, label="Recovery Time (↓)") 

ax2.set_xticks(x) 
ax2.set_xticklabels(models, rotation=20) 
ax2.set_ylabel("Metric Values") 

ax2.legend() 

# Save the plot
fig2.savefig('test_bar_plot.png', dpi=300, bbox_inches='tight')
print("Saved bar plot to test_bar_plot.png")

# --- Plot 3: Bubble Chart --- 
robustness = (1 - nmse) * precoding_gain * 100 

fig3, ax3 = plt.subplots(figsize=(10, 6)) 
scatter = ax3.scatter(nmse, recovery_time, s=robustness, alpha=0.6, c=np.arange(len(models)), cmap="tab10") 

for i, model in enumerate(models): 
    ax3.text(nmse[i]+0.002, recovery_time[i]+0.005, model, fontsize=9) 

ax3.set_xlabel("NMSE (↓)") 
ax3.set_ylabel("Recovery Time (s, ↓)") 

# Save the plot
fig3.savefig('test_bubble_chart.png', dpi=300, bbox_inches='tight')
print("Saved bubble chart to test_bubble_chart.png")

print("\nAll test plots generated successfully!")