# -*- coding: utf-8 -*-
"""Affiliate Promo Code Leakage & Commission Clawback Arbiter for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class AffiliatePromoCodeLeakageArbiter:
    @staticmethod
    def detect_coupon_leakage_anomaly(promo_code: str, affiliate_partner_id: str, session_referrer: str = "direct", time_delta_since_extension_injection_sec: float = 1.2) -> Dict[str, Any]:
        is_leaked = (time_delta_since_extension_injection_sec < 3.0) or ("coupon" in session_referrer.lower())
        return {"promo_code": promo_code, "affiliate_id": affiliate_partner_id, "is_leaked_to_browser_extension": is_leaked, "attribution_status": "FRAUDULENT_HIJACK" if is_leaked else "GENUINE_INFLUENCER_CONVERSION"}

    @staticmethod
    def execute_commission_clawback_adjustment(disputed_commission_total_usd: float, hijacked_orders_count: int) -> Dict[str, Any]:
        return {"clawback_amount_usd": disputed_commission_total_usd, "hijacked_orders": hijacked_orders_count, "action": "ISSUE_NEGATIVE_COMMISSION_ADJUSTMENT", "ledger_status": "CLAWBACK_COMMITTED"}
