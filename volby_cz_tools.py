"""
projekt_1.py: třetí projekt do Engeto Online Python Akademie
author: Anna Peloušková
email: a.pelouskova@seznam.cz
discord: Pel#9400
"""

from bs4 import BeautifulSoup


def is_okrsek_list_page(html):
    parsed_html = BeautifulSoup(html, features="html.parser")
    table = parsed_html.body.find("th", attrs={"id": "s1"})
    if table is None or table.text != "Okrsek":
        return False
    return True


def is_detail_page(html):
    parsed_html = BeautifulSoup(html, features="html.parser")
    scraped_registered = parsed_html.body.find("td", attrs={"headers": "sa2"})
    if scraped_registered:
        return True
    return False


def parse_detail_page(html):
    result_set = {}
    parsed_html = BeautifulSoup(html, features="html.parser")
    scraped_registered = parsed_html.body.find("td", attrs={"headers": "sa2"})
    if scraped_registered:
        result_set["registered"] = scraped_registered.text.replace("\xa0", "")
    scraped_envelopes = parsed_html.body.find("td", attrs={"headers": "sa3"})
    if scraped_envelopes:
        result_set["envelopes"] = scraped_envelopes.text.replace("\xa0", "")
    scraped_valid = parsed_html.body.find("td", attrs={"headers": "sa6"})
    if scraped_valid:
        result_set["valid"] = scraped_valid.text.replace("\xa0", "")

    tables = parsed_html.body.find_all("table", {"class": "table"})

    election_results = tables[1].find_all("tr")
    for party in election_results:
        votes = {}
        cislo = party.find("td", attrs={"class": "cislo", "headers": "t1sa1 t1sb1"})
        if not cislo:
            continue
        jmeno = party.find("td", attrs={"class": "overflow_name"})
        num_votes = party.find("td", attrs={"class": "cislo", "headers": "t1sa2 t1sb3"})
        votes["jmeno"] = jmeno.text
        votes["hlasy"] = num_votes.text
        result_set[cislo.text] = votes

    election_results = tables[2].find_all("tr")
    for party in election_results:
        votes = {}
        cislo = party.find("td", attrs={"class": "cislo", "headers": "t2sa1 t2sb1"})
        if not cislo:
            continue
        jmeno = party.find("td", attrs={"class": "overflow_name"})
        num_votes = party.find("td", attrs={"class": "cislo", "headers": "t2sa2 t2sb3"})
        votes["jmeno"] = jmeno.text
        votes["hlasy"] = num_votes.text
        result_set[cislo.text] = votes

    return result_set


def parse_list_page(html):
    result_set = []
    parsed_html = BeautifulSoup(html, features="html.parser")

    multiple_tables = parsed_html.body.findAll("table", attrs={"class": "table"})
    for table in multiple_tables:
        parsed_obce = table.findAll("tr")
        for parsed_obec in parsed_obce:
            cislo = parsed_obec.find("td", attrs={"class": "cislo"})
            nazev_obce = parsed_obec.find("td", attrs={"class": "overflow_name"})
            detail = parsed_obec.find("td", attrs={"class": "center"})
            if detail:
                obec = {}
                obec["nazev"] = nazev_obce.text
                obec["cislo"] = cislo.text
                obec["odkaz"] = detail.a["href"]
                result_set.append(obec)

    return result_set


def parse_okrsek_list_page(html):
    result_set = []
    parsed_html = BeautifulSoup(html, features="html.parser")

    table = parsed_html.body.find("table", attrs={"class": "table"})
    details = table.findAll("td", attrs={"class": "cislo"})

    for detail in details:
        obec = {}
        obec["odkaz"] = detail.a["href"]
        result_set.append(obec)

    return result_set
