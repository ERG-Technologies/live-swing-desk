# Live Swing Desk

Mobile-first, read-only NFL Polymarket market tape and personal exit-plan tracker.

## Live site

https://erg-technologies.github.io/live-swing-desk/

## Architecture

- Gamma API discovers current NFL moneyline markets; GitHub Actions refreshes `data/current.json` every five minutes.
- Public CLOB WebSocket streams best bid, best ask and trades to the browser.
- Public Sports WebSocket streams score, quarter, clock and possession.
- LocalStorage keeps stake, target and stop on that phone only.
- GitHub Pages deploys `main` automatically.

No wallet, API key, login, order routing or custody is included. The site never places a trade.

## Product flow

1. Read **Now**. No triggered rule means no action.
2. Tap a side in **Game board**.
3. Set stake, target and stop.
4. Return to **Now** for take-profit or stop signals.

## Local test

```bash
python scripts/update_data.py
python -m http.server 8000
```
