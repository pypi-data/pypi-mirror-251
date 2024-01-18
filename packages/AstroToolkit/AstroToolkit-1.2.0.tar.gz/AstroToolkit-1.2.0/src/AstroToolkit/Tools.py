from math import e
from bokeh.plotting import output_file
import re

from .Misc.file_naming import name_file
from .Misc.input_validation import validateinput

'''
Combine all similar queries into one tool
take tools page back to just being a map. handle pm correction within the sub-tools and tools page should only handle inputs and return data

write new test file
'''

'''
changelog:
- rewrote all functions into new toolkit structure, where data gathering tools are separated from plotting tools - far easier to develop, and can now use 3rd party data as long
  as it is formatted according the ATK supported data formats
- combined any split functions (i.e. tools that previous had a survey in their name such as getpanstarrsimage, gaiaquery, getsdssspectrum) into single tools which use a 'survey' parameter 
- implemented all supported surveys as overlay options for images
- can now save files into a ATK file format (including images!), all functionality is retained if the file is read using the (also new) readdata tool.
- made code optimizations throughout, so should be easier to develop
- improved file structure of package
- added comments throughout new code to aid development
- wrote new README to match these changes, and included examples
'''

'''
to-do:
- UPLOAD

- convert all lists to np arrays so that reading them is easier
'''

# Data Query --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def dataquery(survey,pos=None,source=None,radius=3):
	from .Data.data import survey_map
	
	validateinput({'survey':survey,'pos':pos,'source':source,'radius':radius},'dataquery')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in dataquery.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in dataquery.')

	data=survey_map(survey=survey,pos=pos,source=source,radius=radius)
	
	return data

# Phot Queries ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def photquery(survey,pos=None,source=None,radius=3):
	from .Data.photometry import phot_query
	
	validateinput({'survey':survey,'pos':pos,'source':source,'radius':radius},'photquery')
	
	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in photquery.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in photquery.')

	photometry=phot_query(survey=survey,pos=pos,source=source,radius=radius)
	
	return photometry

def bulkphotquery(pos=None,source=None,radius=3):
	from .Data.photometry import bulk_query
	
	validateinput({'pos':pos,'source':source,'radius':radius},'bulkphot')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in bulkphotquery.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in bulkphotquery.')

	data=bulk_query(pos=pos,source=source,radius=radius)
	
	return data

# Imaging -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def imagequery(survey,pos=None,source=None,size=30,band='g',overlays=None):
	from .Data.imaging import image_correction

	f_return=None
		
	validateinput({'survey':survey,'pos':pos,'source':source},'imagequery')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in imagequery.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in imagequery.')

	if overlays=='all':
		overlays='gaia,galex_nuv,galex_fuv,rosat,sdss,twomass,wise,ztf'

	if overlays!=None:
		overlay_list=overlays.split(',')

		for i in range(0,len(overlay_list)):
			overlay_list[i]=overlay_list[i].lower()
		for i in range(0,len(overlay_list)):
			if overlay_list[i] not in ['gaia','galex_nuv','galex_fuv','rosat','ztf','wise','twomass','sdss']:
				raise Exception('invalid overlay')
	else:
		overlay_list=[]
		
	if survey=='panstarrs':
		if size>1500:
			raise Exception(f'Maximum supported size in {survey} is 1500 arcsec.')
		if not re.match('^[grizy]+$', band):
			raise Exception(f'Invalid {survey} bands. Supported bands are [g,r,i,z,y].')
	
	elif survey=='skymapper':
		if size>600:
			raise Exception(f'Maximum supported size in {survey} is 600 arcsec.')
		if re.match('^[grizuv]+$', band):
			pass
		else:
			raise Exception(f'Invalid {survey} bands. Supported bands are [g,r,i,z,u,v].')
	
		band=list(band)
		temp_string=''
		for i in range(0,len(band)):
			temp_string+=(band[i]+',')
		band=temp_string[:-1]
		
	elif survey=='dss':
		if band!='g':
			print('Note: DSS only supports g band imaging, input band has been ignored.')
		if size>7200:
			print(f'Maximum supported size in {survey} is 7200 arcsec.')

	
	if survey=='any':
		image=image_correction(survey='panstarrs',pos=pos,source=source,size=size,band=band,overlay=overlay_list)
		if image==None:
			image=image_correction(survey='skymapper',pos=pos,source=source,size=size,band=band,overlay=overlay_list)
			if image==None:
				image=image_correction(survey='dss',pos=pos,source=source,size=size,band=band,overlay=overlay_list)
				if image==None:
					print('Note: No image found in any supported imaging survey.')
					return f_return
	else:
		image=image_correction(survey=survey,pos=pos,source=source,size=size,band=band,overlay=overlay_list)
	
	return image

def plotimage(data):
	from .Plotting.imaging import plot_image
	
	plot=plot_image(image_dict=data)

	filename=name_file(data=data,data_type='ATKimage')
	output_file(filename)

	return plot

# HRD Plotting ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def plothrd(source=None,sources=None):
	from bokeh.models import CustomJS
	from bokeh import events
	from bokeh.plotting import output_file

	from .Plotting.HRD import get_plot
	
	validateinput({'source':source},'plothrd')

	if source!=None and sources!=None:
		raise Exception('Simultaneous source and sources input detected in plothrd.')


	if source!=None:
		plot=get_plot(source=source)
	elif sources!=None:
		for element in sources:
			if not isinstance(element,int):
				data_type=type(element)
				raise Exception(f'Incorrect source data type in sources. Expected int, got {data_type}.')
		plot=get_plot(sources=sources)
	else:
		raise Exception('source or sources input required in plothrd.')

	filename=name_file(data={'source':source,'sources':sources},data_type='ATKhrd')
	output_file(filename)

	return plot

# Light Curves ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lightcurvequery(survey,pos=None,source=None,radius=3):
	from .Data.lightcurves import lightcurve_handling
	
	validateinput({'survey':survey,'pos':pos,'source':source,'radius':radius},'lightcurvequery')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in lightcurvequery')
	elif source==None and pos==None:
		raise Exception('pos or source input required in lightcurvequery.')

	data=lightcurve_handling(survey=survey,pos=pos,source=source,radius=radius)
	
	return data

def plotlightcurve(data,colour='black'):
	from .Plotting.lightcurves import plot_lightcurve
	
	if colour not in ['green','red','blue','purple','orange','black']:
		raise Exception('Unsupported colour in plotlightcurve.')

	plot=plot_lightcurve(data_dict=data,colour=colour)
		
	filename=name_file(data=data,data_type='ATKlightcurve')
	output_file(filename)

	return plot

# SEDs --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sedquery(pos=None,source=None,radius=3):
	from .Data.sed import get_data
	
	data=get_data(pos=pos,source=source,radius=radius)
	
	validateinput({'source':source,'pos':pos},'sedquery')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in dataquery.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in dataquery.')

	return data

def plotsed(data):
	from .Plotting.sed import plot_sed
	
	plot=plot_sed(sed_data=data)
	
	filename=name_file(data=data,data_type='ATKsed')
	output_file(filename)

	return plot

# Spectra -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def spectrumquery(survey=None,pos=None,source=None,radius=3):
	from .Data.spectra import survey_map
	
	validateinput({'survey':survey,'pos':pos,'source':source,'radius':radius},'spectrumquery')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in spectrumquery.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in spectrumquery.')

	data=survey_map(survey=survey,pos=pos,source=source,radius=radius)
	
	return data

def plotspectrum(data):
	from .Plotting.spectra import get_plot
	
	plot=get_plot(spectrum_dict=data)
	
	filename=name_file(data=data,data_type='ATKspectrum')
	output_file(filename)

	return plot

# Timeseries --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def plotpowspec(data):
	from .Plotting.powspec import get_plot
	
	plot=get_plot(dataset=data)
	
	filename=name_file(data=data,data_type='ATKpowspec')
	output_file(filename)
	
	return plot

def tsanalysis(data):
	from .Timeseries.ztfanalysis import get_analysis
	
	get_analysis(dataset=data)

# Data Pages --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def gridsetup(dimensions,plots,grid_size=250):
	from .Datapages.grid import get_grid
	
	plots=get_grid(dimensions=dimensions,plots=plots,grid_size=grid_size)
	
	return plots

def getbuttons(grid_size,source=None,pos=None,simbad_radius=3,vizier_radius=3):
	from .Datapages.buttons import getinfobuttons	

	validateinput({'source':source,'pos':pos},'databuttons')

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in getbuttons.')
	elif source==None and pos==None:
		raise Exception('pos or source input detected in getbuttons.')

	if not (isinstance(simbad_radius,int) or isinstance(simbad_radius,float)):
		data_type=type(simbad_radius)
		raise Exception(f'Incorrect simbad_radius data type. Expected float/int, got {data_type}.')
	if not (isinstance(vizier_radius,int) or isinstance(vizier_radius,float)):
		data_type=type(vizier_radius)
		raise Exception(f'Incorrect vizier_radius data type. Expected float/int, got {data_type}.')
	if not (isinstance(grid_size,int) or isinstance(grid_size,float)):
		data_type=type(grid_size)
		raise Exception(f'Incorrect grid_size data type. Expected float/int, got {data_type}.')

	plot=getinfobuttons(grid_size=grid_size,source=source,pos=pos,simbad_radius=simbad_radius,vizier_radius=vizier_radius)
	
	return plot

def getmdtable(metadata,pos=None,source=None):
	from .Datapages.metadata import gettable

	if source!=None and pos!=None:
		raise Exception('Simultaneous pos and source input detected in getmdtable.')
	elif source==None and pos==None:
		raise Exception('pos or source input required in getmdtable.')
	
	plot=gettable(metadata_dict=metadata,pos=pos,source=source)

	
	return plot

# Miscellaneous -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def correctpm(inputtime,targettime,ra,dec,pmra,pmdec):
	from .Misc.ProperMotionCorrection import PMCorrection
	
	pos=PMCorrection(input=inputtime,target=targettime,ra=ra,dec=dec,pmra=pmra,pmdec=pmdec)

	return pos

def getpos(source):
	validateinput({'source':source},'getpos')
	data=dataquery(survey='gaia',source=source)

	ra,dec=data['ra'].values[0],data['dec'].values[0]
	
	return [ra,dec]

def getsource(pos):
	import pandas as pd
		
	validateinput({'pos':pos},'getsource')

	data=dataquery(survey='gaia',pos=pos)
	
	if not isinstance(data,pd.DataFrame):
		return None

	source=data['source_id']

	if len(data)>1:
		print('[Gaia: GaiaGetsource] Note: '+len(data), 'objects detected within search radius.')
		source=source.to_list()
	
	return source

def savedata(data):
	from .Misc.file_handling import create_file
	
	create_file(data_copy=data)
	
def readdata(filename):
	from .Misc.file_handling import read_file
	
	if not isinstance(filename,str):
		data_type=type(filename)
		raise Exception(f'Incorrect filename datatype. Expected str, got {data_type}.')

	data=read_file(file_name=filename)
	
	return data

def showplot(plot):
	from bokeh.plotting import show
	
	show(plot)