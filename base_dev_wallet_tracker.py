import requests, time

def dev_tracker():
    print("Base — Dev Wallet Tracker (ловит кошельки создателей токенов в момент создания пула)")
    seen_pairs = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                if addr in seen_pairs:
                    continue

                age = time.time() - pair.get("pairCreatedAt", 0) / 1000
                if age > 45:  # старше 45 сек — не интересно
                    seen_pairs.add(addr)
                    continue

                # Находим транзакцию создания пула (обычно это tx с 2 событиями: Mint + Sync)
                tx_hash = pair.get("pairCreatedTxHash") or pair.get("txHash")
                if not tx_hash:
                    continue

                tx_data = requests.get(f"https://api.basescan.org/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}").json()
                creator = tx_data["result"]["from"]

                print(f"DEV WALLET CAUGHT\n"
                      f"Token: {pair['baseToken']['symbol']} — {pair['baseToken']['name']}\n"
                      f"Dev/Creator: {creator}\n"
                      f"Pool age: {age:.0f}s\n"
                      f"Liq: ${pair['liquidity']['usd']:,.0f}\n"
                      f"https://dexscreener.com/base/{addr}\n"
                      f"https://basescan.org/address/{creator}\n"
                      f"→ Теперь ты знаешь, кто запустил этот мемкоин\n"
                      f"→ Следи за его продажами — получишь выход раньше всех\n"
                      f"{'='*90}")

                seen_pairs.add(addr)

        except:
            pass
        time.sleep(2.1)

if __name__ == "__main__":
    dev_tracker()
