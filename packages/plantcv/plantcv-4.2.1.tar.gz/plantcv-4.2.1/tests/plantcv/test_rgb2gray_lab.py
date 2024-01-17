import pytest
import cv2
from plantcv.plantcv import rgb2gray_lab


def test_rgb2gray_lab(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    gray_img = rgb2gray_lab(rgb_img=img, channel='b')
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert img.shape[:2] == gray_img.shape


def test_rgb2gray_lab_bad_input(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = rgb2gray_lab(rgb_img=img, channel="v")
