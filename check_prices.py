import json

with open('d:/sridevisanitary/HP-/src/ashirvad_products.json', encoding='utf-8') as f:
    data = json.load(f)

susp = []
for p in data:
    m = p['mrp']
    if m in ['₹1', '₹2', '₹3', '₹4', '₹5', '₹10', '₹24', '₹50', '₹100', 'Enquire'] or not m.startswith('₹'):
        susp.append(p)

print(f"Total items: {len(data)}, Suspicious prices: {len(susp)}")
for p in susp[:25]:
    print(f"Page {p['page']}: {p['product_name']} | Size: {p['size']} | Part: {p['part_no']} | MRP: {p['mrp']}")
