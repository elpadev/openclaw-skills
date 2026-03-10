#!/usr/bin/env python3
import argparse
import json
import os
import sys

import resend


def main() -> int:
    parser = argparse.ArgumentParser(description="Send an email using Resend API")
    parser.add_argument("--api-key", help="Resend API key (or use RESEND_API_KEY env)")
    parser.add_argument("--from", dest="from_email", required=True, help="Sender email")
    parser.add_argument("--to", dest="to_email", required=True, help="Recipient email")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--html", help="HTML body")
    parser.add_argument("--text", help="Plain text body")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("RESEND_API_KEY")
    if not api_key:
        print("ERROR: missing API key. Set RESEND_API_KEY or pass --api-key", file=sys.stderr)
        return 2

    if not args.html and not args.text:
        print("ERROR: provide at least one of --html or --text", file=sys.stderr)
        return 2

    payload = {
        "from": args.from_email,
        "to": [args.to_email],
        "subject": args.subject,
    }
    if args.html:
        payload["html"] = args.html
    if args.text:
        payload["text"] = args.text

    resend.api_key = api_key

    try:
        response = resend.Emails.send(payload)
        print(json.dumps(response, ensure_ascii=False))
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
