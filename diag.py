#!/usr/bin/python

import dns.resolver, dns.dnssec, time, requests, json

GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
END = '\033[m'

def print_text(text, color):
    if color == GREEN:
        print(color + "[✓] " + END + text, END)
    elif color == YELLOW:
        print(color + "[!] " + END + text, END)
    elif color == RED:
        print(color + "[X] " + END + text, END)
    else:
        print(RED + "[X] " + END + "Invalid Color", END)

def info(text):
    print(GREEN + "[I] " + END + text, END)

def process_request(domain, dnstype):
    try:
        query = dns.resolver.resolve(domain, dnstype)
        for value in query:
            return value.to_text().replace('"', '' , 2)
    
    except dns.resolver.NXDOMAIN:
        return 100

    except dns.resolver.Timeout:
        return 101

    except dns.resolver.NoAnswer:
        return 102

    except dns.resolver.NoNameservers:
        return 103

def service_test():
    if process_request("test.zerologdns.net", "TXT") == "Ok":
        print_text("The service is available", GREEN)
    elif process_request("test.zerologdns.net", "TXT") == 103:
        print_text("Server-side error [SERVERFAIL]", RED)
        print_text("If you have time, please report the problem to us", YELLOW)
        exit()
    elif process_request("test.zerologdns.net", "TXT") == 101:
        print_text("The service is unavailable. [Timeout]", RED)
        print_text("If you have time, please report the problem to us", YELLOW)
        exit()
    elif process_request("test.zerologdns.net", "TXT") == "No":
        print_text("This script only works if you are using ZeroLogDNS", YELLOW)
        exit()
    else:
        print_text("The server cannot find the domain.", RED)
        exit()

def which_version():
    if process_request("test.zerologdns.net", "TXT") == "Ok" and process_request("adtest.zerologdns.net", "A") != "37.221.197.124":
        print_text("You are using the uncensored version of ZeroLogDNS", GREEN)
    elif process_request("test.zerologdns.net", "TXT") == "Ok" and process_request("adtest.zerologdns.net", "A") == "37.221.197.124":
        print_text("You are using the censored version of ZeroLogDNS", GREEN)
        time.sleep(1)
        censored_test()

def censored_test():
    if process_request("blocked.zerologdns.net", "TXT") == 100:
        print_text("The filter is working.", GREEN)
    elif process_request("blocked.zerologdns.net", "TXT") == "No":
        print_text("The filtered domain is resolving. There is probably a DNS-Leak. Test it here: https://dnscheck.tools/#advanced", YELLOW)
    else:
        print_text("Unknown error", RED)

def dnssec_test():
    if process_request("servfail.sidnlabs.nl", "A") == 103:
        print_text("DNSSEC is working", GREEN)
    else:
        print_text("DNSSEC is not working", RED)

def get_status():
    if (requests.get('https://api.deta.zerologdns.net/dns/1').json()["DNS"] == "ok") and (requests.get('https://api.deta.zerologdns.net/dns/2').json()["DNS"] == "ok"):
        print_text("All servers are available!", GREEN)
    elif (requests.get('https://api.deta.zerologdns.net/dns/1').json()["DNS"] != "ok") or (requests.get('https://api.deta.zerologdns.net/dns/2').json()["DNS"] != "ok"):
        print_text("Only 1 server is available!", YELLOW)
    elif (requests.get('https://api.deta.zerologdns.net/dns/1').json()["DNS"] != "ok") and (requests.get('https://api.deta.zerologdns.net/dns/2').json()["DNS"] != "ok"):
         print_text("No server is available!", RED)
    else:
        print_text("Unknown error", RED)



def test():
    info("Running the diagnostic test.\n")
    service_test()
    time.sleep(1)
    which_version()
    time.sleep(1)
    dnssec_test()
    time.sleep(1)
    get_status()
    time.sleep(1)
    print_text("Done", GREEN)


test()
