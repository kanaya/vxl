import argparse
import math
import numpy as np
import sys
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('xyz_file', help='XYZ file (input)')
parser.add_argument('vxl_file', help='VXL file (output)')
parser.add_argument('-e', '--enhancement', action='store_true', help='Auto enhancement (default: false)')
parser.add_argument('-g', '--geo', action='store_true', help='Geo-coordinate system (default: false)')
parser.add_argument('-r', '--resolution', type=int, default=512, help='Maximum resolution (default: 512)')
args = parser.parse_args()

xyz_filename = args.xyz_file
vxl_filename = args.vxl_file
enhancement = args.enhancement
geo_coordinate_system = args.geo
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
	if geo_coordinate_system:
		mins = [z_min, y_min, x_min]
		dimensions = (dimensions[2], dimensions[1], dimensions[0])
	print('Dimensions are {} [voxels], resolution is {:.3f} [m/voxel]'.format(dimensions, voxel_size))
	voxel = np.zeros(dimensions, dtype=np.uint8)
	p_array = xyz_array.reshape([n, 3])
	print('Creating voxel image', file=sys.stderr)
	for p in tqdm(p_array):
		if geo_coordinate_system:
			q = p_to_q([p[2], p[1], p[0]], mins, d_max, dimensions)
		else:
			q = p_to_q(p, mins, d_max, dimensions)
		if voxel[q[0], q[1], q[2]] < 255:
			voxel[q[0], q[1], q[2]] += 1
	return voxel

def enhance_voxel(voxel):
	print('Enhancing voxel image', file=sys.stderr)
	flat_voxel = voxel.flatten()
	m = max(flat_voxel)
	factor = 255.0 / m
	for vz in tqdm(voxel):
		for vy in vz:
			for vx in vy:
				if vx > 0:
					vx = int(min(vx * factor, 255))
	return voxel

def main():
	print('# Given parameters are:\n'
		'#   --enhancement {}\n'
		'#   --geo {}\n'
		'#   --resolution {}'
		.format(enhancement, geo_coordinate_system, resolution))
	print('Reading {}'.format(xyz_filename), file=sys.stderr)
	with open(xyz_filename, 'r') as xyz:
		xyz_list = xyz.read().split()
	voxel = create_voxel(xyz_list)
	if enhancement:
		enhanced_voxel = enhance_voxel(voxel)
		np.save(vxl_filename, enhanced_voxel)
	else:
		np.save(xvl_filename, voxel)

if __name__ == '__main__':
	main()
