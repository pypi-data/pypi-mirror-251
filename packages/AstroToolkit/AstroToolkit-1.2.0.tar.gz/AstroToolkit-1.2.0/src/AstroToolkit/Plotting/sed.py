from bokeh.plotting import figure
from bokeh.models import Whisker, ColumnDataSource
from bokeh.models import CustomJS
from bokeh import events

def plot_sed(sed_data):
    sed_data=sed_data['data']

    # list colours
    colour_arr=['springgreen','royalblue','gold','aquamarine','deepskyblue','orangered','orange','red','black','grey']
    
    plot=figure(width=400,height=400,title='SED',x_axis_label=r'\[\lambda_{\text{eff}}\text{ }[\text{AA}]\]',y_axis_label=r'\[\text{flux [mJy]}\]',x_axis_type='log',y_axis_type="log")
    
    # get list of surveys with data points
    survey_list=[]
    for entry in sed_data:
        survey=entry['survey']
        if not survey in survey_list:
            survey_list.append(survey)

    # set up array of data points from sed_data
    legend=False
    for survey in survey_list:
        x_arr=[]
        y_arr=[]
        err_arr=[]        
        for i in range(0,len(sed_data)):
            if sed_data[i]['survey']==survey:
                x_arr.append(sed_data[i]['wavelength'])
                y_arr.append(sed_data[i]['flux'])
                err_arr.append(sed_data[i]['rel_err'])

        # set up errors
        upper=[x+e for x,e in zip(y_arr,err_arr)]
        lower=[x-e for x,e in zip(y_arr,err_arr)]
        
        source=ColumnDataSource(data=dict(wavelength=x_arr,flux=y_arr,upper=upper,lower=lower))

        current_survey_index=survey_list.index(survey)

        # plot data
        plot.circle(x='wavelength',y='flux',source=source,color=colour_arr[current_survey_index],legend_label=f'{survey}')
            
        # plot errors
        error=Whisker(source=source,base='wavelength',upper='upper',lower='lower',line_width=0.5,line_color=colour_arr[current_survey_index])
        error.upper_head.line_width,error.lower_head.line_width=0.5,0.5
        error.upper_head.size,error.lower_head.size=3,3
        error.upper_head.line_color,error.lower_head.line_color=colour_arr[current_survey_index],colour_arr[current_survey_index]
        plot.add_layout(error)
        
        legend=True

    if legend==True:
        plot.legend.click_policy="hide"	

		# Double click to hide legend
        toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
				if (leg.visible) {
					leg.visible = false
					}
				else {
					leg.visible = true
				}
		''')
	
        plot.js_on_event(events.DoubleTap, toggle_legend_js)  

    return plot