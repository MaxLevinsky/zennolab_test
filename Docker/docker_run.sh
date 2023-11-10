#!/bin/bash

# choose a directory with ground truth json in COCO format
read -r -p "Input dir: " input_dir

# choose an output dir
read -r -p "Output dir: " output_dir


docker run --gpus all --rm \
	--mount type=bind,source=${input_dir},target=/zennolab/input,readonly \
	--mount type=bind,source=${output_dir},target=/zennolab/output \
	zennolab:latest \
	run_evaluation -i /zennolab/input -o /zennolab/output
