# Fingerprint_Recognition

**Title:** Fingerprint Recognition <br>

**Name:** Sherlon Almeida da Silva <br>

**Abstract:** Given an image containing a fingerprint as an input, the algorithm must verify that this fingerprint is in the database. <br>

**Image Processing Tasks Involved:** Image Enhancement, Image Segmentation, Morphology Processing. <br>

**Steps:** Input -> Image Enhancement (Gabor Filter) -> Image Segmentation (Adaptive Limiarization) -> Morphology Processing (Opening) -> Manual Image Enhancement (Interactive Drawing) -> Skeletonization -> Features Extraction (SIFT) -> Matching

**Application:** Biometry <br>

**Databases available at:** <br>
http://bias.csr.unibo.it/fvc2000/databases.asp <br>
http://biometrics.idealtest.org/dbDetailForUser.do?id=7 <br>

**To run the program type:** <br>
python3 fingerprint.py img1 img2 <br>

**Input examples:** <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/01_example1.jpg) 
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/01_example2.jpg) 
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/01_example3.jpg) <br>
**Database:** The images have different sizes and the fingerprints may have been taken with different rotations and noise.<br>

**Project Steps:**<br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/00-Project_Steps.jpg) <br>

**Steps:** The figure above shows the steps of the implemented system for fingerprint enhancement and recognition. <br>

**Checkpoint 1 Results:**<br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/02_Initial_Enhancement.png) <br>

**Results:** The input images was binarized with adaptive limiarization in order to segment the fingerprint. After that, the morphological processing was applied to remove noise. The actual results show that are necessary a method to improve the input image before the segmentation, to remove the discontinuities in the fingerprint, because the features extraction step depends of it to do a better work.


**Checkpoint 2 Results:**<br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/03_Filtering.png) <br>

**Results:** The Gabor filter presents a small improvement in the original fingerprint. The application of the Gabor Filter applies a blurred effect in the image, in this way a deblurring method was applied. After that, the image was binarized and thinned by a method of skeletonization. The results presented so far seem promising, although the fingerprint segmentation is still not perfect due to the existing noise. The next step is to to avoid the noise in the fingerprints.


**Checkpoint 3 Results:**<br>
In this first image there is no modification with the interactive drawing. It is observed that there are several connections between the ridges and valleys that should not be there. <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/4.1-ManualEnhancement.png) <br>

Then in this second image the ridges were highlighted in some places. The result is interesting, since it shows great improvement in the highlighted regions but loses information in the other regions. <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/4.2-ManualEnhancement.png) <br>

And in the third image the process of interactive drawing was inserted after the stage of segmentation and morphological processing, because in this way the effort to enhance the image is reduced and the results are also satisfactory. <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/4.3-ManualEnhancementAfterOpening.png) <br>

**Results:** 
After preprocessing the image there is an option to draw interactively over the fingerprint, in order to generate an image with less noise. Although a manual step has been employed, it is necessary to appreciate the precision in fingerprint processing. The results obtained are relevant since they have significantly improved the original fingerprint, as can be seen in the images above. The next step is to extract the features from the input fingerprints and match the recognized fingerprints.

**Checkpoint 4 Results:**<br>
In the first image the interactive drawing process was not considered in order to verify the recognition rate with these configurations. <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/5.1-FeatureExtraction-WithoutDraw.png) <br>

But in the second image, although the results of manual enhancement and skeletonization were better, the recognition maintained the same rate. <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/5.2-FeatureExtraction-WithDraw.png) <br>

**Results:** 
In the features extraction step and recognition step, algorithms from the OpenCV library were used. For the extraction of fingerprint features, the SIFT algorithm (Scale-Invariant Feature Transform) was used and the FLANN (Fast Approximate Nearest Neighbor Search Library) algorithm was used for the recognition step. The results show that even if the image is improved manually, the rate of accuracy remains the same. That is, the features obtained from SIFT are not suitable for fingerprint recognition.
