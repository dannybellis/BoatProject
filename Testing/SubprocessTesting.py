#Testing to see how subprocess works

import subprocess

response = subprocess.check_output(['cd ~ && pwd'], shell=True)
response2 = subprocess.check_output(['pwd'], shell=True)
print(response) #this prints out the home directory
print(response2) #this prints out the original directory the code is running from