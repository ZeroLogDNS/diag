import dns.resolver, dns.dnssec

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