# DSR_Project1
Repository for the first project in the Data Storage and Retrieval class. Fall 2017.

~~Deadline is October 31st (or 3 weeks, roughly). Please post any ideas you have at https://github.com/acastrops/DSR_Project1/issues/1 :)~~

* 2017-10-12: Created a basic flask/skeleton framework that can connect to the remote (currently empty) database. Shared the secrets file on Google Drive, which goes in '<project root>/h1b/'. Run `python package_and_run.py` to package the app and start the server. After it's packaged you can just do `flask run`.


# Branches

* master

  * Full, merged branch. "Production"
  
* cleaning_processing
  
  * For cleaning the data and manipulating it into a usable form.

## Data Source

Data was pulled from 

* http://www.flcdatacenter.com/caseh1b.aspx
  * under heading "H-1B EFile Data" years 2002-2006

and 

* https://www.foreignlaborcert.doleta.gov/performancedata.cfm
  * under "Disclosure Data" -> "LCA Programs (H-1B, H-1B1, E-3)" -> years 2008-2016
  * and "Disclosure Data" -> "Latest Quarterly Updates" -> H-1B for FY1 (this could potentially change in the future if a new fiscal year is the latest)
