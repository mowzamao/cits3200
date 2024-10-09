import unittest

import os
import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot
from unittest.mock import patch

import ImageTransforming as it
import ProcessSedimentCore as psc

class TestProcessSedimentCore(unittest.TestCase):
    def test_Scaling(self):
        scaler = psc.Scaling(core_width_in_mm=100)
        self.assertEqual(scaler.get_mm_scale(100), 1.0)
        self.assertEqual(scaler.get_core_length([0, 0, 100, 100]), 100)
    
    def test_ExtractCore(self):
        cwd = os.getcwd()
        img = it.import_image(f'{cwd}/app/utils/image-data/MI-24_03/SCREEN banner 96dpi-3148.jpg')
        core = psc.ExtractCore(img, 10)
        self.assertEqual(core.find_cores(), [[9, 484, 1902, 215], [412, 282, 1072, 141]])
        self.assertEqual(core.get_largest_core([[9, 484, 1902, 215], [412, 282, 1072, 141]]), [9, 484, 1902, 215])
        self.assertEqual(core.get_bounding_box(), [9, 484, 1902, 215])
        self.assertEqual(core.extract_core(from_bounding_box=True, bounding_box=None), 0)

    def test_Colours(self):
        img = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255]],
                        [[255, 0, 255], [128, 128, 0], [0, 128, 128], [128, 0, 128], [64, 64, 64]],
                        [[255, 128, 0], [0, 128, 255], [128, 0, 255], [255, 0, 128], [0, 255, 128]],
                        [[128, 255, 0], [128, 128, 128], [64, 128, 255], [255, 64, 128], [128, 64, 255]],
                        [[255, 255, 255], [0, 0, 0], [128, 255, 128], [255, 128, 64], [64, 255, 128]]], dtype=np.uint8)
        colours = psc.Colours(image = img, scale=1.)
        self.assertEqual(colours.get_weights().all(), np.array([0, 1, 2, 1, 0]).all())

class TestImageFunctions(unittest.TestCase):

    @patch('cv2.imread')
    def test_import_image(self, mock_imread):
        mock_image = np.ones((100, 100, 3), dtype=np.uint8)
        mock_imread.return_value = mock_image

        image = it.import_image('fake_path.jpg')
        self.assertIsNotNone(image)
        self.assertEqual(image.shape, (100, 100, 3))

        mock_imread.return_value = None
        with self.assertRaises(AssertionError):
            it.import_image('invalid_path.jpg')

    @patch('matplotlib.pyplot.show')
    def test_show_image(self, mock_show):
        mock_image = np.ones((100, 100, 3), dtype=np.uint8)
        it.show_image(mock_image)
        mock_show.assert_called_once()

    def test_remove_greys(self):
        image = np.array([[[100, 100, 100], [255, 255, 255]], 
                          [[0, 0, 255], [255, 0, 0]]], dtype=np.uint8)

        result = it.remove_greys(image)
        self.assertEqual(result.shape, image.shape)
        self.assertTrue(np.all(result[0, 0] == [0, 0, 0]))
        self.assertTrue(np.all(result[0, 1] == [0, 0, 0]))

    def test_get_contours(self):
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv.rectangle(image, (25, 25), (75, 75), (255, 255, 255), -1)

        contours = it.get_contours(image)
        self.assertTrue(len(contours) > 0)

    def test_crop_image(self):
        image = np.ones((100, 100, 3), dtype=np.uint8)
        cropped = it.crop_image(image, [10, 10, 50, 50])
        self.assertEqual(cropped.shape, (50, 50, 3))
        self.assertEqual(it.crop_image(image).shape, image.shape)

    def test_scale_rgb_values(self):
        image = np.array([[[255, 0, 0]], 
                          [[0, 255, 0]], 
                          [[0, 0, 255]]], dtype=np.float64)
        scaled_image = it.scale_rgb_values(image)
        self.assertTrue(np.all(scaled_image <= 1.))
        self.assertTrue(np.all(scaled_image >= 0.))

    def test_unscale_rgb_values(self):
        scaled_image = np.array([[[1.0, 0.0, 0.0]], 
                                 [[0.0, 1.0, 0.0]], 
                                 [[0.0, 0.0, 1.0]]], dtype=np.float32)
        unscaled_image = it.unscale_rgb_values(scaled_image)
        self.assertTrue(np.all(unscaled_image <= 255))
        self.assertTrue(np.all(unscaled_image >= 0))

    def test_reshape_image_to_df(self):
        image = np.array([[[255, 0, 0]], 
                          [[0, 255, 0]], 
                          [[0, 0, 255]]], dtype=np.uint8)
        result = it.reshape_image_to_df(image, 'BGR')
        self.assertTrue('Blue' in result.columns)
        self.assertTrue('Green' in result.columns)
        self.assertTrue('Red' in result.columns)
        self.assertEqual(len(result), 3) 

    def test_flip(self):
        df = pd.DataFrame({
            'Depth (mm)': [0, 10, 20],
            'Blue': [255, 0, 0],
            'Green': [0, 255, 0],
            'Red': [0, 0, 255]
        })
        flipped = it.flip(df)
        self.assertTrue('Flipped Depth (mm)' in flipped.columns)
        self.assertTrue(flipped['Flipped Depth (mm)'].iloc[0] > flipped['Flipped Depth (mm)'].iloc[-1])

    def test_orient_array(self):
        horizontal_array = np.ones((50, 100, 3), dtype=np.uint8)
        oriented = it.orient_array(horizontal_array)
        self.assertEqual(oriented.shape, (100, 50, 3))

        vertical_array = np.ones((100, 50, 3), dtype=np.uint8)
        self.assertTrue(np.array_equal(it.orient_array(vertical_array), vertical_array))

if __name__ == '__main__':
    unittest.main()