Command used for training 

```
python  main.py --coco_path <path-to-images-and-anotation-file> --output_dir 'outputs'   --batch_size 10 --epochs 100 --enc_layers 3 --dec_layers 3 --dim_feedforward 1024 --hidden_dim 128 --nheads 4 --num_queries 10 --backbone resnet18  --lr '0.0001'   

```

Command used for evaluation

```
 python  detr_evaluation.py --coco_path 'path-to-images-and-annotation-files' --batch_size 20 --epochs 100 --enc_layers 3 --dec_layers 3 --dim_feedforward 1024 --hidden_dim 128 --nheads 4 --num_queries 10 --backbone resnet18  --lr '0.0001'

```

In case of manim animation, I created a plugin myself to map the shortcuts that 3b1b uses in his tutorial video

