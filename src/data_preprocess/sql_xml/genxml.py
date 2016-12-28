#!/usr/bin/env python

#################################################################################################################
## This script creates HDF5 files from corresponding SQLite db files in many-to-one fashion. So, for all db files 
## present in one input folder, one equivalent HDF5 file is created in the output folder. For input folders 
## containing more hierarchies, one HDF5 file is created for contents of each subfolder.
#################################################################################################################

import sqlite3, sys, glob, os, argparse,errno

DB_SUFFIX = '.db'
XML_ROOT = 'states' 

# Function to check for existing directories, and create a new one if not present 
def dir_check(d):
    if os.path.exists(d):
        reply = raw_input("Specified output directory already exists!! Delete existing directory named <<"+os.path.basename(d)+">> and all its contents? [y/n] ")
        if reply in ['y', 'Y', 'yes']:
            try:
                os.system('rm -r '+ d)
                print("Directory named <<"+os.path.basename(d)+ ">> and all its contents deleted!!")
                # Make new output folder
                try:
                    os.makedirs(d)
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise                
            except:
                error("- Could not delete directory <<" +os.path.basename(d)+">>. Directory may contain additional files, remove files manually and try again!")
        else:
            replytwo = raw_input("Continue & write output files inside existing directory: <<"+os.path.basename(d)+">> ? WARNING: This will overwrite old files having same name, if present in the folder! [y/n]: ")
            if not replytwo in ['y', 'Y', 'yes']:
                try:              
                    print ("Please remove or rename the existing directory <<"+os.path.basename(d)+">> and try again, or choose a different directory for the output")
                    sys.exit()
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise                        
    else:
        os.makedirs(d)

# Function to print out the error messages,if any, and exit
def error(mesg):
    print >>sys.stderr, ">>>>> (Error): %s" % mesg
    sys.exit(1)

def convert2xml(fname, targetFolder):
    # Create folder with sqlname as filename
    verboseprint('\n-Found file: ',fname) 
    outFolderName = targetFolder + '/' +  os.path.basename(fname)[:-len(DB_SUFFIX)]    
    dir_check(outFolderName)
    verboseprint('-Successfully created output folder: ', outFolderName)   

    con = None
    try:
        con = sqlite3.connect(fname)
        cur = con.cursor()
       
        # Get its_names from the table _iters_
        verboseprint('-Extracting its_names: ',os.path.basename(fname))
        cur.execute("SELECT * from _iters_;")
        its_list = [x[0] for x in cur.fetchall()]
        verboseprint(its_list)
        verboseprint('-Extract successful: its_name')
        
        # Create xml files
        verboseprint('-Initializing XML files:')
        for itsName in its_list:
            xmlFile = open(outFolderName + '/' + str(itsName) + '.xml','w')
            xmlFile.write('<' + XML_ROOT + '>' + '\n' + '<itno>' + str(itsName) +'</itno>'+ '\n')
            xmlFile.close()
            verboseprint(' '+str(itsName)+'.xml'),

        # Get the name of all the tables
        verboseprint('-Analysing database structure')
        cur.execute("SELECT name from sqlite_master WHERE type='table';")
        table_list = [x[0].encode('ascii', 'ignore') for x in cur.fetchall()]
        if '_iters_' in table_list: table_list.remove('_iters_')
        
        for table_name in table_list:
            agent_name = table_name
            verboseprint('-Reading table: ',table_name)
            # Get column names of the table
            cur.execute("PRAGMA table_info("+ table_name +")")
            
            # Zeroth column contains '_ITERATION_NO' so we start from index 1
            variable_names = [x[1].encode('ascii', 'ignore') for x in cur.fetchall()]    
            iterNoColIdx = variable_names.index('_ITERATION_NO')
            
            xmlStr = ""
            oldFileName = ""
            xmlFile = None
            for row in cur.execute("SELECT * from "+ table_name):
                xmlStr = ""
                fileName = outFolderName + '/' + str(row[iterNoColIdx]) + '.xml'
                
                # Check if file is already open, for reuse
                if (fileName <> oldFileName):
                    if (xmlFile):
                        xmlFile.close()
                    xmlFile = open(fileName, 'a')
                    oldFileName = fileName
                    
                i = 1
                for var in variable_names[1:]:
                    xmlStr = xmlStr + '<' + var + '>' + ('' if not row[i] else row[i]) + '</' + var + '>' + '\n'
                    i = i + 1
              
                xmlFile.write('<xagent>\n<name>'+ agent_name + '</name>' + '\n' + xmlStr + '</xagent>' + '\n')
                verboseprint('-Writing into XML file: ',os.path.basename(fileName))
            if (xmlFile):
                xmlFile.close()     
                
        # Close the document root tag
        for itsName in its_list:
            xmlFile = open(outFolderName + '/' + str(itsName)+'.xml', 'a')
            xmlFile.write('</' + XML_ROOT + '>')
            xmlFile.close()
        
    except sqlite3.Error, e:
        print "Error ", e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()
    verboseprint('-Done processing: ',os.path.basename(fname), '\n')
       

if __name__ == "__main__":
    # Setup for command line arguments
    parser = argparse.ArgumentParser(prog='genxml.py', description='Converts the sqlite database to xml.')
    parser.add_argument('dbpath', help='path to folder containing the .db files', nargs=1, type=str)
    parser.add_argument('-o', '--outpath', help='path to the folder where the output is desired', nargs=1, type=str)
    parser.add_argument('-v', '--verbose', help='get the status of the intermediate processing steps', action='store_true')   
    parser.add_argument('-s', '--status', help='get the total progress of the processing', action='store_true')
    args = parser.parse_args()
    
    # Set input parameters
    input_dbfolder =  ''
    input_dbfolder = args.dbpath[0]
    dir_list =[]
    # Checking for nested subdirectories within a directory
    for (dirpath,dirnames,filenames) in os.walk(input_dbfolder):
        dir_list.append(dirpath)
    if len(dir_list) == 0:
        error("- Make sure the specified input directory is an actual directory, and not a file!")
    if os.getcwd() == os.path.abspath(input_dbfolder):    
        error("- BAD IDEA!!! Execution script and input db files both inside a single folder <<" +os.getcwd()+">>. Might cause a recursive loop leading to erroneous output in some cases. Expected at least one level of separation. Please keep the script somewhere else and retry!")
        
    if len(dir_list)>1:
        N = 1
        F = len(dir_list)-1
    else:
        N = 0 
        F = len(dir_list)
    
    # Set output parameters
    output_folder =  ''
    if args.outpath:
        output_folder = args.outpath[0]
    else:
        # Choose one of the options below and comment out the other as desired.
        
        #output_folder =  './output_'+os.path.basename(input_dbfolder) # Creates output folder in the same folder where Python script is located.
        output_folder =  os.path.dirname(input_dbfolder)+'/output_'+os.path.basename(input_dbfolder)  # Creates output folder in the same folder where input folder is located
        

    # Function call to check if the output folder already exists, and create if not present 
    dir_check(output_folder)
       
    #Setup for verbose arguments
    if args.verbose:
        def verboseprint(*args):
            for arg in args:
                print arg,
            print 
    else:
        verboseprint = lambda *a: None 
        
    #Setup for process status arguments
    if args.status:
        def statusprint(*args):
            for arg in args:
                sys.stdout.write("\r" + arg)
                sys.stdout.flush()
            print
    else:
        statusprint = lambda *a: None 
    
    # Process each folder in the input directory
    processed_folders = 0
    statusprint('\n- Total number of input folders: '+ str(F)+'\n')  
    for i in range(N,len(dir_list)):
        statusprint('- Started processing folder: '+os.path.basename(dir_list[i]))     
        # Populate the list with all sql file names in the folder
        sql_file_list = []
        for fname in glob.glob(os.path.join(dir_list[i], '*'+DB_SUFFIX)):
            sql_file_list.append(fname)
        statusprint('Total number of files in current folder: '+ str(len(sql_file_list)))
         
        # Generate xml
        processed_files =[] 
        for fname in sql_file_list:
            verboseprint ('\n- Started processing: '+os.path.basename(fname))
            convert2xml(fname, output_folder)
            processed_files.append(fname)
            percent = round((float(len(processed_files))/len(sql_file_list))*100,2)
            statusprint('Number processed files: '+str(len(processed_files))+', of total: '+str(len(sql_file_list))+'    Progress:'+ str(percent) +'%'),
        statusprint('- Finished processing folder: '+ os.path.basename(dir_list[i])+'\n')
        processed_folders = processed_folders+1
        f_percent = round((float(processed_folders)/F)*100,2)
        statusprint('- Total progress:'+ str(f_percent) +'%', '\n')
            
            
            
            
