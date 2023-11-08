import argparse

from inference import calculate_and_save_metric


def run_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="/zennolab/input", help="A path to the input data")
    parser.add_argument("-o", "--output", default="/zennolab/output", help="An output directory")
    parser.add_argument("-d", "--device", default="cpu", help="cpu or cuda")
    args = parser.parse_args()

    calculate_and_save_metric(input_dir=args.input, output_dir=args.output, device=args.device)