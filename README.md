# Writing RT-Struct 
## Description : 
  This code gets 3D mask (nii format) and converts it to RT struct readable with medical softwares. 
## Note: 
 1. Works with Nifti & Numpy input 
	* nii input in order (rows,cols,slices)
	* npy input in order (slices,cols,rows) 
		* The code rearranges npy order to conventional format
 2. Only creates body contour 
 3. CT Serie must be placed in a clean directory 
    * No CT check happens
 
 ### Updated version : 0.0.9 (10-21-2021)