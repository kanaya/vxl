import argparse
import cv2
import numpy as np
import sys
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from vtk.util.vtkConstants import *
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('vxl_file', help='VXL file (input)')
args = parser.parse_args()

vxl_filename = args.vxl_file

def render(voxel):
    volume_data = voxel
    dataImporter = vtk.vtkImageImport()
    data_string = volume_data.tobytes()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))

    dataImporter.SetDataScalarType(VTK_UNSIGNED_CHAR)
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, volume_data.shape[2]-1, 0, volume_data.shape[1]-1, 0, volume_data.shape[0]-1)
    dataImporter.SetWholeExtent(0, volume_data.shape[2]-1, 0, volume_data.shape[1]-1, 0, volume_data.shape[0]-1)

    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)
    alphaChannelFunc.AddPoint(127, 0.5)
    alphaChannelFunc.AddPoint(255, 1.0)

    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(0, 0.0, 0.0, 0.0)
    colorFunc.AddRGBPoint(63, 0.0, 0.0, 1.0)
    colorFunc.AddRGBPoint(127, 1.0, 1.0, 0.0)
    colorFunc.AddRGBPoint(255, 1.0, 1.0, 1.0)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    # 多視点画像生成で深度画像を生成したい場合は以下
    # volumeMapper = vtk.vtkGPUVolumeRayCastMapper()

    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    renderer = vtk.vtkRenderer()
    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)

    renderer.AddVolume(volume)
    renderer.SetBackground(0,0,0)
    renderWin.SetSize(1200, 1200)

    renderInteractor.Initialize()
    renderWin.Render()
    renderInteractor.Start()

def main():
	print('Reading {}... '.format(vxl_filename), end='', file=sys.stderr)
	voxel = np.load(vxl_filename)
	print('done', file=sys.stderr)
	render(voxel)

if __name__ == '__main__':
	main()
