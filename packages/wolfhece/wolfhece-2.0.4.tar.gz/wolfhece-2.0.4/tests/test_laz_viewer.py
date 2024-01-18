import _add_path
import unittest
import tempfile

from wolfhece.lazviewer import viewer
from wolfhece.lazviewer.laz_viewer import myviewer, xyz_laz_grids, Colors_Lazviewer

class LazViewer(unittest.TestCase):

    def test_viewer_Theux_2023(self):

        mygrids = xyz_laz_grids(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\LAZ_Vesdre\2023\grids')
        xyz = mygrids.scan([[252500, 252700],[136400,136500]])
        newview_code = myviewer(xyz,Colors_Lazviewer.CODE_2023)
        newview = myviewer(xyz,Colors_Lazviewer.ORTHO_2021)

        self.assertTrue(isinstance(newview, viewer), 'Bad type viewer')
        self.assertTrue(isinstance(newview_code, viewer), 'Bad type viewer')
        self.assertTrue(xyz.shape==(2220375,4), 'badv shape in xyz')
