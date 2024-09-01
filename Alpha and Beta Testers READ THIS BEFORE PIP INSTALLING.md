During the alpha and beta tests of FireWxPy, **there is an issue with installation only for windows users**. If you are using mac or linux, you shouldn't have this issue. 
The issue is with pygrib since pygrib does not have a binary wheel for windows and thus the wheel won't build for firewxpy when pip installing from my github page. 

**How to install firewxpy for windows users for Python>=3.9** during the alpha-beta (the stages before I try to get this on conda-forge):
1) conda install pygrib
2) pip install "git+https://github.com/edrewitz/FireWxPy.git"
   **For Python 3.8**
     - Must use conda to install cartopy and netcdf4. 

**mac and linux users**
1) pip install "git+https://github.com/edrewitz/FireWxPy.git"
