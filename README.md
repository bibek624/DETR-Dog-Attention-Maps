# DETR-Dog-Attention-Maps

## Project Overview
This repository contains the results of an experiment to visualize how a modified DETR (DEtection TRansformer) model learns to detect dogs through attention maps across training epochs. The focus is on understanding how the model progressively learns to attend to specific dog features like ears, paws, and fur.

## Experiment Setup

### Model Modifications
The experiment uses a modified version of the official DETR model with reduced complexity:
- Hidden dimension: 128 (reduced from 256)
- Feedforward dimension: 1024 (reduced from 2048)
- Number of encoder/decoder layers: 3 (reduced from 6)
- Number of attention heads: 4 (reduced from 8)
- Number of queries: 10 (reduced from 100)
- Backbone: ResNet-18 (changed from ResNet-50)
- batch_size: 20
- epochs: 150

### Dataset
A custom dataset was created using a subset of COCO:
- 3,000 dog images for training
- 600 dog images for testing
- 1,000 non-dog images for training (to reduce false positives)
- 200 non-dog images for testing

## Repository Contents

### Attention Map Visualizations
- `attention_maps/`: Directory containing decoder layer attention maps for 4 out-of-distribution dog images across all training epochs
- `attention_maps/individual_query_attention_maps`: Directory containing decoder layer attention maps for individual queries across all training epochs
- `attentoin_maps/merged_attention_maps`: Directory containing merged attention maps for all queries across all training epochs. Has subfolders for attention maps with object bounding boxes overlaid and with just attention map with attention weight colormap.

  ![epoch88](https://github.com/user-attachments/assets/e23f7ba5-a277-42bb-bb53-4bed7cec5e3a)


### Convolutional Feature Visualizations
- `convolutional_features/`: Directory containing resnet18 feature maps for each convoultional layer across all training epochs
![epoch105](https://github.com/user-attachments/assets/3e42a053-561b-4ef3-bfba-64d4b1f3d028)


### Training Statistics
- `logs/training_stats.txt`: Contains loss values, learning rates, and other metrics for each epoch
- `logs/mAP_progression.txt`: Mean Average Precision (mAP) values for each epoch (the format for logging is provided in `logs/mAP_log_format.txt`)

### Animations
- `animations/final_animation.mp4`: Timelapse animation showing how attention maps evolve for test image 1 across training epochs along with the metrics for each epoch
- `animations/individual_images_time_lapse`: Timelapse animation showing how attention maps evolve for individual test images across training epochs

<!-- ## Key Findings
*[Note: Add your key findings here after completing your analysis]*

## Future Work
*[Note: Add potential future directions for this research]* -->

## Acknowledgments
This work builds upon the [official DETR implementation](https://github.com/facebookresearch/detr) by Facebook Research.
