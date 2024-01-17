"""
HTTP Health Checker
A program to check the health of a set of HTTP endpoints fed in from a yaml file
"""
import time
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta
from urllib.parse import urlparse

import requests
import typer
import yaml


app = typer.Typer()


ENDPOINTS = []
DOMAINS = []


def get_file():
    """Prompts user to select a file with a file dialog"""
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    return file


def parse_endpoints_from_file():
    """Creates endpoint entries from passed-in file"""
    yaml_file = get_file()
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.full_load(file)
        for row in data:
            endpoint = {
                'headers': row.get('headers'),
                'method': row.get('method'),
                'name': row.get('name'),
                'url': row.get('url'),
                'body': row.get('body')
            }
            ENDPOINTS.append(endpoint)


def extract_domains():
    """Creates a set of unique domains"""
    endpoints = ENDPOINTS
    domain_set = set()
    for endpoint in endpoints:
        url = endpoint.get('url')
        domain = urlparse(url).netloc
        domain_set.add(domain)
    return domain_set


def sort_domains(the_set):
    """Sorting domains for consistent output"""
    return sorted(the_set)


def transform_domain_set_to_dict():
    """Transforms set into dictionary"""
    domain_set = extract_domains()
    sorted_domains = sort_domains(domain_set)
    for domain in sorted_domains:
        element = {
            'name': domain,
            'up_count': 0,
            'down_count': 0
        }
        DOMAINS.append(element)


def calculate_domain_availability():
    """Caculates the availability of the domains"""
    domains = DOMAINS
    for domain in domains:
        domain_name = domain.get('name')
        up_count = domain.get('up_count')
        down_count = domain.get('down_count')
        total_count = up_count + down_count
        domain_availability = round(100 * (up_count/total_count))
        print(f'{domain_name} has {domain_availability}% availability percentage')


def build_payload(endpoint):
    """Builds the payload from endpoint data"""
    header_data = endpoint.get('headers')
    body_data = endpoint.get('body')
    payload = {
        'headers': header_data,
        'body': body_data
    }
    return payload


def set_request_structure(endpoint):
    """Sets the request structure for the endpoint response"""
    url = endpoint.get('url')
    method = endpoint.get('method')
    payload = build_payload(endpoint)
    default_get_request = requests.get(url, params=payload, timeout=10)
    http_methods = {
        'GET': requests.get(url, params=payload, timeout=10),
        'POST': requests.post(url, data=payload, timeout=10),
        'PUT': requests.put(url, data=payload, timeout=10),
        'PATCH': requests.patch(url, data=payload, timeout=10),
        'HEAD': requests.head(url, timeout=10)
    }
    response = http_methods.get(method, default_get_request)
    return response


def increase_domain_up_count(url_domain):
    """Increase the domain's up count by 1"""
    domains = DOMAINS
    for domain in domains:
        if domain['name'] == url_domain:
            domain['up_count'] += 1


def increase_domain_down_count(url_domain):
    """Increase the doamin's down count by 1"""
    domains = DOMAINS
    for domain in domains:
        if domain['name'] == url_domain:
            domain['down_count'] += 1


def return_endpoint_status():
    """Returns endpoint status"""
    endpoints = ENDPOINTS
    for endpoint in endpoints:
        response = set_request_structure(endpoint)
        url = endpoint.get('url')
        url_domain = urlparse(url).netloc
        if response.status_code and response.elapsed < timedelta(microseconds=500000):
            increase_domain_up_count(url_domain)
        else:
            increase_domain_down_count(url_domain)
    calculate_domain_availability()

@app.command()
def run_program():
    """Runs program on a loop"""
    parse_endpoints_from_file()
    transform_domain_set_to_dict()
    i = 0
    while True:
        i += 1
        print(f'Test cycle #{i}')
        return_endpoint_status()
        time.sleep(15)


@app.command()
def rick():
    """
    Do not run this command
    """
    typer.echo('♪ Never Gonna Give You Up ♪')


if __name__ == "__main__":
    app()
