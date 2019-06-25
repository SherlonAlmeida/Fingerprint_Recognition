# Fingerprint_Recognition

**Title:** Fingerprint Recognition <br>

**Name:** Sherlon Almeida da Silva <br>

**Abstract:** Given an image containing a fingerprint as an input, the algorithm must verify that this fingerprint is in the database. <br>

**Image Processing Tasks Involved:** Image Enhancement, Image Segmentation, Morphology Processing. <br>

**Steps:** Input -> Image Enhancement: Gabor Filter + Deblurring (Constrained Least Squares Filtering Operation) -> Image Segmentation (Adaptive Limiarization) -> Morphology Processing (Opening) -> Manual Image Enhancement (Interactive Drawing) -> Skeletonization -> Features Extraction (SIFT) -> Matching

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

But in the second image, although the results of manual enhancement and skeletonization were better, the recognition maintained the same rate (**Update:The rate was equal because i forgot of modify the input of SIFT algorithm, then the original image was used. This fault was fixed.). <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/5.2-FeatureExtraction-WithDraw.png) <br>

**Results:** 
In the features extraction step and recognition step, algorithms from the OpenCV library were used. For the extraction of fingerprint features, the SIFT algorithm (Scale-Invariant Feature Transform) was used and the FLANN (Fast Approximate Nearest Neighbor Search Library) algorithm was used for the recognition step. The results show that even if the image is improved manually, the rate of accuracy remains the same. That is, the features obtained from SIFT are not suitable for fingerprint recognition.

**Checkpoint 5 Results:**<br>
In the first figure below the similarity rate between 101_1.tif and 101_2.tif fingerprints was compared. The algorithm identified 217 features in image 1 and 125 features in image 2. The algorithm found 93 hits, achieving a similarity rate of 74.4% between images 1 and 2.  <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/6.1-101_1x101_2.png) <br>

In the second figure, the similarity rate between 101_1.tif and 102_4.tif was compared. The algorithm identified 217 features in image 1 and 401 features in image 2. The algorithm found 75 hits, achieving a similarity rate of 34.5% between images 1 and 2. <br>
![image text](https://github.com/SherlonAlmeida/Fingerprint_Recognition/blob/master/6.2-101_1x102_4.png) <br>

To validate invariance to Rotation, Mirroring and Scaling, the 101_1.tif image was modified in 4 versions. The first and second versions correspond to the same rotated image 90 and 180 degrees, respectively. In the third version the image was mirrored horizontally. And in the fourth version the image was resized to a larger size than the original. When comparing the image 101_1.tif with itself the similarity rate is equal to 100%, when rotated 90 ° the similarity rate dropped to 45%. With the 180º rotation the similarity rate was 56.7%. With mirroring the similarity rate dropped to 40.1%, and finally with the resizing the similarity rate was 52.5%.

The similarity between images of the same class and distinct classes was performed using 5 test cases, as can be seen in the table below.

| INPUT     | 101_1.tif | 101_2.tif | 101_3.tif | 102_4.tif | 103_5.tif | 104_6.tif |
|-----------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| 101_1.tif |    100%   |   74.4%   |   59.4%   |   34.5%   |   36.4%   |   38.2%   |

**Results:** 
The results show that the variation of rotation, mirroring and scale affect the performance of the algorithm, but in the test cases the algorithm showed reasonable results. As can be seen, for images of the same class the algorithm obtained rates of 74.4% and 59.4% for the images 101_2.tif and 101_3.tif, respectively. While with the images of other classes the algorithm kept the similarity rate lower than 38%. As future works the feature extraction technique can be modified to try to improve the similarity rate.
