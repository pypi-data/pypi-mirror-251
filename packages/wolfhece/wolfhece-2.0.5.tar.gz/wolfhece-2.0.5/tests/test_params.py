import _add_path
from unittest import TestCase
import wx

from wolfhece.PyTranslate import _
from wolfhece.PyParams import Type_Param, Wolf_Param, Buttons, new_json, key_Param

example = r""" Outlet Coordinates :
Station Code	-1	Code of the SPW station (integer)
Station Name		Name of the SPW station
River Name		Name of the river on which is the SPW station
X	0.0000000000000000E+00	X coordinate of the outlet - Lambert72 [m] (double) (double)
Y	0.0000000000000000E+00	Y coordinate of the outlet - Lambert72 [m] (double) (double)
 Topographical mesh :
Space step	2.5000000000000000E+02	Spatial resolution [m] (integer) (double)
%json{"Values":{"1 m":1, "10 m": 10, "20 m": 20, "100 m": 100, "250 m": 250, "500 m": 500, "5000 m": 5000}}
 Model Type :
Spatial distribution	1	Possible values -- lumped = 1 ; semi distributed = 2 ; fully distributed = 3
%json{"Values":{"lumped":1, "semi distributed": 2, "fully distributed": 3}}
Type of hydrological model	1	Possible values -- linear reservoir = 1 ; VHM = 2 ; Unit Hydrograph = 3
%json{"Values":{"linear reservoir":1, "VHM": 2, "Unit Hydrograph": 3, "VHMmodif": 4, "VHMmodif2": 5, "GR4": 6, "2 layers distributed/lumped": 7, "2 layers distributed UH": 8}}
Type of hydraulic model	1	Possible values -- temporal shift = 1
%json{"Values":{"temporal shift":1}}
 Runoff :
How to compute local runoff speed?	3	Possible values -- ADALI = 3 ; Ven te Chow = 2 ; Froude based = 1
%json{"Values":{"ADALI":3, "Ven te Chow": 2, "Froude based": 1}}
Time step	300	Rounded time step (integer) [s] (double) (integer)
 Preprocessing :
Cropping topo	1	Generate the topographic data cropped from RW Lidar (0, 1 or 2) (integer) (integer)
%json{"Values":{"All data":0, "To crop": 1, "To read from existing file": 2}}
Delimiting subbasin	1	Delimiting the basin attached to the outlet (1 = yes; 0 = no) (integer) (integer)
%json{"Values":{"False":0, "True": 1}}
Whole basin (atmospheric geometry & data)	1	Execute preprocessing on the whole basin (1 = yes; 0 = no) (integer) (integer)
%json{"Values":{"False":0, "True": 1}}
Subbasin (atmospheric geometry & data)	1	Execute preprocessing on each subbasin (1 = yes; 0 = no) -- Whole basin prepro necessary (integer) (integer)
%json{"Values":{"False":0, "True": 1}}
Lumped input	1	Compute lumped data (rain and evapotranspiration) (1 = yes; 0 = no) (integer) (integer)
%json{"Values":{"False":0, "True": 1}}
 Atmospheric data :
Type of source	3	Possible values -- SPW = 4 ; IRM = 2 ; NetCDF = 1 ; QDF Municipality = 3
%json{"Values":{"SPW":4, "IRM": 2, "NetCDF": 1, "QDF Municipality": 3}}
Time step	86400	Time Step (integer) [s] (double) (integer)
 Temporal Parameters :
Start date time	19710101-000000	Start date [YYYYMMDD-HHMMSS]
End date time	20190101-000000	End date [YYYYMMDD-HHMMSS]
Time step	8.6400000000000000E+04	Computation time step (double precision) [s] (double) (double)
 Cropping Parameters :
X minimum	4.2000000000000000E+04	X coordinate - left [m] (double) (double)
X maximum	2.9600000000000000E+05	X coordinate - Right [m] (double) (double)
Y minimum	2.0000000000000000E+04	Y coordinate - Down [m] (double) (double)
Y maximum	1.6800000000000000E+05	Y coordinate - Up [m] (double) (double)
 Semi distributed model :
How many?	0	Number of interior points (integer) (integer)
Compute all?	-1	Computation of all interior points (-1 == No, and take the outlet ; 0 == No ; 1 == Yes) (integer) (integer)
 Interior point 1 :
X	0.0000000000000000E+00	X Coordinate of the outlet 1 (double) (double)
Y	0.0000000000000000E+00	Y Coordinate of the outlet 1 (double) (double)
Which type	0	outlet 1 (integer) (integer)
Active	0	Computation of outlet 1 ? (0 == No ; 1 == Yes) (integer) (integer)
 Interior point $n(Semi distributed model,How many?,0,100)$ :
X	0.0000000000000000E+00	X Coordinate of the outlet n (double) (double)
Y	0.0000000000000000E+00	Y Coordinate of the outlet n (double) (double)
Which type	0	outlet n (integer) (integer)
Active	0	Computation of outlet n ? (0 == No ; 1 == Yes) (integer) (integer)
 Measuring stations SPW :
Directory	P:/Donnees/Debits/RealTime/Data	Path to the measures (directory)
Filename	Stations_RT.txt	File containing the characteristics of the stations (file)
To read	1	Must we read the data from files? (0 == No ; 1 == Yes) (integer) (integer)
%json{"Values":{"False":0, "True": 1}}
 Municipality QDF :
Directory	P:/Donnees/Debits/Données IDF - 2016/hydro/	Directory containing Municipality data (directory)
Pluvio Filename	pluvio.ini	Name of the "Pluvio.ini" file (file)
Matching Filename	Match_num_zone_shapefile_INS_index.txt	Name of the matching file (INS->name) (file)
Return period	25	Return period to compute (5,10,25,50,100) (integer) (integer)
%json{"Values":{"5 years":5, "10 years": 10, "25 years": 25, "50 years": 50, "100 years": 100}}
Symmetry coefficient	5.0000000000000000E-01	.5 == symmetry, 1. --> assymmertry on the right (double) (double)
Value	1	Possible values (mean value = 1 ; confidence interval 95% up = 3 ; confidence interval 95% down = 2(integer) (integer)
Max time	8.6400000000000000E+04	Total time (double) (double)
 NetCDF :
Directory	DirNetCDF	Directory (directory)
Generic filename	MAR2WOLF-MARv3.9.0-	Local Generic NetCDF file
First filename	MAR2WOLF-MARv3.9.0-1990.nc	Local NetCDF file for the first year (file)
 LandUse :
Directory	P:/Donnees/Cartes/LandUse/Landuse_matriciel_OCCSOL	Directory of the LandUse map (vector or array format) (directory)
 Topography :
Directory	P:/Donnees/MNT_MNS/MNT_MNS_2013-2014	Directory of the MNT (directory)
Filename	mnt.flt	File name of the MNT file (file)
 SPW Rain :
Directory of the SPW data (directory)
 IRM Rain :
Directory of the IRM data (directory)
 Forced Exchanges :
Directory	C:\Users\u228412\OneDrive - Universite de Liege\Documents\Share_offline\Code\Exemples\Vesdre\Simulations\Lumped_Spixhe\Référence	Directory of the forced Exchanges (directory)
Filename	N-O	File of the forced Exchanges (file)
"""
class WolfParams(TestCase):

    def test_create(self):
        """
        Create a Wolf_Param object.
        """
        wp = Wolf_Param()
        self.assertIsInstance(wp, Wolf_Param)

    def test_add(self):
        """
        Add a parameter.
        Test type
        """
        wp = Wolf_Param()

        wp.addparam('test_group', 'testint', 1, Type_Param.Integer, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testint')], 1)

        wp.addparam('test_group', 'testfloat', 1.1, Type_Param.Float, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testfloat')], 1.1)

        wp.addparam('test_group', 'testbool', True, Type_Param.Logical, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testbool')], True)

        wp.addparam('test_group', 'testcol', (255,255,1,0), Type_Param.Color, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testcol')], (255,255,1,0))

        wp.addparam('test_group', 'testmix1', 1.5, Type_Param.Integer_or_Float, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testmix1')], 1.5)

        wp.addparam('test_group', 'testmix2', 3, Type_Param.Integer_or_Float, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testmix2')], 3)

        wp.addparam('test_group', 'testfile', r'c:\test', Type_Param.File, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testfile')], r'c:\test')

        wp.addparam('test_group', 'testdir', r'c:\test', Type_Param.Directory, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'testdir')], r'c:\test')

        wp.addparam('test_group', 'teststr', 'mystréèö', Type_Param.String, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'teststr')], 'mystréèö')

        wp.addparam('test_group', 'teststrempty', 'mystréèö', Type_Param.Empty, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        self.assertEqual(wp[('test_group', 'teststrempty')], 'mystréèö')

        self.assertEqual(wp.get_nb_params('test_group'), (10,10), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_groups(), (1,1), 'Number of groups is not correct')

        self.assertEqual(wp.get_nb_params('notexists'), (None,None), 'Number of parameters is not correct')

    def test_newjson(self):
        """ new_json routine """
        wp = Wolf_Param()
        json = new_json({"rk22":1, "rk44":2}, 'this is a comment\nwith 2 lines')
        wp.addparam('test_group', 'testint', 1, Type_Param.Integer, 'comment', json, 'All')

        self.assertEqual(wp[('test_group', 'testint')], 1)
        ret = wp.get_param_dict('test_group', 'testint')

        self.assertEqual(ret[key_Param.ADDED_JSON]['Values'],{"rk22":1, "rk44":2})
        self.assertEqual(ret[key_Param.ADDED_JSON]['Full_Comment'],'this is a comment\nwith 2 lines')

    def test_change_value(self):
        """ Change a value """
        wp = Wolf_Param()
        wp.addparam('test_group', 'testint', 1, Type_Param.Integer, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        wp[('test_group', 'testint')] = 2
        self.assertEqual(wp[('test_group', 'testint')], 2)

        wp.change_param('test_group', 'testint', 3)
        self.assertEqual(wp[('test_group', 'testint')], 3)

    def test_setitem(self):
        """ Set an item """
        wp = Wolf_Param()
        wp.addparam('test_group', 'testint', 1, Type_Param.Integer, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')
        wp[('test_group', 'testint')] = 2
        self.assertEqual(wp[('test_group', 'testint')], 2)

        wp[('test_group', 'testfloat')] = 2.5
        self.assertEqual(wp[('test_group', 'testfloat')], 2.5)

    def test_callbackdestroy(self):
        """ Callback """
        wp = Wolf_Param()
        wp.addparam('test_group', 'testint', 1, Type_Param.Integer, 'comment', '%json{"Values":{"rk22":1, "rk44":2}}', 'All')

        ret_callback = False
        ret_callback_destroy = False

        def callback():
            return True
        def callback_destroy():
            return True

        wp.set_callbacks(callback, callback_destroy)
        ret_callback = wp.callback()
        ret_callback_destroy = wp.callbackdestroy()
        self.assertTrue(ret_callback, 'Callback not called')
        self.assertTrue(ret_callback_destroy, 'Callback destroy not called')


    def test_extract_ingroup(self):
        """ Extract the group name and the reference """
        wp = Wolf_Param()

        string = 'mygroup$n(group, nb, 1, 10)$'
        groupname, ref = wp._Extract_IncrInfo(string)

        self.assertEqual(groupname, 'mygroup$n$')
        self.assertTrue(ref ==  ['group', 'nb', 1, 10])

    def test_incr_group(self):
        """ Increment a group """
        wp = Wolf_Param()
        wp.addparam('general', 'nb', 1, Type_Param.Integer, whichdict='All')

        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb')

        # test if the group is created
        self.assertEqual(len(wp.myIncGroup), 1)

        # change the value of nb
        wp[('general', 'nb')] = 2

        # test if the groups are created
        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')

        # change the value of nb
        wp[('general', 'nb')] = 3

        # test if the groups are created and saved
        self.assertEqual(wp.get_nb_groups(), (4,1), 'Number of groups is not correct')
        self.assertEqual(len(wp.myIncGroup['test_group_$n$']["Saved"]), 2, 'Saved value is not correct')

        # decrement the value of nb
        wp[('general', 'nb')] = 1

        # test if the groups are created and saved
        self.assertEqual(wp.get_nb_groups(), (2,1), 'Number of groups is not correct')
        self.assertEqual(len(wp.myIncGroup['test_group_$n$']["Saved"]), 3, 'Saved value is not correct')

    def test_incr_param(self):
        """ increment of parameters """

        wp = Wolf_Param()
        wp.addparam('general', 'nb', 1, Type_Param.Integer, whichdict='All')
        wp.add_IncParam('general', 'incr$n$', 1, 'comment', Type_Param.Integer, 1, 10, 'nb')

        #increment the value of nb
        wp[(('general', 'nb'))] = 2

        # test if the parameters are created
        self.assertEqual(wp.get_nb_params('general'), (3,1), 'Number of parameters is not correct')

        wp[(('general', 'nb'))] = 3
        self.assertEqual(wp.get_nb_params('general'), (4,1), 'Number of parameters is not correct')
        self.assertEqual(len(wp.myIncParam['general']['incr$n$']["Saved"]['general']), 3, 'Saved value is not correct')

    def test_incr_param_ref_group(self):
        """ increment of parameters with reference in another group """

        wp = Wolf_Param()
        wp.addparam('group1', 'nb', 1, Type_Param.Integer, whichdict='All')
        wp.add_IncParam('group', 'incr$n$', 1, 'comment', Type_Param.Integer, 1, 10, 'nb', 'group1')

        #increment the value of nb
        wp[(('group1', 'nb'))] = 2

        # test if the parameters are created
        self.assertEqual(wp.get_nb_params('group'), (2,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('group1'), (1,1), 'Number of parameters is not correct')
        self.assertEqual(len(wp.myIncParam['group']['incr$n$']["Saved"]['group']), 1, 'Saved value is not correct')

        wp[(('group1', 'nb'))] = 3
        self.assertEqual(wp.get_nb_params('group'), (3,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('group1'), (1,1), 'Number of parameters is not correct')
        self.assertEqual(len(wp.myIncParam['group']['incr$n$']["Saved"]['group']), 3, 'Saved value is not correct')

        wp[(('group1', 'nb'))] = 1
        self.assertEqual(wp.get_nb_params('group'), (1,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('group1'), (1,1), 'Number of parameters is not correct')
        self.assertEqual(len(wp.myIncParam['group']['incr$n$']["Saved"]['group']), 4, 'Saved value is not correct')

    def test_incr_param_and_group(self):
        """
        Increment of parameters and groups based on 2 general references

        All groups must have the same number of parameters
        """
        wp = Wolf_Param()
        wp.addparam('general', 'nb_group', 1, Type_Param.Integer, whichdict='All')
        wp.addparam('general', 'nb_param', 1, Type_Param.Integer, whichdict='All')

        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb_group')
        wp.add_IncParam('test_group_$n$', 'incr$n$', 1, 'comment', Type_Param.Integer, 1, 10, 'nb_param', 'general')

        #increment the value of nb
        wp[(('general', 'nb_group'))] = 2

        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (2,2), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (1,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (1,None), 'Number of parameters is not correct')

        wp[(('general', 'nb_group'))] = 3
        self.assertEqual(wp.get_nb_groups(), (4,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (2,2), 'Number of parameters is not correct')

        wp[(('general', 'nb_param'))] = 2
        self.assertEqual(wp.get_nb_params('general'), (2,2), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (2,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (2,None), 'Number of parameters is not correct')

    def test_add_param_in_IncGroup(self):
        """
        Multiple parameters in an incremental group

        All groups must have the same number of parameters
        """
        wp = Wolf_Param()
        wp.addparam('general', 'nb_group', 1, Type_Param.Integer, whichdict='All')
        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb_group')
        wp.addparam('test_group_$n$', 'nb_param', 1, Type_Param.Integer, whichdict='IncGroup')
        wp.addparam('test_group_$n$', 'param2', 1, Type_Param.Integer, whichdict='IncGroup')

        wp.change_param('general', 'nb_group', 2)

        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (1,1), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (2,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (2,None), 'Number of parameters is not correct')

    def test_add_incparam_in_IncGroup(self):
        """
        Increment of parameters and groups based on 2 general references

        All groups must have the same number of parameters
        """
        wp = Wolf_Param()
        wp.addparam('general', 'nb_group', 1, Type_Param.Integer, whichdict='All')
        wp.addparam('general', 'nb_param', 1, Type_Param.Integer, whichdict='All')
        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb_group')
        wp.add_IncParam('test_group_$n$', 'incr$n$', 1, 'comment', Type_Param.Integer, 1, 10, 'nb_param', 'general')

        wp.change_param('general', 'nb_group', 2)
        wp.change_param('general', 'nb_param', 2)

        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (2,2), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (2,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (2,None), 'Number of parameters is not correct')

        wp.change_param('general', 'nb_group', 2)
        wp.change_param('general', 'nb_param', 4)

        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (2,2), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (4,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (4,None), 'Number of parameters is not correct')

    def test_add_incparam_in_IncGroup2(self):
        """
        Increment of parameters and groups based on 1 general reference and 1 local reference

        Groups can have different number of parameters
        """

        wp = Wolf_Param()
        wp.addparam('general', 'nb_group', 1, Type_Param.Integer, whichdict='All')
        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb_group')
        wp.addparam('test_group_$n$', 'nb_param', 1, Type_Param.Integer, 'comment', whichdict='IncGroup')
        wp.add_IncParam('test_group_$n$', 'incr$n$', 1, 'comment', Type_Param.Integer, 1, 10, 'nb_param', 'test_group_$n$')

        wp.change_param('general', 'nb_group', 2)
        wp.change_param('test_group_1', 'nb_param', 2)
        wp.change_param('test_group_2', 'nb_param', 4)

        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (1,1), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (3,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (5,None), 'Number of parameters is not correct')

    def test_add_incparam_in_IncGroup_with_addparam(self):
        """
        Increment of parameters and groups based on 1 general reference and 1 local reference

        Groups can have different number of parameters
        """

        wp = Wolf_Param()
        wp.addparam('general', 'nb_group', 1, Type_Param.Integer, whichdict='All')
        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb_group')
        wp.addparam('test_group_$n$', 'nb_param', 1, Type_Param.Integer, 'comment', whichdict='IncGroup')

        # this line must be equal to the next one
        wp.addparam('test_group_$n$', 'incr$n(test_group_$n$, nb_param, 1, 10)$', 1, Type_Param.Integer, 'comment')
        # wp.add_IncParam('test_group_$n$', 'incr$n$', 1, 'comment', Type_Param.Integer, 1, 10, 'nb_param', 'test_group_$n$')

        wp.change_param('general', 'nb_group', 2)
        wp.change_param('test_group_1', 'nb_param', 2)
        wp.change_param('test_group_2', 'nb_param', 4)

        self.assertEqual(wp.get_nb_groups(), (3,1), 'Number of groups is not correct')
        self.assertEqual(wp.get_nb_params('general'), (1,1), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_1'), (3,None), 'Number of parameters is not correct')
        self.assertEqual(wp.get_nb_params('test_group_2'), (5,None), 'Number of parameters is not correct')

    def test_add_param_in_IncGroup(self):

        wp = Wolf_Param()
        wp.addparam('general', 'nb_group', 1, Type_Param.Integer, whichdict='All')

        ret = wp.addparam('group$n$', 'test_gourpIncr', 1) # must log an error because the incgroup does not exist

        self.assertEqual(ret, -2, 'Parameter should not be added')

        wp.add_IncGroup('test_group_$n$', 1, 10, 'general', 'nb_group')
        ret = wp.addparam('test_group_$n$', 'test_gourpIncr', 1) # OK becasue the incgroup exists

        self.assertEqual(ret, 0, 'Parameter should be added')

        ret = wp.add_param('test_$n(general, nb_group, 2, 20)$', 'test_param', 1) # OK because infos are given

        self.assertEqual(ret, 0, 'Parameter should be added')
        self.assertEqual(wp.get_nb_inc_groups(),2, 'Number of inc groups is not correct')

    def test_init_from_chain(self):
        """ Test the initialization from a chain """
        wp = Wolf_Param()
        wp.fill_from_strings(example)

        lines = example.splitlines()
        nbgroups = 0
        nbjson = 0
        for curline in lines:
            if curline.endswith(':'):
                nbgroups += 1
                print(curline)
            if '%json' in curline:
                nbjson += 1

        nbjson_param = 0
        for group, params in wp.myparams.items():
            for param in params.values():
                if key_Param.ADDED_JSON in param.keys() :
                    if param[key_Param.ADDED_JSON] !='':
                        nbjson_param += 1


        self.assertEqual(wp.get_nb_groups(), (nbgroups-2,nbgroups-1), 'Number of groups is not correct')
        self.assertEqual(nbjson, nbjson_param, 'Number of json is not correct')

    def test_init_from_chain2(self):
        """ Test the initialization from a chain """
        wp = Wolf_Param()
        wp.fill_from_strings(example, example)

        lines = example.splitlines()
        nbgroups = 0
        nbjson = 0
        for curline in lines:
            if curline.endswith(':'):
                nbgroups += 1
                print(curline)
            if '%json' in curline:
                nbjson += 1

        nbjson_param = 0
        for group, params in wp.myparams.items():
            for param in params.values():
                if key_Param.ADDED_JSON in param.keys() :
                    if param[key_Param.ADDED_JSON] !='':
                        nbjson_param += 1


        self.assertEqual(wp.get_nb_groups(), (nbgroups-2,nbgroups-1), 'Number of groups is not correct')
        self.assertEqual(nbjson, nbjson_param, 'Number of json is not correct')
