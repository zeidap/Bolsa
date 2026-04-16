#!/usr/bin/env python3
"""
Fetcher de precios para Carteras 1738 y 6106.
Corre automáticamente via GitHub Actions todos los días hábiles.
También puede ejecutarse manualmente: python scripts/fetch_prices.py
"""

import json
import os
import sys
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    print("Instalando yfinance...")
    os.system(f"{sys.executable} -m pip install yfinance --quiet")
    import yfinance as yf

# ── TICKERS A MONITOREAR ────────────────────────────────────────
# Todos los tickers únicos entre todas las carteras
TICKERS = [
    # Cartera 1738 – Accrogliano Gabriela
    {"id": "AGRO", "yf": "AGRO.BA"},   # Agrometal (también en 6106)
    {"id": "CEPU", "yf": "CEPU.BA"},   # Central Puerto
    {"id": "CTIO", "yf": "CTIO.BA"},   # Consultatio (también en 6106)
    {"id": "ECOG", "yf": "ECOG.BA"},   # Ecogas
    {"id": "PAMP", "yf": "PAMP.BA"},   # Pampa Energía
    {"id": "ADGO", "yf": "AGRO"},      # CEDEAR Adecoagro (NYSE)
    {"id": "LAC",  "yf": "LAC"},       # CEDEAR Lithium Americas (NYSE)
    {"id": "NU",   "yf": "NU"},        # CEDEAR Nu Holdings (NYSE)
    {"id": "TXR",  "yf": "TX"},        # CEDEAR Ternium (NYSE)
    # Cartera 6106 – Zeida Patricio Eduardo
    {"id": "AUSO", "yf": "AUSO.BA"},   # Autopistas del Sol
    {"id": "FERR", "yf": "FERR.BA"},   # Ferrum S.A.
    {"id": "OEST", "yf": "OEST.BA"},   # Grupo Conc. del Oeste
    {"id": "B",    "yf": "GOLD"},      # CEDEAR Barrick Gold (NYSE)
]

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "prices.json")

# ── FUNCIONES ────────────────────────────────────────────────────

def load_existing():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tc": 1395, "prices": {}}


def fetch_price(ticker_id, yf_ticker):
    try:
        t = yf.Ticker(yf_ticker)
        info = t.fast_info
        price = getattr(info, "last_price", None)
        prev  = getattr(info, "previous_close", None) or price
        if not price:
            raise ValueError("Sin precio")
        chg_pct = round((price - prev) / prev * 100, 2) if prev else None
        return {
            "price":  round(float(price), 4),
            "prev":   round(float(prev), 4) if prev else None,
            "chgPct": chg_pct,
            "open":   _safe(info, "open"),
            "high":   _safe(info, "day_high"),
            "low":    _safe(info, "day_low"),
            "vol":    int(getattr(info, "three_month_average_volume", 0) or 0),
            "w52h":   _safe(info, "year_high"),
            "w52l":   _safe(info, "year_low"),
            "mktCap": _safe(info, "market_cap", decimals=0),
            "pe":     _safe(t.info.get("trailingPE") if hasattr(t, "info") else None, decimals=1),
        }
    except Exception as e:
        print(f"  ❌ Error en {ticker_id} ({yf_ticker}): {e}")
        return None


def fetch_tc():
    for sym in ["ARS=X", "USDARS=X"]:
        try:
            price = yf.Ticker(sym).fast_info.last_price
            if price and price > 500:
                return round(float(price), 0)
        except Exception:
            pass
    return None


def _safe(obj_or_val, attr=None, decimals=2):
    try:
        val = getattr(obj_or_val, attr) if attr else obj_or_val
        if val is None or (isinstance(val, float) and val != val):
            return None
        return round(float(val), decimals)
    except Exception:
        return None


# ── MAIN ─────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*55}")
    print(f"  Actualizando precios – {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Carteras: 1738 (Accrogliano) + 6106 (Zeida)")
    print(f"{'='*55}\n")

    existing = load_existing()
    prices = {}
    ok_count = 0

    for t in TICKERS:
        print(f"📡 {t['id']:6s} ({t['yf']:8s})...", end=" ")
        result = fetch_price(t["id"], t["yf"])
        if result:
            prices[t["id"]] = result
            chg = result.get("chgPct") or 0
            arrow = "▲" if chg > 0 else ("▼" if chg < 0 else "–")
            print(f"✅  {result['price']:.2f}  {arrow} {chg:+.2f}%")
            ok_count += 1
        else:
            prices[t["id"]] = existing.get("prices", {}).get(t["id"])
            print(f"⚠️  usando caché")

    tc = fetch_tc()
    if tc:
        print(f"\n💱 TC USD/ARS: {tc:.0f}")
    else:
        tc = existing.get("tc", 1395)
        print(f"\n💱 TC: {tc:.0f} (caché)")

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tc": tc,
        "prices": prices,
    }

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {ok_count}/{len(TICKERS)} precios guardados → data/prices.json")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
