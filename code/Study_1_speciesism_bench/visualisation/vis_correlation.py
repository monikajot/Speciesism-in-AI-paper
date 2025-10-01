import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr

from ..src.constants import FINAL_RESULTS, model_mapping

# Convert your data
data = []
for run in FINAL_RESULTS:
    total_items = run['speciesist'] + run['not speciesist']
    classification_acc = (run['speciesist'] / total_items) * 100

    total_moral = run['wrong'] + run['not wrong']
    moral_judgment_acc = (run['wrong'] / total_moral) * 100

    data.append({
        'model': run['model'],
        'classification_accuracy': classification_acc,
        'moral_judgment_accuracy': moral_judgment_acc
    })

df = pd.DataFrame(data)

model_means = df.groupby('model').agg({
    'classification_accuracy': ['mean', 'std'],
    'moral_judgment_accuracy': ['mean', 'std']
}).round(2)

# Flatten column names
model_means.columns = ['class_mean', 'class_std', 'moral_mean', 'moral_std']

# Calculate correlation using model means
correlation, p_value = pearsonr(model_means['class_mean'],
                                model_means['moral_mean'])

# Create much larger figure
plt.figure(figsize=(14,10))
plt.errorbar(model_means['class_mean'], model_means['moral_mean'],
             xerr=model_means['class_std'], yerr=model_means['moral_std'],
             fmt='o', capsize=5, capthick=2, markersize=8)

# Use strategic positioning with xytext offsets for each label
label_positions = {
    'gpt-4o': (15, 15),
    'o1': (-25, 15),
    'gemini-1.5': (20, 10),
    'gemini-2': (-20, 10),
    'llama-3.1-405b': (-30, 20),
    'gpt-4.1': (0, -25),
    'gpt-5': (-10, -15),
    'deepseek-v3': (-40, 5),
    'gemini-2.5': (-25, 10),
    'claude-3.5':(0, -15),
    'claude-4': (0, 15),
    'claude-3.7': (-20, 20),
    'grok-3': (20, 10),
    'deepseek-r1': (0, 25),
    'gpt-3.5': (-35, -10),
    'llama4': (0, 15)
}

# Add labels with smart positioning
for idx, model in enumerate(model_means.index):

    x_pos = model_means.loc[model, 'class_mean']
    y_pos = model_means.loc[model, 'moral_mean']

    # Get position offset or use default
    if model in label_positions:
        offset_x, offset_y = label_positions[model]
    else:
        offset_x, offset_y = (10, 10)  # default offset
    model = model_mapping[model]  if model in model_mapping.keys() else model

    plt.annotate(model,
                 xy=(x_pos, y_pos),
                 xytext=(offset_x, offset_y),
                 textcoords='offset points',
                 fontsize=10,
                 ha='center', va='center',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor='gray'),
                 arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

plt.xlabel('Speciesism Classification in Task 1 (%)', fontsize=12)
plt.ylabel('Morally Wrong Responses in Task 2 (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
# plt.show()
plt.savefig('model_correlation.svg', dpi=300, bbox_inches='tight')
