# H1-B Explorer

H1-B filing data is used to attempt to understand 

1. Which companies are hiring the most H1-B workers?

2. Who pays the most for foreign talent? The lease?

3. How do salaries for H1-B workers compare to average salaries in the area?

4. What fields are most in demand now? How is that different from 5 or 10 years ago?
 
## Installation

* Clone the repository with `git clone https://github.com/mackenziedg/H1B-Site.git`
 
* Create a virtual Python environment with [`virtualenv`](https://virtualenv.pypa.io/en/stable/)
 
* Activate the virtual environment and install the neccessary packages with `pip install -r requirements.txt`
 
* Run `python package_and_run.py` to package the app and start the server. This also sets the environment variables needed for `flask` to run, so as of right now this script needs to run every time to start up the server
 
* A file `<package_root>/h1b/instances/config.py` is required to connect to the database

## Data Sources

Data was pulled from 

* http://www.flcdatacenter.com/caseh1b.aspx
  * under heading "H-1B EFile Data" years 2002-2006

and 

* https://www.foreignlaborcert.doleta.gov/performancedata.cfm
  * under "Disclosure Data" -> "LCA Programs (H-1B, H-1B1, E-3)" -> years 2008-2016
  * and "Disclosure Data" -> "Latest Quarterly Updates" -> H-1B for FY1 (this location could potentially change in the future if a new fiscal year is the latest)
