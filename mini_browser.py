"""
Very small terminal web browser using only Python standard library.
- Fetches pages with urllib.request
- Parses <title> and <a href> links with html.parser
- Shows list of links; type number to follow
- Commands: number, b (back), r (reload), q (quit), or full URL
"""

import sys
import urllib.request
import urllib.parse
from html.parser import HTMLParser


class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base = base_url
        self.links = []  # list of (href, text)
        self.in_a = False
        self.current_href = None
        self.current_text = []
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            href = None
            for k, v in attrs:
                if k.lower() == 'href':
                    href = v
                    break
            if href:
                # Resolve relative URLs
                href = urllib.parse.urljoin(self.base, href)
                self.in_a = True
                self.current_href = href
                self.current_text = []
        elif tag.lower() == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == 'a' and self.in_a and self.current_href:
            text = ''.join(self.current_text).strip() or self.current_href
            self.links.append((self.current_href, text))
            self.in_a = False
            self.current_href = None
            self.current_text = []
        elif tag.lower() == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self.in_a:
            self.current_text.append(data)
        if self._in_title:
            self.title = (self.title or '') + data


def fetch_url(url, timeout=10):
    req = urllib.request.Request(url, headers={'User-Agent': 'MiniBrowser/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        content = resp.read().decode(charset, errors='replace')
        final_url = resp.geturl()
    return final_url, content


def show_page(url, content, parser: LinkParser, max_links=30):
    print('\n' + '=' * 80)
    print('URL:', url)
    title = (parser.title or '').strip()
    if title:
        print('Title:', title)
    print('Links (first', min(len(parser.links), max_links), 'shown):')
    for i, (href, text) in enumerate(parser.links[:max_links], start=1):
        print(f'  {i}. {text} -> {href}')
    if len(parser.links) > max_links:
        print(f'  ... ({len(parser.links)-max_links} more links)')
    print('=' * 80)


def run(start_url=None):
    history = []  # stack of (url, content, parser)
    current = None

    if not start_url:
        start_url = 'https://example.com'

    def load(url):
        try:
            print('\nLoading', url)
            final, content = fetch_url(url)
            parser = LinkParser(final)
            parser.feed(content)
            parser.close()
            return (final, content, parser)
        except Exception as e:
            print('Error loading', url, '-', e)
            return None

    current = load(start_url)
    if not current:
        return

    while True:
        url, content, parser = current
        show_page(url, content, parser)
        cmd = input("Enter link number, full URL, 'b' back, 'r' reload, or 'q' quit: ").strip()
        if not cmd:
            continue
        if cmd.lower() == 'q':
            print('Goodbye')
            break
        if cmd.lower() == 'b':
            if history:
                current = history.pop()
            else:
                print('No history')
            continue
        if cmd.lower() == 'r':
            # reload
            new = load(url)
            if new:
                current = new
            continue
        # number -> follow link
        if cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(parser.links):
                href = parser.links[idx][0]
                history.append(current)
                new = load(href)
                if new:
                    current = new
                else:
                    # pop back if failed
                    current = history.pop() if history else current
            else:
                print('Invalid link number')
            continue
        # otherwise treat as URL
        if not cmd.startswith(('http://', 'https://')):
            cmd = 'https://' + cmd
        history.append(current)
        new = load(cmd)
        if new:
            current = new
        else:
            current = history.pop() if history else current


if __name__ == '__main__':
    start = sys.argv[1] if len(sys.argv) > 1 else None
    run(start)
