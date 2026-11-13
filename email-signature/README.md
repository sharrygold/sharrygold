# Email signature

The images and HTML behind my Gmail signature. The files here are public on purpose, because email clients load signature images from a public link.

- `now-shipping.gif`: the rotating "Built and live" line (Remi, PR Tracker, Solace)
- `signature-full.html`: the full signature, used on new emails
- `signature-reply.html`: the one-line signature, used on replies and forwards
- `src/`: the scripts and icons that make them

To change a product, edit `PRODUCTS` in `src/make_gif.py`, run `python3 src/make_gif.py now-shipping.gif`, and commit. The URL stays the same, so signatures already set up in Gmail pick up the new GIF.
