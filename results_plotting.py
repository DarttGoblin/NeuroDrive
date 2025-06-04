import matplotlib.pyplot as plt

# Define stages and their corresponding times (in milliseconds)
stages = ['Preprocessing', 'Inference', 'Postprocessing']
times = [2.8, 69.2, 135.7]

# Plot settings
plt.figure(figsize=(8, 5))
bars = plt.bar(stages, times, color=['skyblue', 'lightgreen', 'salmon'])

# Add text labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 2, f'{height:.1f} ms',
             ha='center', va='bottom', fontsize=10)

# Labels and title
plt.ylabel('Time (ms)')
plt.title('YOLOv8n Inference Pipeline Processing Times')
plt.ylim(0, max(times) + 30)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot
plt.tight_layout()
plt.savefig('results_plot.png', dpi=300)
plt.close()
