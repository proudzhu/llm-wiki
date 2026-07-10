#!/usr/bin/env python3
"""Step 1-2: Search Zotero and fetch paper metadata + PDF attachment key.

Subcommands:
  search <query>    Search Zotero by title/creator/year, print matches.
  metadata <key>    Fetch full metadata for an item + locate its PDF attachment.

Usage:
  python .agents/skills/paper-reader/scripts/zotero_fetch.py search "RT-Tango"
  python .agents/skills/paper-reader/scripts/zotero_fetch.py metadata 8ZWV2E4T

Requires Zotero running with "Allow other applications" enabled.
"""
import argparse, json, sys, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

ZOTERO_BASE = "http://localhost:23119/api/users/0/items"


def api_get(url):
    """GET a Zotero local API URL and return parsed JSON."""
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def fmt_authors(creators):
    """Format a Zotero creators list into 'First Last, First Last'."""
    names = []
    for c in creators or []:
        if c.get('name'):
            names.append(c['name'])
        elif c.get('firstName') and c.get('lastName'):
            names.append(f"{c['firstName']} {c['lastName']}")
        elif c.get('lastName'):
            names.append(c['lastName'])
    return ', '.join(names)


def cmd_search(args):
    params = urllib.parse.urlencode({
        'q': args.query,
        'qmode': 'titleCreatorYear',
        'limit': args.limit,
        'itemType': '-attachment',
    })
    items = api_get(f"{ZOTERO_BASE}?{params}")
    if not items:
        print("No matching items found.")
        return
    print(f"Found {len(items)} item(s):\n")
    for it in items:
        d = it.get('data', {})
        key = d.get('key', '?')
        title = d.get('title', '(no title)')
        authors = fmt_authors(d.get('creators'))
        year = d.get('date', '')[:4]
        item_type = d.get('itemType', '?')
        print(f"  [{key}] {title}")
        print(f"        Authors: {authors}")
        print(f"        Year: {year}  Type: {item_type}")
        if d.get('DOI'):
            print(f"        DOI: {d['DOI']}")
        print()


def cmd_metadata(args):
    item = api_get(f"{ZOTERO_BASE}/{args.key}")
    d = item.get('data', {})
    print("=== Item Metadata ===")
    print(f"Key:       {d.get('key', '?')}")
    print(f"Title:     {d.get('title', '(no title)')}")
    print(f"Authors:   {fmt_authors(d.get('creators'))}")
    print(f"Date:      {d.get('date', '?')}")
    print(f"Type:      {d.get('itemType', '?')}")
    if d.get('DOI'):
        print(f"DOI:       {d['DOI']}")
    if d.get('url'):
        print(f"URL:      {d['url']}")
    if d.get('abstractNote'):
        print(f"Abstract:  {d['abstractNote'][:200]}...")
    tags = [t.get('tag', '') for t in d.get('tags', []) if t.get('tag')]
    if tags:
        print(f"Tags:      {', '.join(tags)}")
    if d.get('publicationTitle'):
        print(f"Venue:     {d['publicationTitle']}")

    # Find PDF attachment
    children = api_get(f"{ZOTERO_BASE}/{args.key}/children")
    pdf_key = None
    print("\n=== Attachments ===")
    for ch in children:
        cd = ch.get('data', {})
        ct = cd.get('contentType', '')
        print(f"  [{cd.get('key')}] {cd.get('filename', '(no name)')}  ({ct})")
        if ct == 'application/pdf' and not pdf_key:
            pdf_key = cd.get('key')
    if pdf_key:
        print(f"\nPDF attachment key: {pdf_key}")
    else:
        print("\nNo PDF attachment found.")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)

    ps = sub.add_parser('search', help='Search Zotero by title/creator/year')
    ps.add_argument('query', help='Search terms')
    ps.add_argument('--limit', type=int, default=5, help='Max results (default 5)')
    ps.set_defaults(func=cmd_search)

    pm = sub.add_parser('metadata', help='Fetch full metadata for a Zotero key')
    pm.add_argument('key', help='Zotero item key (e.g. 8ZWV2E4T)')
    pm.set_defaults(func=cmd_metadata)

    args = p.parse_args()
    try:
        args.func(args)
    except urllib.error.URLError as e:
        print(f"ERROR: Cannot reach Zotero local API: {e}", file=sys.stderr)
        print("Is Zotero running with 'Allow other applications' enabled?",
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
