import numpy as np
import os
from shutil import copyfile
from glob import glob

class PIMAIM_Run:

    def __init__( self, configuration, clean = True, executable = 'pimaim_serial' ):
        self.configuration = configuration
        self.clean = clean
        self.executable = executable
        self.common_input_dir = 'common_input'
        self.cwd = os.getcwd()
        self.ran_okay = None

    def set_up( self ):
        copyfile( 'potential.inpt', os.path.join( self.configuration.directory, 'potential.inpt' ) )
        for f in os.listdir( self.common_input_dir ):
            copyfile( os.path.join( self.common_input_dir, f ), os.path.join( self.configuration.directory, f ) )
        os.chdir( self.configuration.directory )
        self.clean_dir()
        copyfile( self.configuration.runtime, 'runtime.inpt' )
        copyfile( self.configuration.restart, 'restart.dat' )
        return self 

    def run( self ):
        os.system( '{} > out.out'.format( self.executable ) )
        cg_error = 'cg failed to converge' in open( 'out.out' ).read()
        if cg_error:
            self.ran_okay = False
        self.ran_okay = True
    
    def collect_data( self ):
        self.configuration.new_forces = np.loadtxt( 'forces.out' )[0::self.configuration.nsupercell]
        number_of_ions = self.configuration.new_forces.shape[0]
        self.configuration.new_dipoles = np.loadtxt( 'dipoles.out' )[0:number_of_ions:self.configuration.nsupercell]
        diag_stresses = np.loadtxt( 'xxyyzzstress.out' )[1:4]
        off_diag_stresses = np.loadtxt( 'xyxzyzstress.out' )[1:4]
        self.configuration.new_stresses = np.concatenate( ( diag_stresses, off_diag_stresses ) )
        # TODO How should the stress tensors be treated if we have a supercell

    def clean_dir( self ):
        to_delete = glob( '*out*' ) + glob( '*.fort' )
        for f in to_delete:
            os.remove( f )

    def tear_down( self ):
        if self.clean:
            self.clean_dir()
        os.chdir( self.cwd )
        

