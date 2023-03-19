import time, requests, json
import dnslocal

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

def service_test():
    if dnslocal.process_request("t.zerologdns.net", "TXT") == "yes":
        print_text("The service is available", GREEN)
    elif dnslocal.process_request("t.zerologdns.net", "TXT") == 103:
        print_text("Server-side error [SERVERFAIL]", RED)
        print_text("If you have time, please report the problem to us", YELLOW)
        exit()
    elif dnslocal.process_request("t.zerologdns.net", "TXT") == 101:
        print_text("The service is unavailable. [Timeout]", RED)
        print_text("If you have time, please report the problem to us", YELLOW)
        exit()
    elif dnslocal.process_request("t.zerologdns.net", "TXT") == "no":
        print_text("This script only works if you are using ZeroLogDNS", YELLOW)
        exit()
    else:
        print_text("The server cannot find the domain.", RED)
        exit()

def which_version():
    if dnslocal.process_request("t.zerologdns.net", "TXT") == "yes" and dnslocal.process_request("ad-test.zerologdns.net", "TXT") == "ok":
        print_text("You are using the uncensored version of ZeroLogDNS", GREEN)
    elif dnslocal.process_request("t.zerologdns.net", "TXT") == "yes" and dnslocal.process_request("ad-test.zerologdns.net", "TXT") == 100 :
        print_text("You are using the censored version of ZeroLogDNS", GREEN)
        time.sleep(1)
    else:
        print_text("Unknown error", RED)

def dnssec_test():
    if dnslocal.process_request("servfail.sidnlabs.nl", "A") == 103:
        print_text("DNSSEC is working", GREEN)
    else:
        print_text("DNSSEC is not working", RED)


def test():
    info("Running the diagnostic test.\n")
    service_test()
    time.sleep(1)
    which_version()
    time.sleep(1)
    dnssec_test()
    time.sleep(1)
    print_text("Done", GREEN)

if __name__ == "__main__":
    test()