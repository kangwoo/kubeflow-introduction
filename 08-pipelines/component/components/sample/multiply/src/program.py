from pathlib import Path

import argparse


def do_work(input_file, output_file, param):
    while True:
        line = input_file.readline()
        if not line:
            break
        number = int(line)
        output_file.write('{} * {} = {}\n'.format(number, param, (number * param)))


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='Program description')
parser.add_argument('--input-path', type=str, help='Path of the local file containing the Input data.')
parser.add_argument('--param', type=int, default=1, help='Parameter.')
parser.add_argument('--output-path', type=str, help='Path of the local file where the Output data should be written.')
args = parser.parse_args()

Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)

with open(args.input_path, 'r') as input_file:
    with open(args.output_path, 'w') as output_file:
        do_work(input_file, output_file, args.param)
