Today I would like to shed more light on the first project I have previously mentioned in [my last blog post](https://aleksod.github.io/Project-1-Presentation-and-More/). The premise of the task is as follows:  

### Back Story

An email from a potential client:

> Krishna & Julia -
>
> It was great to meet with you and chat at the event where we recently met and had a nice chat. We’d love to take some next steps to see if working together is something that would make sense for both parties.
>
> As we mentioned, we are interested in harnessing the power of data and analytics to optimize the effectiveness of our street team work, which is a significant portion of our fundraising efforts.
>
> WomenTechWomenYes (WTWY) has an annual gala at the beginning of the summer each year. As we are new and inclusive organization, we try to do double duty with the gala both to fill our event space with individuals passionate about increasing the participation of women in technology, and to concurrently build awareness and reach.
>
> To this end we place street teams at entrances to subway stations. The street teams collect email addresses and those who sign up are sent free tickets to our gala.
>
> Where we’d like to solicit your engagement is to use MTA subway data, which as I’m sure you know is available freely from the city, to help us optimize the placement of our street teams, such that we can gather the most signatures, ideally from those who will attend the gala and contribute to our cause.
>
> The ball is in your court now—do you think this is something that would be feasible for your group? From there we can explore what kind of an engagement would make sense for all of us.
>
> Best,
>
> Karrine and Dahlia
>
> WTWY International

#### Data:

 * MTA Data (Google it!)
 * Additional data sources welcome!

#### Skills:

 * `python` and `pandas`
 * visualizations via Matplotlib & seaborn

#### Analysis:

 * Exploratory Data Analysis

#### Deliverable/communication:

 * Group presentation (4-5 people per)
 * slide presentation
 * visual and oral communication in group presentations
 * organized project repository

# 00 - Obtaining data  
Two data types were used:
1. [Three](http://web.mta.info/developers/data/nyct/turnstile/turnstile_160903.txt) [weeks](http://web.mta.info/developers/data/nyct/turnstile/turnstile_160910.txt) [worth](http://web.mta.info/developers/data/nyct/turnstile/turnstile_160917.txt) of [MTA turnstile data](http://web.mta.info/developers/turnstile.html)
2. [MTA subway geolocation data](http://web.mta.info/developers/data/nyct/subway/Stations.csv)  
The data was loaded through this nifty Python script shared by our Metis instructors:  

```python
# Source: http://web.mta.info/developers/turnstile.html
def get_data(week_nums):
    url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt"
    dfs = []
    for week_num in week_nums:
        file_url = url.format(week_num)
        dfs.append(pd.read_csv(file_url))
    return pd.concat(dfs)

week_nums = [160903, 160910, 160917]
turnstiles_df = get_data(week_nums)
```

# 01 - Cleaning up Data  
It turns out that the turnstile data needs quite a lot of cleanup. The major problem with the data revolves around how turnstiles register each subway rider entry/exit. They run a counter that keeps on adding every passing subway rider. Therefore, to obtain meaningful data for, say, number of riders that used subway on a particular station on a given day, we need to subtract the counter for the previous day from the current day. For that, we have created two new columns, ```"PREV_DATE"``` and ```"PREV_ENTRIES"```, first:  
```python
turnstiles_daily[["PREV_DATE", "PREV_ENTRIES"]] = (turnstiles_daily
                                                       .groupby(["C/A", "UNIT", "SCP", "STATION"])["DATE", "ENTRIES"]
                                                       .transform(lambda grp: grp.shift(1)))


```
After look at the resultant data, a small minority of turnstiles actually had counters running in reverse!
```python
(turnstiles_daily[turnstiles_daily["ENTRIES"] < turnstiles_daily["PREV_ENTRIES"]]
    .groupby(["C/A", "UNIT", "SCP", "STATION"])
     .size())
```
```
C/A    UNIT  SCP       STATION        
A011   R080  01-00-00  57 ST-7 AV         20
             01-00-04  57 ST-7 AV         17
             01-00-05  57 ST-7 AV         20
A016   R081  03-06-01  49 ST               1
A025   R023  01-03-02  34 ST-HERALD SQ    20
A049   R088  02-05-00  CORTLANDT ST       15
A066   R118  00-00-00  CANAL ST           20
C019   R232  00-00-02  45 ST              20
H003   R163  01-00-02  6 AV               20
H023   R236  00-06-00  DEKALB AV          20
J034   R007  00-00-02  104 ST             20
JFK01  R535  00-00-01  HOWARD BCH JFK      1
             00-00-02  HOWARD BCH JFK      1
             00-00-03  HOWARD BCH JFK      2
JFK02  R535  01-00-01  HOWARD BCH JFK      1
             01-00-02  HOWARD BCH JFK      1
             01-00-03  HOWARD BCH JFK      1
             01-00-04  HOWARD BCH JFK      1
             01-00-05  HOWARD BCH JFK      1
             01-00-06  HOWARD BCH JFK      1
JFK03  R536  00-00-01  JFK JAMAICA CT1     2
             00-00-02  JFK JAMAICA CT1     2
             00-00-03  JFK JAMAICA CT1     1
             00-00-04  JFK JAMAICA CT1     1
             00-00-05  JFK JAMAICA CT1     1
             00-03-00  JFK JAMAICA CT1     1
             00-03-01  JFK JAMAICA CT1     1
             00-03-02  JFK JAMAICA CT1     1
             00-03-03  JFK JAMAICA CT1     1
             00-03-04  JFK JAMAICA CT1     1
                                          ..
PTH07  R550  00-01-02  CITY / BUS          1
PTH16  R550  01-00-03  LACKAWANNA          1
             01-02-03  LACKAWANNA          1
PTH19  R549  02-00-01  NEWARK C            2
R126   R189  01-00-02  CHRISTOPHER ST      6
R127   R105  00-00-00  14 ST              20
R148   R033  01-00-01  TIMES SQ-42 ST     20
R158   R084  00-06-03  59 ST COLUMBUS      1
R175   R169  01-00-04  137 ST CITY COL     1
R210   R044  00-03-04  BROOKLYN BRIDGE     6
R227   R131  00-00-00  23 ST              20
R238A  R046  02-00-03  GRD CNTRL-42 ST     1
R242   R049  01-00-02  51 ST               1
R256   R182  00-00-02  116 ST              1
R258   R132  00-00-03  125 ST             20
R304   R206  00-00-00  125 ST             20
R305   R206  01-00-00  125 ST              1
             01-00-02  125 ST             20
R310   R053  01-00-02  3 AV-149 ST        20
R317   R408  01-05-01  SIMPSON ST          1
R322   R386  00-00-02  174 ST             20
R333   R366  00-00-01  225 ST              1
R414   R162  00-00-01  ELDER AV            1
             00-03-00  ELDER AV            1
R526   R096  00-05-03  82 ST-JACKSON H     1
R550   R072  00-03-0A  34 ST-HUDSON YD     2
R622   R123  00-00-00  FRANKLIN AV        20
R629   R065  00-03-02  ROCKAWAY AV         1
R632   R067  00-00-02  PENNSYLVANIA AV     1
R646   R110  01-00-01  FLATBUSH AV-B.C    20
dtype: int64
```

The strategy of dealing with such data was borrowed yet again from our skillful Metis instructors:
```python
def get_daily_counts(row, max_counter):
    counter = row["ENTRIES"] - row["PREV_ENTRIES"]
    if counter < 0:
        # Maybe counter is reversed?
        counter = -counter
    if counter > max_counter:
        print(row["ENTRIES"], row["PREV_ENTRIES"])
        counter = min(row["ENTRIES"], row["PREV_ENTRIES"])
    if counter > max_counter:
        # Check it again to make sure we are not giving a counter that's too big
        return 0
    return counter

# If counter is > 1Million, then the counter might have been reset.  
# Just set it to zero as different counters have different cycle limits
turnstiles_daily["DAILY_ENTRIES"] = turnstiles_daily.apply(get_daily_counts, axis=1, max_counter=1000000)
```

This allowed us to create another column with actual number of entries per each turnstile without yielding negative or unrealistically huge numbers:  
![result 1](http://i.imgur.com/oJL5DU6.png)  

From there on, we could proceed with data analysis.

# 02 - Culling the Turnstile Data

The cleaned up data included all ~480 New York City stations. Such number of stations was not helpful at all, so our team needed some way to focus only on those stations that would potentially yield the best impact.  

We decided to focus only on those stations located near top tech companies hoping that their employees would be more likely to either attend the gala, donate to WomenTechWomenYes organization, or help spread the word. I used the following statement from [Built in NYC](http://www.builtinnyc.com/2017/01/17/unknown-nyc-tech-neighborhoods):  
> The majority of New York-based startups run between Midtown and lower Manhattan, a geographic result of the local tech scene getting its start in ‘Silicon Alley.’ But as real estate in Manhattan is a hot commodity, and tech startups need the space to house growing employee counts, New York City startups are opting for locations off the beaten path.  

With the help of Google Maps, we took it to mean the rectangular area enclosed by the following coordinates:  

| | Left | Right |
| --- | --- | --- |
| **Upper** | lat: 40.753512, long: -74.001387 | lat: 40.753512, long: -73.977641 |
| **Lower** | lat: 40.731191, long: -74.001387 | lat: 40.731191, long: -73.977641 |  

MTA data with geolocations was filtered with the following code:  

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')

subset = df[['Stop Name', 'GTFS Latitude', 'GTFS Longitude']]
coord_data = subset[(subset['GTFS Latitude'] >= 40.731191) &
                     (subset['GTFS Latitude'] <= 40.753512) &
                     (subset['GTFS Longitude'] >= -74.001387) &
                     (subset['GTFS Longitude'] <= -73.977641)]
# subset3 = coord_data.drop_duplicates('Stop Name')

'''
The next lines clean up the coordinates data frame and aling station names with
those in the main data frame.
'''
coord_data.rename(columns={'Stop Name': 'STATION'}, inplace=True)
coord_data['STATION'] = coord_data['STATION'].str.upper()
coord_data['STATION'] = coord_data['STATION'].str.replace(' - ','-')
coord_data['STATION'] = coord_data['STATION'].str.upper()
coord_data['STATION'] = coord_data['STATION'].str.replace('STATION', 'STA')
coord_data['STATION'] = coord_data['STATION'].str.replace('GRAND CENTRAL-42 ST', 'GRD CNTRL-42 ST')
coord_data = coord_data.rename(columns={'GTFS Latitude': 'Lat', 'GTFS Longitude': 'Long'})
```  

As can be seen from the above code, I edited certain station names in order to match those in turnstile data, otherwise stations with mismatched spelling would have been discarded when I would cross-reference the two data frames.  

When the work with MTA subway station coordinates was done, the data was merged with turnstile data to filter out all stations not included in the geographical region of interest:  

```python
stations_that_matter = turnstiles_daily.merge(geo_filtered_list, on=['STATION'])
```  

The resultant data frame included turnstile entries data of only those stations located within our geographical region of interest. Since we also had a column with the time frame information, we were able to first sort all the data in descending order based on the number of entries to come up with our recommendations on canvasser placement:  
![result 2](http://i.imgur.com/4BsO6I6.png)  
All data points have been divided by their total sum in order to create a probability mass function. Based on these results, the recommendation for WTWY is to place their canvassers on 34 St - Herald Sq station platform during the evening hours as their to priority. If WTWY has more resources, they can continue going down the list to maximize the output. You can see our resultant presentation below:  

<iframe src="https://docs.google.com/presentation/d/1gFRfIS_WktEA1gCVaVPfKRrByc2BJvZ4WLUJ7kYvmQQ/embed?start=true&loop=true&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
