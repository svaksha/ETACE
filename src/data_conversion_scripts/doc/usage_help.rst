Notes on usage of the python scripts
------------------------------------

1. DB_HDF5
~~~~~~~~~~

- These scripts convert ``SQLite`` database files to ``HDF5`` files.
- There are two versions of the script currently, each having a slightly different functionality:

#. The script ``db_hdf5_v1.py`` creates HDF5 files from corresponding SQLite db files in *many-to-one* fashion.
   So, for all db files present in one input folder, one equivalent HDF5 file is created in the output folder.
   For input folders containing more hierarchies, a **-r** flag can be passed which results in one HDF5 file for the contents of each subfolder.
   
#. The script ``db_hdf5_v2.py`` creates HDF5 files from corresponding SQLite db files in *one-to-one* fashion.
   So, for each db file present in the input folder, an equivalent HDF5 file is created in the output folder.
   To combine db files into a single HDF5 file , version 1 of script named ``db_hdf5_v1.py`` can be used instead.

- The script runs on both Python 2.7.10 / Python 3.5.2 and above. Any help regarding the execution of the script can be obtained by using the following command in any terminal window::

    python db_hdf5_v1.py -h
    
- There is an option to specify a desired output folder for the output files, by passing an **-o** flag.
- However, by default the output is created either in the folder containing the script, in the same folder that has the input folder, or the input folder itself.
  These three options can be adjusted by commenting out the appropriate line in the script. Please look for the section *"Set output parameters"* in the script and comment out
  the option that is not preferred. Currently, the default is such that the output is created in the input folder.

**Note:** *There is no difference in the size of combined HDF5 (many-to-one generated by db_hdf5_v1.py) and separate HDF5 (one-to-one generated by db_hdf5_v2.py) files, even when compressing.* 
        *However, separate HDF5 files are easier to manipulate when restructuring the HDF5 into files per Agent-type (i.e. Bank.h5, Eurostat.h5 and so on).*
        *Therefore, use of db_hdf5_v2.py is recommended for simplicity.*


2. XML_HDF5
~~~~~~~~~~~

- This script converts ``XML`` files to ``HDF5`` files.

- This script creates HDF5 files from corresponding XML files in *many-to-one* fashion. So, for all xml files present in one input folder, one equivalent HDF5 file is created in the output folder. 
  For input folders containing more hierarchies, given that a *-r* flag is passed, one HDF5 file is created for contents of each subfolder.
  
- The script runs on both Python 2.7.10 / Python 3.5.2 and above. Any help regarding the execution of the script can be obtained by using the following command in any terminal window::

        python xml_hdf5.py -h
    
- There is an option to specify a desired output folder for the output files, by passing an **-o** flag.
- However, by default the output is created either in the folder containing the script, in the same folder that has the input folder, or the input folder itself.
  These three options can be adjusted by commenting out the appropriate line in the script. Please look for the section *"Set output parameters"* in the script and comment out
  the option that is not preferred. Currently, the default is such that the output is created in the input folder.
  

3. DB_XML
~~~~~~~~~

- This script converts ``SQLite`` Db files to ``XML`` files.
- This script creates XML files from corresponding DB files in *one-to-many* fashion. For each DB file, a folder is created and multiple corresponding XML files are created inside the folder, based on time samples.
- The script runs on both Python 2.7.10 / Python 3.5.2 and above. Any help regarding the execution of the script can be obtained by using the following command in any terminal window::

        python genxml.py -h

- There is an option to specify a desired output folder for the output files, by passing an **-o** flag.
- However, by default the output is created either in the folder containing the script, in the same folder that has the input folder, or the input folder itself.
  These three options can be adjusted by commenting out the appropriate line in the script. Please look for the section *"Set output parameters"* in the script and comment out
  the option that is not preferred. Currently, the default is such that the output is created in the input folder.
  

4. MERGE_HDF_AGENTWISE
~~~~~~~~~~~~~~~~~~~~~~

- This script converts HDF5 files from ``set_*_run_*_iters.h5`` format to ``HDF5`` files per agent (**Eurostat.h5**, **Firm.h5** etc). 
- So, for each HDF5 file present in the input folder, all corresponding agents are filtered and placed on a new agent-based HDF5 file.
- The script runs on both Python 2.7.10 / Python 3.5.2 and above. Any help regarding the execution of the script can be obtained by using the following command in any terminal window::

        python merge_hdf_agentwise.py -h
    
- There is an option to specify a desired output folder for the output files, by passing an **-o** flag.
- However, by default the output is created either in the folder containing the script, in the same folder that has the input folder, or the input folder itself.
  These three options can be adjusted by commenting out the appropriate line in the script. Please look for the section *"Set output parameters"* in the script and comment out
  the option that is not preferred. Currently, the default is such that the output is created in the input folder.
  


