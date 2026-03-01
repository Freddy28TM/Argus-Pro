import dns.resolver

# Common fingerprints for 2026 services
FINGERPRINTS = {
    "github.io": "There isn't a GitHub Pages site here",
    "herokuapp.com": "herokuhosted.com",
    "s3.amazonaws.com": "The specified bucket does not exist",
    "azure": "404 Not Found"
}

def check_takeover(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            cname = str(rdata.target).lower()
            for provider, sig in FINGERPRINTS.items():
                if provider in cname:
                    return f"[bold red][!] Potential Takeover ({provider}): {subdomain} -> {cname}[/bold red]"
        return None
    except:
        return None
