import _add_path
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib
from os.path import exists, join
import wx
import sys

from wolfhece.scenario import update_void, check_scenario, config_manager


class TestScenario(unittest.TestCase):

    def test_init_void(self):

        with TemporaryDirectory() as tmpdir:
            update_void.create_new_file(Path(tmpdir) / "test_update_void.py")

            with open(Path(tmpdir) / "test_update_void.py", 'r') as file:
                code = file.read()

                # Assert
                self.assertTrue('def update_topobathy' in code)
                self.assertTrue('def update_manning' in code)

    def test_scan_dir(self):

        scen = config_manager.Config_Manager_2D_GPU('./tests/data/GPU_Scen')

        self.assertTrue(scen.configs is not None, "No configs found")
        self.assertTrue(len(scen.configs['subdirs']) ==2, "Not all subdirs found")
        self.assertTrue(scen.configs['test']['is_simul'] == True, "Bad discovery of is_simul for test directory")
        self.assertTrue(scen.configs['Theux']['is_simul'] == True, "Bad discovery of is_simul for Theux directory")
        self.assertTrue(scen.configs['test']['scen1']['is_simul'] == False, "Bad discovery of is_simul for test/scen1 directory")

        self.assertTrue(scen.configs['test']['is_scenario'] == False, "Bad discovery of is_scenario for test directory")
        self.assertTrue(scen.configs['Theux']['is_scenario'] == False, "Bad discovery of is_scenario for Theux directory")
        self.assertTrue(scen.configs['test']['scen1']['is_scenario'] == True, "Bad discovery of is_scenario for test/scen1 directory")
        pass

    def test_import_module(self):

        module_path = r'tests\data\GPU_Scen\test\scen1'
        module_name = 'modprint'

        self.assertTrue(exists(join(module_path, module_name+'.py')), "Module not found")

        modpath = Path(module_path)
        sys.path.insert(0, str(modpath.absolute()))

        module1 = importlib.import_module(module_name)

        module_name = 'update_scen'
        self.assertTrue(exists(join(module_path, module_name+'.py')), "Module not found")

        module2 = importlib.import_module(module_name)

        self.assertTrue(module1 is not None, "Bad import of module1")
        self.assertTrue(module2 is not None, "Bad import of module2")

        """ Import de modules et vérification de l'héritage de Update_Sim """
        module_path = r'tests\data\GPU_Scen\test\scen1'
        module_name = 'modprint'

        self.assertTrue(exists(join(module_path, module_name+'.py')), "Module not found")

        validate_mod1 = check_scenario.check_file_update(Path(module_path) / module_name)

        module_name = 'update_scen'
        self.assertTrue(exists(join(module_path, module_name+'.py')), "Module not found")

        validate_mod2 = check_scenario.check_file_update(Path(module_path) / module_name)

        module_name = 'update_void'
        self.assertTrue(exists(join(module_path, module_name+'.py')), "Module not found")

        validate_mod3 = check_scenario.check_file_update(Path(module_path) / module_name)

        self.assertTrue(validate_mod1 == False, "Bad check of module1")
        self.assertTrue(validate_mod2 == True, "Bad check of module2")
        self.assertTrue(validate_mod3 == True, "Bad check of module")

    def test_create_and_check(self):
        """ CRéation d'un fichier vide via le module et vérification de l'héritage de Update_Sim"""

        with TemporaryDirectory() as tmpdir:
            update_void.create_new_file(Path(tmpdir) / "test_update_void.py")
            validate_mod = check_scenario.check_file_update(Path(tmpdir) / "test_update_void.py")
            self.assertTrue(validate_mod == True, "Bad check")

    def test_UI(self):
        app = wx.App()
        scen = config_manager.Config_Manager_2D_GPU('./tests/data/GPU_Scen')
        app.MainLoop()
        pass