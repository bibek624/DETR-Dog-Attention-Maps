from manimlib import *
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob
import random
import pandas as pd
from manim import constants
from importlib import reload


class DETRAttentionEvolution(InteractiveScene):
    
        
    def construct(self):
        # Set aspect ratio to 4:3

        
        
        self.clear()
        LIGHT_GREY = GREY
        # Configuration
        base_path = r"C:\Users\bparaju\OneDrive - Oklahoma A and M System\DETR\detr\Final Visualization\Images"
        base_path = r"C:\Users\bparaju\OneDrive - Oklahoma A and M System\DETR\detr\Final Visualization\attention_map and box"
        attention_folders = sorted([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])[:4]
        num_epochs = 150
        num_frames = 30  # Number of frames to show in the time-lapse
        
        # Create a stylish gradient background
        background = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Add a subtle gradient effect using a different approach
        gradient_overlay = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fill_color=BLUE_E,
            fill_opacity=0.1,
            stroke_width=0
        )
        
        self.add(background, gradient_overlay)
        
        # Create title with a more modern look
        title = Text("Detection Transformer (DETR)", font="Arial", color=BLUE_C).scale(0.8).to_edge(TOP, buff = 0.1)
        subtitle = Text("Decoder Attention Map Evolution During Training", font="Arial", color=LIGHT_GREY).scale(0.6)
        subtitle.next_to(title, DOWN, buff=0.1)
        title_group = VGroup(title, subtitle)
        
        

        test_image_path = r"C:\Users\bparaju\OneDrive - Oklahoma A and M System\DETR\detr\test images"
        test_image1 = ImageMobject(test_image_path + r"\im1.jpg")
        map_folder = r"C:\Users\bparaju\OneDrive - Oklahoma A and M System\DETR\detr\Final Visualization\attention_map and box"
        # Load all attention map images for animation
        attention_images = []
        
        # Preload all attention map images
        for epoch in range(1, 150+1):
            img_path = os.path.join(map_folder, f'im1\\epoch{epoch}.png')
            if os.path.exists(img_path):
                attention_images.append(ImageMobject(img_path))
            else:
                # If specific epoch doesn't exist, use the last available one
                if attention_images:
                    attention_images.append(attention_images[-1])
                else:
                    # If no images are available yet, use the first epoch
                    first_img_path = os.path.join(map_folder, f'im1\\epoch1.png')
                    if os.path.exists(first_img_path):
                        attention_images.append(ImageMobject(first_img_path))
        
        # Position all images correctly (same position as the initial_map)
        initial_map_path = os.path.join(map_folder, f'im1\\epoch1.png')
        initial_map = ImageMobject(initial_map_path)
        initial_map.move_to(test_image1.get_center())
        # Position all attention maps to match the initial one
        for img in attention_images:
            img.match_width(initial_map)
            img.match_height(initial_map)
            img.move_to(initial_map)
        
        
        
        main_axes = Axes(
            x_range=[0, 150, 25],
            y_range=[0, 16, 4],  # Adjusted max to better fit loss values
            width=test_image1.get_width()*1.25,
            height=test_image1.height,
            axis_config={"color": BLUE},
        )
        
        main_axes.next_to(test_image1, RIGHT, buff=0.6)
        
        # Create y-axis labels for loss
        label_scale = 0.3
        y_labels = VGroup()
        for y_val in range(0, 17, 2):
            label = Text(str(y_val), font="Arial", color=RED_C).scale(label_scale)
            label.next_to(main_axes.c2p(0, y_val), LEFT, buff=0.1)
            y_labels.add(label)
        
        # Create x-axis labels
        x_labels = VGroup()
        for x_val in range(0, 151, 25):
            label = Text(str(x_val), font="Arial", color=WHITE).scale(label_scale)
            label.next_to(main_axes.c2p(x_val, 0), DOWN, buff=0.1)
            x_labels.add(label)
        
        # Create right y-axis as a NumberLine for mAP (in percentage 0-40%)
        right_y_axis = NumberLine(
            x_range=[0, 40, 5],
            width=test_image1.height,
            color=GREEN,
            include_numbers=False,  # Turn off default numbers to create our own
            line_to_number_direction=DOWN,
        ).rotate(PI/2).next_to(main_axes.x_axis.get_end(), UP, buff=0)
        
        # Create custom mAP y-axis labels
        map_y_labels = VGroup()
        for y_val in range(0, 41, 5):
            label = Text(str(y_val), font="Arial", color=GREEN_C).scale(label_scale)
            # label.rotate(PI/2)  # Rotate labels to match axis orientation
            label.next_to(right_y_axis.n2p(y_val), RIGHT, buff=0.1)
            map_y_labels.add(label)
        
     
        # Create rotated labels with appropriate positioning
        loss_label = Text("Training Loss", font="Arial", color=RED_C).scale(label_scale)
        loss_label.rotate(PI/2)  # Rotate 90 degrees
        loss_label.next_to(main_axes.y_axis, LEFT, buff=0.3)
        
        map_label = Text("Mean Average Precision (mAP) %", font="Arial", color=GREEN_C).scale(label_scale)
        map_label.rotate(PI/2)  # Rotate 90 degrees
        map_label.next_to(right_y_axis, RIGHT, buff=0.4)
        
        x_label = Text("Training Epochs", font="Arial", color=WHITE).scale(label_scale)
        x_label.next_to(main_axes.x_axis, DOWN, buff=0.4)
        
        main_group = Group(main_axes, right_y_axis, y_labels, x_labels, map_y_labels, loss_label, map_label, x_label, test_image1)
        main_group.move_to(ORIGIN).shift(DOWN*0.5)
           # Add all axes to the scene
        self.play(ShowCreation(title_group),ShowCreation(main_group[:-1]),FadeIn(test_image1), run_time = 2)
        initial_map.move_to(test_image1.get_center())
        self.play(FadeIn(initial_map))
        
        # Helper function to map (x, y_right) to scene coordinates
        def get_right_point(x, y):
            # Get x-coordinate from main x-axis
            x_scene = main_axes.c2p(x, 0)[0]
            # Get y-coordinate from right y-axis
            y_scene = right_y_axis.n2p(y)[1]
            return [x_scene, y_scene, 0]
        
        # Load actual data
        df = pd.read_csv(r'C:\Users\bparaju\OneDrive - Oklahoma A and M System\DETR\detr\loss_vs_epoch.csv')
        epochs = df['epoch'].values
        losses = df['train_loss'].values
        map_values = df['mAP'].values * 100  # Convert to percentage
        
        probas_df = pd.read_csv(r'C:\Users\bparaju\OneDrive - Oklahoma A and M System\DETR\detr\epoch_probas.csv')
        image_1_probas = probas_df['Image1'].values
        
        # Helper function to get color based on probability
        def get_prob_color(prob):
            # Red to green gradient based on probability
            # 0.5 (min): Red, 0.98 (max): Green
            # Normalize the probability to a 0-1 range based on our min/max values
            normalized_prob = max(0, min(1, (prob - 0.5) / (1 - 0.5)))
            r = max(0, 1 - normalized_prob)
            g = max(0, normalized_prob)
            b = 0.1  # Small blue component for better visibility
            return rgb_to_color([r, g, b])
        
        # Create probability display with background
        prob_bg = RoundedRectangle(
            width=test_image1.get_width()/2,
            height=0.4,
            fill_opacity=0.8,
            stroke_width=1,
            stroke_color=WHITE,
            corner_radius=0.1
        )
        prob_bg.next_to(test_image1, DOWN, buff=0.1)
        
        # Initial probability text
        initial_prob = image_1_probas[0] if len(image_1_probas) > 0 else 0
        prob_label = TexText(r"$P_{Dog} = $").scale(0.6)
        prob_text = TexText('$' + f"{initial_prob:.2f}" + '$',use_labelled_svg=True).scale(0.6)
        prob_text.next_to(prob_label, RIGHT, buff=0.1)
        prob_display = VGroup(prob_label, prob_text)
        prob_display.move_to(prob_bg)
        
        # Set initial background color
        prob_bg.set_fill(get_prob_color(initial_prob))
        
        # Add probability display to scene
        self.add(prob_bg, prob_display)
        
        num_epochs = len(epochs)
        
        
        # Progressive curve drawing with image updates
    
        current_loss_dot = Dot(main_axes.c2p(0, losses[0]), color=BLUE, radius=0.05)
        current_map_dot = Dot(get_right_point(0, map_values[0]), color=GREEN, radius=0.05)
        
        self.add(current_loss_dot, current_map_dot)
        
        # Add initial label for current epoch - moved to top right of loss graph
        # OPTIMIZATION: Use text instead of Integer for epoch counter
        epoch_label = Text("Epoch: ", font="Arial").scale(0.4)
        epoch_text = Text("0", font="Arial").scale(0.4)
        epoch_text.next_to(epoch_label, RIGHT)
        epoch_display = VGroup(epoch_label, epoch_text)
        # Position at top right of loss graph
        epoch_display.next_to(main_axes.c2p(-5, 16), DR, buff=0.5)
        epoch_display.shift(UP * 0.5)
        self.add(epoch_display)
        
        # Create empty curves that will be updated
        loss_curve = VMobject(color=BLUE)
        map_curve = VMobject(color=GREEN)
        self.add(loss_curve, map_curve)

        # Create learning rate annotation that will be displayed at epoch 50
        lr_annotation = TexText("$Learning \, rate \, changed \, to \, 10^{-6}$",color=YELLOW).scale(0.4)
        lr_annotation_arrow = Arrow(
            start=ORIGIN, 
            end=DOWN * 0.5,
            color=YELLOW,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2
        )
        lr_annotation_group = VGroup(lr_annotation, lr_annotation_arrow)
        # Keep track of points for smooth curves
        loss_points = []
        map_points = []
        
        # OPTIMIZATION: Update epoch counter less frequently
        epoch_update_frequency = 5  # Update every 5 epochs
        
        # Animation steps - how many epochs to show in each animation frame
        animation_steps = 1  # Show 1 epoch in each animation frame
        
        for i in range(0, num_epochs, animation_steps):
            end_idx = min(i + animation_steps, num_epochs)
            
            new_epoch_text = Text(str(int(epochs[end_idx-1])), font="Arial").scale(0.4)
            new_epoch_text.next_to(epoch_label, RIGHT)
          
            if(i<10):
                run_time = 0.8
            elif(i<100):
                run_time = 0.4
            else:
                run_time = 0.3
            # Update attention map to match current epoch
            if i < len(attention_images):
                # Use direct index for exact epoch if available
                target_map = attention_images[i]
            else:
                # Use the last available image
                target_map = attention_images[-1]
                
            target_map.move_to(test_image1.get_center())
            
            
            # Update probability display
            current_prob = image_1_probas[i] if i < len(image_1_probas) else image_1_probas[-1]
            new_prob_text = TexText('$' + f"{current_prob:.2f}" + '$',use_labelled_svg=True).scale(0.6)
            new_prob_text.next_to(prob_label, RIGHT, buff=0.1)
            new_prob_color = get_prob_color(current_prob)
            
            # Add new points to the curves
            for j in range(i, end_idx):
                loss_points.append(main_axes.c2p(epochs[j], losses[j]))
                map_points.append(get_right_point(epochs[j], map_values[j]))
            
            # Update the curves
            if len(loss_points) > 1:
                new_loss_points = [main_axes.c2p(e, l) for e, l in zip(epochs[:end_idx], losses[:end_idx])]
                new_map_points = [get_right_point(e, m) for e, m in zip(epochs[:end_idx], map_values[:end_idx])]
                
                # Animate all updates simultaneously
                self.play(
                    FadeTransform(initial_map, target_map),
                    UpdateFromFunc(loss_curve, lambda m: m.set_points_as_corners(new_loss_points)),
                    UpdateFromFunc(map_curve, lambda m: m.set_points_as_corners(new_map_points)),
                    current_loss_dot.animate.move_to(new_loss_points[-1]),
                    current_map_dot.animate.move_to(new_map_points[-1]),
                    ReplacementTransform(epoch_text, new_epoch_text),
                    ReplacementTransform(prob_text, new_prob_text),
                    prob_bg.animate.set_fill(new_prob_color),
                    run_time=run_time,
                    rate_func=linear
                )
                initial_map = target_map
                prob_text = new_prob_text
                epoch_text = new_epoch_text
                # Show learning rate annotation at epoch 50
                if epochs[end_idx-1] == 50:
                    # Position annotation near the loss dot
                    lr_annotation_group.arrange(DOWN, buff=0.1)
                    lr_annotation_group.next_to(current_loss_dot, UP, buff=0.2)
                    
                    # Show annotation
                    self.play(
                        FadeIn(lr_annotation_group),
                        run_time=0.5
                    )
                    
                    # Hold for 2 seconds
                    self.wait(1.5)
                    
                    # Fade out
                    self.play(
                        FadeOut(lr_annotation_group),
                        run_time=0.5
                    )
        
        # Final animation to hold the scene
        self.wait(2)
        # Zoom and pan the attention map to center
        self.play(
            initial_map.animate.scale(1.6).move_to(ORIGIN).shift(UP*0.2),
            FadeOut(test_image1),
            FadeOut(main_axes),
            FadeOut(right_y_axis),
            FadeOut(y_labels),
            FadeOut(x_labels),
            FadeOut(map_y_labels),
            FadeOut(loss_label),
            FadeOut(map_label),
            FadeOut(x_label),
            FadeOut(epoch_display),
            FadeOut(loss_curve),
            FadeOut(map_curve),
            FadeOut(current_loss_dot),
            FadeOut(current_map_dot),
            FadeOut(prob_bg),
            FadeOut(prob_display),
            FadeOut(prob_label),
            FadeOut(prob_text),
            FadeOut(epoch_label),
            FadeOut(epoch_text),
            FadeOut(title_group),
            # FadeOut(initial_map),
            run_time=2
        )
        
        # Create highlights for corners
        top_right_highlight = SurroundingRectangle(
            initial_map, 
            width=initial_map.get_width()/3,
            height=initial_map.height/3,
            color=YELLOW,
            buff=0
        ).move_to(initial_map.get_corner(UR) + DOWN*0.5 + LEFT*0.5)
        
        bottom_left_highlight = SurroundingRectangle(
            initial_map,
            width=initial_map.get_width()/3,
            height=initial_map.height/3,
            color=YELLOW,
            buff=0
        ).move_to(initial_map.get_corner(DL) + UP*0.5 + RIGHT*0.5)
        
        # Create annotation text
        annotation = Text(
            "The model learns to identify features of the dog",
            font="Arial",
            color=WHITE
        ).scale(0.5)
        annotation.next_to(initial_map, DOWN, buff=0.3)
        
        # Show highlights and text
        self.play(
            # ShowCreation(top_right_highlight),
            # ShowCreation(bottom_left_highlight),
            Write(annotation),
            run_time=2
        )
        
        self.wait(2)
        
        # Fade everything out
        self.play(
            FadeOut(initial_map),
            FadeOut(annotation),
            run_time=1
        )
        
        self.play(Write(Text("Thank you for watching!")), run_time = 2)
        self.wait(2)
