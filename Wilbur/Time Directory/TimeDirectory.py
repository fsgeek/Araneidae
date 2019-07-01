'''Creates groups of files (fixed number) as folders based on last modification time
Adjacent ranges of time group folders have symlinks between them
Creates the folder 'time_root'
'''

import os, time
import operator
import shutil

# directory being scanned
path = '../FileSystemTest'

file_threshhold = 50 #Number of files in a group
files = []
timeroot_path = 'time_root'

# root directory
try:
    os.mkdir(timeroot_path)
except FileExistsError:
    print("Directory already exists")

# r=root, d=directories, f = files
#getting all files in the directory
for r, d, f in os.walk(path):
    f = [file for file in f if not file[0] == '.']
    d[:] = [dr for dr in d if not dr[0] == '.']
    for file in f:
    		filepath = os.path.join(r, file)
    		filepath2 = filepath.split('/')
    		last_modif_time = os.path.getmtime(filepath)
    		files.append((filepath, filepath2[-1],last_modif_time))

# sorting based on last modification time		
files.sort(key = operator.itemgetter(2))

i=0
j=0
f = []
time_dir_names = []
time_dir_paths = []

# creating a list of folders needed
for f in files:
   
    if (i%file_threshhold) == 0:
        file_time = time.ctime(f[2]).split() 
        time_dir_names.append(file_time[1] + '_' + file_time[2] + '_' + file_time[4])
        
    

    if (i%file_threshhold) == (file_threshhold -1):
        file_time = time.ctime(f[2]).split()
        time_dir_names[j] = time_dir_names[j] + '-' + (file_time[1] + '_' + file_time[2] + '_' + file_time[4])
        time_dir_paths.append(os.path.join(timeroot_path, time_dir_names[j]))
        j = j+1


    i=i+1


# the last time folder
if (i%file_threshhold) != file_threshhold:
    file_time = time.ctime(f[2]).split()
    time_dir_names[j] = time_dir_names[j] + '-' + (file_time[1] + '_' + file_time[2] + '_' + file_time[4])
    time_dir_paths.append(os.path.join(timeroot_path, time_dir_names[j]))


# creting all the folders with symlinks to previous and next folder
tdp_previous = ''
for tdp in time_dir_paths:
    try:
        os.mkdir(tdp)
        if tdp_previous!='' :
            tdp_previous_name = tdp_previous.split("/")[-1]
            tdp_name = tdp.split("/")[-1]
            os.symlink(os.path.abspath(tdp_previous), os.path.join(tdp, tdp_previous_name))
            os.symlink(os.path.abspath(tdp), os.path.join(tdp_previous, tdp_name))
    except FileExistsError:
        print("Directory already exists")
        print(tdp)
    tdp_previous = tdp


i = 0
j = 0

# creting links to all the files
for f in files:
   
    try:

        os.symlink(os.path.abspath(f[0]), os.path.join(time_dir_paths[j],str(i)+'-'+f[1]))
    except FileExistsError:
        print("File already exists")

    if (i%file_threshhold) == (file_threshhold -1):
        j = j+1

    i = i+1
   
