# AstroToolkit
Collection of tools for data fetching, plotting and analysis

## Installation

1. With pip, the package can be installed using:

```
pip install AstroToolkit
```

2. Once this has finished, you should navigate to the package location. This should be in a '.../Lib/site-packages/AstroToolkit' folder where ... is your python install location. If you wish to find this, you can can run the following commands:

```
python

from AstroToolkit.Tools import lightcurvequery, tsanalysis
tsanalysis(lightcurvequery(survey='ztf',source=6050296829033196032))
```

As long as there are no issues with ZTF, this **should return an error** which will include the file path.

3. Navigate to this file in any terminal that can access your python environment, and run either buildwin.bat (windows) or build.sh (linux).

4. Re-run the above python commands and the error should no longer appear. The package is now fully installed.

***NOTE***: See README.txt (Linux) or README - Windows.txt (Windows) in the above directory for any additional dependencies.

## Usage

### 1. Bokeh

***NOTE:*** AstroToolkit uses Bokeh as its plotting library. The official documentation can be found at https://bokeh.org/. All plots will be saved as a static .html file, which can be opened in the browser (or from a python script using:

```
from AstroToolkit.Tools import showplot
showplot(plot)
```

where 'plot' is the name of the parameter that the plot is assigned to.

***NOTE:*** All legends can be hidden/shown in plots by double clicking the figure. Individual legend elements can be hidden/shown by single clicking them in the legend.

### 2. Importing Tools

**All Tools in the package are located in AstroToolkit.Tools**

### 3. Input

***All Toolkit functions require atleast one input from:***
1. source = ...
   
where source is a Gaia source_id (string)

2. pos = ...

where pos is a 1D list with two elements: [ra,dec] in units of degrees

<br>

**For example:**

when trying to obtain a panstarrs image, there are therefore two options:

```
dataquery(source=...)
```

and

```
dataquery(pos=...)
```

The key difference between these input formats is the way that proper motion is handled. Given coordinates (pos), the results retrieved by any Toolkit function are simply the raw data obtained from that location
in the epoch of the survey in question, with no proper motion correction. The one exception for this is detection overlays in imaging functions, as these are still possible without an initial reference proper motion (i.e. a specific object in Gaia).

In contrast to this, any Toolkit functions called using a Gaia source_id as input will correct for any proper motion of that object between the time at which the data was taken and Gaia's epoch of Jan 2016, *pre-execution*. An
example of this difference is seen in imaging functions for objects with a large proper motion. Here, using a source as input will result in an image that is centred on the object, regardless of the magnitude of its
proper motion.

Using a position as input may still produce an image which contains the object, but it is unlikely to be centred as the focus of the image has not accounted for the proper motion of the object.


<br>

***Note:*** As the functions need to sort between the different input formats, explicit declaration is required, i.e.:

```
dataquery(survey='gaia',6050296829033196032)
```

will fail.

Instead, use:

```
dataquery(survey='gaia',source=6050296829033196032)
```

# AstroToolkit Functions

All ATK functions are split into two types: those that gather data, and those that plot data.

## Data functions

### 1. dataquery

**Get all available data from a given survey.**

Supported surveys:
- gaia
- panstarrs
- skymapper
- galex
- rosat
- sdss
- wise
- twomass

```
dataquery(survey,pos=None,source=None,radius=3)
```

where:
```
survey = str, name of a supported survey
```
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
radius = int/float, radius of data query
```

##### returns:

```
{
'survey' : str, survey of data
'type' : 'data'
'source' : int/float/str, source used to get data (None if a pos was used)
'pos' : [ra,dec], pos used to get data (None if a source was used)
'data' : pandas DataFrame, the returned data
}
```

<br>

##### Example
To retrieve the gaia data for an object:
```
from AstroToolkit.Tools import dataquery

data=dataquery(survey='gaia',source=6050296829033196032)['data']
```

### 2. photquery

**Get data from a given survey, filtered to only include photometry.**

Supported surveys:
- gaia
- panstarrs
- skymapper
- galex
- rosat
- sdss
- wise
- twomass

```
photquery(survey,pos=None,source=None,radius=3)
```

where:
```
survey = str, name of a supported survey
```
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
radius = int/float, radius of data query
```

##### returns:

```
{
'survey' : str, survey of data
'type' : 'data'
'source' : int/float/str, source used to get data (None if a pos was used)
'pos' : [ra,dec], pos used to get data (None if a source was used)
'data' : pandas DataFrame, the returned data
}
```

<br>

##### Example
To retrieve the gaia photometry for an object:
```
from AstroToolkit.Tools import photquery

data=photquery(survey='gaia',source=6050296829033196032)['data']
```

### 3. bulkphotquery

**Returns available photometry from all supported surveys.**

```
bulkphotquery(pos=None,source=None,radius=3)
```

where:
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
radius = int/float, radius of data query
```

##### returns:

```
{
'type' : 'bulkphot'
'source' : int/float/str, source used to get data (None if a pos was used)
'pos': [ra,dec], pos used to get data (None if a source was used)
'data' : {
         'gaia' : pandas DataFrame, returned data (or None if no data returned)
         'galex' : pandas DataFrame, returned data (or None if no data returned)

          etc. for each survey in supported surveys
         }
}
```

<br>

##### Example
To retrieve the gaia and galex data for an object:
```
from AstroToolkit.Tools import bulkphotquery

bulk_phot=bulkphotquery(source=6050296829033196032)['data']

gaia_data=bulk_phot['gaia']
galex_data=bulk_phot['galex']
```

## Imaging functions

These functions produce images of objects from supported surveys.

***Note:*** When not using source mode, some detections can be missing for high proper motion objects. When using a source_id as input, this is no longer an issue as 'adaptive' proper motion correction is used. Here, the search radius for detections is increased to include the maximum distance that the object could have travelled in the gap between the epoch of the image and the epoch of the detection coordinates so that it is still picked up.

### 1. imagequery

**Get an image from a given survey.**

Supported surveys:
- panstarrs, supported bands = [g,r,i,z,y]
- skymapper, supported bands = [g,r,i,z,u,v]
- dss, supported bands = [g]

***Note:*** Can also use 'any' to perform an image query according to the hierarchy: panstarrs > skymapper > dss

Supported overlays: [gaia,galex_nuv,galex_fuv,rosat,sdss,twomass,wise,ztf]
***Note:*** Can also use 'all', which will enable overlays for all supported surveys.

<br>

```
imagequery(survey,pos=None,source=None,size=30,band='g',overlays=None
```

where:
```
survey = str, name of a supported survey
```
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
size = int/float, size of image in arcsec
```
```
band = str, string containing the required bands (e.g. for all panstarrs bands, use band='grizy')
```
```
overlays = str, required detection overlays (e.g. for gaia + wise, use overlays='gaia,wise') 
```

##### returns:

```
{
'type' : 'image'
'data' : array, image data
'header' : astropy header, image header
'metadata' : {
             'survey' : str, image survey
             'source' : int/float/str, source used to get image (None if a pos was used)
             'pos' : [ra,dec], pos used to get image (None if a source was used)
             'location' : [ra,dec], actual location of the image
             'size' : int/float, image size in arcsec
             'image_time' : [year,month], image time
             'wcs' : astropy wcs object of image
             'overlay' : list of overlay entries
             }
}
```

***NOTE:***  overlays are stored as a list of individual detections in the format:

```
{
'survey' : int/float/str, survey of detection
'position: [ra,dec], coordinates of detection
'radius' : float, radius of detection
'corrected' : bool, whether or not the 
'mag' : str, name of the magnitude that the detection uses in a given survey
'marker' : 'circle' or 'cross', detection symbol to overlay. circles are scaled with radius, crosses are not 
}
```

### 2. plotimage

```
plotimage(data)
```

where:
```
data = dict in format returned by imagequery
```

##### returns: 

bokeh figure object

<br>

##### Example
To retrieve and plot an image:
```
from AstroToolkit.Tools import imagequery,plotimage,showplot

image=imagequery(survey='any',source=6050296829033196032,overlays='gaia')
plot=plotimage(image)
showplot(plot)
```

## HRD function

### 1. plothrd

**Returns a HRD with a source or list of sources overlayed over a background sample.**

```
plothrd(source=None,sources=None)
```

where:

```
source = int/float/str, Gaia source_id
```
```
sources = list of sources
```

##### returns:

bokeh figure object

<br>

##### Example
To retrieve and plot an image:
```
from AstroToolkit.Tools import plothrd,showplot

plot=plothrd(source=6050296829033196032)
showplot(plot)
```

## Lightcurve functions

### 1. lightcurvequery

**Returns lightcurve data for a given survey.**

Supported surveys:
- ztf [g,r,i]

<br>

```
lightcurvequery(survey,pos=None,source=None,radius=3)
```

where:
```
survey = str, name of a supported survey
```
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
radius = int/float, radius of lightcurve query
```

##### returns:

list of lightcurve data dictionaries with an entry for each band in that survey (see below). If no data is found for a given band, that entry will be set to None. The order of these entries matches the band listing for a given survey in 'supported surveys' above.

e.g. for ztf, if g and r data were found, but no i data was found, the result would be a list:

```
[g_entry,r_entry,None]
```

where each non-None entry has the format:

```
{
'type' : 'lightcurve'
'source' : int/float/str, source used to get data (None if a pos was used)
'pos': [ra,dec], pos used to get data (None if a source was used)
'survey' : str, survey of data
'band' : str, band of lightcurve data
'data' : {
         'ra' : list of returned ra values
         'dec' : list of returned dec values
         'hjd' : list of returned hjd values
         'mag' : list of returned magnitude values
         'mag_err' : list of returned magnitude error values
         }
}
```

### 2. plotlightcurve
Supported colours: [green,red,blue,purple,orange,black]

```
plotlightcurve(data,colour='black')
```

where:
```
data = dict in format returned by lightcurvequery
```
```
colour = str, name of a supported colour
```

##### returns:

bokeh figure object

<br>

##### Example
To retrieve and plot lighcurves:
```
from AstroToolkit.Tools import lightcurvequery,plotlightcurve,showplot

lightcurves=lightcurvequery(survey='ztf',source=6050296829033196032)
for lightcurve in lightcurves:
	if lightcurve!=None:
		plot=plotlightcurve(lightcurve)
		showplot(plot)
```

## SED Functions

### 1. sedquery

**Queries all available survey for photometry and returns SED data.**

```
sedquery(pos=None,source=None,radius=3)
```

where:
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
radius = int/float, radius of data query
```

##### returns:

```
{
'type' : 'sed'
'source' : int/float/str, source used to get data (None if a pos was used)
'pos': [ra,dec], pos used to get data (None if a source was used)
'data': {
        'survey' : str, survey of data point
        'wavelength' : filter wavelength of data point
        'flux' : flux through filter
        'rel_err' : relative error on flux
        }
}
```

### 2. plotsed

```
plotsed(data)
```

where:

```
data = dict in format returned by sedquery
```

### returns:

bokeh figure object

<br>

##### Example
To retrieve and plot an SED:
```
from AstroToolkit.Tools import sedquery,plotsed,showplot

data=sedquery(source=6050296829033196032)
plot=plotsed(data)
showplot(plot)
```

## Spectrum Tools

### 1. spectrumquery

**Requests a spectrum from a given survey.**

```
spectrumquery(survey=None,pos=None,source=None,radius=3)
```

where:
```
survey = str, name of a supported survey
```
```
pos = list, [ra,dec]
```
```
source = int/float/str, Gaia source_id
```
```
radius = int/float, radius of data query
```

##### returns:

```
{
'type' : 'spectra'
'survey' : int/float/str, survey of detection
'source' : int/float/str, source used to get data (None if a pos was used)
'pos': [ra,dec], pos used to get data (None if a source was used)
'data': {
        'wavelength' : list of wavelength values
        'flux' : list of flux values
        }
}
```

### 2. plotspectrum

```
plotspectrum(data)
```

where:

```
data = dict in format returned by spectrumquery
```

##### returns:

bokeh figure object

<br>

##### Example
To retrieve and plot a spectrum:
```
from AstroToolkit.Tools import spectrumquery,plotspectrum,showplot

data=spectrumquery(survey='sdss',source=587316166180416640)
plot=plotspectrum(data)
showplot(plot)
```

## Timeseries functions

### 1. plotpowspec

**Creates a power spectrum from lightcurve data.**

```
plotpowspec(data)
```

where:
```
data = dict or list in format returned by lightcurvequery
```

<br>

##### Example
To retrieve data for and plot a power spectrum:
```
from AstroToolkit.Tools import lightcurvequery,plotpowspec,showplot

data=lightcurvequery(survey='ztf',source=6050296829033196032)
plot=plotpowspec(data)
showplot(plot)
```

### 2. tsanalysis

**Allows for period analysis of lightcurve data.**

```
tsanalysis(data)
```

where:

```
data = dict or list in format returned by lightcurvequery
```

<br>

##### Example
To retrieve data for and perform timeseries analysis:
```
from AstroToolkit.Tools import lightcurvequery,tsanalysis

data=lightcurvequery(survey='ztf',source=6050296829033196032)
plot=tsanalysis(data)
```

## Datapage functions

These functions are used to create custom datapages from any plots/data supported by AstroToolkit.

***NOTE:*** An example of datapage creation can be found within the packages 'Examples' folder, named 'datapage_creation.py' (within the …/Lib/site-packages/AstroToolkit from earlier). This can be imported from a python terminal using from AstroToolkit.Examples import datapage_creation.

### 1. gridsetup

**Helps with datapage creation.**

```
getgrid(dimensions,plots,grid_size=250)
```
where:
```
dimensions = list, grid dimensions in format [width,height]. E.g. for a grid that is 6 units wide and 3 units tall, use dimensions = [6,3]
```
```
plots = list of lists, plots with their desired dimensions included. E.g. for a 2x2 plot and two 2x1 plots, use plots = [[plot1,2,2],[plot2,2,1],[plot3,2,1]].
```
```
grid_size  = int, size of each square of the grid to which all plots are scaled.
```

##### returns:
list of plots stripped of their dimensions. E.g. for the plots = ... input above, the following will be returned:

```
[plot1,plot2,plot3]
```

where all plots have been scaled to the desired grid size.

***NOTE:*** Again, see the datapage_creation example as noted above for an example.

### 2. getbuttons

**Returns a Bokeh figure containing SIMBAD and Vizier buttons for use in datapages.**

```
getinfobuttons(grid_size,source=None,pos=None,simbad_radius=3,vizier_radius=3)
```

where:
```
grid_size = int, size of the grid to which the buttons are scaled.
```
```
pos = list, [ra,dec] in degrees
```
```
source = int/float/str, Gaia source_id
```
```
simbad_radius = int, radius to use in SIMBAD queries
```
```
vizier_radius = int, radius to use in Vizier queries
```

##### returns:

bokeh figure object

### 3. getmdtable

**Gets a table of metadata table using data from supported surveys and/or custom data.**

```
getmdtable(metadata,pos=None,source=None)
```

where:

```
metadata = dict, dictionary of metadata in accepted format (see below)
```
```
pos = list, [ra,dec] in degrees
```
```
source = int/float/str, Gaia source_id
```

The expected metadata format is:

```
{
'gaia' : {
         'parameters' : names of parameters that exist in that survey
         'errors' : names of errors for these parameters that exist in that survey
         'notes' : str, any notes to include on this parameter/error/etc.
         }
}

etc. for any supported survey
```

if a key is provided that is not the name of a supported, that key will be interpreted as a custom entry.

In this case, an additional 'values' key must be included, and the 'errors' key becomes the actual value of that error:

```
{
'custom' : {
           'parameters' : names of parameters
           'values' : parameter values
           'errors' : error values
           'notes' : str, any notes to include on this parameter/error/etc.
           }
}
```

## Miscellaneous functions

### 1. correctpm

**Corrects for proper motion of an object between an input time and a target time.**

```
correctpm(inputtime,targettime,ra,dec,pmra,pmdec)
```

where:

```
inputtime = [year,month] where both entries are integers
```
```
targettime = [year,month] where both entries are integers
```
```
ra = float, ra of object in degrees
```
```
dec = float, dec of object in degrees
```
```
pmra = float, proper motion in ra direction of object in mas/yr
```
```
pmdec = float, proper motion in dec direction of object in mas/yr
```

##### returns: 

[ra,dec] of object in degrees, corrected for proper motion.

<br>

##### Example
To correct an object for proper motion to the year 2000:
```
from AstroToolkit.Tools import dataquery,correctpm

data=dataquery(survey='gaia',source=6050296829033196032)['data']
ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]

ra_corrected,dec_corrected=correctpm([2016,0],[2000,0],ra,dec,pmra,pmdec)
```

### 2. getpos

**Gets the position of an object given its Gaia source_id.**

```
getpos(source)
```

where:
```
source = int/float/str, Gaia source_id
```

##### returns:
[ra,dec] of object in degrees

### 3. getsource

**Gets the Gaia source_id of an object given its position.**

```
getsource(pos)
```

where:
```
pos = list, [ra,dec] in degrees
```

##### returns:

gaia source_id


### 4. showplot

**Uses bokeh's show() functionality to show a plot, just here so that you can implement it from ATK along with other tools.**

```
showplot(plot)
```

where:

```
plot = bokeh figure object
```

##### returns:

nothing, saves .html plot to current working directory

## File functions

### 1. savedata

**Saves the data output from any of the query tools to a file.**

```
savedata(data)
```

where:

```
data = data returned by a query tool
```

##### returns:

nothing, saves data file to current working directory

### 2. readdata

**Reads a file created by savedata, reconstructing the original data used to create it.**

```
readdata(filename)
```

where:

```
filenname = str, name of file to read. This file name will include an ATK... identifier which is required.
```

##### returns:

original data used to create the file