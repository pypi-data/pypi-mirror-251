import unittest
from unittest.mock import MagicMock, patch

import pytest
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

from src.auto_feature_engineering.feature_generator import generate_features


class TestFeatureGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.appName("TestFeatureGenerator").getOrCreate()

    @patch("src.auto_feature_engineering.feature_generator.generate_date_features")
    @patch(
        "src.auto_feature_engineering.feature_generator.generate_categorical_features"
    )
    @patch("src.auto_feature_engineering.feature_generator.generate_numerical_features")
    def test_generate_features(self, mock_num, mock_cat, mock_date):
        # Create a sample DataFrame
        data = [
            ("1", "a", "2020-01-01"),
            ("2", "b", "2020-02-01"),
            ("3", "c", "2020-03-01"),
        ]
        df = self.spark.createDataFrame(data, ["A", "B", "C"])

        # Create a sample yaml_data dictionary
        yaml_data = {
            "date_variables": ["C"],
            "categorical_variables": ["B"],
            "numerical_variables": ["A"],
        }

        # Each mock should return the DataFrame unchanged
        mock_date.return_value = df
        mock_cat.return_value = df
        mock_num.return_value = df

        # Call the function
        result_df = generate_features(df, yaml_data)

        # Assert that the result is as expected
        self.assertEqual(result_df, df)


if __name__ == "__main__":
    unittest.main()
