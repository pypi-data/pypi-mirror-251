from bokeh.plotting import figure,output_file

def get_grid(dimensions,plots,grid_size=250):
	for i in range(0,len(plots)):
			# Creates None objects to fill blank space since there cannot be anything that is empty.
			if plots[i][0]==None:
				plots[i][0]=figure(width=plots[i][1]*grid_size,height=plots[i][2]*grid_size)
			else:
				plots[i][0].width,plots[i][0].height=plots[i][1]*grid_size,plots[i][2]*grid_size
	
	# Checks the area occupied by the input plots (i.e. just normalized by /grid_size)
	unit_area=0
	for i in range(0,len(plots)):
		unit_area+=(plots[i][1]*plots[i][2])

	# Checks if the unit area calculated above matches the target unit area as given by the dimensions (i.e. all space must be filled)
	if unit_area!=dimensions[0]*dimensions[1]:
		raise Exception('Entire dimensions must be filled with figures. Pass None to fill empty space.')

	output_file('datapage.html')

	# Strips the plots of their dimensions etc.
	for i in range(0,len(plots)):
		plots[i]=plots[i][0]

	return plots