"""
projekt_1.py: třetí projekt do Engeto Online Python Akademie
author: Anna Peloušková
email: a.pelouskova@seznam.cz
discord: Pel#9400
"""

import requests
from urllib.request import urlopen, urlparse, URLError
from volby_cz_tools import *
import csv
import sys


def combine_results(counter, increase):
    if counter == {}:
        return increase
    for key in counter.keys():
        if not key.isdigit() and counter[key].isdigit():
            counter[key] = str(int(counter[key]) + int(increase[key]))
        else:
            counter[key]["hlasy"] = str(
                int(counter[key]["hlasy"]) + int(increase[key]["hlasy"])
            )
    return counter


def generate_csv_header(election_results):
    header = ["code", "location", "registered", "envelopes", "valid"]
    for key in election_results.keys():
        if key.isdigit():
            header = header + [election_results[key]["jmeno"]]

    return header


def generate_csv_row(obec_details, election_results):
    row = [
        obec_details["code"],
        obec_details["location"],
        election_results["registered"],
        election_results["envelopes"],
        election_results["valid"],
    ]
    for key in election_results.keys():
        if key.isdigit():
            row = row + [election_results[key]["hlasy"]]

    return row


def main():
    if len(sys.argv) != 3:
        print("Zadej dva argumenty.")
        exit()

    verbose = True

    scraped_address = sys.argv[1]
    export_filename = sys.argv[2]

    try:
        parsed_address = urlparse(scraped_address)
        if parsed_address.scheme == "":
            raise URLError("Adresa neni validni")
        urlopen(scraped_address)
    except URLError:
        print(scraped_address, "neni validni adresa.")
        exit()

    f = open(export_filename, "w", encoding="utf-8")
    writer = csv.writer(f)
    header_written = False
    obce = []

    r = requests.get(scraped_address)
    html = r.content

    obce = parse_list_page(html)

    election_structure = []

    for obec in obce:
        election_row = {}
        election_row["code"] = obec["cislo"]
        election_row["location"] = obec["nazev"]

        r = requests.get(requests.compat.urljoin(scraped_address, obec["odkaz"]))
        html = r.content
        okrsek = is_okrsek_list_page(html)
        if okrsek:
            okrsky = parse_okrsek_list_page(html)
            election_results_counter = {}
            for okrsky_item in okrsky:
                r = requests.get(
                    requests.compat.urljoin(scraped_address, okrsky_item["odkaz"])
                )
                html = r.content
                election_results = parse_detail_page(html)
                election_results_counter = combine_results(
                    election_results_counter, election_results
                )
            election_results = election_results_counter
        else:
            election_results = parse_detail_page(html)

        if not header_written:
            header = generate_csv_header(election_results)
            if verbose:
                print(header)
            writer.writerow(header)
            header_written = True

        row = generate_csv_row(election_row, election_results)
        writer.writerow(row)
        if verbose:
            print(election_row, election_results)

    f.close()


if __name__ == "__main__":
    main()
