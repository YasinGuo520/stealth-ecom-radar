import re
import json
from typing import Dict, Any, List, Optional

class ShopifyAuditor:
    """
    Shopify 独立站零幻觉底层数据与死链审计引擎
    直接调取公开 /products.json 规范，杜绝 DOM 渲染幻觉
    """

    @staticmethod
    def parse_products_json(raw_json_str: str) -> List[Dict[str, Any]]:
        try:
            data = json.loads(raw_json_str)
            products = data.get("products", [])
            results = []
            for p in products:
                variants = p.get("variants", [])
                total_stock = sum(v.get("inventory_quantity", 0) for v in variants if v.get("inventory_quantity") is not None)
                prices = [float(v.get("price", 0)) for v in variants if v.get("price")]
                min_price = min(prices) if prices else 0.0
                max_price = max(prices) if prices else 0.0

                results.append({
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "handle": p.get("handle"),
                    "variants_count": len(variants),
                    "min_price": min_price,
                    "max_price": max_price,
                    "total_stock": total_stock,
                    "published_at": p.get("published_at"),
                    "is_active": len(variants) > 0 and any(v.get("available", True) for v in variants)
                })
            return results
        except Exception as e:
            return []

class ProductParser:
    """自适应元数据与价格解析器"""
    
    @staticmethod
    def extract_price(text: str) -> Optional[float]:
        patterns = [
            r"[\$¥€£]\s*(\d+(?:\.\d{1,2})?)",
            r"price[\"']?\s*:\s*[\"']?(\d+(?:\.\d{1,2})?)"
        ]
        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return None
