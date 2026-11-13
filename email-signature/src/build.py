"""Build the Gmail-ready signature HTML files.

Usage: python3 build.py <asset-base-url> <out-dir>
Gmail keeps only inline styles, so everything is tables and inline CSS.
"""
import sys, os

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'img'
OUT = sys.argv[2] if len(sys.argv) > 2 else '.'

PORTFOLIO = 'https://sharry.netlify.app'
LINKEDIN = 'https://linkedin.com/in/sharonakpunne'
GITHUB = 'https://github.com/sharrygold'
SHIPPING_LINK = GITHUB  # the profile README lists every product with its own link

INK = '#1a1a1a'
MUTED = '#6b6b6b'
ACCENT = '#9b3426'
RULE = '#dddddd'
SERIF = "Georgia,'Times New Roman',serif"
SANS = 'Helvetica,Arial,sans-serif'


def link(href, text):
    return (f'<a href="{href}" target="_blank" '
            f'style="color:{ACCENT};text-decoration:none;font-family:{SANS};font-size:13px;">{text}</a>')


DOT = f'<span style="color:#a6a6a6;font-family:{SANS};font-size:13px;">&nbsp;&nbsp;&middot;&nbsp;&nbsp;</span>'

FULL = f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;">
<tr><td style="font-family:{SERIF};font-size:17px;line-height:22px;color:{INK};padding:0;">Sharon Praise-Akpunne</td></tr>
<tr><td style="font-family:{SERIF};font-style:italic;font-size:14px;line-height:20px;color:{MUTED};padding:0;">Product &amp; project manager, PMP<sup style="font-size:9px;line-height:0;vertical-align:super;">&reg;</sup></td></tr>
<tr><td style="padding:4px 0 0 0;line-height:18px;">{link(PORTFOLIO, 'Portfolio')}{DOT}{link(LINKEDIN, 'LinkedIn')}{DOT}{link(GITHUB, 'GitHub')}</td></tr>
<tr><td style="padding:12px 0 10px 0;"><table cellpadding="0" cellspacing="0" border="0" role="presentation"><tr><td width="28" height="1" style="width:28px;height:1px;background-color:{RULE};font-size:1px;line-height:1px;">&nbsp;</td></tr></table></td></tr>
<tr><td style="font-family:{SANS};font-size:10px;line-height:14px;letter-spacing:1.4px;text-transform:uppercase;color:{MUTED};padding:0 0 6px 0;">BUILT AND LIVE</td></tr>
<tr><td style="padding:0;"><a href="{SHIPPING_LINK}" target="_blank" style="text-decoration:none;"><img src="{BASE}/now-shipping.gif" width="351" height="28" alt="Built and live: Remi for Mac, PR Tracker and Solace" style="display:block;border:0;outline:none;width:351px;max-width:100%;height:auto;"></a></td></tr>
</table>'''

SHORT = f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;">
<tr><td style="font-family:{SERIF};font-size:15px;line-height:20px;color:{INK};padding:0 10px 0 0;vertical-align:baseline;">Sharon</td>
<td style="font-family:{SANS};font-size:13px;line-height:20px;color:#c4c4c4;padding:0 10px 0 0;vertical-align:baseline;">|</td>
<td style="line-height:20px;padding:0;vertical-align:baseline;">{link(PORTFOLIO, 'Portfolio')}{DOT}{link(LINKEDIN, 'LinkedIn')}</td></tr>
</table>'''


def page(title, sig):
    return f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:40px;background:#ffffff;">
<!-- Copy from here: select everything below this line in the browser, copy, paste into Gmail -->
{sig}
</body>
</html>
'''


os.makedirs(OUT, exist_ok=True)
for name, title, sig in [('signature-full.html', 'Sharon: full signature', FULL),
                         ('signature-reply.html', 'Sharon: reply signature', SHORT)]:
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(page(title, sig))
    with open(os.path.join(OUT, name.replace('.html', '.fragment.html')), 'w') as f:
        f.write(sig)
    print(name, len(sig), 'chars (Gmail limit 10,000)')
