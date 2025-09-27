#!/usr/bin/env python3

# Test script to check if the security fix works with plotting code containing "evaluation"

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Data
# ----------------------------
models = ["FiD-ANCE-REALM", "LLM-only", "Retrieval-only", "RAG-Baseline", "BioBERT", "BoneBERT", "AlzheimerRAG"]
x = np.arange(len(models))

# F1 and Accuracy
accuracy = [96.2, 89.0, 83.1, 91.0, 87.8, 86.8, 92.5]
f1_scores = [95.8, 88.5, 82.3, 90.1, 87.2, 86.5, 92.0]

# ----------------------------
# 1. Accuracy & F1 Comparison
plt.figure(figsize=(10,4))
plt.plot(x, accuracy, marker='o', label='Accuracy', color='blue')
plt.plot(x, f1_scores, marker='s', label='F1-Score', color='green')
plt.xticks(x, models, rotation=30)
plt.ylabel('Percentage (%)')
plt.ylim(0,100)
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.tight_layout()
plt.show()

# ----------------------------
# 2. Precision vs Recall
precision = [0.96, 0.89, 0.85, 0.91, 0.88, 0.86, 0.93]
recall    = [0.95, 0.87, 0.82, 0.89, 0.85, 0.84, 0.91]

plt.figure(figsize=(8,5))
plt.scatter(recall, precision, c='red')
for i, model in enumerate(models):
    plt.text(recall[i]+0.005, precision[i], model, fontsize=8)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.xlim(0,1)
plt.ylim(0,1)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# ----------------------------
# 3. Latency vs Document Volume
doc_volumes = [100, 500, 1000, 2000, 5000]
latency = [
    [0.5, 0.7, 1.0, 1.5, 2.8],
    [0.4, 0.6, 0.9, 1.4, 2.5],
    [0.3, 0.5, 0.8, 1.2, 2.2],
    [0.45, 0.68, 1.05, 1.48, 2.6],
    [0.48, 0.7, 1.02, 1.5, 2.7],
    [0.46, 0.69, 1.01, 1.49, 2.65],
    [0.5, 0.72, 1.08, 1.52, 2.75]
]

plt.figure(figsize=(10,5))
for i in range(len(models)):
    plt.plot(doc_volumes, latency[i], marker='o', label=models[i])
plt.xlabel('Number of Retrieved Documents')
plt.ylabel('Latency (s/query)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.tight_layout()
plt.show()

# ----------------------------
# 4. Human Evaluation Scores
criteria = ['Factual Correctness', 'Evidence Alignment', 'Clinical Utility']
human_scores = [
    [9.2, 9.0, 9.1],
    [7.5, 7.2, 7.0],
    [7.0, 6.8, 6.5],
    [8.0, 7.9, 8.1],
    [7.8, 7.5, 7.6],
    [7.6, 7.4, 7.5],
    [8.5, 8.3, 8.4]
]

width = 0.1
x_pos = np.arange(len(criteria))
plt.figure(figsize=(10,5))
for i in range(len(models)):
    plt.bar(x_pos + i*width, human_scores[i], width, label=models[i])
plt.xticks(x_pos + width*3, criteria)
plt.ylabel('Avg Score (1-10)')
plt.ylim(0,10)
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.tight_layout()
plt.show()
