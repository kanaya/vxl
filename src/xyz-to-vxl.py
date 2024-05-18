import argparse
import math
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

def p_to_q(p, mins, d_max, dimensions):
	x = round((p[0] - mins[0]) / d_max * resolution)
	y = round((p[1] - mins[1]) / d_max * resolution)
	z = round((p[2] - mins[2]) / d_max * resolution)
	x = min(x, dimensions[0] - 1)
	y = min(y, dimensions[1] - 1)
	z = min(z, dimensions[2] - 1)
	return [x, y, z]

def create_voxel(xyz_list):
	n = int(len(xyz_list) / 3)
	xyz_array = np.array(xyz_list, dtype=float)
	x_array = xyz_array[0::3]
	y_array = xyz_array[1::3]
	z_array = xyz_array[2::3]
	x_min, x_max = np.min(x_array), np.max(x_array)
	y_min, y_max = np.min(y_array), np.max(y_array)
	z_min, z_max = np.min(z_array), np.max(z_array)
	mins = [x_min, y_min, z_min]
	diffs = [x_max - x_min, y_max - y_min, z_max - z_min]
	d_max = max(diffs)
	voxel_size = d_max / resolution
	dimensions = (math.ceil(diffs[0] / voxel_size), math.ceil(diffs[1] / voxel_size), math.ceil(diffs[2] / voxel_size))
	print('Dimensions are {}'.format(dimensions))
	voxel = np.zeros(dimensions, dtype=np.uint8)
	p_array = xyz_array.reshape([n, 3])
	for p in tqdm(p_array):
		q = p_to_q(p, mins, d_max, dimensions)
		if voxel[q[0], q[1], q[2]] < 127:
			voxel[q[0], q[1], q[2]] += 1
	return voxel

def enhance_voxel(voxel):
	for vz in tqdm(voxel):
		for vy in vz:
			for vx in vy:
				if vx > 0:
					vx = 127
	return voxel

def main():
	print('# Given parameters are:\n'
		'#   --resolution {}'
		.format(resolution))
	print('Reading {}... '.format(xyz_filename), end='', file=sys.stderr)
	with open(xyz_filename, 'r') as xyz:
		xyz_list = xyz.read().split()
	print('done', file=sys.stderr)
	voxel = create_voxel(xyz_list)
	enhanced_voxel = enhance_voxel(voxel)
	np.save(vxl_filename, enhanced_voxel)

if __name__ == '__main__':
	main()
