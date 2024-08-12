# Scope of Work

#### Sediment Colour Project

CITS3200 Group 20  
2024  
University of Western Australia

**Revision History**  
Version R0.1 12/08/2024 Sophie Mowe. Created

# Preface

This document addresses the requirements of the Sediment Colour system. The intended audience for this document are the designers and the clients of this project.

## **Team Members**

* Sophie Mowe (23197128)  
* Joshua Mance (23420013)  
* Matthew Booth (23073872)  
* Blair Smith (23154502)  
* Rishwanth Katherapalle (23463452)

## **Milestones**

| Milestone | Description | Date |
| :---- | :---- | :---- |
| *Sprint 1* | Setting up overall project direction. | August 15 |
| *Sprint 2* | Delivering set of interim goals. | September 18 |
| *Sprint 3* | Delivery of final system. | October 14 |

# General Goals

Our objective is to construct a simple desktop application to perform colour stratigraphy of a sediment core from colour images. This program will specifically be used to process an image of a highly-laminated sediment core retrieved from Pink Lake in Esperance by Dr Ingrid Ward.

# Background Information

## **Sediment Colour Information**

Laminated sediment cores provide a chronological record of environmental changes, with the deepest layers representing the oldest deposits and the shallowest layers reflecting more recent conditions. This stratification is a fundamental concept in geology known as the law of superposition.

Sediment colour serves as a proxy indicator for sediment composition in paleoenvironmental and climate studies. It is affected by environmental factors such as chemical composition, organic matter and oxidation states. Analysing how sediment colour changes over time provides valuable insights into climate change.

## **Current System**

At UWA, geoarchaeologists currently measure sediment colour manually using the Munsell Colour Chart, a labour-intensive process that becomes impractical with large, extensively laminated cores. Documenting each sediment layer’s colour and size can take up to a year for complex cores.

# Proposed System

## **Overview**

Our new system will be able to produce plots depicting changes in sediment colour over time from an image of a sediment core. It will be used alongside traditional sediment analysis methods, providing additional data for geoarchaeologists at UWA.

### *General Process*

The following describes the general process of the proposed system:

1. The user uploads a list of one or more high-definition colour images of sediment core  
2. The following processes occur for each image:  
   1. Colour and lighting normalisation \- the images are pre-processed to remove artefacts  
   2. Perimeter detection \- Automatic line detection with OpenCV’s LineSegmentDetector class is utilised to determine the perimeter of the sediment core. The image is cropped to the detected sediment core perimeter, ensuring only colours from the sediment core itself are analysed.  
   3. Colour channel conversion \- A toggle will be displayed that allows the user to pick between displaying the results in the RGB or CIELAB colour space. The image will be converted to the chosen colour space.
   4. Each of the colour channel values are plotted over time, and displayed next to a rendering of the processed sediment core where the scale of the image matches the scale of the time axis.  
3. The directory to save the results to is determined:  
   1. A file explorer dialogue box will be opened so that the user can choose the directory graphically.  
      1. If the user has not used the application before, the folder will be automatically set to desktop  
      2. If the user has used the application before, the flower will automatically be set to the previously chosen file location.  
4. The results are saved by the user.  
   1. The processed sediment core image is saved as a PNG file.
   2. The plot of each colour channel over time is saved as a PNG file.
   3. The data corresponding to the plot of each colour channel over time is saved as a XLSX file, so that it is compatible with Microsoft Excel.  
5. The application’s user data is updated so that preferences (such as previously processed images and previously chosen save directories) are saved.

## **Functional Requirements**

### *Database*

An online database is not required. Users will upload the images they wish to use at the time of use. However, we will need to record user preferences regarding save location.

### *Packages*

| Package | Purpose | Licence |
| :---- | :---- | :---- |
| *Pandas* | Data processing | BSD 3-Clause |
| *OpenCV* | Computer vision, image processing | Apache 2 |
| *Matplotlib* | Plotting figures | PSF |
| *Seaborn* | Plotting figures | BSD 3-Clause |
| *PyQT* | GUI Framework | GNU General Public License 3 |

## **Nonfunctional requirements**

### *User Interface*

The interface must be graphical, featuring image and plot displays, along with buttons for loading images and saving data. It should be simple and intuitive, ensuring that geoarchaeologists with limited computing skills can easily and efficiently use the application.

### *Installation*

A user-friendly installation wizard will be used to install the application. This is required so that anyone working on sediment cores at UWA can install  the program without assistance.

### *Images*

Any sediment core image, regardless of quality and centering of the sediment core, should be able to be uploaded and processed. The application must correct for errors and image noise and detect sediment cores.

### *Documentation*

Thorough documentation, including the mathematical basis for the algorithms used, must be made available to UWA’s Ocean Institute so that results can be used in experiments and publications.

### *Hardware Considerations*

The system must run efficiently on an offline Windows operating system. The team will ensure that the image processing pipeline is minimally complex, so that the application can run quickly without requiring specialised hardware like GPUs or high-end CPUs. 

### *System Modifications*

Future Windows updates, python releases or updates to packages may render our software obsolete. The team will not provide support beyond October 2024\.

### *Security Issues*

No data other than user preferences regarding the save directory will be stored. Thus, there are no issues regarding data reliability or confidentiality. 

The program must be developed such that only image files are accepted as input. This ensures that malicious scripts or code will not be able to be executed on the system through our software.

### *Resources Issues*

Our team is not responsible for sourcing sediment core images. Any required images will be supplied by the client.