import os
import datetime
from rich.console import Console

console = Console()

def generate_h1_report():
    console.print("[bold cyan]Generating HackerOne Professional Report...[/bold cyan]")
    
    title = input("Enter Vulnerability Title (e.g., IDOR on api.oppo.com): ")
    severity = input("Severity (Low/Medium/High/Critical): ")
    url = input("Affected URL/Endpoint: ")
    
    report_content = f"""
# Report for OPPO Security Team
**Date:** {datetime.date.today()}
**Researcher:** Freddy28TM

## Summary:
[Briefly describe the bug. Example: I discovered an Insecure Direct Object Reference (IDOR) on the {url} endpoint that allows unauthorized access to user data.]

## Severity: {severity}
**Impact:** [Example: An attacker can view private order history/PII of other OPPO users by changing the 'uid' parameter.]

## Steps to Reproduce:
1. Navigate to `{url}`.
2. Intercept the request using Burp Suite.
3. Locate the parameter (e.g., `uid=10001`).
4. Change the value to a different user ID (e.g., `uid=10002`).
5. Observe that the server returns the private data of the other user.

## Proof of Concept (PoC):
```http
GET /api/v1/user/profile?uid=10002 HTTP/1.1
Host: api.oppo.com
Authorization: Bearer [REDACTED]
