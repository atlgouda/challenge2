# Graphing with Flask and Dash

## Timeline
Started by creating SQL tables for price with: <br>

    def create_tables(contract_root):
    df = get_contract_family(contract_root,
        field='px_last').fillna(method='ffill')
        pretty_plot(df, title=contract_root, ylabel='px_last')
        df.to_sql(contract_root, localhost, if_exists='replace', chunksize=250)

## Plotly Charts
Created plotly charts through their website by importing CSVs of tables.  Created CSVs of price and returns tables by exporting from MySQL workbench.

The remaining tables I converted to CSV directly in python due to the formulas not returning column titles.  I then added the column titles onto the first line of the CSV and then imported into my Plotly account.

This was my first attempt, and the code is currently still in this project.  I have learned some better ways to handle this such as:
<ul>
<li>Change the column titles of the SQL file in MySQL Workbench, then exporting</li>
<li>Use Dash to create the graphs in an offline environment</li>
</ul>

I would like to learn the method for changing the column titles before exporting it to SQL so that no outside changes or CSV files are needed.  Though at the time, my priority was getting the graphs created.

I then created a "dashboard" for each contract root bringing in all of the charts so that everything could be viewed on on page. This had the benefit of being a good spot to view a lot of information in one spot, but had the disadvantage of not being able to compare different contract roots on one axis.  I addressed this later through using Dash.

## Building the website

After creating some graphs, I used Flask as my front end to crate some routes for each graph.  I brought in Bootstrap to style my css including the dropdown navbar.  I created a "parent" layout an then extended it into each page.

At this point I wanted to deploy my progress to Heroku.  I was running into an error with some of the lines in my Pipfile so I had to clear out "mysql-client" due to compatibility issues.

## Dash

After loaing the graphs I embedded from Plotly, I started to teach myself how to use Dash.  For my first attempt, I created a graph by manually entering the values for Annualized Vol into a dcc.Graph.  I knew this wasn't the method I would end up using, but thought it would be good practice.

I was able to put 4 data points into each contract route, and graph them on the same axis.

I then created a datavis.py module (still here in the project for reference) and created two graphs with Dash comparing prices of GC and ES, and was able to pull from SQL the whole time instead of relying on a CSV.

I created a new module (pricedash.py) and made some large SQL tables by through MySQL workbench by joining the tables together and loading those files into my project.

The problem with this method was that is that it will work locally, but not when I deploy to Heroku due to the info being on a SQL database.  I attempted to troubleshoot this by using JawsDB which was the suggested Heroku add on for python/sql, but ran into some compatibility issues.


## Moving forward

There are some items I would like to address goin forward with my site:

<ol>
<li>  Most importantly, My dash module is not able to be brought into Flask.  I can currently view Flask on one port, and Dash on a different one.  Once I get this fixed, I can move forward with polishing the site</li>
<li>Find a way to use sql databases instead of CSVs.  I am not sure which way is the accepted method, but using JawsDB did not work.  This will not affect how the site looks, but would help with scaling out future additions</li>
<li> Styling:  I used limited styling with creating my navbar, but would like to be able to devote some more time to the design of the site.  In its current state, the main focus is on functionality instead of user experience</li>
<li>Cut out the first attempts.  I left in the embedded plotly graphs for now, but they will be unnecessary when I switch everything to the cleaner, more powerful Dash graphs</li>
</ol>
