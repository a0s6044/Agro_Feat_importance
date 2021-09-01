# Agro_Feat_importance

## Here we train decision trees based on an input vector which we construct.

The Input vector construction is based on soil, weather and harvest data (related to a chosen crop - e.g. Hostvete) for all fields in a chosen region (i.e. Heddinge). The data timeframe starts at seeding the year before and ends at harvest for a given year. Data is also included from a relevant slope.tiff image as well as all 13 bands from Sentinel 2 over the same exact time frame.
This file should run 4th after running all the files listed below.

With the above specifications, the actual time to load and process all data can be 1 hour when looking. That time estimate includes running all 4 files needed for the data processing. The training time is much faster and may be as little at 2 minutes (in a 56 core machine - Intel® Xeon(R) CPU E5-2697 v3 @ 2.60GHz × 56) due to the parallel processing.

The above time and spatial data specifications can easily be extended to much larger regions or much larger timeframes. Early on I have tested with 4 years instead of one year and the file worked just fine with all that data although took more time to train.

Files must be run in the following order:

    1. storeSoilCenters.ipynb on AgricultureProject (AP) dir creates the centers.txt from soil data
    2. cut_out_bb.py on AP/Slope_Images/ creates 100s of npy files with bboxes of slope.tiff with side 2r
    3. downSent2.ipynb on eo-learn-master/examples/crop-type-classification creates eopatches of AOI and in particular respective npy files of 13 bands for that region over same timeframe (see dates below) as required in this file here.
    4. inpVecVPN_Sent2_Aug31.ipynb to import all the data, do the data clearning and training and finally produce the harvest prediction.

We now include the correct dates for weather grouping for hostvete which begin from seed date -> 1st Nov year before + 15Marh->midsummer + midsummer -> max harvest date

We load all soil, field, year and weather data for all fields in Heddinge and predict the harvest for that field during a single year. Can be any of: 2017, 2018, 2019 or 2020

Also improoved the grouping in time for weather data and it can be a single season or monthly or even daily grouping instead of just the original weekly grouping

We segment per crop and year in this particular notebook
