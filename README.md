# Feature Importance and Harvest Prediction in Agriculture 

## Combining Sentinel 2 (all bands + computed indexes), soil, field, weather to predict harvest. 
![SHAP value](shap_bar_plot1.jpg?raw=true)

The end result of these algorithms is to a) predict harvest and b) extract importance of the input features (via SHAP) used towards that prediction. A coorelation matrix for features used is also computated. The training is based on decision trees currently. 

The method works and can be applied world-wide when just the Sentinel 2 is used. In Sweden we have the extra benefit of the actual data from farmers which further localized information about soil and harvest conditions.

The input vector construction is based on farmer data provided/collected related to soil, field info and harvest. The current version of the files requires the user to choose a crop  (e.g. Hostvete) for all fields in a user chosen region (i.e. Heddinge). The data timeframe starts at seeding the year before and ends at harvest for a given year. Data is also included from a relevant slope.tiff image as well as all 13 bands from Sentinel 2 over the same exact time frame.
This file should run 4th after running all the files listed below.

In the current version of the file we load all soil, field, year and weather data for all fields in Heddinge and predict the harvest for Hostvete for these field during a single year for which we are provided with data. The data we had included any of the years: 2017, 2018, 2019 or 2020

With the above input requirements, the actual run time which includes loading and processing all data as well as training can be 1 hour for a region like Heddinge. That time estimate includes running all 4 files (see below) needed for the data processing. The training time itself is fast and may be as little at 2 minutes (in a 56 core machine - Intel® Xeon(R) CPU E5-2697 v3 @ 2.60GHz × 56) due to the parallel processing.

The above time and spatial data specifications can easily be extended to much larger regions or much larger timeframes. In previous versions of the file I tested a time frame of 4 years for a specific crop (instead of the current implementation of one year) with comparable results in terms of accuracy of prediction.  Clearly the overall time to upload and process the algorithm increased linearly with the number of data (training was very fast).

## Order of files to be run for processing the data and subsequent training

We now discuss the work-flow for this project. we first need to produce bounding boxes around all the soil coordinates provided in the chosen region (e.g. Heddinge). This is done with file storeSoilCenters.ipynb. The resulting file of soil coordinate centers is then used by the file cut_out_bb.py to cut out small bounding boxes from the image file slope.tiff. All these bounding boxes are stored in individual numpy arrays for later processing. Then file 3, downSent2.ipynb is run in order to download Sentinel 2 data from the region of interest which are then stored in newly created subdirectories for later processing. Finaly file 4, inpVecVPN_Sent2_Aug31.ipynb is run which does all the data processing and eventual trainding. Specifically it: a) reads the file centers.txt containing the soil coordinates and uploads the numpy arrays (i.e. the bounding boxes cut out of the slope.tiff image) and creates a feature in our input vector; b) reads in all the soil, harvest, field and weather data via VPN from t-kartor service; c) processes all data from part b to extract spatial and temporal features and stores them into the input vector dataframe; d) loads the images and bands already stored into the subdirectories e) processes these and extract spatial and temporal features which are also stored into the input vector dataframe. A coorelation matrix is also created between the input features.

Once all of the input vector dataframe has been built the training starts. This is done with decision trees using a k-fold method. Subsequently SHAP importance values are produced and a mean absolute SHAP values is computed among some 260 features.

![SHAP value](shap_bar_plot1.jpg?raw=true)
![Mean Absolute of SHAP](shap_bar_plot2.jpg?raw=true)

Files must be run in the following order:

    1. storeSoilCenters.ipynb on AgricultureProject (AP) dir creates the centers.txt from soil data
    2. cut_out_bb.py on AP/Slope_Images/ creates 100s of npy files with bboxes of slope.tiff with side 2r
    3. downSent2.ipynb on eo-learn-master/examples/crop-type-classification creates eopatches of AOI and in particular respective npy files of 13 bands for that region over same timeframe (see dates below) as required in this file here.
    4. inpVecVPN_Sent2_Aug31.ipynb to import all the data, do the data clearning and training and finally produce the harvest prediction.

The dates used in the current implementation of the algorithm begin at seed data (the year before) until harvest date. 
Thus weather grouping is performed based on the seasons which begin from seed date -> 1st Nov year before + 15Marh->midsummer + midsummer -> max harvest date
Currently the code allows the used to choose to group the above automatically to daily, weekly, monthly or seasonal grouping in the final input vector. This is achieved simply by changing the hyperparameters to, respectively, "d", "w", "m" or "s". Instructions are included in the file.

#### Note: extensive descriptions are provided within each cell of the notebook files. So specific information of what is done can be found there.
