import unittest
from slcsp_processor import get_silver_plans_from_file, get_zips_rate_areas, get_rate_for_zip


class TestSLCSPReader(unittest.TestCase):

    def test_get_silver_plans_from_file_state_with_silver_plans(self):
        """Test get_silver_plans_from_file and spot check output"""
        silver_plans = get_silver_plans_from_file()
        self.assertTrue(silver_plans.get("VA"))
        self.assertEqual(len(silver_plans["VA"]["3"]), 11)

        self.assertTrue(silver_plans.get("WV"))
        self.assertEqual(len(silver_plans["WV"]["9"]), 4)

    def test_get_zips_rate_areas(self):
        """Test get_zips_rate_areas and validate
            length and data types of zipcode keys' values"""
        zip_rate_areas = get_zips_rate_areas()
        self.assertEqual(len(zip_rate_areas["15935"]), 1)
        self.assertEqual(len(zip_rate_areas["53181"]), 1)
        self.assertEqual(type(zip_rate_areas["53181"]), set)
        self.assertEqual(type(zip_rate_areas["53181"].pop()), tuple)

    def test_get_zips_rate_areas_multiple_rate_areas(self):
        """Test get_zips_rate_areas and validate that some zips
            have more than one rate area tuple"""
        zip_rate_areas = get_zips_rate_areas()
        self.assertEqual(len(zip_rate_areas["63359"]), 3)
        self.assertEqual(len(zip_rate_areas["48418"]), 2)

    def test_get_rate_for_zip(self):
        """Test get_rate_for_zip"""
        silver_plans = get_silver_plans_from_file()
        zip_rate_areas = get_zips_rate_areas()
        rate_areas_for_zip = zip_rate_areas["38849"]
        self.assertEqual(len(rate_areas_for_zip), 1)

        rate = get_rate_for_zip(rate_areas_for_zip, silver_plans)
        self.assertEqual(rate, "285.69")

    def test_get_rate_for_zip_ambiguous_rate_areas(self):
        """Test get_rate_for_zip with a set of rate areas greater
            than one"""
        silver_plans = get_silver_plans_from_file()
        zip_rate_areas = get_zips_rate_areas()
        ambiguous_rate_areas = zip_rate_areas["63359"]
        self.assertEqual(len(ambiguous_rate_areas), 3)

        ambiguous_rate = get_rate_for_zip(ambiguous_rate_areas, silver_plans)
        self.assertEqual(ambiguous_rate, "")
