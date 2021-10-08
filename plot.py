
#Amos Research Lab. Oct 8th, 2021


import bokeh
import pandas as pd
import math
import numpy as np
import glob
import csv
from six.moves import cStringIO as StringIO
from bokeh import plotting
from bokeh.plotting import figure, show, save, output_file, ColumnDataSource, reset_output
from bokeh.models import Legend, HoverTool
from bokeh.io import export_png, curdoc
import os


"""
Reads CSVs into dictionaries 
"""

extension = 'csv'
path = r'Data'
all_filenames = [i for i in glob.glob(path + "/*." + format(extension))]

students={}
student_tags={}
tag_average={}

#len(all_filenames)
count = 0
for i in range(len(all_filenames)):

    if (os.path.split(all_filenames[i])[1] != "Tag Categories.csv"):
        with open(all_filenames[i]) as csvfile:
            df=pd.read_csv(csvfile)

            max_score=4.0
            for index, row in df.iterrows():
                s = row['Student name'] + '(' + str(row['Student ID']) + ')'

                students[s]= {'Abstraction': (float(row['Abstraction result']), max_score),
                              'Code Fluency': (float(row['Code Fluency result']), max_score),
                              'Correctness': (float(row['Correctness result']), max_score),
                              'Documentation': (float(row['Documentation result']), max_score),
                              'Reflection': (float(row['Reflection result']), max_score),
                              'Resourcefulness': (float(row['Resourcefulness result']), max_score),
                              'Style': (float(row['Style result']), max_score)}


            '''if not pd.isna(row['Tags']):
                    
                    count += 1
                    tags = row['Tags'].split('; ')

                    for tag in tags:
                        score = float(row['Score'])
                        
                        if s in students:
                            student_tags = students.get(s)
                            
                            if tag in student_tags:
                                Utag=student_tags[tag]
                                
                                Utag=((Utag[0]+score), (float(Utag[1])+max_score))
                                student_tags[tag]=Utag
                                
                            else:
                                student_tags[tag]=(score, max_score)

                            students[row['Email']] = student_tags
                        else:
                            students[s] = {tag: (score, max_score)}'''
            
"""
Calculates Tag averages
"""
                    
for student, tag_lib in students.items():
    for tag, score in tag_lib.items():
        tag_score = score[0]
        max_tag_score = score[1]
        if not pd.isna(tag_score):
          if tag in tag_average:
            tag_data = tag_average[tag]
            tag_data = (tag_data[0] + tag_score, tag_data[1] + max_tag_score)
            tag_average[tag] = tag_data
          else:
            tag_average[tag] = (tag_score, max_tag_score)

# set width and height of image
width = 800
height = 800
inner_radius = 80
outer_radius = 310


# radius of each data point
def rad(original_radius):
    return inner_radius + (outer_radius - inner_radius) * original_radius

"""
Set up plot background
"""
slice_angle = 2.0 * np.pi / (len(tag_average))  # angle of each slice of the chart in radians
angles = np.arange(0.0, 2 * math.pi, slice_angle)  # angle of each axes radiating outwards
angle_array = np.array(angles + slice_angle / 2)  # array to hold angles for category labels radiating outwards
labels = ["", 0.2, 0.4, 0.6, 0.8, 1.0]  # axis labels
axis_distance = (outer_radius - inner_radius) / (len(labels) - 1)  # distance between circular axes
radii = np.arange(inner_radius, outer_radius + 10, axis_distance)

# category labels
label_radius = outer_radius + 10
x_pos = label_radius * np.cos(angle_array)
y_pos = label_radius * np.sin(angle_array)
label_angle = np.array(angles + slice_angle / 2)
label_angle[np.logical_and(label_angle > np.pi / 2, label_angle < 3 * np.pi / 2)] += np.pi
number_labels = len(tag_average.keys())
tag_list = list(tag_average.keys())


def plot(student):

    # plot of score for each competency
    p = figure(plot_width=width, plot_height=height,
               x_axis_type=None, y_axis_type=None,
               min_border=0, outline_line_color="black", match_aspect=True, background_fill_color="white",
               tooltips='hover')

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # circular axes
    p.arc(0, 0, radius=radii, start_angle=0, end_angle=math.pi * 2, color="black")

    # axes scale
    p.text(radii, 0, [str(r) for r in labels], y_offset=7, x_offset=-5,
           text_font_size="8pt", text_align="right", text_baseline="middle")

    # grey radial axes
    p.annular_wedge(0, 0, inner_radius, outer_radius,
                    -slice_angle + angles, -slice_angle + angles, color="grey")

    """
    Plot data
    """

    x_point = []
    y_point = []
    average_score = []
    count = 0
    for tag, scores in tag_average.items():
        #print(scores)
        #scores=list(scores)
        #scores[1]=float(scores[1])
        #print(scores)
        average_score.append(scores[0] / scores[1])
        x_point.append(rad(scores[0] / scores[1]) * np.cos(angle_array[count]))
        y_point.append(rad(scores[0] / scores[1]) * np.sin(angle_array[count]))
        label_source = ColumnDataSource(data={
            'label': [tag]
        })
        if angle_array[count] > math.pi / 2 and angle_array[count] < 3*math.pi/2:
            p.text(x_pos[count], y_pos[count], 'label',
                   source=label_source, angle=label_angle[count],
                   text_font_size="9pt", text_align='right', text_baseline="middle")
        else:
            p.text(x_pos[count], y_pos[count], 'label',
                   source=label_source, angle=label_angle[count],
                   text_font_size="9pt", text_align='left', text_baseline="middle")

        count += 1

    source = ColumnDataSource(data={
        'x_point': x_point,
        'y_point': y_point,
        'score': average_score,
        'description': tag_list
    })
    p.line(x_point, y_point, line_width=2.5, color="black")
    p.line(x_point, y_point, line_width=1.75, color="purple")
    p.line([x_point[0], x_point[-1:]], [y_point[0], y_point[-1:]], line_width=2.5, color="black")
    p.line([x_point[0], x_point[-1:]], [y_point[0], y_point[-1:]], line_width=1.75, color="purple")
    p.circle('x_point', 'y_point', source=source, radius=2.5, color="black", name='point_shadow')
    p.circle('x_point', 'y_point', source=source, radius=1.75, color="purple", name='point_point')
    p.patch(x_point, y_point, alpha=0.25, color="grey")

    """
    Plot score
    """
    x_point = []
    y_point = []
    average_score = []
    count = 0
    colors = []

    sdict = dict(students[student].items())
        
    for tag, score in tag_average.items():
        if tag in sdict:
            score = sdict[tag]
            if pd.isna(score):
              score = (0,score[1])
              colors.append("red")
            else:
              colors.append("pink")
        else:
            score = (0,score[1])
            colors.append("red")

        #score=list(score)
        #score[1]=float(score[1]
        #print(score)
        average_score.append(score[0] / score[1])
        x_point.append(rad(score[0] / score[1]) * np.cos(angle_array[count]))
        y_point.append(rad(score[0] / score[1]) * np.sin(angle_array[count]))
        count += 1

    source = ColumnDataSource(data={
        'x_point': x_point,
        'y_point': y_point,
        'score': average_score,
        'description': tag_list,
        'colors': colors
    })
    p.line(x_point, y_point, line_width=2.5, color="black")
    p.line(x_point, y_point, line_width=1.75, color="pink")
    p.line([x_point[0], x_point[-1:]], [y_point[0], y_point[-1:]], line_width=2.5, color="black")
    p.line([x_point[0], x_point[-1:]], [y_point[0], y_point[-1:]], line_width=1.75, color="pink")
    p.circle('x_point', 'y_point', source=source, radius=2.5, color='black', name='point_shadow')
    p.circle('x_point', 'y_point', source=source, radius=1.75, color='colors', name='point_point')

    # legends for category colors
    p.circle([-30, -30], [10, -10], radius=6.5, color=['purple', 'pink'])
    p.text([-20, -20], [10, -10], text=['Average Score', 'Your Score'],
           text_font_size="9pt", text_align="left", text_baseline="middle")

    # tooltip to display info on each point plotted
    hover = p.select(HoverTool)
    hover.names = ['point_point', 'point_shadow']
    hover.tooltips = [('Score', '@score'),
                      ('Description', '@description')]
    hover.mode = "mouse"

    output_file("%s.html" % student)
    save(p)

for student in students.items():
     bokeh.plotting.reset_output()
     curdoc().clear()
     plot(student[0])
