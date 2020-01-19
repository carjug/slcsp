#!/usr/bin/env python3

import csv
from os import path


PLANS_CSV = path.join(path.dirname(path.abspath(__file__)), "./plans.csv")
ZIPS_CSV = path.join(path.dirname(path.abspath(__file__)), "./zips.csv")
SLCSP_CSV = path.join(path.dirname(path.abspath(__file__)), "./slcsp.csv")


def main():
    """
    Outer function responsible for executing the subsequent
    loading and processing functions
    """
    silver_plans = get_silver_plans_from_file()
    zip_rate_areas = get_zips_rate_areas()
    get_slcsp_by_zip(silver_plans, zip_rate_areas)


def get_silver_plans_from_file():
    """
    Loads all silver plans from csv and returns
    a dict of dicts mapping a state and rate area
    to a set of rates

    :return: dict

    e.g.
    {"CA":
        {11:
            {345.51, 375.66}
        }
    }
    """
    silver_plans = {}
    with open(PLANS_CSV) as plans_csv:
        plans_reader = csv.DictReader(plans_csv)
        for row in plans_reader:
            if row["metal_level"] == "Silver":
                if not silver_plans.get(row["state"]):
                    silver_plans[row["state"]] = {row["rate_area"]: set()}
                elif not silver_plans[row["state"]].get(row["rate_area"]):
                    silver_plans[row["state"]][row["rate_area"]] = set()

                silver_plans[row["state"]][row["rate_area"]].add(row["rate"])
        return silver_plans


def get_zips_rate_areas():
    """
    Loads the ZIPS csv and constructs the data into
    a dict of sets with each key being a zipcode
    and each set containing tuples of associated
    rate areas for the zipcode

    :return: dict
    e.g.
    {90026:
        {(CA,1), (CA,4), (CA,7)}
    }
    """
    zip_rate_areas = {}
    with open(ZIPS_CSV) as csvfile:
        zip_reader = csv.DictReader(csvfile)
        for row in zip_reader:
            if not zip_rate_areas.get(row["zipcode"]):
                zip_rate_areas[row["zipcode"]] = set()
            zip_rate_areas[row["zipcode"]].add(
                (row["state"], row["rate_area"]))
    return zip_rate_areas


def get_slcsp_by_zip(silver_plans, zip_rate_areas):
    """
    Loads SLCSP csv and gets the associated data
    for each zipcode therein and prints the results
    to stdout

    :param silver_plans:
    :param zip_rate_areas:
    """
    print("zipcode,rate")
    with open(SLCSP_CSV) as slcsp_file:
        slcsp_reader = csv.DictReader(slcsp_file)
        for row in slcsp_reader:
            zipcode = row["zipcode"]
            rate_areas_for_zip = zip_rate_areas.get(zipcode)
            slcsp_rate = get_rate_for_zip(rate_areas_for_zip, silver_plans)
            print(f"{zipcode},{slcsp_rate}")


def get_rate_for_zip(rate_areas_for_zip, silver_plans):
    """
    Helper function to get slcsp rate from all the silver plans
    associated with the passed in rate area

    Returns empty string if there is more than one rate area in the
    rate_areas_for_zip set

    :param rate_areas_for_zip: set of rate area tuples
    :param silver_plans: dict of dicts
    :return: String - empty or formatted rate

    e.g. "234.50"
    """
    slcsp_rate = ""
    # if zip has more than one rate area it is ambiguous
    # and should not be processed
    if len(rate_areas_for_zip) == 1:
        rate_area_tuple = rate_areas_for_zip.pop()
        rates = silver_plans.get(rate_area_tuple[0], {}).get(rate_area_tuple[1])
        if rates and len(rates) >= 2:
            sorted_rates = sorted(rates)
            # get the second lowest rate and format it
            slcsp_rate = "{0:.2f}".format(float(sorted_rates[1]))
    return slcsp_rate


if __name__ == "__main__":
    main()
