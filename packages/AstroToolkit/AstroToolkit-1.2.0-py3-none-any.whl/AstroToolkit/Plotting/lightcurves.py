import matplotlib
import numpy as np
from bokeh.plotting import figure
from bokeh.models import Whisker, ColumnDataSource
from bokeh.transform import linear_cmap

def plot_lightcurve(data_dict,colour):
	if data_dict==None:
		print('Note: Note: Lightcurve entry was None, and so was ignored.')
		return None

	if isinstance(data_dict,list):
		raise Exception('Multiple light curves passed to plotlightcurve. Only one can be plotted at a time.')

	hjd=data_dict['data']['hjd']
	mag=data_dict['data']['mag']
	mag_err=data_dict['data']['mag_err']
	
	survey=data_dict['survey']
	band=data_dict['band']

	# set up colour maps
	if colour=='green':
		colourmap=matplotlib.colors.LinearSegmentedColormap.from_list('',['greenyellow','forestgreen','greenyellow'])
		palette=[matplotlib.colors.rgb2hex(c) for c in colourmap(np.linspace(0,1,255))]
		error_colour='forestgreen'
	elif colour=='red':
		colourmap=matplotlib.colors.LinearSegmentedColormap.from_list('',['yellow','red','yellow'])
		palette=[matplotlib.colors.rgb2hex(c) for c in colourmap(np.linspace(0,1,255))]
		error_colour='red'
	elif colour=='blue':
		colourmap=matplotlib.colors.LinearSegmentedColormap.from_list('',['aqua','royalblue','aqua'])
		palette=[matplotlib.colors.rgb2hex(c) for c in colourmap(np.linspace(0,1,255))]
		error_colour='royalblue'
	elif colour=='black':
		colourmap=matplotlib.colors.LinearSegmentedColormap.from_list('',['lightgray','black','lightgray'])
		palette=[matplotlib.colors.rgb2hex(c) for c in colourmap(np.linspace(0,1,255))]
		error_colour='black'
	elif colour=='orange':
		colourmap=matplotlib.colors.LinearSegmentedColormap.from_list('',['gold','orange','gold'])
		palette=[matplotlib.colors.rgb2hex(c) for c in colourmap(np.linspace(0,1,255))]
		error_colour='orange'
	elif colour=='purple':
		colourmap=matplotlib.colors.LinearSegmentedColormap.from_list('',['orchid','darkviolet','orchid'])
		palette=[matplotlib.colors.rgb2hex(c) for c in colourmap(np.linspace(0,1,255))]
		error_colour='darkviolet'
		
	plot=figure(width=400,height=400,title=f'{survey} {band} lightcurve',x_axis_label=r'\[\text{Observation Date [days]}\]',y_axis_label=fr'\[\text{{band}}\]')
	
	plot.y_range.flipped=True

	# set up data source
	upper=[x+e for x,e in zip(mag,mag_err)]
	lower=[x-e for x,e in zip(mag,mag_err)]
	source=ColumnDataSource(data=dict(hjd=hjd,mag=mag,upper=upper,lower=lower))

	g_mapper=linear_cmap(field_name='mag',palette=palette,low=min(mag),high=max(mag))

	# plot points
	plot.circle(x='hjd',y='mag',source=source,color=g_mapper)
	# plot errors
	errors=Whisker(source=source,base='hjd',upper='upper',lower='lower',line_width=0.5,line_color=error_colour)
	errors.upper_head.line_width,errors.lower_head.line_width=0.5,0.5
	errors.upper_head.size,errors.lower_head.size=3,3
	errors.upper_head.line_color,errors.lower_head.line_color=error_colour,error_colour		

	plot.add_layout(errors)
	
	return plot