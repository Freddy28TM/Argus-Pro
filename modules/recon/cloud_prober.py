import requests

def probe_cloud_signatures(ip):
    # Cloudflare check
    headers = requests.get(f"http://{ip}", timeout=3).headers
    if "CF-RAY" in headers or "server" in headers and "cloudflare" in headers.lower():
        return "CLOUDFLARE_DETECTED"
    
    # AWS Check (Using IP ranges or specific headers)
    if "x-amz-id-2" in headers:
        return "AWS_DETECTED"
    
    # Oracle Cloud (OCI) check
    if "opc-request-id" in headers:
        return "ORACLE_DETECTED"
    
    return "GENERIC_TARGET"
