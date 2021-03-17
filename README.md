This project was funded by NSF Award # 1623141
Please contact co-PI Jenny Amos (jamos@illinois.edu or git: jennyamos) for questions

# Gradescope_Tags_Visualizations
This repo has code to scrape Gradescope exported data to create various tag organized visualizations of assessment data

## plot.py
This python script scrapes Gradescope exported data into tag organized studentwise radar plots visualizing student perfromance vs class perfromance

## Usage
Install necessary Python packages: bokeh, numpy, pandasBokeh installation: https://docs.bokeh.org/en/latest/docs/first_steps/installation.html
(Install numpy and pandas similarly)
 
All the csv files exported from gradescope to be scraped should be placed in a folder named 'Data'. Store this 'Data' folder in the same place as the plot.py script. To store data differently or to use files with different extension, 'path' and 'extension' variables can be changed in the script respectively.

Running this script: [python/python3/py] plot.py shall create plot for every student with their email as the filename.

Canvas or mail mege can be used to share these files with students 

## Contributing & License
Please reference the work from this grant in any use.

This code is licensed under GNU General Public License v3.0 (GNU GPLv3).
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

Please push any modifications of the code back to this repository.
