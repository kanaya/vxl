import argparse
import numpy as np
import sys
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('xyz_file', help='XYZ file (input)')
parser.add_argument('vxl_file', help='VXL file (output)')
parser.add_argument('-r', '--resolution', type=int, default=512, help='Maximum resolution (default: 512)')
args = parser.parse_args()

xyz_filename = args.xyz_file
vxl_filename = args.vxl_file
resolution = args.resolution

def main():
	print('# Given parameters are:\n'
		'#   --resolution {}\n'
		.format(resolution))
	print('Reading {}... '.format(xyz_filename), end='', file=sys.stderr)
	with open(xyz_filename, 'r') as xyz:
		xyz_list = xyz.read().split()
	print('done', file=sys.stderr)
	print(xyz_list)

if __name__ == '__main__':
	main()
