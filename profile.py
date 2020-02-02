import os
import shutil
import random
rndnum = random.randint(1, 1000)
email = "{name}@random_com".format(name=rndnum)
usertree = '/home/phil/python/abcapp/users/{useremail}/profile/imgs'.format(useremail=email)
os.makedirs(usertree)
# copy default information to that directory
defaultprofile = '/home/phil/python/abcapp/default_profile/'
target = '/home/phil/python/abcapp/users/{useremail}/profile'.format(useremail=email)
src_files = os.listdir(defaultprofile)

for file in src_files:
    full_file_name = os.path.join(defaultprofile, file)
    try:
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, target)
    except:
        print('not copied ' +   full_file_name)
        print(target)