"""
Unit tests for preprocessing utilities.
"""

from src.common.preprocessing import CATEGORIES, split_images


def test_categories_include_expected_mvtec_category():
    assert "bottle" in CATEGORIES


def test_split_images_returns_three_splits():
    images = list(range(100))

    train, validation, test = split_images(images)

    assert len(train) == 70
    assert len(validation) == 15
    assert len(test) == 15
