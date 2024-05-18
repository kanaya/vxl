import argparse
import cv2
import numpy as np
import sys
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('img_file_prefix', help='IMG file prefix (input)')
args = parser.parse_args()

img_file_prefix = args.img_file_prefix

def render(volume_data):
    dataImporter = vtk.vtkImageImport()
    data_string = volume_data.tobytes()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))

    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, volume_data.shape[2]-1, 0, volume_data.shape[1]-1, 0, volume_data.shape[0]-1)
    dataImporter.SetWholeExtent(0, volume_data.shape[2]-1, 0, volume_data.shape[1]-1, 0, volume_data.shape[0]-1)

    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)
    alphaChannelFunc.AddPoint(63, 0.05)
    alphaChannelFunc.AddPoint(127, 0.5)

    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(15, 0.0, 0.0, 1.0)
    colorFunc.AddRGBPoint(63, 0.0, 1.0, 0.0)
    colorFunc.AddRGBPoint(127, 1.0, 0.0, 0.0)

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
	render(voxel)

if __name__ == '__main__':
	main()
