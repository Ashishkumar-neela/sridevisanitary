import pymupdf, re, json

doc = pymupdf.open('d:/sridevisanitary/HP-/Master - Ashirvad by Aliaxis - New Price List - 100826.pdf')

suspicious = []
for pno in range(4, len(doc)):
    page = doc[pno]
    blocks = page.get_text('blocks')
    for b in blocks:
        txt = b[4].strip()
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        part_idx = -1
        for i, l in enumerate(lines):
            if re.match(r'^(700\d{5}|500\d{5}|800\d{5}|\d{8})$', l):
                part_idx = i
                break
        if part_idx != -1:
            # Check last element as price
            last = lines[-1]
            if not re.match(r'^[\d,]+(\.\d{2})?$', last):
                suspicious.append((pno+1, lines))

print(f"Rows where last element is NOT a price: {len(suspicious)}")
for p, l in suspicious[:20]:
    print(f"Page {p}: {l}")
