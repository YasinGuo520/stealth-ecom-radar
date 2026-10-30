import unittest
from stealth_radar.engine import StealthEngine
from stealth_radar.parsers import ShopifyAuditor, ProductParser

class TestStealthRadar(unittest.TestCase):
    def test_engine_init(self):
        engine = StealthEngine(timeout=10)
        self.assertEqual(engine.timeout, 10)
        resp = engine.fetch("https://example.com")
        self.assertEqual(resp.status_code, 200)

    def test_shopify_parser(self):
        mock_json = '{"products": [{"id": 123, "title": "Silk Shirt", "variants": [{"price": "99.00", "inventory_quantity": 50, "available": true}]}]}'
        res = ShopifyAuditor.parse_products_json(mock_json)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["min_price"], 99.00)
        self.assertEqual(res[0]["total_stock"], 50)

    def test_price_extract(self):
        text = '{"product": {"title": "Shoes", "price": "149.50"}}'
        price = ProductParser.extract_price(text)
        self.assertEqual(price, 149.50)

if __name__ == '__main__':
    unittest.main()
