#!/usr/bin/env python3
"""
Fetcher de precios para Cartera 1738.
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

# ── CONFIGURACIÓN DE LA CARTERA ─────────────────────────────────
# Si agregás acciones, añadí una entrada acá y en index.html
PORTFOLIO = [
    # Acciones argentinas (BCBA) — precio en ARS
    {"id": "AGRO", "yf": "AGRO.BA", "type": "accion"},
    {"id": "CEPU", "yf": "CEPU.BA", "type": "accion"},
    {"id": "CTIO", "yf": "CTIO.BA", "type": "accion"},
    {"id": "ECOG", "yf": "ECOG.BA", "type": "accion"},
    {"id": "PAMP", "yf": "PAMP.BA", "type": "accion"},
    # CEDEARs — precio en USD del subyacente
    {"id": "ADGO", "yf": "AGRO",    "type": "cedear"},  # Adecoagro
    {"id": "LAC",  "yf": "LAC",     "type": "cedear"},  # Lithium Americas
    {"id": "NU",   "yf": "NU",      "type": "cedear"},  # Nu Holdings
    {"id": "TXR",  "yf": "TX",      "type": "cedear"},  # Ternium
]

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "prices.json")

# ── FUNCIONES ────────────────────────────────────────────────────

def load_existing():
    """Carga datos existentes como fallback."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tc": 1395, "prices": {}}


def fetch_price(ticker_id, yf_ticker):
    """Obtiene precio actual y métricas de Yahoo Finance."""
    try:
        t = yf.Ticker(yf_ticker)
        info = t.fast_info

        price = getattr(info, "last_price", None)
        prev  = getattr(info, "previous_close", None) or price

        if not price:
            raise ValueError("Sin precio disponible")

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
    """Intenta obtener tipo de cambio USD/ARS."""
    for sym in ["ARS=X", "USDARS=X"]:
        try:
            t = yf.Ticker(sym)
            price = t.fast_info.last_price
            if price and price > 500:  # Sanity check (TC debería ser > 1000)
                return round(float(price), 0)
        except Exception:
            pass
    return None


def _safe(obj_or_val, attr=None, decimals=2):
    """Helper: obtiene atributo de forma segura."""
    try:
        val = getattr(obj_or_val, attr) if attr else obj_or_val
        if val is None or (isinstance(val, float) and (val != val)):  # NaN check
            return None
        return round(float(val), decimals)
    except Exception:
        return None


# ── MAIN ─────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*50}")
    print(f"  Actualizando precios – {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*50}\n")

    existing = load_existing()
    prices = {}
    ok_count = 0

    for pos in PORTFOLIO:
        print(f"📡 {pos['id']} ({pos['yf']})...", end=" ")
        result = fetch_price(pos["id"], pos["yf"])

        if result:
            prices[pos["id"]] = result
            chg = result.get("chgPct")
            arrow = "▲" if chg and chg > 0 else ("▼" if chg and chg < 0 else "–")
            print(f"✅  {result['price']:.4f}  {arrow} {chg or 0:+.2f}%")
            ok_count += 1
        else:
            cached = existing.get("prices", {}).get(pos["id"])
            prices[pos["id"]] = cached
            print(f"⚠️  usando datos en caché")

    # Tipo de cambio
    tc = fetch_tc()
    if tc:
        print(f"\n💱 TC USD/ARS: {tc:.0f}")
    else:
        tc = existing.get("tc", 1395)
        print(f"\n💱 TC: {tc:.0f} (caché)")

    # Guardar
    output = {
        "updated":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tc":       tc,
        "prices":   prices,
    }

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {ok_count}/{len(PORTFOLIO)} precios actualizados → data/prices.json")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
