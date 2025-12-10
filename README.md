# Base — Dev Wallet Tracker

Every memecoin has a dev.  
Most people discover the dev wallet after the dump.

This script finds the dev wallet **within 45 seconds** of pool creation.

How?
- Catches new Base pairs
- Pulls the exact transaction that created the pool
- Extracts the `from` address — that’s the creator

Now you own the puppet master.

## Run

```bash
python base_dev_wallet_tracker.py
