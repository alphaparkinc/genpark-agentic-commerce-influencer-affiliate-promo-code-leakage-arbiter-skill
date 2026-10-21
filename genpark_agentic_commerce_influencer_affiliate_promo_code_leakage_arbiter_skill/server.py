# -*- coding: utf-8 -*-
"""MCP Server for Affiliate Promo Code Leakage & Commission Clawback Arbiter Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import AffiliatePromoCodeLeakageArbiter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "detect_coupon_leakage_anomaly",
        "description": "Identify affiliate promo codes leaked to public coupon aggregator scrapers and browser extensions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "promo_code": {
                    "type": "string"
                },
                "affiliate_partner_id": {
                    "type": "string"
                },
                "session_referrer": {
                    "type": "string"
                },
                "time_delta_since_extension_injection_sec": {
                    "type": "number"
                }
            },
            "required": [
                "promo_code",
                "affiliate_partner_id"
            ]
        }
    },
    {
        "name": "execute_commission_clawback_adjustment",
        "description": "Calculate commission clawback for unearned affiliate attribution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "disputed_commission_total_usd": {
                    "type": "number"
                },
                "hijacked_orders_count": {
                    "type": "integer"
                }
            },
            "required": [
                "disputed_commission_total_usd",
                "hijacked_orders_count"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-influencer-affiliate-promo-code-leakage-arbiter-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(AffiliatePromoCodeLeakageArbiter, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-influencer-affiliate-promo-code-leakage-arbiter-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
