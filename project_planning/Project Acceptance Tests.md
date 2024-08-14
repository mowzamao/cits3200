# Project Acceptance Tests

### Sediment Colour Project

### CITS3200 Group 20

### 2024

### University Of Western Australia

### Crawley, WA 6009

# Objectives

This document describes the acceptance tests for the sediment colour analysis system and outlines the testing strategy and system tests for the software. The objective is to ensure that the software converts colour images of laminated sediment cores into meaningful data, producing plots depicting changes in sediment colour over time.

As the results are yet to be determined, test analysis reports are incomplete.

# Test Summary

## Test Outline

Our tests will cover the following primary functions:

1. Image uploading and preprocessing.  
2. Sediment core perimeter detection.  
3. Converting images between the RGB and CIELAB colour spaces.  
4. Plotting colour channels over the length of the sediment core, and exporting the results.

## Testing Strategy

### Integration

Tests will be conducted in two steps:

1. Unit tests

2. System tests

Unit tests will be employed to test small subsystems and functions within our software. For instance, a unit test will be written to test that our file upload works correctly, and then a larger system test will be written to check the image upload and preprocessing test as a whole.

### Testing Locations

Tests will initially be conducted in the development environment. Later, further testing will occur in the client’s local environment.

### Responsibility

Team members will be responsible for conducting and documenting the tests.

# Test 1: Image Upload and Preprocessing

This test has been designed to check that image uploading and preprocessing functions work correctly and efficiently.

## Specifications / Requirements

1. The system must accept image files and perform pre-processing tasks to normalise colour and lighting.   
2. The system must then display the final, normalised image.   
3. The system must accept and correctly pre-process both high-quality and low-quality images.   
4. Files that are not image files should be rejected, and an error message should appear to tell the user that the application can only process image files.

## Description / Procedure

1. Testers will manually select input files from various images of assorted quality and non-image files.  
2. Testers will attempt to upload a file to the application using the application’s GUI.   
3. If the file is accepted:  
   1. The testers will press the ‘Begin Analysis’ button on the GUI to start the colour and light correction process.   
   2. The resulting image(s) will be displayed.  
4. If the file is not accepted:  
   1. The testers will close the error dialogue box.  
   2. The testers will re-attempt to upload the next file.  
5. The process will be repeated for each of the selected files.

## Test Analysis Report

*Function and Performance Characteristics to be Demonstrated*

1. Verify the system can correctly handle non-image inputs.  
   1. Ensure the system displays an error dialogue box if any file type other than PNG or JPEG is uploaded.  
2. Verify the system effectively preprocess various image qualities.  
3. Ensure that the image pre-processing time is acceptable (i.e., should take less than one minute)

# Test 2: Perimeter Detection

The perimeter detection function automatically determines the positioning of the sediment core in an image. Allowing for manual adjustments of the result provides a failsafe if the sediment core is obscured or if the background colours are too similar to the sediment core edges. This test aims to verify the correctness of these functions.

## Specification / Requirements

1. The system must automatically detect the perimeter of the sediment core.  
   1. Various images with different sediment core orientations must be tested.  
2. The system must allow manual alterations to the sediment core perimeter through the GUI.

## Description / Procedure

1. Input data will consist of five randomly selected pre-processed images of sediment cores.  
2. The software will attempt to detect the perimeter of the sediment core (if there is one contained in the image)  
3. The application will direct the tester to use their mouse to confirm the positioning of the sediment core’s perimeter.  
4. The tester will alter the sediment core perimeter positioning.

## Test Analysis Report

*Function and Performance Characteristics to be Demonstrated*

1. Verify the system’s perimeter detection accuracy.  
   1. Check perimeters are within an acceptable range based on previous, manually selected perimeter positions.  
2. Verify the system’s GUI allows for manually selecting sediment core perimeters.

# Test 3: Colour Space Conversion

## Test Specification / Requirements

1. The system must convert RGB images to the CIELAB colour space correctly.  
2. The system must convert CIELAB images to the RGB colour space correctly.

## Test Description / Procedure

1. Input data will comprise five randomly selected sediment core images in the (default) RGB colour space.  
2. Each image will be transformed into the CIELAB colour space.  
3. Each image will be transformed back into the RGB colour space.  
4. The system will output success messages if the final image colour values match the original.

## Test Analysis Report

*Function and Performance Characteristics to be Demonstrated*

1. Verify the system successfully converts images from the RGB colour space to CIELAB in less than one minute.  
2. Verify the system successfully converts images from the CIELAB colour space to RGB in less than one minute.

# Test 4: Data Plotting and Export

## Specification / Requirements

1. The software should accurately plot the colour data over time and export the results in both image and spreadsheet formats.

## Test Description / Procedure

1. Ensure the colour extraction and conversion functions are validated, and load the extracted colour data into the software for plotting.  
2. Use the plotting function to create a graph of the extracted colour data over the core depth and review the graph accuracy ensuring the plots reflect the expected patterns based on the core stratigraphy.  
3. Check that the graph is properly labelled, with axes representing core depth and colour information.  
4. Use the export function to save the graph as a .png file and verify that the image is correctly formatted.  
5. Export the colour data and any associated metadata to a .xlsx file and check that the data is correctly formatted and relevant data (e.g., colour values, depth measurements) is included and properly organised.  
6. Compare the exported image and spreadsheet against a reference for consistency and ensure no data is missing or incorrectly plotted.

##  

## Test Analysis Report

1. The software should accurately plot and export data.  
2. Verify the correctness and usability of graphs and exported files and compare them with references available for accuracy.  
3. Review the exported .png and .xlsx for formatting consistency and data integrity as incorrect plotting or export could hinder data analysis and interpretation.

# Testing Schedule

1. All the tests are to be performed on the initial design \- by the end of sprint 2 \- September 18\.  
2. Re-evaluate the tests according to project progress and changing requirements and perform the tests again for the final design \- by the end of sprint 3 \- October 14\. 

# Test Materials

## Hardware

* Development machines  
* Target system

## Software

* Python  
* Python packages:  
  * OpenCV  
  * PyQt  
  * Numpy  
  * Seaborn  
  * Matplotlib  
* Microsoft Windows (Target Operating System)

## Test Images / Data

* High-quality sediment core colour images  
* Low-quality sediment core colour images  
* Non-image files (.xlsx, .docx, .exe, etc.)

## Documentation

* User manual  
* Test scripts

