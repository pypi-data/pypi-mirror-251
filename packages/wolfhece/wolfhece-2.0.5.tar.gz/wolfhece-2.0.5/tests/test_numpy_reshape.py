import _add_path
import unittest
import numpy as np
from wolfhece.wolf_array import WolfArray, WOLF_ARRAY_FULL_SINGLE
from tempfile import TemporaryDirectory, TemporaryFile
from os.path import join


class NumpyTests(unittest.TestCase):

    def test_reshape(self):
        
        a = np.zeros((4,4))
        a[0:2,0:2] = 0
        a[0:2,2:]  = 1
        a[2:,0:2]  = 2
        a[2:,2:]   = 3

        b = np.mean(a.reshape((2,2,2,2)), axis=(1,3))
        # b = a.reshape((2,2,2,2))
        c = np.asarray([[0,1],[2,3]])
        d=np.sum(np.abs(b-c))
        
        self.assertEqual(d, 0., 'bad reshape and mean')
        

    def test_wolf2Numpy(self):

        # Create wolfarray
        w_array = WolfArray()
        # set sizes/shape
        w_array.nbx, w_array.nby = 100,200
        # allocate memory space
        w_array.allocate_ressources()     

        # fill-in with data
        w_array.array.data[:,:] = np.arange(100*200, dtype=np.float32).reshape(w_array.array.shape, order='F')

        with TemporaryDirectory() as tmpdir:
            # write on disk
            w_array.write_all(join(tmpdir, 'test.bin'))
            # read in another array
            r_array = WolfArray(join(tmpdir, 'test.bin'))

            # binary read
            with open(join(tmpdir, 'test.bin'), 'rb') as f:
                # numpy from buffer
                locarray = np.frombuffer(f.read(100*200 * 4), dtype=np.float32)

                # copy buffer in numpy array alive after "with open"
                np_array_F = np.asarray(locarray.copy(), dtype=np.float32)
                # using order "F", data is aligned/ordered as Fortran (first indice most rapid)                 
                np_array_F = np_array_F.reshape(100, 200, order='F')

                # using order "C", data is aligned/ordered as C (last indice most rapid)                 
                # the array is 'transposed' --> like numpy default definition
                np_array_C = np.asarray(locarray.copy(), dtype=np.float32)                
                np_array_C = np_array_C.reshape(200, 100, order='C')

            self.assertEqual(np.all(w_array.array-r_array.array == 0.), True)
            self.assertEqual(np.all(w_array.array-np_array_F == 0.), True)
            self.assertEqual(np.all(w_array.array-np_array_C.T == 0.), True)
            self.assertEqual(np.all(w_array.array.T-np_array_C == 0.), True)
