import argparse
import sys
from .engine import StealthEngine
from .parsers import ShopifyAuditor

def main():
    parser = argparse.ArgumentParser(
        description="⚡ Stealth E-Com Radar CLI - Global Cross-Border Intelligence"
    )
    parser.add_argument("--url", "-u", type=str, required=True, help="Target store URL or endpoints")
    parser.add_argument("--shopify", action="store_true", help="Audit Shopify store inventory and products")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout in seconds")

    args = parser.parse_args()

    print(f"[*] Initializing Stealth E-Com Radar v1.2.0 ...")
    print(f"[*] Target URL: {args.url}")
    
    engine = StealthEngine(timeout=args.timeout)
    resp = engine.fetch(args.url)
    
    print(f"[+] Status: {resp.status_code} | Latency: {resp.elapsed_ms}ms")
    print(f"[+] Anti-Bot Challenge: {'Passed (Silent)' if not resp.is_cloudflare_challenged else 'Challenged'}")
    print(f"[✓] Intelligence pipeline execution completed successfully.")

if __name__ == "__main__":
    main()
