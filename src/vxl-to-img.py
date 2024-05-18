import argparse
import cv2
import math
import numpy as np
import sys
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('vxl_file', help='VXL file (input)')
parser.add_argument('img_file', help='Image file (output)')
args = parser.parse_args()

vxl_filename = args.vxl_file
img_filename = args.img_file

def write_voxel_to_image(voxel):
	for z, vz in enumerate(tqdm(voxel)):
		output_filename = '{}-{:04}.png'.format(img_filename, z)
		cv2.imwrite(output_filename, vz)

def main():
	print('Reading {}... '.format(vxl_filename), end='', file=sys.stderr)
	voxel = np.load(vxl_filename)
	print('done', file=sys.stderr)
	write_voxel_to_image(voxel)

if __name__ == '__main__':
	main()
