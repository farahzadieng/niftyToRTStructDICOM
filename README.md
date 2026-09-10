# NII to RT-Struct Converter

Converts 3D segmentation masks (NIfTI or NumPy format) into DICOM RT-Struct files compatible with medical imaging and radiotherapy planning software.

## Features

- **Multi-format support**: Accepts NIfTI (.nii) and NumPy (.npy) segmentation masks
- **Automatic contour extraction**: Converts 3D masks to 2D contours aligned with CT slices
- **DICOM compliance**: Generates valid DICOM RT-Struct files with proper metadata
- **CT reference**: Links contours to source CT series with correct spatial positioning
- **Configuration-based**: Uses config.ini for easy directory management

## How It Works

1. Reads a CT series from a directory
2. Loads a 3D segmentation mask (NIfTI or NumPy)
3. Extracts 2D contours from each slice using image processing
4. Maps contours to CT image coordinates and positions
5. Creates a DICOM RT-Struct file with proper geometric and reference data
6. Saves output as a standard .dcm file

## Input Formats

| Format | Axis Order | Note |
|--------|-----------|------|
| **NIfTI** (.nii) | (rows, cols, slices) | Native format |
| **NumPy** (.npy) | (slices, cols, rows) | Automatically transposed to conventional format |

## Setup

1. Create `config.ini`:
   ```ini
   [Path]
   CT\_Directory = /path/to/ct/series
   Body = /path/to/mask.nii
   save\_Directory = /path/to/output
