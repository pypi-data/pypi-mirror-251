import pandas as pd
from bokeh.plotting import figure

def get_plot(spectrum_dict):
	x=spectrum_dict['data']['wavelength']
	y=spectrum_dict['data']['flux']

	plot=figure(width=400,height=400,title="SDSS Spectrum",x_axis_label=r'\[\lambda\text{ }[\text{AA}]\]',y_axis_label=r"\[\text{flux [erg}\text{ cm }^{-2}\text{ s }^{-1}\text{AA}^{-1}]\]")
	plot.line(x,y,color='black',line_width=1)

	return plot