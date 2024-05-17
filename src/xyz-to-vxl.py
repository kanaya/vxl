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

def create_voxel(xyz_list):
	n = int(len(xyz_list) / 3)
	xyz_array = np.array(xyz_list, dtype=float) # .reshape([n, 3])
	x_array = xyz_array[0:len(xyz_list):3]
	y_array = xyz_array[1:len(xyz_list):3]
	z_array = xyz_array[2:len(xyz_list):3]
	x_min, x_max = np.min(x_array), np.max(x_array)
	y_min, y_max = np.min(y_array), np.max(y_array)
	z_min, z_max = np.min(z_array), np.max(z_array)
	mins = [x_min, y_min, z_min]
	maxs = [x_max, y_max, z_max]
	diffs = [x_max - x_min, y_max - y_min, z_max - z_min]
	voxel_size = max(diffs) / resolution
	dimensions = [round(diffs[0] / voxel_size), round(diffs[1] / voxel_size), round(diffs[2] / voxel_size)]
	print(dimensions)
	return ()


def main():
	print('# Given parameters are:\n'
		'#   --resolution {}\n'
		.format(resolution))
	print('Reading {}... '.format(xyz_filename), end='', file=sys.stderr)
	with open(xyz_filename, 'r') as xyz:
		xyz_list = xyz.read().split()
	print('done', file=sys.stderr)
	voxel = create_voxel(xyz_list)
	print(voxel)

if __name__ == '__main__':
	main()
