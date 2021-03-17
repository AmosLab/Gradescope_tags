# Gradescope_scrape
This repo has code to scrape Gradescope exported data to create various tag organized visualizations of assessment data

# plot.py
This python script scrapes Gradescope exported data into tag organized studentwise radar plots visualizing student perfromance vs class perfromance

# Usage
Install necessary Python packages: bokeh, numpy, pandas
 Bokeh installation: https://docs.bokeh.org/en/latest/docs/first_steps/installation.html
 (Install numpy and pandas similarly)
 
All the csv files exported from gradescope to be scraped should be placed in a folder named 'Data'. Store this 'Data' folder in the same place as the plot.py script. To store data differently or to use files with different extension, 'path' and 'extension' variables can be changed in the script respectively.

Running this script: [python/python3/py] plot.py shall create plots for every student with their email as the filename and the identifier.

Canvas or mail mege can be used to share these with students 

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
