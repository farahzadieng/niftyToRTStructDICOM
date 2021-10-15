"""

> This program converts number of arrays to RT Struct
> Nii version
> author : Mohamdareza Farahzadi
> owner : wira a.i. systems 
> contact : farahzadiphy@gmail.com
"""
import sys,os, random
import datetime
import numpy as np
import nibabel as nib
import pydicom
from pydicom import dcmread
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.sequence import Sequence
from pydicom.uid import UID 
from pydicom.uid import  generate_uid
from skimage import measure

class Process:
    def __init__(self,ctDir,rsPath):
        self.position, self.SOPClass, self.SOPinstance, self.header , ct = self.get_ct(ctDir)
        self.contour = self.get_contour(rsPath, self.position)
    
    # EDIT    
    def get_contour(self,rsPath,imagePosition):
        rs = nib.load(rsPath).get_fdata()
        contourList = []
        for i in range(rs.shape[2]):
            contourList.append(measure.find_contours(rs[:,:,i])[0])
        contourPoints = []
        for idx,val in enumerate(contourList):
            # points = np.zeros([val.shape[0] * 3],dtype='float')
            points = [None] * (val.shape[0] * 3)
            for index in range(val.shape[0]):
                points[(3*(index+1))-3] = val[index,0]
                points[(3*(index+1))-2] = val[index,1]
                points[(3*(index+1))-1] = imagePosition[idx,3]
            contourPoints.append(points)
        return contourPoints
    # EDIT END
    def get_ct(self,ctDir):
        osSep = os.sep
        files = os.listdir(ctDir)
        imagePosition = np.zeros([len(files),5])
        SOPInstanceList = [None] * len(files)
        SOPClassList = [None] * len(files)
        for idx,val in enumerate(files):
            a = dcmread(ctDir+osSep+val)
            imagePosition[idx,0] = idx
            imagePosition[idx,1] = a.ImagePositionPatient[0]
            imagePosition[idx,2] =a.ImagePositionPatient[1]
            imagePosition[idx,3] = a.ImagePositionPatient[2]
            imagePosition[idx,4] = a.SliceLocation
            SOPInstanceList[idx] = a.SOPInstanceUID
            SOPClassList[idx] = a.SOPClassUID
        imagePosition = imagePosition[np.argsort(imagePosition[:,4])]
        header = Header(ctDir,osSep,files,imagePosition)
        ct = dcmread(ctDir+osSep+files[random.randint(range(len(files)))])
        return imagePosition,SOPClassList,SOPInstanceList, header , ct
        
    def RT_struct(self, ct):
        file_meta = FileMetaDataset()
        file_meta.FileMetaInformationGroupLength = 164
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = UID('1.2.840.10008.5.1.4.1.1.481.3')
        file_meta.MediaStorageSOPInstanceUID = SOPInstanceUID = generate_uid()
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
        file_meta.ImplementationClassUID = ct.file_meta.ImplementationClassUID
        ds = Dataset()
        ds.is_little_endian = False
        ds.is_implicit_VR = False
        ds.SpecificCharacterSet = 'ISO_IR 192'
        dt = datetime.datetime.now()
        ds.InstanceCreationDate = dt.strftime('%Y%m%d')
        ds.InstanceCreationTime = dt.strftime('%H%M%S.%f')
        ds.SOPClassUID = UID('1.2.840.10008.5.1.4.1.1.481.3')
        ds.SOPInstanceUID = SOPInstanceUID
        ds.StudyDate = ct.StudyDate
        ds.StudyTime = ct.StudyTime
        ds.AccessionNumber = ''
        ds.Modality = 'RTSTRUCT'
        ds.Manufacturer = 'wira a.i. systems'
        ds.ReferringPhysicianName = ''
        ds.StationName = 'wirasystems'
        ds.StudyDescription = ct.StudyDescription
        ds.SeriesDescription = 'Contouring'
        ds.ManufacturerModelName = 'wirasystems'
        ds.PatientName = ct.PatientName
        ds.PatientID = ct.PatientID
        ds.PatientBirthDate = ct.PatientBirthDate
        ds.PatientSex = ct.PatientSex
        ds.OtherPatientIDs = ct.OtherPatientIDs
        ds.DeviceSerialNumber = 'developer01-master'
        ds.SoftwareVersions = '0.0.6'
        ds.StudyInstanceUID = ct.StudyInstanceUID
        ds.SeriesInstanceUID = generate_uid()
        ds.StudyID = ct.StudyID
        ds.SeriesNumber = ''
        ds.StructureSetLabel = 'segment_auto'
        ds.StructureSetDescription = ''
        ds.StructureSetDate = datetime.datetime.now().strftime('%Y%m%d')
        ds.StructureSetTime = datetime.datetime.now().strftime('%H%M%S.%f')
        ds.ApprovalStatus = 'UNAPPROVED'
        ds.ReviewDate = ''
        ds.ReviewTime = ''
        ds.ReviewerName = ''

class Header: 
    def __init__(self,ctPath,osSep,files,imagePosition):
        infoLast1 = dcmread(ctPath+osSep+files[int(imagePosition[-1,0])])
        infoLast2 =  dcmread(ctPath+osSep+files[int(imagePosition[-2,0])])
        origin1 = infoLast1.ImagePositionPatient
        origin2 = infoLast2.ImagePositionPatient
        self.x0 = origin1[0]
        self.y0 = origin1[1]
        self.z0 = origin1[2]
        self.rows = infoLast1.Rows
        self.cols = infoLast1.Columns
        self.pixelSize = infoLast1.PixelSpacing
        self.sliceSpacing = np.linalg.norm(origin2[2]-origin1[2])
        
def get_lists(args):
    try:
        ctDir = args[1]
        rsPath = args[2]
    except:
        print('The corect form to run the program :')
        print('python main.py [path to ct directory] [path to nmp file]')
    finally:
        return ctDir, rsPath
        
if __name__ == '__main__':
    ctDir ,rsPath = get_lists(sys.argv)
    process = Process(ctDir,rsPath)
    print(process.header.x0)


"""
rs is path to Nii. rt struct 
edit in case for nmpy format
"""