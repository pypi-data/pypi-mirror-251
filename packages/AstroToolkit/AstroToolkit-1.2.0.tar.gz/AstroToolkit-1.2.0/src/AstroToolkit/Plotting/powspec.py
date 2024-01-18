from astropy.time import Time
from astropy.timeseries import TimeSeries
from astropy.units import cds
from astropy import units as u
import pandas as pd
from bokeh.plotting import figure

from ..Timeseries import pyaov

'''
plots a powspec given lightcurve data (or a list of lighcurve data)
'''
def get_plot(dataset):    
    # if a list of lightcurve data is given, combines them

    if isinstance(dataset,list):
        dataframes=[]
        for band in dataset:
            # collapse dictionary
            if band!=None:
                for key in band['data']:
                    band[key]=band['data'][key]
                del band['data']
                df=pd.DataFrame.from_dict(band)
                dataframes.append(df)
            
        data=pd.concat(dataframes)
    else:
        # collapse dictionary
        for key in dataset['data']:
            dataset[key]=dataset['data'][key]
        del dataset['data']
        data=pd.DataFrame.from_dict(dataset)
           
    survey=data['survey'].values[0]

    data.sort_values('hjd_ori',inplace=True)

    xd=data['hjd_ori']-2400000.5
    yd=data['mag']
    ed=data['mag_err']
    
    # creates power spectrum using pyaov
    filters = list(set(data['band']))
    first_filter = filters[0]
    med_first_filter = data.query('band==@first_filter')['mag'].median()
    
    for filt in filters:
        med_filtered = data.query('band==@filt')['mag'].median()
        data.loc[data['band'] == filt,'mag'] += (med_first_filter-med_filtered)
    yd=data['mag']
    
    start_freq=0
    final_freq=50
    step_size=(final_freq-start_freq)/250000

    th,freqs,_=pyaov.amhw(xd,yd,ed,final_freq,step_size)
    
    plot=figure(width=400,height=400,title=f'{survey} Power Spectrum',x_axis_label=r'\[\text{Frequency [days}^{-1}]\]',y_axis_label=r'\[\text{Power}\]')
    plot.line(x=freqs,y=th,color='black',line_width=0.5)

    return plot