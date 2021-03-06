'''Combination of 'TimeDirectoryDeeperTime.py' and 'TimeDirectoryDeeperLocation.py'
Eg of path - /time_root_deeper/2019/Mar/Mar_12_2019-Mar_17_2019/COP/Traffic road sim/makefile
Creates the folder 'time_root_deeper'
'''


import os, time
import operator
import shutil

# function to create necessary location directories
def create_loc_dir(path,dir):
    if len(dir)>0:
        dir_path = os.path.join(path,dir[0])
        
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            print("Directory already exists")

        create_loc_dir(dir_path,dir[1:])

# directory being scanned
path = '../FileSystemTest'

file_threshhold = 50
files = []
timeroot_path = 'time_root_deeper'

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
year_dir_paths = []
month_dir_paths = []
time_dir_paths = []

# creating a list of folders needed
for f in files:
   
    if (i%file_threshhold) == 0:
        file_time = time.ctime(f[2]).split()
        time_dir_names.append(os.path.join(file_time[4], file_time[1], file_time[1] + '_' + file_time[2] + '_' + file_time[4]))
        year_dir_paths.append(os.path.join(timeroot_path,file_time[4]))
        month_dir_paths.append(os.path.join(timeroot_path,file_time[4], file_time[1]))
        
    
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


# creating all the folders with symlinks to previous and next folder
ydp_previous = ''
for ydp in year_dir_paths:
    try:
        os.mkdir(ydp)
        if ydp_previous!='' :
            ydp_previous_name = ydp_previous.split("/")[-1]
            ydp_name = ydp.split("/")[-1]
            os.symlink(os.path.abspath(ydp_previous), os.path.abspath(os.path.join(ydp, ydp_previous_name)))
            os.symlink(os.path.abspath(ydp), os.path.abspath(os.path.join(ydp_previous, ydp_name)))
    except FileExistsError:
        print("Directory already exists")
    ydp_previous = ydp

mdp_previous = ''
for mdp in month_dir_paths:
    try:
        os.mkdir(mdp)
        if mdp_previous!='' :
            mdp_previous_name = mdp_previous.split("/")[-1]
            mdp_name = mdp.split("/")[-1]
            os.symlink(os.path.abspath(mdp_previous), os.path.abspath(os.path.join(mdp, mdp_previous_name)))
            os.symlink(os.path.abspath(mdp), os.path.abspath(os.path.join(mdp_previous, mdp_name)))
    except FileExistsError:
        print("Directory already exists")
    mdp_previous = mdp

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
    tdp_previous = tdp


i = 0
j = 0

# creting links to all the files with location heirarchy
for f in files:
   
    try:
        location_dir_path = f[0].split('/')[2:-1]
        create_loc_dir(time_dir_paths[j],location_dir_path)
       
        os.symlink(os.path.abspath(f[0]), os.path.join(time_dir_paths[j], *location_dir_path, f[1]))
    except FileExistsError:
        print("File already exists")

    if (i%file_threshhold) == (file_threshhold -1):
        j = j+1

    i = i+1
   
