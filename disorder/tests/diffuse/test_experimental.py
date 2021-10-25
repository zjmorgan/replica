#!/usr/bin/env python3

import unittest
import numpy as np

from disorder.diffuse import experimental

import os
directory = os.path.dirname(os.path.abspath(__file__))     

class test_experimental(unittest.TestCase):
    
    def test_data(self):
        
        folder = os.path.abspath(os.path.join(directory, '..', 'data'))
        
        np.random.seed(13)
        
        signal, sigma_sq, \
        h_range, k_range, l_range, \
        nh, nk, nl = experimental.data(os.path.join(folder, 'test.nxs'))
        
        self.assertEqual(nh, 13)
        self.assertEqual(nk, 7)
        self.assertEqual(nl, 26)
                
        self.assertEqual(h_range, [-4,2])
        self.assertEqual(k_range, [-2,4])
        self.assertEqual(l_range, [-3,3])
        
        shape = (13,7,26)
        np.testing.assert_array_almost_equal(signal, np.random.random(shape))
        np.testing.assert_array_almost_equal(sigma_sq, np.random.random(shape))
        
    def test_mask(self):
        
        np.random.seed(13)
        
        signal = 1000*np.random.random((10,11,12))
        error_sq = np.sqrt(signal)
        
        signal[1,2,3] = np.nan
        signal[2,3,4] = np.inf
        signal[4,5,6] = -1
        
        error_sq[2,3,4] = np.nan
        error_sq[3,4,5] = -1
        
        mask = experimental.mask(signal, error_sq)
        
        self.assertTrue((signal[~mask] > 0).all())
        self.assertTrue((error_sq[~mask] > 0).all())
        
    # def test_rebin(self):
        
    #     x, y, z = np.meshgrid(np.arange(6), 
    #                           np.arange(14), 
    #                           np.arange(10), indexing='ij')
        
    #     data = 0.5*x+2.5*y-z
        
    #     tmp_data = experimental.rebin(data, [6,14,10])
    #     np.testing.assert_array_almost_equal(tmp_data, data)
        
    #     tmp_data = experimental.rebin(data, [3,14,10])
    #     np.testing.assert_array_almost_equal(np.sum(tmp_data, axis=0)*2, 
    #                                          np.sum(data, axis=0))
        
    #     tmp_data = experimental.rebin(data, [6,14,5])
    #     np.testing.assert_array_almost_equal(np.sum(tmp_data, axis=2)*2, 
    #                                          np.sum(data, axis=2))
    
    def test_weights(self):
        
        weight = experimental.weights(4, 2)
        np.testing.assert_array_almost_equal(weight.sum(axis=0), 0.5)
        np.testing.assert_array_almost_equal(weight.sum(axis=1), 1.0)
            
        weight = experimental.weights(10, 2)
        np.testing.assert_array_almost_equal(weight.sum(axis=0), 0.2)
        np.testing.assert_array_almost_equal(weight.sum(axis=1), 1.0)
        
        weight = experimental.weights(5, 3)
        np.testing.assert_array_almost_equal(weight.sum(axis=0), 0.6)
        np.testing.assert_array_almost_equal(weight.sum(axis=1), 1.0)
        
    def test_factors(self):
        
        fact = np.array([1, 2, 5, 10])
        np.testing.assert_array_equal(experimental.factors(10), fact)
        
        fact = np.array([1, 11])
        np.testing.assert_array_equal(experimental.factors(11), fact)
        
        fact = np.array([1, 5, 25])
        np.testing.assert_array_equal(experimental.factors(25), fact)

    def test_reflections(self):
        
        cntr = 'P'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 5, 3, centering=cntr), 1)
        self.assertEqual(experimental.reflections(4, 2, 6, centering=cntr), 1)
        
        cntr = 'I'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 5, 3, centering=cntr), 0)
        self.assertEqual(experimental.reflections(4, 2, 6, centering=cntr), 1)

        cntr = 'F'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 0)
        self.assertEqual(experimental.reflections(1, 5, 3, centering=cntr), 1)
        self.assertEqual(experimental.reflections(4, 2, 6, centering=cntr), 1)

        cntr = 'A'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 0)
        self.assertEqual(experimental.reflections(2, 5, 3, centering=cntr), 1)
        self.assertEqual(experimental.reflections(3, 2, 6, centering=cntr), 1)

        cntr = 'B'
        self.assertEqual(experimental.reflections(3, 1, 2, centering=cntr), 0)
        self.assertEqual(experimental.reflections(3, 2, 5, centering=cntr), 1)
        self.assertEqual(experimental.reflections(6, 3, 2, centering=cntr), 1)

        cntr = 'C'
        self.assertEqual(experimental.reflections(2, 3, 1, centering=cntr), 0)
        self.assertEqual(experimental.reflections(5, 3, 2, centering=cntr), 1)
        self.assertEqual(experimental.reflections(2, 6, 3, centering=cntr), 1)
        
        cntr = 'R (hexagonal axes, triple obverse cell)'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 0)
        self.assertEqual(experimental.reflections(1, 2, 2, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 2, 5, centering=cntr), 1)
        
        cntr = 'R (hexagonal axes, triple reverse cell)'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 0)
        self.assertEqual(experimental.reflections(1, 2, 4, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 2, 5, centering=cntr), 0)
        
        cntr = 'H (hexagonal axes, triple hexagonal cell)'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 0)
        self.assertEqual(experimental.reflections(1, 4, 4, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 4, 5, centering=cntr), 1)
        
        cntr = 'D (rhombohedral axes, triple rhombohedral cell)'
        self.assertEqual(experimental.reflections(1, 2, 3, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 4, 4, centering=cntr), 1)
        self.assertEqual(experimental.reflections(1, 4, 5, centering=cntr), 0)
                
if __name__ == '__main__':
    unittest.main()