import argparse
import math
import numpy as np
import sys
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('vxl_file', help='VXL file (input)')
args = parser.parse_args()

vxl_filename = args.vxl_file

def print_voxel(voxel):
	for z, vz in enumerate(voxel):
		for y, vy in enumerate(vz):
			for x, vx in enumerate(vy):
				if vx > 0:
					print('{} {} {}'.format(x, y, z))

def main():
	print('Reading {}... '.format(vxl_filename), end='', file=sys.stderr)
	voxel = np.load(vxl_filename)
	print('done', file=sys.stderr)
	print_voxel(voxel)

if __name__ == '__main__':
	main()
