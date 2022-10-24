from naked.py import *
import os

#Parbauda vai tads fails pastav
print('----------')
print('Checking if there is naked file.')
assert os.path.isfile('naked.py') == True
print('OK')
print('----------')
#Parbauda vai fails nav tukss
print('----------')
print('Cheking if file does not contain anything')
naked_file = 'naked.py'
os.stat(naked_file).st_size != 0
print('OK')
print('----------')
