# Graphing with Flask and Plotly

## To Begin
Run "python get_data.py"

This will set up the SQL tables needed.

## Plotly Charts
I initially created plotly charts through their website by importing CSVs of tables.  I then used their GUI to adjust the specifications of each graph.

I improved on this in the final version by using plotly's offline mode to have dynamic graphs and tables, making this project much easier to scale.  These were pulled from the mysql raw dataframe instead of CSVs.  I then ran the calculations after the raw data was pulled.

![Imgur](https://i.imgur.com/oCjgX4Sl.png "Sample Graphs")

## Building the website

I used Flask as my front end to crate some routes for each graph.  I brought in Bootstrap to style my css including the dropdown navbar.  I created a "parent" layout an then extended it into each page.



## Overview
Switching to dynamic graphs greatly improved the ability to change future contract routes and made my code DRY.  I had a great time with learning new skills throughout this challenge (Some that didn't make it into the final app as well!)  
