# Feature Importance and Harvest Prediction in Agriculture 

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/heddinge.png" width="500" height="500">
<h6>Fig. Overview of fields to be analyzed. Heddinge, Sweden 2019. </h6>


### Combining Sentinel 2 (all bands + computed indexes), slope images, soil, field, weather to predict harvest. 

<img align="right"  src="images/index.png" width="200" height="500" />
The end result of the included algorithms in this repository is to a) predict harvest and b) extract importance of the input features (via SHAP) used towards that prediction. A coorelation matrix for features used is also computed. The training is based on decision trees currently. 
<img align="left" src="images/inp_vec.png" width="250" height="250" />
The input vector construction, seen in the Figure to the left, is based on farmer data provided/collected related to soil, field info and harvest. The provided schematic outlines the relationships in time and space between some (see Sentinel 2 later below) of the input data. The current version of the files requires the user to choose a crop  (e.g. Hostvete) for all fields in a user chosen region (i.e. Heddinge). The data timeframe starts at seeding the year before and ends at harvest for a given year. Data is also included from a relevant slope.tiff image as well as all 13 bands from Sentinel 2 over the same exact time frame.
This file should run 4th after running all the files listed below.

In the current version of the file we load all soil, field, year and weather data for all fields in Heddinge and predict the harvest for Hostvete for these field during a single year for which we are provided with data. The data we had included any of the years: 2017, 2018, 2019 or 2020. Since we are interested to predict harvest we begin by taking a look at its distribution. The harvest data distribution for hostvete can be seen below (for 2019).
<p float="left">
  <img src="images/harv_distr.png" width="200" height="200" /> 
</p>
<h6>Fig. Harvest distribution for Hostvete for fields in Heddinge, Sweden 2019. Horizontal axis is showing production of hostvete. Vertical axis is showing how many locations (input locations in our region of interest) produced that much hostvete. We see for instance that some (very few) fields produced as much as 16 hostvete.</h6>

The approach followed, has been tested and is general enough to be possible to apply world-wide when just the Sentinel 2 is used. In Sweden we have the extra benefit of the actual data from farmers which enriched our localized information about soil and harvest conditions.
To expedite the processing related to the satelite data we cut out the Swedish map into coordinate boxes (figure to the right) in order to later instruct Sentinel 2 to only provide us with data from a specific few such box coordinates (instead of all the data for Sweden). In the Figure to the left we see the specific 3 coordinate boxes corresponding to the coordinates of the fields from the region of Heddinge.
<img align="left"  src="images/pick3gridsSouthernSweden.png" width="200" height="250" /> 

With all of the above input requirements, the actual run time which includes loading and processing all data as well as training can be 1 hour for a region like Heddinge. That time estimate includes running all 4 files (see below) needed for the data processing. The training time itself is fast and may be as little at 2 minutes (in a 56 core machine - Intel?? Xeon(R) CPU E5-2697 v3 @ 2.60GHz ?? 56) due to the parallel processing.


The dates used in the current implementation of the algorithm begin at seed data (the year before) until harvest date. 
Thus weather grouping is performed based on the seasons which begin from seed date -> 1st Nov year before + 15 March -> midsummer + midsummer -> max harvest date.
Currently the code allows the used to choose to group the above automatically to daily, weekly, monthly or seasonal grouping in the final input vector. This is achieved simply by changing the hyperparameters to, respectively, "d", "w", "m" or "s". Instructions are included in the file.

The above time and spatial data specifications can easily be extended to much larger regions or much larger timeframes. In previous versions of the file I tested a time frame of 4 years for a specific crop (instead of the current implementation of one year) with comparable results in terms of accuracy of prediction.  Clearly the overall time to upload and process the algorithm increased linearly with the number of data (training was very fast).

## Order of files to be run for processing the data and subsequent training

Files must be run in the following order:

    1. storeSoilCenters.ipynb on AgricultureProject (AP) dir creates the centers.txt from soil data
    2. cut_out_bb.py on AP/Slope_Images/ creates 100s of npy files with bboxes of slope.tiff with side 2r
    3. downSent2.ipynb on eo-learn-master/examples/crop-type-classification creates eopatches of AOI and in particular respective npy files of 13 bands for that region over same timeframe (see dates below) as required in this file here.
    4. inpVecVPN_Sent2_Aug31.ipynb to import all the data, do the data clearning and training and finally produce the harvest prediction.

#### (Note: extensive descriptions are provided within each cell of the notebook files. So specific information of what is done can be found there.)

We now outline the work-flow for this project. 

We first need to produce bounding boxes around all the soil coordinates provided in the chosen region (e.g. Heddinge). This is done with file storeSoilCenters.ipynb. 

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/centers.png" width="200" height="200">
<h6>Fig. Sample of soil coordinates from Heddinge, Sweden. </h6>

The resulting file of soil coordinate centers is then used by the file cut_out_bb.py to cut out small bounding boxes from the image file slope.tiff. All these bounding boxes are stored in individual numpy arrays for later processing. 

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/bb_cut_out.png" width="400" height="100">
<h6>Fig. Pixel values from the slope.tiff file for a random bounding box cut-out. </h6>

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/centerpng.png" width="20" height="20">
<h6>Fig. Pixel image from the slope.tiff file of a random bounding box cut-out. </h6>

Clearly based on the above idea any other file can be included and processed in the dame way in order to later be a part of the input vector used in training (see later below).

Then file 3, downSent2.ipynb is run in order to download Sentinel 2 data from the region of interest which are then stored in newly created subdirectories for later processing. 

<p float="left">
  <img src="images/Band9Heddinge.png" width="400" height="400" />
  <img src="images/meanNDVIHeddinge.png" width="400" height="400" /> 
</p>

<h6>Fig. (Left) Example of one of the 10 downloaded bands from Sentinel 2. This is band 9 for the Heddinge fields. <br> (Right) In this example we present mean NDVI over all time requested from Sentinel 2 in order to observe any spatial changes in NDVI for the Heddinge fields, Sweden 2019.</h6>

Finally file 4, inpVecVPN_Sent2_Aug31.ipynb is run which does all the data processing and eventual training. Specifically it: 
a) reads the previously created file centers.txt based on the soil coordinates and uploads the corresponding slope data as numpy arrays (i.e. the bounding boxes cut out of the slope.tiff image - see above) and creates a feature in our input vector; 
b) reads in all the soil, harvest, field and weather data via VPN from t-kartor service; 

<p float="left">
  <img src="images/before_clean.png" width="350" />
  <img src="images/after_clean.png" width="350" /> 
</p>

<h6>Fig. (Left) Soil and harvest data happen to not coinside in general. <br>
    (Right) We removed any such data that was too far away from each other. After clean up we therefore obtain the figure above for the Heddinge fields. </h6>

c) processes all data from part b to extract spatial and temporal features and stores them into the input vector dataframe; 
d) loads the images and bands already stored into the subdirectories 
e) processes these and extract spatial and temporal features which are also stored into the input vector dataframe. 

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/ndviwithcloudclean.png" width="700" height="200">
<h6>Fig. During processing we also observe the NDVI averaged over space for each time point. To fill in the gaps from throwing out too clowdy data we perform linear Interpolation. Data from Heddinge, Sweden Nov. 2018-Aug. 2019.</h6>

Cloud cleaning is performed and linear interpolation is used when clouds made the data not possible to use. Our hyper-parameter here is 80% or above, in terms of cloud coverage, implies we had to throw away that data.

<p float="left">
  <img src="images/cloud_RGB.png" width="150" />
  <img src="images/cloud_mask.png" width="150" /> 
</p>
<h6>Fig. Cloud cover example (RGB bands). Cloud mask computed for later processing of the same image as above. Heddinge, Sweden. </h6>

If below 80% then the linear interpolation (in time) is implemented to patch-up the missing pixels.

## Input data correlation

A correlation matrix is also created between the input features.

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/coorel1.png" width="500" height="500">
<h6>Fig. Feature correlations. Note that in each feature s_ and the h_ indicates whether the data originaed from the soil database or the harvest database.</h6>

## Training Decision Trees

Once all of the input vector dataframe has been built the training starts. This is done with decision trees using a k-fold method. As you will see in the files a gradient boosting method is mainly implemented. A number of classic ML metrics are also computed,

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/accuracy_F1.png" width="200" height="200">
<h6>Fig. Metrics computed show good accuracy for several categories. The average F1 was 82% for this data. </h6>

Confusion matrices are provided below,
<p float="left">
  <img src="images/conf1_Aug22.png" width="250" />
  <img src="images/Conf2_Aug22.png" width="250" /> 
</p>
<h6>Fig. Confusion matrices (original and transpose) based on above data. </h6>


## Feature Importance

Feature importance comparisons are now performed.


<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/feat_imp_Aug22.png " width="300" height="300">
<h6>Fig. Feature importance. Note: "B" indicates band, "NORM" and "NDVI" or "NDWI" are the indexes computed. Also note that each feature indicates which date it originated from. </h6>

Subsequently SHAP importance values are produced and a mean absolute SHAP values is computed among some 260 features.

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/shap_bar_plot1.jpg" width="400" height="200">
<h6>Fig. SHAP value. </h6>

<img src="https://github.com/a0s6044/Agro_Feat_importance/blob/main/images/shap_bar_plot2.jpg" width="400" height="200">
<h6>Fig. Mean Absolute of SHAP. </h6>

### This is work in progress.... so still more to come :) 
