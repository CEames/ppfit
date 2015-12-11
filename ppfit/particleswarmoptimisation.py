import os
import sys
import fileinput
import subprocess
from subprocess import call
import re
import shutil
import glob
import operator
from operator import add
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import basinhopping
from pyswarm import pso

#Creates a log file
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("log.dat", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

sys.stdout = Logger()


#Define a function that will replace a string in a file in-situ
def inplace_change(filename, old_string, new_string):
        s=open(filename).read()
        if old_string in s:
                s=s.replace(old_string, new_string)
                f=open(filename, 'w')
                f.write(s)
                f.flush()
                f.close()
        else:
                print 'No occurances of "{old_string}" found.'.format(**locals())

def fitness(x):
	#print x
	shutil.copy2('template', 'potentials')
	#Substitute the current best parameters into the template file
	for index, param in enumerate(x, start=1):
		tmp = "POT%02d" % index
		tag ="%s" % tmp
		paramstring ="%s" % param
		templatefile = "potentials"
		inplace_change(templatefile, tag, paramstring)

	#Run the calculations via the bash script runall		
	os.system("./runall 2> /dev/null")		
        
        #Get the sum of squares via the bash script getsos
	sos = subprocess.check_output("./getsos", shell=True)
	ss = float(sos)

	print ss
	return ss

#This function prints a progress summary and is an optional extra when calling  
def callbackF(x, convergence=0.1):
        global Nfeval
        print Nfeval, x, fitness(x)
	os.system("./plot")
	Nfeval += 1

#Here we define lower and upper bounds for the parameters - defines a box to contain the swarm
#within physically meaningful regions
lb = [
18000, 0.320, 250,
3400,  0.375, 400,
1800,  0.375, 100,
3000, 0.310, 0,
2400,  0.315, 0,
2400,  0.310, 0,
5000,  0.340, 0,
9000,  0.370, 600, 1.5, 1.5
]

ub = [
20000, 0.330, 500,
4500,  0.385, 750,
4500,  0.385, 750,
30000, 0.340, 700,
7500,  0.395, 850,
7500,  0.395, 550,
21000, 0.395, 1300,
11000, 0.395, 1300, 2.0, 2.0
 ]

#Here we use the pso module to drive the optimisation of the fitness function. We could use the 
#callback function as an extra option here for a summary (see pso module documentation)
xopt = pso(fitness, lb, ub, debug=True, swarmsize=100, maxiter=500)
