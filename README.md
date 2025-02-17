# Data_Cleanup
An example of a data cleanup and data transformation project I've done. The full scale project included 8 files, but this was a slimmed down version for a Python User Group meeting I lead to demonstrate the concepts to new programmers. The agricultural trade data is updated monthly, and this script allows the data to be processed very quickly to then be used in data visualization tools such as Tableau and Power BI. 

Some of the data cleanup steps included in this project are:

* Skipping unnecessary rows at the top and bottom of the data
* Deleting unnecessary columns from the dataset
* Removing extra data from the year string to only return a 4 digit year
* Deleting columns that have specific special characters at the end as they are subsets of a group and this prevents double counting
* Renaming the columns to get the months labeled in the correct row
* Transforming the data so a month over month and year over year calculation can be added
* Transforming the data to structure it in a way that makes data visualization more easy and effective
* Clearing out extra string characters that are not needed in the country column
