import pymupdf, re

doc = pymupdf.open('d:/sridevisanitary/HP-/Master - Ashirvad by Aliaxis - New Price List - 100826.pdf')

for pno in [5, 6, 12, 19, 33, 43, 55, 59, 73, 97]:
    page = doc[pno]
    blocks = page.get_text('blocks')
    for b in blocks:
        txt = b[4].strip()
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        for i, l in enumerate(lines):
            if re.match(r'^(700\d{5}|500\d{5}|800\d{5}|\d{8})$', l):
                print(f"Page {pno+1}: Part at index {i}/{len(lines)}: {lines}")
                break
        else:
            continue
        break
