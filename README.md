# DETR-Dog-Attention-Maps

## Project Overview
This repository contains the results of an experiment to visualize how a modified DETR (DEtection TRansformer) model learns to detect dogs through attention maps across training epochs. The focus is on understanding how the model progressively learns to attend to specific dog features like ears, paws, and fur.

## Experiment Setup

### Model Modifications
The experiment uses a modified version of the official DETR model with reduced complexity:
- Hidden dimension: 128 (reduced from 256)
- Embedding dimension: 1024
- Number of encoder/decoder layers: 4
- Number of attention heads: 4
- Backbone: ResNet-18

### Dataset
A custom dataset was created using a subset of COCO:
- 3,000 dog images for training
- 600 dog images for testing
- 1,000 non-dog images for training (to reduce false positives)
- 200 non-dog images for testing

## Repository Contents

### Attention Map Visualizations
- `attention_maps/`: Directory containing decoder layer attention maps for 4 out-of-distribution dog images across all training epochs
- Each subfolder represents a different test image
- Files are organized by epoch number for easy tracking of progression

### Training Statistics
- `logs/training_stats.log`: Contains loss values, learning rates, and other metrics for each epoch
- `logs/mAP_progression.log`: Mean Average Precision (mAP) values for each epoch

### Animations
- `animations/attention_timelapse.mp4`: Timelapse animation showing how attention maps evolve for a single image across training epochs
- `animations/metrics_evolution.mp4`: Animation of training metrics showing the decrease in loss and increase in mAP over time

## Key Findings
*[Note: Add your key findings here after completing your analysis]*

## Future Work
*[Note: Add potential future directions for this research]*

## Acknowledgments
This work builds upon the [official DETR implementation](https://github.com/facebookresearch/detr) by Facebook Research.
