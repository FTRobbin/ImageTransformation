```
python ImageTransformationKai.py -h
usage: ImageTransformationKai.py [-h] [--image_dir IMAGE_DIR]
                                 [--transformation TRANSFORMATION]
                                 [--const_alpha CONST_ALPHA]
                                 [--const_beta CONST_BETA]
                                 [--output_image_dir OUTPUT_IMAGE_DIR]
                                 [--output_type OUTPUT_TYPE]
                                 [--num_workers NUM_WORKERS]
                                 [--max_images MAX_IMAGES]

optional arguments:
  -h, --help            show this help message and exit
  --image_dir IMAGE_DIR
                        Directory containing all images
  --transformation TRANSFORMATION
                        0 = none, 1 = shift, 2 = rotation, 3 = random
                        Gaussian, 4 = random Uniform
  --const_alpha CONST_ALPHA
                        Degree for rotation, dx for shift, std dev for
                        gaussian, +- range for random uniform
  --const_beta CONST_BETA
                        dy for shift, number of trails for random
  --output_image_dir OUTPUT_IMAGE_DIR
                        Directory to output transformed images
  --output_type OUTPUT_TYPE
                        File type to output
  --num_workers NUM_WORKERS
                        Number of threads
  --max_images MAX_IMAGES
                        Total number of images to process
```