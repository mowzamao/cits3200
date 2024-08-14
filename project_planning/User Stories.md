# Sprint 2 User Stories

1. As a researcher, I want to take a photo of a sediment core and plot the changes in colour over the length of the core so that I can use an automatic process for colour stratigraphy for comparison against laboratory chemical analysis.

2. As a researcher, I want to be able to access the sediment core data as corresponding to a length in millimetres, so that I can easily compare the application’s results to the physical sediment core.

3. As a researcher, I want to be able to use the same application to analyse different sediment cores, so that I can get accurate results from cores other than just the MI-24-03 and MI-24-04 sediment cores from Pink Lake instead of performing a stratigraphical analysis.

4. As a researcher, I want the output data to include a predicted Munsell colour chart index associated with each sediment data point, so that I can use that information to get a more standardised and non-subjective colour output.

5. As a researcher, I want to have the option of inputting multiple images of the core, so that I can get a more accurate average reading of colour data as output and be able to account for different lighting conditions.

6. As an end-user, I want the application to be packaged into a single executable, so that I can have the application be easier to use and share.

7. As an end user, I want to choose the folder on my computer that the program saves the plots and sediment core data to, so that I can more easily store and access the data.

8. As a researcher, I want to be able to convert the data and plots between the RGB and CIELAB colour spaces, so that I can present findings in a more standardised format for my research.

9. As a researcher, I want to submit an image of a Munsell colour chart along with the sediment core image to the program, so that I can update the Munsell colour chart indices in the program to match that of the camera’s specifications.

10. As an end-user, I want to have an intuitive and graphical user interface for the application, so that I can use it easily and quickly.

# 

# 

# Task Breakdown of User Stories

**Story 1:** As a researcher, I want to take a photo of a sediment core and plot the changes in colour over the length of the core so that I can use an automatic process for colour stratigraphy for comparison against laboratory chemical analysis.

*Task Breakdown:*

* Make it possible to input an image to the program

* Parse input image into data

  * Clean image data to only that of sediment core

  * Transform image data to 2D arrays of RGB colour values

    * Isolate RGB data within the image

    * Format data in a standard format

* Turn image data into individual RGB colour plots

* Output graphs to user

  * Display graph as output

  * Create file for graph output

  * Create file for data output

**Story 2:** As a researcher, I want to be able to access the sediment core data as corresponding to a length in millimeters, so that I can easily compare the application’s results to the physical sediment core.

*Task breakdown:*

* Correct for barrel / pincushion distortion  
* Format image data by length

  * Take pixels as relative measurement per data point, or

  * Calculate length from point of reference

    * Potentially accept user input length of core

    * Potentially have a ruler in the image

**Story 3:** As a researcher, I want to be able to use the same application to analyse different sediment cores, so that I can get accurate results from other cores than just the MI-24-03 and MI-24-04 sediment cores from Pink Lake instead of performing a stratigraphical analysis.

* Make program general to work on different input images

  * Make image input be able to work for various resolutions and ratios

  * Make output be able to work for various sizes of data

* Make data fulfill a significant accuracy for more generalised inputs

**Story 4:** As a researcher, I want the output data to include a predicted Munsell colour chart index associated with each sediment data point, so that I can use that information to get a more standardised and non-subjective colour output.

* Associate data points to indexes in a Munsell colour chart

  * Store Munsell colour indexes to RGB map in program files

  * Map likelihood of Munsell colour index to RGB data

* Potentially map regions of Munsell colour indexes to areas on graph

**Story 5:** As a researcher, I want to have the option of inputting multiple images of the core, so that I can get a more accurate average reading of colour data as output and be able to account for different lighting conditions.

* Allow multiple images to be added as input for program

  * Standardise image inputs to be independent of resolution

  * Parse and store images data separately

* Create average graphs for RGB colour out of individual image data

* Create multi-threaded processes for parsing multiple images to data

**Story 6:** As an end-user, I want the application to be packaged into a single executable, so that I can have the application be easier to use and share.

* Implement application framework to package and run program

  * Compile a ‘single file’ application for version releases

  * Create application GUI for ease of use

    * Connect application interface to program controls

    * Connect program output to application GUI

**Story 7:** As an end user, I want to choose the folder on my computer that the program saves the plots and sediment core data to, so that I can more easily store and access the data.

* Make folder selection method for Windows computers to save output

  * Add output folder as input, or

  * Prompt user for output folder after creating graphs and data

* Make folder selection method for Unix-based OSs to save output (lower priority)

**Story 8:** As a researcher, I want to be able to convert the data and plots between the RGB and CIELAB colour spaces, so that I can present findings in a more standardised format for my research.

* Make program optionally output CIELAB colour coordinates

  * Add input option for CIELAB or RGB colour data

    * Create function to change RGB data to CIELAB

**Story 9:** As a researcher, I want to submit an image of a Munsell colour chart along with the sediment core image to the program, so that I can update the Munsell colour chart indices in the program to match that of the camera’s specifications.

* Regenerate Munsell indices to RGB values based on input Munsell colour chart image

  * Recognise image as Munsell colour chart (or inversely as a sediment core)

  * Get RGB colour values for each Munsell index on page

    * Format image for finding Munsell colours on the page

**Story 10:** As an end-user, I want to have an intuitive and graphical user interface for the application, so that I can use it easily and quickly.

* Make user interface readable and clean, overall intuitive

  * Potential tutorial for first-time use

  * Make an easy to understand GUI interface

* Make non-user specific documentation