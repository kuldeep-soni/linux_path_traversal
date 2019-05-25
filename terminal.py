# linux_interface module handles queries by user and processes it.
from linux_interface import Linux
import time

print('$ <Starting your application...>')

# class Linux containing methods for linux path traversal instantiated
ILinux = Linux()
while True:
    curr_dir = ILinux.getcwd()
    print('$ {} >>'.format(curr_dir), end = ' ')
    query = input().strip() #Read from user
    if query == 'exit()':
        break
    ILinux.set_query(query) #query sent for processing
# Wait for 0.1 sec and then exit the terminal
time.sleep(0.1)