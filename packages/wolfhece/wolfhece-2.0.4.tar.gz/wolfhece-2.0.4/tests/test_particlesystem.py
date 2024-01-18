import _add_path
from unittest import TestCase
import numpy as np
from tempfile import TemporaryDirectory

from wolfhece.PyVertexvectors import vector, wolfvertex
from wolfhece.lagrangian.emitter import Emitter
from wolfhece.lagrangian.velocity_field import Velocity_Field
from wolfhece.lagrangian.particles import Particles
from wolfhece.lagrangian.particle_system import Particle_system

class TestParticlesSystem(TestCase):

    def test_uniform_x_velocity_field(self):
        """
        Uniform velocity field along X.
        """
        u = np.zeros((10,20), dtype=np.float64)
        v = np.zeros((10,20), dtype=np.float64)

        u[2:9,2:19] = 1.
        v[2:9,2:19] = 0.

        domain = np.zeros(u.shape, dtype=np.int8)
        domain[2:8,2:18] = 1

        vel = Velocity_Field(u, v)
        vect_emit = vector()
        vect_emit.add_vertices_from_array(np.array([[2.,2.],
                                            [3.,2.],
                                            [3.,4.],
                                            [2.,4.]], dtype=np.float64))
        vect_emit.find_minmax()

        emit = Emitter(vect_emit.asshapely_pol(), 100, 10.)

        ps = Particle_system(domain, [emit], [vel])

        def callback(time:float):
            print(f'Time: {time}')


        ps.bake(20., 1., 'RK22', callback=callback)

        with TemporaryDirectory() as tmpdir:
            # save and load
            ps.save(f'{tmpdir}/test')
            newps = Particle_system()
            newps.load(f'{tmpdir}/test')

            newps.reset()
            newps.bake(20., 1., 'RK22', callback=callback)

        # fig, ax = newps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass

    def test_linear_x_velocity_field(self):
        """
        Uniform velocity field along X.
        """
        u = np.zeros((10,20), dtype=np.float64)
        v = np.zeros((10,20), dtype=np.float64)

        u[:,2:18] = np.tile(np.linspace(.1, 1., 16), u.shape[0]).reshape((u.shape[0], 16))
        v[2:9,2:18] = 0.

        domain = np.zeros(u.shape, dtype=np.int8)
        domain[2:8,2:18] = 1

        vel = Velocity_Field(u, v)
        vect_emit = vector()
        vect_emit.add_vertices_from_array(np.array([[2.,2.],
                                            [2.1,2.],
                                            [2.1,19.],
                                            [2.,19.]], dtype=np.float64))
        vect_emit.find_minmax()

        emit = Emitter(vect_emit.asshapely_pol(), 100, 10.)

        ps = Particle_system(domain, [emit], [vel])
        ps.bake(5., 1., 'RK22')

        # fig, ax = ps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass

    def test_uniform_y_velocity_field(self):
        """
        Uniform velocity field along Y.
        """
        u = np.zeros((10,20), dtype=np.float64)
        v = np.zeros((10,20), dtype=np.float64)

        u[2:9,2:19] = 0.
        v[2:9,2:19] = 1.

        domain = np.zeros(u.shape, dtype=np.int8)
        domain[2:8,2:18] = 1

        vel = Velocity_Field(u, v)
        vect_emit = vector()
        vect_emit.add_vertices_from_array(np.array([[2.,2.],
                                            [3.,2.],
                                            [3.,4.],
                                            [2.,4.]], dtype=np.float64))
        vect_emit.find_minmax()

        emit = Emitter(vect_emit.asshapely_pol(), 100, 10.)

        ps = Particle_system(domain, [emit], [vel])
        ps.bake(20., 1., 'RK22')

        # fig, ax = ps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass

    def test_circle_Euler(self):
        """
        Velocity field like a circle.
        Temporal scheme Euler Explicite.
        """
        from wolfhece.lagrangian.example_domain import circle_velocity_field

        ps, t_total = circle_velocity_field()
        ps.bake(t_total, 1., 'Euler_expl')

        with TemporaryDirectory() as tmpdir:
            # save and load
            ps.save(f'{tmpdir}/test')
            newps = Particle_system()
            newps.load(f'{tmpdir}/test')

        # fig, ax = ps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        # fig, ax = newps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass

    def test_circle_RK22(self):
        """
        Velocity field like a circle.
        Temporal scheme RK22.
        """
        from wolfhece.lagrangian.example_domain import circle_velocity_field

        ps, t_total = circle_velocity_field()
        ps.bake(t_total, 1., 'RK22')

        # fig, ax = ps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass

    def test_circle_RK22_2m(self):
        """
        Velocity field like a circle.
        Temporal scheme RK22.
        """
        from wolfhece.lagrangian.example_domain import circle_velocity_field

        ps, t_total = circle_velocity_field(oxoy=(100.,100.), dxdy=(2.,2.))
        ps.bake(t_total, 1., 'RK22')

        ps.save(r'.\doc\examples\Particle_system\circle\circle', save_particles=False)

        # fig, ax = ps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass

    def test_read(self):
        ps = Particle_system()
        ps.load(r'.\doc\examples\Particle_system\circle\circle')

        self.assertEqual(ps.number_of_emitters,1, 'Number of emitters')
        self.assertEqual(ps.number_of_vf,1, 'Number of velocity fields')
        self.assertEqual(ps._velocity_fields[0.]._vf_numba.u.shape,(201,201), 'Shape of velocity field')
        self.assertEqual(ps.get_header(),(100.,100.,2.,2.,201,201), 'Header of velocity field')
        self.assertEqual(ps.nb_steps, 1258, 'Number of steps')
        self.assertEqual(ps._emitters[0].how_many, 100, 'Number of particles')
        self.assertEqual(ps._emitters[0].every_seconds, 1356.6370614359173, 'Emission rate')
        self.assertEqual(ps._emitters[0].area.wkt, 'POLYGON ((299 104, 303 104, 303 498, 299 498, 299 104))', 'Emission area')
        self.assertEqual(ps._emitters[0].origx, 0., 'Emission origx')
        self.assertEqual(ps._emitters[0].origy, 0., 'Emission origy')
        self.assertEqual(ps._emitters[0].dx, 1., 'Emission dx')
        self.assertEqual(ps._emitters[0].dy, 1., 'Emission dy')
        self.assertEqual(ps._emitters[0].active, True, 'Emission active')
        self.assertEqual(ps._emitters[0].color_area, [0.,0.,0.,1.], 'Emission color_area')
        self.assertEqual(ps._emitters[0].color_particles, [0.,0.,0.,1.], 'Emission color_particles')
        self.assertEqual(len(ps._emitters[0].clock.times), 1, 'Emission clock')
        self.assertEqual(ps._emitters[0].clock.times[0], [0., np.Infinity], 'Emission clock')

        pass

    def test_circle_RK4(self):
        """
        Velocity field like a circle.
        Temporal scheme RK4.
        """
        from wolfhece.lagrangian.example_domain import circle_velocity_field

        ps, t_total = circle_velocity_field()
        ps.bake(t_total, 1., 'RK4')

        fig, ax = ps.plot_mpl('all')
        ax.set_aspect('equal')
        fig.show()
        pass

    def test_circle_RK45(self):
        """
        Velocity field like a circle.
        Temporal scheme RK45.
        """
        ps, t_total = self.init_circle_velocity_field()
        ps.bake(t_total, 1., 'RK45')

        fig, ax = ps.plot_mpl('all')
        ax.set_aspect('equal')
        fig.show()
        pass

    def test_laby(self):
        """
        Labyrinth -- (u,v) obtained by potential flow between inlet and outlet
        """
        from wolfhece.lagrangian.example_domain import labyrinth

        ps = labyrinth(nb_particles=200, every=1000.)
        ps.bake(1000., 20., 'RK22')

        ps.save(r'.\doc\examples\Particle_system\Labyrinth\labyrinth', save_particles=False)

        # fig, ax = ps.plot_mpl('all')
        # ax.set_aspect('equal')
        # fig.show()
        pass
