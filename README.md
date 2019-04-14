# Graphing with Flask and Plotly

##To Begin
Run "python get_data.py", then "python analysis.py"

This will set up the SQL tables needed.

## Timeline
Created SQL tables with the following sample code: <br>
```
def get_annualized_vol(contract_root):
    contracts = get_contract_family(contract_root).replace(np.nan, 0)
    ann_vol_cont = (contracts.std() * math.sqrt(252))
    ann_vol_sql = pd.DataFrame({'ann_vol': ann_vol_cont})
    ann_vol_sql.to_sql("combined_ann_vol", localhost,
                       if_exists='append', chunksize=250, index=True,
                       dtype={'code_name': VARCHAR(ann_vol_sql.index.get_level_values('code_name').str.len().max())})
    return ann_vol_sql
```
## Plotly Charts
I initially created plotly charts through their website by importing CSVs of tables.  I then used their GUI to adjust the specifications of each graph.

I improved on this in the final version by using plotly's offline mode to have dynamic graphs and pages, making this project much easier to scale.  These were pulled from the mysql dataframes instead of CSVs.

![Imgur](https://i.imgur.com/oCjgX4Sl.png "Sample Graphs")

## Building the website

I used Flask as my front end to crate some routes for each graph.  I brought in Bootstrap to style my css including the dropdown navbar.  I created a "parent" layout an then extended it into each page.



## Overview
Switching to dynamic graphs greatly improved the ability to change future contract routes and made my code DRY.  I had a great time with learning new skills throughout this challenge (Some that didn't make it into the final app as well!)  
