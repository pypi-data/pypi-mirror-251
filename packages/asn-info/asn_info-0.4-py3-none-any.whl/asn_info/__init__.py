
import os
import re
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
        total=8,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

__version__ = "0.4"
__author__ = "Massimiliano Stucchi"
__author_email__ = "max@stucchi.ch"
__copyright__ = "Copyright 2023, Massimiliano Stucchi"
__license__ = "BSD"
__status__ = "Stable"
__url__ = "https://github.com/stucchimax/asn_info"

class Asns:
    def __init__(self):
        
        self.asns = {}

    def load_asn_data(self, add_manrs_data = False):

        url = "https://ftp.ripe.net/ripe/asnames/asn.txt"

        q = requests.Session()

        p = q.get(url, timeout=20)

        for line in p.iter_lines():
            split_line = line.decode().split(", ")
            
            try:
                country = split_line[1]
                split_line.pop(1)
            except:
                country = "ZZ"

            as_details = split_line[0].split()

            asn = int(as_details[0])
            
            as_details.pop(0)
            
            try:
                as_name = ' '.join(as_details)
            except:
                as_name = "None/Reserved"

            self.asns[asn] = {"country": country, "as_name": as_name}
        
        if add_manrs_data == True:
            self.manrs_data = True
            for asn in self.asns:
                # Some MANRS data from time to time comes in as empty,
                # so it's better to fill in all the ASNs as not being
                # MANRS participants, and then flip to True those who are.
                self.asns[asn]['manrs'] = False

            self.load_manrs_asn_data()
        else:
            self.manrs_data = False

    def load_manrs_asn_data(self):

        url = "https://api.manrs.org/asns/info"

        headers = {
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(os.getenv("MANRS_API_KEY"))
                }
        q = requests.Session()

        p = q.get(url, timeout=20, headers=headers)

        manrs_asns = p.json()
        
        for asn in manrs_asns['asns']:
            if asn['number'] in self.asns:
                self.asns[asn['number']]['manrs'] = asn['manrs']


    def get_as_name(self, asn):
        if asn in self.asns:
            return(self.asns[asn]["as_name"])
        else:
            return("Name not available")

    def get_as_country(self, asn):
        if asn in self.asns:
            return(self.asns[asn]["country"])
        else:
            return("ZZ")

    def is_manrs_participant(self, asn):
        if self.manrs_data == True:
            if asn in self.asns:
                return(self.asns[asn]["manrs"])
            else:
                return(False)
        else:
            return("No MANRS Data available")

    def asns_per_country(self, country):
        if re.match("^[A-Z]{2}$", country):
            output = {}
        
            for asn in self.asns:
                if self.asns[asn]['country'] == country:
                    output[asn] = self.asns[asn]
        
            return(output)
        else:
            raise Exception("Country should be in ISO 2-letter format, all uppercase")
