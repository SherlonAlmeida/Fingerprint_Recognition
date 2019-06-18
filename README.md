# Fingerprint_Recognition

**Title:** Fingerprint Recognition <br>

**Name:** Sherlon Almeida da Silva <br>

**Abstract:** Given an image containing a fingerprint as an input, the algorithm must verify that this fingerprint is in the database. <br>

**Image Processing Tasks Involved:** Image Enhancement, Image Segmentation, Morphology Processing. <br>

**Steps:** Input -> Image Enhancement (Gabor Filter) -> Image Segmentation (Adaptative Limiarization) -> Morphology Processing (Opening) -> Manual Image Enhancement (Interactive Drawing) -> Skeletonization -> Features Extraction (Minutiae) -> Matching

**Application:** Biometry <br>

**Databases available at:** <br>
http://bias.csr.unibo.it/fvc2000/databases.asp <br>
http://biometrics.idealtest.org/dbDetailForUser.do?id=7 <br>

**Input examples:** <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/01_example1.jpg) 
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/01_example2.jpg) 
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/01_example3.jpg) <br>
**Database:** The images have different sizes and the fingerprints may have been taken with different rotations and noise.<br>

**Checkpoint 1 Results:**<br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/02_Initial_Enhancement.png) <br>

**Results:** The input images was binarized with adaptive limiarization in order to segment the fingerprint. After that, the morphological processing was applied to remove noise. The actual results show that are necessary a method to improve the input image before the segmentation, to remove the discontinuities in the fingerprint, because the features extraction step depends of it to do a better work.


**Checkpoint 2 Results:**<br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/03_Filtering.png) <br>

**Results:** The Gabor filter presents a small improvement in the original fingerprint. The application of the Gabor Filter applies a blurred effect in the image, in this way a deblurring method was applied. After that, the image was binarized and thinned by a method of skeletonization. The results presented so far seem promising, although the fingerprint segmentation is still not perfect due to the existing noise. The next step is to to avoid the noise in the fingerprints.


**Checkpoint 3 Results:**<br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/4.1-ManualEnhancement) <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/4.2-ManualEnhancement) <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/4.3-ManualEnhancementAfterOpening) <br>

**Results:** 
After preprocessing the image there is an option to draw interactively over the fingerprint, in order to generate an image with less noise. Although a manual step has been employed, it is necessary to appreciate the precision in fingerprint processing. The results obtained are relevant since they have significantly improved the original fingerprint, as can be seen in the images above. The next step is to extract the features from the input fingerprints and match the recognized fingerprints.
