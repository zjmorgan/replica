#!/usr/bin/env python3

import unittest
import numpy as np
import scipy.linalg

from disorder.material import crystal
from disorder.material import symmetry

import os
directory = os.path.dirname(os.path.abspath(__file__))

class test_crystal(unittest.TestCase):
    
    def test_unitcell(self):
        
        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
                                        
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='Cu3Au.cif', 
                                   tol=1e-4)
        
        u = uc_dict['u']
        v = uc_dict['v']
        w = uc_dict['w']
        occ = uc_dict['occupancy']
        disp = uc_dict['displacement']
        site = uc_dict['site']
        atm = uc_dict['atom']
        n_atm = uc_dict['n_atom']
                
        self.assertEqual(n_atm, 4)
        
        np.testing.assert_array_almost_equal(u[atm == 'Au'], 0)
        np.testing.assert_array_almost_equal(v[atm == 'Au'], 0)
        np.testing.assert_array_almost_equal(w[atm == 'Au'], 0)
               
        np.testing.assert_array_equal(atm[site == 0], 'Au')
        np.testing.assert_array_equal(atm[site == 1], 'Cu') 
               
        np.testing.assert_array_almost_equal(occ, 1)
        np.testing.assert_array_almost_equal(disp, 0)

        # ---
        
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='H2O.cif', 
                                   tol=1e-4)
        
        occ = uc_dict['occupancy']
        atm = uc_dict['atom']
        
        np.testing.assert_array_almost_equal(occ[atm == '0'], 1.0)
        np.testing.assert_array_almost_equal(occ[atm == 'H'], 0.5)
        
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='CaTiOSiO4.cif', 
                                   tol=1e-4)
        
        disp = uc_dict['displacement']
        atm = uc_dict['atom']
        
        np.testing.assert_array_almost_equal(disp[atm == 'Ca'][:,0], 0.02200)
        np.testing.assert_array_almost_equal(disp[atm == 'Ca'][:,1], 0.00497)
        np.testing.assert_array_almost_equal(disp[atm == 'Ca'][:,2], 0.00537)
        np.testing.assert_array_almost_equal(disp[atm == 'Ca'][:,5], 0.00069)
        np.testing.assert_array_almost_equal(disp[atm == 'Ca'][:,4], -0.00098)
        np.testing.assert_array_almost_equal(disp[atm == 'Ca'][:,3], 0.00029)
        
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='chlorastrolite.cif', 
                                   tol=1e-4)
        
        u = uc_dict['u']
        v = uc_dict['v']
        w = uc_dict['w']
        occ = uc_dict['occupancy']
        disp = uc_dict['displacement']
        op = uc_dict['operator']
        atm = uc_dict['atom']
        
        np.testing.assert_array_almost_equal(occ[atm == 'FeX']+\
                                             occ[atm == 'AlX']+\
                                             occ[atm == 'MgX'], 1.0, 2)
        np.testing.assert_array_almost_equal(occ[atm == 'FeY']+\
                                             occ[atm == 'AlY'], 1.0)
            
        np.testing.assert_array_almost_equal(disp[atm == 'FeX'], 
                                             disp[atm == 'AlX'])
        np.testing.assert_array_almost_equal(disp[atm == 'AlX'], 
                                             disp[atm == 'MgX'])
            
        x, y, z = np.array([0.2541,0.242,0.4976])  
        for i in range(8):
            ux, vy, wz = symmetry.evaluate(op[atm == 'FeY'][i], [x,y,z])
            ux += 1*(ux < 0)-1*(ux >= 1)
            vy += 1*(vy < 0)-1*(vy >= 1)
            wz += 1*(wz < 0)-1*(wz >= 1)
            np.testing.assert_array_almost_equal(u[atm == 'FeY'][i], ux)
            np.testing.assert_array_almost_equal(v[atm == 'FeY'][i], vy)
            np.testing.assert_array_almost_equal(w[atm == 'FeY'][i], wz)
        
        # ---
        
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='CuMnO2.mcif', 
                                   tol=1e-4)
        
        mom = uc_dict['moment']
        mag_op = uc_dict['magnetic_operator']
        atm = uc_dict['atom']
        
        np.testing.assert_array_almost_equal(mom[atm == 'Cu'], 0.0)
        np.testing.assert_array_almost_equal(mom[atm == 'O'], 0.0)        
        
        mx, my, mz = np.array([1.8,0.0,1.4])  
        for i in range(8):
            moment = symmetry.evaluate_mag(mag_op[atm == 'Mn'][i], [mx,my,mz])
            np.testing.assert_array_almost_equal(mom[atm == 'Mn'][i], moment)
            
        uc_dict = crystal.unitcell(folder=folder, 
                                 filename='natrolite.cif', 
                                 tol=1e-4)
        
        disp = uc_dict['displacement']
        
        np.testing.assert_array_equal(atm[152:184], 'H')
        
        adp = [0.034, 0.034, 0.034, 0, 0, 0]
        for i in range(152, 168):
            np.testing.assert_array_almost_equal(disp[i], adp)
        
        adp = [0.032, 0.032, 0.032, 0, 0, 0]
        for i in range(168, 184):
            np.testing.assert_array_almost_equal(disp[i], adp)
        
    def test_supercell(self):

        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
                
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='CaTiOSiO4.cif', 
                                   tol=1e-4)
        
        u = uc_dict['u']
        v = uc_dict['v']
        w = uc_dict['w']
        occ = uc_dict['occupancy']
        disp = uc_dict['displacement']
        mom = uc_dict['moment']
        site = uc_dict['site']
        atm = uc_dict['atom']
        n_atm = uc_dict['n_atom']
        
        constants = crystal.parameters(folder=folder, filename='CaTiOSiO4.cif')
        
        a, b, c, alpha, beta, gamma = constants
        
        nu, nv, nw = 2, 3, 1
      
        crystal.supercell(atm,
                          occ,
                          disp,
                          mom,
                          u, 
                          v, 
                          w,
                          nu,
                          nv,
                          nw,
                          folder+'/supercell_CaTiOSiO4.cif',
                          folder=folder,
                          filename='CaTiOSiO4.cif')
        
        UC_dict = crystal.unitcell(folder=folder, 
                                   filename='supercell_CaTiOSiO4.cif', 
                                   tol=1e-4)
        
        U = UC_dict['u']
        V = UC_dict['v']
        W = UC_dict['w']
        Occ = UC_dict['occupancy']
        Disp = UC_dict['displacement']
        Mom = UC_dict['moment']
        Site = UC_dict['site']
        Atm = UC_dict['atom']
        N_atm = UC_dict['n_atom']
        
        Constants = crystal.parameters(folder=folder,
                                       filename='supercell_CaTiOSiO4.cif')
        
        A, B, C, Alpha, Beta, Gamma = Constants
        
        n_uvw = nu*nv*nw
        
        i, j, k = np.meshgrid(np.arange(nu), 
                              np.arange(nv), 
                              np.arange(nw), indexing='ij')
        
        i = i.flatten()[:,np.newaxis]
        j = j.flatten()[:,np.newaxis]
        k = k.flatten()[:,np.newaxis]
                
        np.testing.assert_array_almost_equal((i+u).flatten(), nu*U, 4)
        np.testing.assert_array_almost_equal((j+v).flatten(), nv*V, 4)
        np.testing.assert_array_almost_equal((k+w).flatten(), nw*W, 4)
                
        np.testing.assert_array_equal(np.tile(atm, n_uvw), Atm)
        np.testing.assert_array_almost_equal(np.tile(occ, n_uvw), Occ)
        np.testing.assert_array_almost_equal(np.tile(disp.T, n_uvw).T, Disp)
        
        self.assertEqual(n_atm*n_uvw, N_atm)
        
        self.assertAlmostEqual(a*nu, A)
        self.assertAlmostEqual(b*nv, B)
        self.assertAlmostEqual(c*nw, C)
        
        self.assertAlmostEqual(alpha, Alpha)
        self.assertAlmostEqual(beta, Beta)
        self.assertAlmostEqual(gamma, Gamma)
        
        os.remove(folder+'/supercell_CaTiOSiO4.cif')

        # ---
        
        uc_dict = crystal.unitcell(folder=folder, 
                                   filename='CuMnO2.mcif', 
                                   tol=1e-4)
        
        u = uc_dict['u']
        v = uc_dict['v']
        w = uc_dict['w']
        occ = uc_dict['occupancy']
        disp = uc_dict['displacement']
        mom = uc_dict['moment']
        site = uc_dict['site']
        atm = uc_dict['atom']
        n_atm = uc_dict['n_atom']
                
        nu, nv, nw = 1, 2, 3
      
        crystal.supercell(atm,
                          occ,
                          disp,
                          mom,
                          u, 
                          v, 
                          w,
                          nu,
                          nv,
                          nw,
                          folder+'/supercell_CuMnO2.mcif',
                          folder=folder,
                          filename='CuMnO2.mcif')
        
        UC_dict = crystal.unitcell(folder=folder, 
                                   filename='supercell_CuMnO2.mcif', 
                                   tol=1e-4)
        
        U = UC_dict['u']
        V = UC_dict['v']
        W = UC_dict['w']
        Occ = UC_dict['occupancy']
        Disp = UC_dict['displacement']
        Mom = UC_dict['moment']
        Site = UC_dict['site']
        Atm = UC_dict['atom']
        N_atm = UC_dict['n_atom']
        
        n_uvw = nu*nv*nw
                
        np.testing.assert_array_almost_equal(np.tile(mom.T, n_uvw).T, Mom)
        
        self.assertEqual((atm == 'Cu').sum()*n_uvw, (Atm == 'Cu').sum())
        self.assertEqual((atm == 'Mn').sum()*n_uvw, (Atm == 'Mn').sum())
        self.assertEqual((atm == 'O').sum()*n_uvw, (Atm == 'O').sum())
        
        os.remove(folder+'/supercell_CuMnO2.mcif')
    
    def test_laue(self):
        
        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
        
        laue = crystal.laue(folder=folder, filename='chlorastrolite.cif')
        
        self.assertAlmostEqual(laue, '2/m')
        
    def test_twins(self):
        
        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
        
        twins, fraction = crystal.twins(folder=folder, filename='bixbyite.cif')
        
        U = np.eye(3)
        np.testing.assert_array_almost_equal(twins[0], U)
        
        U = np.array([[0,-1,0],[-1,0,0],[0,0,-1]])
        np.testing.assert_array_almost_equal(twins[1], U)
        
        self.assertAlmostEqual(fraction.sum(), 1.0)
        
        twins, fraction = crystal.twins(folder=folder, filename='Cu3Au.cif')
        
        np.testing.assert_array_almost_equal(twins[0], np.eye(3))
                
        self.assertAlmostEqual(fraction, 1.0)
            
    
    def test_parameters(self):
        
        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
        
        constants = crystal.parameters(folder=folder, filename='CaTiOSiO4.cif')
        
        a, b, c, alpha, beta, gamma = constants
        
        self.assertAlmostEqual(a, 7.069)
        self.assertAlmostEqual(b, 8.722)
        self.assertAlmostEqual(c, 6.566)
        self.assertAlmostEqual(alpha, np.deg2rad(90))
        self.assertAlmostEqual(beta, np.deg2rad(113.86))
        self.assertAlmostEqual(gamma, np.deg2rad(90))
        
    def test_group(self):
        
        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
        
        hm, sg = crystal.group(folder=folder, filename='CaTiOSiO4.cif')
        
        self.assertEqual(sg, 'P121/a1')
        self.assertEqual(hm, 14)
                                     
    def test_d(self):

        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
        
        h, k, l = 1, 2, -3

        d = crystal.d(a, b, c, alpha, beta, gamma, h, k, l)

        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants

        B = crystal.cartesian(a_, b_, c_, alpha_, beta_, gamma_)
        
        u_, v_, w_ = np.dot(B, [1,0,0]), np.dot(B, [0,1,0]), np.dot(B, [0,0,1])

        self.assertAlmostEqual(d, 1/np.sqrt(np.dot(h*u_+k*v_+l*w_, 
                                                   h*u_+k*v_+l*w_)))

    def test_interplanar(self):

        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
        
        h0, k0, l0 = 1, 2, -3
        h1, k1, l1 = 2, -1, -4

        angle = crystal.interplanar(a, b, c, alpha, beta, gamma, \
                                    h0, k0, l0, h1, k1, l1)
        
        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants

        B = crystal.cartesian(a_, b_, c_, alpha_, beta_, gamma_)
        
        u_, v_, w_ = np.dot(B, [1,0,0]), np.dot(B, [0,1,0]), np.dot(B, [0,0,1])

        self.assertAlmostEqual(angle, np.arccos(np.dot(h0*u_+k0*v_+l0*w_, 
                                                       h1*u_+k1*v_+l1*w_)
                                      / np.linalg.norm(h0*u_+k0*v_+l0*w_)
                                      / np.linalg.norm(h1*u_+k1*v_+l1*w_)))
        
    def test_volume(self):
        
        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4

        V = crystal.volume(a, b, c, alpha, beta, gamma)
        
        A = crystal.cartesian(a, b, c, alpha, beta, gamma)

        u, v, w = np.dot(A, [1,0,0]), np.dot(A, [0,1,0]), np.dot(A, [0,0,1])
        
        self.assertAlmostEqual(V, np.dot(u, np.cross(v, w)))
        
    def test_reciprocal(self):
        
        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
        
        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants
        
        A = crystal.cartesian(a, b, c, alpha, beta, gamma)
        B = crystal.cartesian(a_, b_, c_, alpha_, beta_, gamma_)

        u, v, w = np.dot(A, [1,0,0]), np.dot(A, [0,1,0]), np.dot(A, [0,0,1])
        
        V = np.dot(u, np.cross(v, w))
        
        self.assertAlmostEqual(a_, np.linalg.norm(np.cross(v, w)/V))
        self.assertAlmostEqual(b_, np.linalg.norm(np.cross(w, u)/V))
        self.assertAlmostEqual(c_, np.linalg.norm(np.cross(u, v)/V))
        
        u_, v_, w_ = np.dot(B, [1,0,0]), np.dot(B, [0,1,0]), np.dot(B, [0,0,1])
        
        self.assertAlmostEqual(alpha_, np.arccos(np.dot(v_, w_)/
                                                 np.linalg.norm(v_)/
                                                 np.linalg.norm(w_)))
        self.assertAlmostEqual(beta_, np.arccos(np.dot(w_, u_)/
                                                 np.linalg.norm(w_)/
                                                 np.linalg.norm(u_)))
        self.assertAlmostEqual(gamma_, np.arccos(np.dot(u_, v_)/
                                                 np.linalg.norm(u_)/
                                                 np.linalg.norm(v_)))
    
    def test_metric(self):
        
        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
    
        G = crystal.metric(a, b, c, alpha, beta, gamma)

        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants
        
        G_ = crystal.metric(a_, b_, c_, alpha_, beta_, gamma_)
        
        np.testing.assert_array_almost_equal(np.eye(3), np.dot(G, G_))
        
    def test_cartesian(self):
        
        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
                        
        A = crystal.cartesian(a, b, c, alpha, beta, gamma)
        
        G = crystal.metric(a, b, c, alpha, beta, gamma)
        
        U = scipy.linalg.cholesky(G, lower=False)
        np.testing.assert_array_almost_equal(A, U)
        
        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants
        
        B = crystal.cartesian(a_, b_, c_, alpha_, beta_, gamma_)
        
        G_ = crystal.metric(a_, b_, c_, alpha_, beta_, gamma_)
        
        U_ = scipy.linalg.cholesky(G_, lower=False)
        np.testing.assert_array_almost_equal(B, U_)
        
    def test_cartesian_rotation(self):
        
        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
                        
        A = crystal.cartesian(a, b, c, alpha, beta, gamma)
                
        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants
        
        B = crystal.cartesian(a_, b_, c_, alpha_, beta_, gamma_)
                
        hkl = np.array([-3.3,1.1,2.5])
        uvw = np.array([4.2,-2.7,1.8])
        
        R = crystal.cartesian_rotation(a, b, c, alpha, beta, gamma)
        
        self.assertAlmostEqual(hkl.dot(uvw), A.dot(uvw).dot(R.dot(B.dot(hkl))))
        
    def test_cartesian_moment(self):
        
        a, b, c, alpha, beta, gamma = 5, 5, 7, np.pi/2, np.pi/2, 2*np.pi/3
                                
        C = crystal.cartesian_moment(a, b, c, alpha, beta, gamma)
                
        self.assertAlmostEqual(np.arccos(np.dot(C[:,0],C[:,1])), gamma)
        self.assertAlmostEqual(np.arccos(np.dot(C[:,1],C[:,2])), alpha)
        self.assertAlmostEqual(np.arccos(np.dot(C[:,2],C[:,0])), beta)
        
    def test_cartesian_displacement(self):
        
        a, b, c, alpha, beta, gamma = 5, 5, 7, np.pi/2, np.pi/2, 2*np.pi/3
                                
        D = crystal.cartesian_displacement(a, b, c, alpha, beta, gamma)
        
        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants

        U = np.array([[1,0.1,0.2],
                      [0.1,3,0.3],
                      [0.2,0.3,4]])
                 
        Up, _ = np.linalg.eig(np.dot(np.dot(D, U), D.T))
        Uiso = np.mean(Up).real
        
        Viso = (U[0,0]*(a*a_)**2+U[1,1]*(b*b_)**2+U[2,2]*(c*c_)**2+\
                2*U[0,1]*a*a_*b*b_*np.cos(gamma)+\
                2*U[0,2]*a*a_*c*c_*np.cos(beta)+\
                2*U[1,2]*b*b_*c*c_*np.cos(alpha))/3
            
        self.assertAlmostEqual(Uiso, Viso)
        
    def test_vector(self):

        a, b, c, alpha, beta, gamma = 5, 6, 7, np.pi/2, np.pi/3, np.pi/4
        
        inv_constants = crystal.reciprocal(a, b, c, alpha, beta, gamma)
        
        a_, b_, c_, alpha_, beta_, gamma_ = inv_constants
        
        B = crystal.cartesian(a_, b_, c_, alpha_, beta_, gamma_)
        
        h, k, l = -3, 1, 2
        
        Qh, Qk, Ql = crystal.vector(h, k, l, B)
    
        d = crystal.d(a, b, c, alpha, beta, gamma, h, k, l)
        
        Q = np.sqrt(Qh**2+Qk**2+Ql**2)
        
        self.assertAlmostEqual(d, 2*np.pi/Q)

    def test_transform(self):
        
        u, v, w = np.array([1,1,0]), np.array([-1,1,2]), np.array([2,-2,2])
        
        u = u/np.linalg.norm(u)
        v = v/np.linalg.norm(v)
        w = w/np.linalg.norm(w)
        
        R = np.stack((u,v,w)).T
        
        x = np.array([3.5, 4, -1.2])        
        y = crystal.transform(x[0], x[1], x[2], R)
        
        np.testing.assert_array_almost_equal(y, np.dot(R, x))
        
    def test_lattice(self):
        
        lat = crystal.lattice(5, 5, 5, np.pi/2, np.pi/2, np.pi/2)
        self.assertEqual(lat, 'Cubic')
        
        lat = crystal.lattice(5, 5, 7, np.pi/2, np.pi/2, 2*np.pi/3)
        self.assertEqual(lat, 'Hexagonal')
        
        lat = crystal.lattice(5, 5, 6, np.pi/2, np.pi/2, np.pi/2)
        self.assertEqual(lat, 'Tetragonal')
        
        lat = crystal.lattice(5, 6, 7, np.pi/2, np.pi/2, np.pi/2)
        self.assertEqual(lat, 'Orthorhombic')
        
        lat = crystal.lattice(5, 5, 5, np.pi/3, np.pi/3, np.pi/3)
        self.assertEqual(lat, 'Rhombohedral')
        
        lat = crystal.lattice(5, 6, 7, np.pi/2, np.pi/3, np.pi/2)
        self.assertEqual(lat, 'Monoclinic')
        
        lat = crystal.lattice(5, 6, 7, np.pi/2, np.pi/2, np.pi/3)
        self.assertEqual(lat, 'Monoclinic')
        
        lat = crystal.lattice(5, 6, 7, np.pi/2, np.pi/3, np.pi/4)
        self.assertEqual(lat, 'Triclinic')
        
if __name__ == '__main__':
    unittest.main()