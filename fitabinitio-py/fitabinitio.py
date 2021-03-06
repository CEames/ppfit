#! /usr/bin/env python3

import numpy as np
import os

from ppfit.chi import chi_squared, sumOfChi
from ppfit.configuration import Configuration
from ppfit.fitting_parameter_set import Fitting_Parameter_Set
from ppfit.potential_file import Potential_File
from ppfit.training_set import Training_Set
from ppfit.io import read_from_file, mkdir_p
from ppfit.optimisation import read_optimisation_options, optimise

outfile = open('OUTPUT','w')

config1 = Configuration( directory = 'configs/cubic/',
                         runtime_file = 'runtime_cubic.inpt',
                         restart_file = 'restart_cubic.dat',
                         forces_file  = 'cubic.force',
                         dipoles_file = 'cubic.dip', 
                         stresses_file = 'cubic.stress' )

config2 = Configuration( directory = 'configs/tet',
                         runtime_file = 'runtime_tet.inpt',
                         restart_file = 'restart_tet.dat',
                         forces_file  = 'tet.force',
                         dipoles_file = 'tet.dip', 
                         stresses_file = 'tet.stress' )

config3 = Configuration( directory = 'configs/rhombo',
                         runtime_file = 'runtime_rhombo.inpt',
                         restart_file = 'restart_rhombo.dat',
                         forces_file  = 'rhombo.force',
                         dipoles_file = 'rhombo.dip', 
                         stresses_file = 'rhombo.stress' )

training_set = Training_Set( [ config1, config2, config3 ] )
fitting_parameters = Fitting_Parameter_Set.from_parameters_file( 'PARAMS' )
potential_file = Potential_File( 'template_BaTiO3', fitting_parameters )
opt_options = read_optimisation_options( 'OPT' )
min_method = opt_options.method_min

chi_squared_scaling = { 'forces':   opt_options.scalingF,
                        'dipoles':  opt_options.scalingD,
                        'stresses': opt_options.scalingS }

sum_of_chi = sumOfChi( potential_file, training_set, chi_squared_scaling, plot = True )

# # evaluate sum_of_chi with our initial potential parameters, and save a .pdf plot
# sum_of_chi.evaluate( fitting_parameters.to_fit.initial_values )
# # TODO move plotting capabilities of sum_of_chi to a .plot method, and allow the target directory to be set here
# mkdir_p('./initial-errors-pdfs')
# os.system('mv *.pdf ./initial-errors-pdfs')

sum_of_chi.plot = False
optimise( sum_of_chi.evaluate, fitting_parameters, method = min_method, opts = opt_options )
