# This file will make sure the hostname is fully changed
from os.path import isfile
from shutil import copyfile
from sys import argv

hostname = argv[1]
files = ['/etc/hostname', '/etc/hosts']

print('New Hostname: ', hostname)
with open('/etc/hostname', 'r') as fid:
  old_hostname = fid.read()
print('Old Hostname:', old_hostname)
for filename in files:
  if not(isfile(str(filename + '.orig'))):
    copyfile(filename, str(filename + '.orig'))

  newfile = []
  with open(filename, 'r') as fid:
    for line in fid:
      newfile.append(line.replace(old_hostname, hostname))

  with open(filename, 'w') as fid:
    for line in newfile:
      fid.write(line)
