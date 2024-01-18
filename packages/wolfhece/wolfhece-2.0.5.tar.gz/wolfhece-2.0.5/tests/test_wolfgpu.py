import _add_path
import unittest
from pathlib import Path
import numpy as np

from wolfhece.Results2DGPU import wolfres2DGPU, Cache_Results2DGPU


class test(unittest.TestCase):

    def test_simfiles(self):

        dir_sim = Path('tests\data\GPU_Sim\Theux')

        files = ['bathymetry.npy',
                 'manning.npy',
                 'infiltration_zones.npy',
                 'h.npy',
                 'qx.npy',
                 'qy.npy',
                 'nap.npy']

        # test if files exist
        for curfile in files:
            self.assertTrue((dir_sim / curfile).exists(), f'{curfile} does not exist')

        # load files
        npy = [np.load(dir_sim / curfile) for curfile in files]

        ref = npy[0].shape

        # test if all files have the same shape
        for cur in npy:
            self.assertEqual(cur.shape, ref, 'Bad shape')

    def test_simfiles_vs_results(self):
        """ Test if bathymetry is the same from npy or res """
        dir_sim = Path('tests\data\GPU_Sim\Theux')

        files = ['bathymetry.npy',
                #  'manning.npy',
                #  'infiltration_zones.npy',
                #  'h.npy',
                #  'qx.npy',
                #  'qy.npy',
                #  'nap.npy',
                 ]

        # test if files exist
        for curfile in files:
            self.assertTrue((dir_sim / curfile).exists(), f'{curfile} does not exist')

        # load files
        npy = [np.load(dir_sim / curfile) for curfile in files]

        res = wolfres2DGPU(str(dir_sim / 'simul_gpu_results'), plotted=False)

        # npy has the same shape than WOLF file/array
        #  i is along X, j is along Y
        self.assertEqual(res.myblocks['block1'].top.array.shape, npy[0].shape, 'Bad shapes')
        self.assertTrue((res.myblocks['block1'].top.array.data == npy[0]).all(), 'Bad bathymetry values')


    def test_cache(self):
        """ Test cache for GPU results"""

        dir_sim = Path('tests\data\GPU_Sim\Theux')
        dir_res= dir_sim / 'simul_gpu_results'

        self.assertTrue(dir_sim.exists(), 'Sim directory does not exist')
        self.assertTrue(dir_res.exists(), 'Results directory does not exist')

        # init results
        res1 = wolfres2DGPU(str(dir_res.absolute()), plotted=False)
        res2 = wolfres2DGPU(str(dir_res.absolute()), plotted=False)

        # test if cache is None
        self.assertTrue(res1._cache is None, 'Cache should be None')
        self.assertTrue(res2._cache is None, 'Cache should be None')

        # setup cache for res2
        res2.setup_cache(0, -1)

        # test cache status
        self.assertTrue(res1._cache is None, 'Cache should be None')
        self.assertTrue(res2._cache is not None, 'Cache should be not None')

        # test nb results
        self.assertEqual(res1.get_nbresults(), res2.get_nbresults(), 'Bad number of results')

        # test results for different steps
        for idx in [0, 5, -1]:
            res1.read_oneresult(idx)
            res2.read_oneresult(idx)

            self.assertEqual(res1[0].array.shape, res2[0].array.shape, 'Bad shape')
            self.assertTrue((res1[0].array == res2[0].array).all(), 'Bad values')

    def test_cache_only_h(self):
        """ Test cache for GPU results for water depth only"""

        dir_sim = Path('tests\data\GPU_Sim\Theux')
        dir_res= dir_sim / 'simul_gpu_results'

        self.assertTrue(dir_sim.exists(), 'Sim directory does not exist')
        self.assertTrue(dir_res.exists(), 'Results directory does not exist')

        # init results
        res1 = wolfres2DGPU(str(dir_res.absolute()), plotted=False)
        res2 = wolfres2DGPU(str(dir_res.absolute()), plotted=False)

        # test if cache is None
        self.assertTrue(res1._cache is None, 'Cache should be None')
        self.assertTrue(res2._cache is None, 'Cache should be None')

        # setup cache for res2
        res2.setup_cache(0, -1, only_h=True)

        # test cache status
        self.assertTrue(res1._cache is None, 'Cache should be None')
        self.assertTrue(res2._cache is not None, 'Cache should be not None')

        # test nb results
        self.assertEqual(res1.get_nbresults(), res2.get_nbresults(), 'Bad number of results')

        # test results for different steps
        for idx in [0, 5, -1]:
            res1.read_oneresult(idx)
            res2.read_oneresult(idx)

            self.assertEqual(res1[0].array.shape, res2[0].array.shape, 'Bad shape')
            self.assertTrue((res1[0].array == res2[0].array).all(), 'Bad values')
            self.assertTrue(res2._cache.get_qx(idx) is None, 'qx should be None')
            self.assertTrue(res2._cache.get_qy(idx) is None, 'qx should be None')
