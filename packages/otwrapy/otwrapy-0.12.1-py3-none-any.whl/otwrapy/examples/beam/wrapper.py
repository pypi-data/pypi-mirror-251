#!/usr/bin/env python

"""
General purpose OpenTURNS python wrapper
"""

import openturns as ot
import os
from xml.dom import minidom
import time
import otwrapy as otw
import openturns.coupling_tools as otct

ot.ResourceMap.SetAsUnsignedInteger('Cache-MaxSize', int(1e6))

__author__ = "Felipe Aguirre Martinez"
__copyright__ = "Copyright 2015-2019 Phimeca"
__version__ = "0.2"
__email__ = "aguirre@phimeca.fr"
__all__ = ['Wrapper']


class Wrapper(ot.OpenTURNSPythonFunction):
    """Wrapper of a C++ code that computes the deviation of a beam.

    The C++ code computes the deviation with the given formula:

    .. math::

        y = \\frac{FL^{3}}{3EI}

    with :

    - :math:`F` : Load
    - :math:`E` : Young modulus
    - :math:`L` : Length
    - :math:`I` : Inertia

    The wrapped code is an executable that is run from the shell as follows :

    .. code-block:: sh

        $ beam -x beam.xml

    where :file:`beam.xml` is the input file containing the four parameters
    :math:`F, E, L, I`.

    The output of the code is an xml output file :file:`_beam_outputs_.xml`
    containing the deviation and its derivates.
    """

    def __init__(self, tmpdir=None, sleep=0.0):
        """
        Parameters
        ----------
        tmpdir : string
            The root directory on which temporary working directories will be
            created for each independent simulation.

        sleep : float (Optional)
            Intentional delay (in seconds) to demonstrate the effect of
            parallelizing.
        """

        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.temp_work_dir = tmpdir
        self.input_template = os.path.join(self.base_dir,
                                           'beam_input_template.xml')
        self.executable = os.path.join(self.base_dir, 'beam -x beam.xml')
        self.sleep = sleep

        # Number of input/output values:
        super(Wrapper, self).__init__(4, 1)
        self.setInputDescription(['Load', 'Young modulus', 'Length', 'Inertia'])
        self.setOutputDescription(['deviation'])

    # @otw.Debug('wrapper.log')
    def _exec(self, X):
        """Run the model in the shell for a given point :math:`X`.

        This is the default OpenTURNS method that executes the function on a
        given point. It has to be overloaded so that it executes/wraps your
        code. Semantically speaking, the function is divided on three parts :

        - Create an input file with values of :math:`X` using :func:`~Wrapper._create_input_file`.

        - Run the executable on the shell using :func:`~Wrapper._call`.

        - Read the value of the output from the XML output file using :func:`~Wrapper._parse_output`.

        The three steps are executed on a temporary working directory using the
        context manager :class:`otwrapy.TempWorkDir`

        Parameters
        ----------
        X : 1D array (e.g. ot.Point or a 1D np.array)
            Input vector of size :math:`n` on which the model will be evaluated

        Returns
        -------
        Y : list
            Output vector of the model. Univariate in this case.
        """

        # Create intentional delay
        time.sleep(self.sleep)

        # File management. Move to temp work dir. Cleanup at the end
        with otw.TempWorkDir(self.temp_work_dir, 'ot-beam-example-', True):

            # Create input file
            self._create_input_file(X)

            # Execute code
            _ = self._call()

            # Retrieve output (see also ot.coupling_tools.get_value)
            Y = self._parse_output()

        return Y

    def _create_input_file(self, X):
        """Create the input file required by the code.

        Replace the values of the vector :math:`X` to their corresponding tokens
        on the :file:`beam_input_template.xml` and create the input file :file:`beam.xml`
        on the current working directory.

        Parameters
        ----------
        X : 1D array (e.g. ot.Point or a 1D np.array)
            Input vector of size :math:`n` on which the model will be evaluated
        """
        otct.replace(
            self.input_template,
            'beam.xml',
            ['@F', '@E', '@L', '@I'],
            X)

    def _call(self):
        """Execute code on the shell and return the runtime

        Returns
        -------
        runtime : float
            Total runtime (wall time and not cpu time)
        """

        time_start = time.time()
        otct.execute(self.executable, shell=True)
        time_stop = time.time()

        return time_stop - time_start

    def _parse_output(self):
        """Parse the XML output given by the code and get the value of deviation

        Returns
        -------
        Y : list
            Output vector of the model. Univariate in this case.
        """

        # Retrieve output (see also coupling_tools.get_value)
        xmldoc = minidom.parse('_beam_outputs_.xml')
        itemlist = xmldoc.getElementsByTagName('outputs')
        deviation = float(itemlist[0].attributes['deviation'].value)

        # Make a list out of the output(s)
        Y = [deviation]

        return Y


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description="Python wrapper example used for the PRACE training on HPC and uncertainty.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-tmp', default=None, type=str,
                        help='Root directory on which temporary working directories will be'
                        + 'created for each independent simulation.')

    parser.add_argument('-seed', default=int(0), type=int,
                        help='Seed number for the random number generator')

    parser.add_argument('-MonteCarlo', nargs=1,
                        help="Launch a MonteCarlo simulation of given size")

    parser.add_argument('-X', nargs='*',
                        help='List of floats [X1, X2.. Xp] or PATH to a pickled DOE')

    parser.add_argument('-n_cpus', default=-1, type=int,
                        help="(Optional) number of cpus to use.")

    parser.add_argument('-backend', default='joblib', type=str,
                        choices=['joblib', 'multiprocessing', 'ipyparallel'],
                        help="Whether to parallelize using 'joblib' or 'multiprocessing'.")

    parser.add_argument('-run', default=False, type=bool, nargs='?',
                        const='True', help='If True, run the model', choices=[True, False])

    parser.add_argument('-dump', default=False, type=bool, nargs='?',
                        const='True', choices=[True, False],
                        help='If True, dump the output for later posttreatment')

    args = parser.parse_args()

    model = otw.Parallelizer(Wrapper(tmpdir=args.tmp, sleep=1),
                             backend=args.backend, n_cpus=args.n_cpus)

    print("The wrapper has been instantiated as 'model'.")

    if args.MonteCarlo is not None:
        from _probability_model import X_distribution
        ot.RandomGenerator.SetSeed(args.seed)
        N = int(args.MonteCarlo[0])
        X = X_distribution.getSample(N)
        print("Generated a MonteCarlo DOE of size {}".format(N))

    elif args.X is not None:
        if isinstance(args.X[0], str) and os.path.isfile(args.X[0]):
            X = otw.load_array(args.X[0])
            print("Loaded a DOE of size {} from file: '{}'".format(X.getSize(),
                  args.X[0]))
        else:
            X = ot.Point([float(x) for x in args.X])

    if args.run:
        Y = model(X)
        # Dump the results if asked
        if args.dump:
            otw.dump_array(Y, 'OutputSample.pkl')
            print("The output has been saved to 'OutputSample.pkl'")
        else:
            print("Finished evaluationg the model. Take a look at 'Y' variable.")
    elif (args.MonteCarlo is not None) or (args.X is not None):
        print("The desired input is ready to be run using --> 'Y = model(X)'")
