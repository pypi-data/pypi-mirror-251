import requests
from requests.adapters import HTTPAdapter, Retry
from io import BytesIO
import pandas as pd

from ..Data.data import get_survey_times

survey_times=get_survey_times()

def get_data(survey,ra,dec,radius=3,bands='gri',source=None,pos=None):
	f_return=None

	# convert radius into degrees
	radius=radius/3600
	
	if survey=='ztf':
		service='https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves'
		url=f'{service}?POS=CIRCLE {ra} {dec} {radius}&BANDNAME=g,r,i&FORMAT=CSV'
	
	# performs query, have to set up some extra querying parameters as ZTF often has issues.
	s=requests.Session()
	retries=Retry(total=5,backoff_factor=1,status_forcelist=[500,502,503,504])
	s.mount('http://',HTTPAdapter(max_retries=retries))
	
	# high timeout value is used here as ZTF data can take a long time to apply to large images in an overlay (as so much data is returned)
	try:
		r=s.get(url,timeout=180)
	except:
		print(f'Note: Experiencing issues with {survey}.')
		return f_return
	
	if r.status_code!=200:
		print(f'Note: Experiencing issues with {survey}.')
		return f_return

	# convert to pandas array (containing all bands)
	data=pd.read_csv(BytesIO(r.content))
	if len(data)==0:
		print(f'Note: {survey} lightcurvequery returned no data.')
		return f_return
	
	if survey=='ztf':
		# split into separate bands
		gData=data.loc[data['filtercode']=='zg']
		rData=data.loc[data['filtercode']=='zr']
		iData=data.loc[data['filtercode']=='zi']
	
		gData,rData,iData=gData.reset_index(drop=True),rData.reset_index(drop=True),iData.reset_index(drop=True)
	
		data_arr=[{'g':gData},{'r':rData},{'i':iData}]
	
		# set empty data sets to None in dict (e.g. [dict,dict,None]) if no i data is available. note that the above data_arr is a list of dicts, not a single dictionary
		for i in range(0,len(data_arr)):
			for key in data_arr[i]:
				if data_arr[i][key].empty:
					data_arr[i]=None
	
	# sets up list of lightcurve data dictionaries, with None for missing bands, so resulting list always has len() = 3
	data_dict_arr=[]
	for band in data_arr:
		if band!=None:
			for key in band:
				data=band[key]
				current_band=key

				mag=data.loc[:,'mag'].tolist()
				hjd=data.loc[:,'hjd'].tolist()
				ra=data.loc[:,'ra'].tolist()
				dec=data.loc[:,'dec'].tolist()
				hjd_min=min(hjd)
				hjd_ori=hjd		
				hjd=[x-hjd_min for x in hjd]
				mag_err=data.loc[:,'magerr'].tolist()

				data_dict={'type':'lightcurve','source':source,'pos':pos,'survey':survey,'band':current_band,'data':{'ra':ra,'dec':dec,'hjd':hjd,'hjd_ori':hjd_ori,'mag':mag,'mag_err':mag_err}}
				data_dict_arr.append(data_dict)
		else:
			data_dict_arr.append(None)

	return data_dict_arr

'''
corrects for proper motion to the survey time (if source input is used)
'''
def lightcurve_handling(survey,pos=None,source=None,radius=3):
	from ..Tools import dataquery
	from ..Misc.ProperMotionCorrection import PMCorrection

	# different surveys can have a different number of bands, so need to return an empty list with that survey's band count (i.e. here, ztf is [None,None,None] for g,r,i)
	if survey=='ztf':
		f_return=[None,None,None]

	if pos!=None:
		ra,dec=pos[0],pos[1]
	elif source!=None:
		gaia_data=dataquery(survey='gaia',source=source)['data']
		if gaia_data!=None:
			ra,dec,pmra,pmdec=gaia_data['ra'][0],gaia_data['dec'][0],gaia_data['pmra'][0],gaia_data['pmdec'][0]
		else:
			return f_return
			
		# correct for proper motion
		pos_corrected=PMCorrection(input=survey_times['gaia'],target=survey_times[survey],ra=ra,dec=dec,pmra=pmra,pmdec=pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	data=get_data(survey=survey,ra=ra,dec=dec,radius=radius,pos=pos,source=source)
	
	return data