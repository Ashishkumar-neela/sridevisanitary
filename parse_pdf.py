import pymupdf
import json
import re
import os

pdf_path = "d:/sridevisanitary/HP-/Master - Ashirvad by Aliaxis - New Price List - 100826.pdf"
doc = pymupdf.open(pdf_path)

out_img_dir = "d:/sridevisanitary/HP-/public/images/products"
os.makedirs(out_img_dir, exist_ok=True)

sections_def = [
    (5, 18, "FlowGuard Plus CPVC", "CPVC Hot & Cold Water Plumbing Systems", "Zap"),
    (19, 32, "FlowPro+ CPVC", "High Performance Commercial CPVC Systems", "ShieldCheck"),
    (33, 42, "Bath and Kitchen", "Concealed Valves, Taps & Sanitary Fixtures", "Bath"),
    (43, 52, "Aqualife+ uPVC", "uPVC Cold Water Plumbing & Agricultural Systems", "Droplets"),
    (53, 54, "Aqualife Reclaim", "Treated Water & Greywater Recycled Systems", "Waves"),
    (55, 58, "Water Storage Tanks", "3-Layer, 4-Layer & Underground Sump Tanks", "TowerControl"),
    (59, 72, "SWR Drainage Systems", "Ringfit & Selfit Soil, Waste & Rainwater Drainage", "Wrench"),
    (73, 78, "Silent SWR", "Low-Noise Commercial & Residential Drainage", "Volume2"),
    (79, 86, "Silent Plus SWR", "Acoustic Triple-Layer Drainage System", "Sparkles"),
    (87, 88, "SWR Pro", "Heavy-Duty High Performance Drainage", "Factory"),
    (89, 90, "SWR 4K", "High-Pressure Withstanding Drainage Systems", "CheckCircle"),
    (91, 92, "Rainwater Harvesting", "Rooftop Filters & Harvesting Solutions", "CloudRain"),
    (93, 94, "Siphonic Roof Drainage", "Engineered Large Roof Siphonic Rainwater Systems", "Building2"),
    (95, 96, "Surface Drain Channel", "Channels for Parking, Patios & Driveways", "LayoutGrid"),
    (97, 110, "Underground Drainage", "Chambers, Gullies & Underground Sewer Solutions", "Layers")
]

def get_section(page_idx):
    pno = page_idx + 1
    for start, end, name, desc, icon in sections_def:
        if start <= pno <= end:
            return name, desc, icon
    return "Other Solutions", "Ashirvad Piping Systems", "Zap"

extracted_products = []

BOILERPLATE_PATTERNS = [
    r'WARRANTY APPLICABLE',
    r'NSF® certified',
    r'FIRST IN INDIA',
    r'Revised',
    r'Introducing Shortly',
    r'Speciality',
    r'New',
    r'Ideal for',
    r'Enhanced Efficiency',
    r'Mfg\. as per',
    r'PRICE\s*LIST',
    r'PRICELIST',
    r'HSN CODE',
    r'FOR BEST RESULTS',
    r'ACOUSTIC GIRPI',
    r'HIGH IMPACT',
    r'European Standards',
    r'IS\s*\d+',
    r'Taxes/pc',
    r'Incl\. of all',
    r'Std\.\s*Pkg',
    r'Box\s*Qty',
    r'Part No\.',
    r'Size\s*\(cm\)',
    r'Turn\s*Spindle',
    r'^\s*Size\s*$'
]

def is_boilerplate(text):
    for pat in BOILERPLATE_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False

TABLE_HEADER_WORDS = {
    'Size', 'Std.', 'Box', 'Part No.', 'MRP', 'Pkg.', 'Qty.', '(cm)', '(inch)',
    '(mtr)', '(ft)', '(Ltrs)', 'Colour', 'Turn', 'Knob', 'Incl. of all', 'Taxes/pc',
    'Type', 'Length', 'Class', 'Socket', 'Spindle', 'Item Code', 'Description', 'Capacity',
    'Quarter', 'Full', '3/4', '1/2', '1', 'Std'
}

for page_idx in range(4, len(doc)):
    pno = page_idx + 1
    cat_name, cat_desc, cat_icon = get_section(page_idx)
    page = doc[page_idx]
    blocks = page.get_text('blocks')
    
    page_img_items = []
    for img in page.get_images():
        xref = img[0]
        fname = f'prod_img_{xref}.jpeg'
        if not os.path.exists(os.path.join(out_img_dir, fname)):
            fname = f'prod_img_{xref}.png'
        if os.path.exists(os.path.join(out_img_dir, fname)):
            rects = page.get_image_rects(xref)
            for r in rects:
                page_img_items.append({
                    'path': f'/images/products/{fname}',
                    'x0': r.x0,
                    'y0': r.y0,
                    'x1': r.x1,
                    'y1': r.y1,
                    'cx': (r.x0 + r.x1) / 2,
                    'cy': (r.y0 + r.y1) / 2
                })

    page_text = page.get_text()
    if "Available on Request" in page_text or "Price: Available on Request" in page_text:
        sample_img = page_img_items[0]['path'] if page_img_items else ""
        if pno in [93, 94]:
            extracted_products.append({
                "page": pno,
                "category": cat_name,
                "category_desc": cat_desc,
                "category_icon": cat_icon,
                "subcategory": "Siphonic Systems",
                "product_name": "Ashirvad Siphonic Roof Drainage System",
                "size": "Engineered for Large Commercial Roofs",
                "part_no": "ASH-SIPHONIC-ROOF",
                "std_pkg": "Custom",
                "box_qty": "Engineered",
                "mrp": "Price on Request",
                "image": sample_img
            })
            continue
        elif pno in [95, 96]:
            extracted_products.append({
                "page": pno,
                "category": cat_name,
                "category_desc": cat_desc,
                "category_icon": cat_icon,
                "subcategory": "Surface Channels",
                "product_name": "Ashirvad Surface Drain Channel",
                "size": "Parking Lots, Courtyards, Driveways",
                "part_no": "ASH-SURFACE-CHNL",
                "std_pkg": "Modular",
                "box_qty": "Heavy Duty",
                "mrp": "Price on Request",
                "image": sample_img
            })
            continue

    data_rows = []
    title_candidates = []
    
    is_bath_valves = (33 <= pno <= 42)
    valve_main_titles = []
    if is_bath_valves:
        for b in blocks:
            txt = b[4].strip()
            if "Concealed Valve" in txt or "Bib Tap" in txt or "Angle Valve" in txt or "Pillar Cock" in txt or "Ball Valve" in txt:
                titles = [t.strip() for t in txt.split('\n') if t.strip()]
                for t in titles:
                    valve_main_titles.append((b[:4], t))
    
    for b in blocks:
        txt = b[4].strip()
        if not txt:
            continue
        if re.match(r'^\d+$', txt) and (b[1] < 50 or b[1] > 780):
            continue
        if is_boilerplate(txt):
            continue
            
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        if not lines:
            continue
            
        if len(lines) >= 2 and all(l in TABLE_HEADER_WORDS for l in lines):
            continue
            
        part_idx = -1
        for i, l in enumerate(lines):
            if re.match(r'^(700\d{5}|500\d{5}|800\d{5}|\d{8})$', l):
                part_idx = i
                break
                
        if part_idx != -1:
            data_rows.append({
                'bbox': b[:4],
                'lines': lines,
                'part_idx': part_idx
            })
        else:
            clean_t = ' '.join(lines)
            if len(clean_t) <= 90 and not re.search(r'\b\d+\.\d{2}\b', clean_t):
                if not all(w in TABLE_HEADER_WORDS for w in clean_t.split()):
                    if not re.match(r'^[\d/\.\s"x]+$', clean_t):
                        title_candidates.append({
                            'bbox': b[:4],
                            'title': clean_t
                        })
                        
    for row in data_rows:
        rx0, ry0, rx1, ry1 = row['bbox']
        raw_lines = row['lines']
        pidx = row['part_idx']
        part_no = raw_lines[pidx]
        
        # Filter out trailing HSN code line if inside the block
        lines = [l for l in raw_lines if 'HSN CODE' not in l]
        # Recompute pidx in clean lines
        try:
            pidx = lines.index(part_no)
        except ValueError:
            pass

        # ACCURATE PRICE EXTRACTION:
        # Search backwards from the end of the row for the actual decimal price
        mrp = "Enquire"
        price_idx = -1
        for i in range(len(lines) - 1, pidx, -1):
            val = lines[i]
            # Match decimal price (e.g. 1823.00, 390.00, 7,600.00, 29.00)
            if re.match(r'^[\d,]+(\.\d{1,2})?$', val):
                mrp = val
                price_idx = i
                break
            elif val == '-':
                mrp = "Price on Request"
                price_idx = i
                break

        # If not found after part_no, check end of line
        if mrp == "Enquire" and len(lines) > 0:
            last_val = lines[-1]
            if re.match(r'^[\d,]+(\.\d{1,2})?$', last_val):
                mrp = last_val
                price_idx = len(lines) - 1

        # Now extract size and packaging from other tokens
        before_part = lines[:pidx]
        between_part_and_price = lines[pidx + 1 : price_idx] if price_idx > pidx else []
        
        size_str = ""
        std_pkg = "-"
        box_qty = "-"
        
        # When part_no is at index 4 (standard pipe/fitting table):
        # lines: [cm, inch, std_pkg, box_qty, part_no, mrp]
        if len(before_part) == 4:
            size_str = f"{before_part[0]} cm ({before_part[1]}\")"
            std_pkg = before_part[2]
            box_qty = before_part[3]
        elif len(before_part) == 3:
            size_str = f"{before_part[0]}"
            std_pkg = before_part[1]
            box_qty = before_part[2]
        elif len(before_part) == 2:
            size_str = f"{before_part[0]}"
            std_pkg = before_part[1]
        elif len(before_part) == 5:
            size_str = f"{before_part[1]} cm ({before_part[2]}\") - {before_part[3]}m/{before_part[4]}ft [{before_part[0]}]"
        elif len(before_part) == 1:
            size_str = before_part[0]
            # Check if std_pkg / box_qty are in between_part_and_price (like Concealed valves!)
            if len(between_part_and_price) >= 2:
                std_pkg = between_part_and_price[0]
                box_qty = between_part_and_price[1]
            elif len(between_part_and_price) == 1:
                std_pkg = between_part_and_price[0]
        elif len(before_part) == 0 and len(between_part_and_price) >= 1:
            size_str = "Standard"
            std_pkg = between_part_and_price[0]
            if len(between_part_and_price) >= 2:
                box_qty = between_part_and_price[1]
        else:
            size_str = " ".join(before_part[:2]) if before_part else "Standard"
            if len(before_part) > 2:
                std_pkg = before_part[2]
            if len(before_part) > 3:
                box_qty = before_part[3]
            
        best_title = None
        best_dist = 999999
        is_right = rx0 >= 280
        
        if is_bath_valves and valve_main_titles:
            col_vtitles = [vt for vt in valve_main_titles if (vt[0][0] >= 280) == is_right]
            if col_vtitles:
                main_vtitle = col_vtitles[0][1]
                knob_type = size_str if size_str in ['Triangle', 'Square', 'Round', 'Flora'] else ''
                best_title = f"{main_vtitle} ({knob_type})" if knob_type else main_vtitle
        
        if not best_title:
            for cand in title_candidates:
                cx0, cy0, cx1, cy1 = cand['bbox']
                if cy1 <= ry0 + 10:
                    cand_is_right = cx0 >= 270
                    same_col = (is_right == cand_is_right)
                    dist = ry0 - cy1
                    if same_col:
                        if dist < best_dist:
                            best_dist = dist
                            best_title = cand['title']
                    else:
                        if (cx1 - cx0) > 280 and dist < best_dist:
                            best_dist = dist
                            best_title = cand['title']
                            
        if not best_title:
            for cand in title_candidates:
                cx0, cy0, cx1, cy1 = cand['bbox']
                if cy1 <= ry0 + 10:
                    dist = ry0 - cy1
                    if dist < best_dist:
                        best_dist = dist
                        best_title = cand['title']
                        
        if not best_title:
            best_title = f"{cat_name} Component"
            
        best_title = re.sub(r'^(CPVC|uPVC|SWR)\s+', '', best_title).strip()
        best_title = re.sub(r'\s+(CPVC|uPVC|SWR)$', '', best_title).strip()
        for bp in ['FITTINGS & CPVC SOLVENT', 'SOLVENT CEMENT ARE USED', 'IS13592', 'IS14735', 'IS16098-1', 'IS15328']:
            best_title = best_title.replace(bp, '').strip()
        if not best_title:
            best_title = f"{cat_name} Fitting"

        subcat = "Fittings"
        title_lower = best_title.lower()
        if "pipe" in title_lower or "conduit" in title_lower:
            subcat = "Pipes & Conduits"
        elif "valve" in title_lower or "tap" in title_lower or "cock" in title_lower or "spindle" in title_lower:
            subcat = "Valves & Taps"
        elif "tank" in title_lower or "aquafer" in title_lower:
            subcat = "Water Storage Tanks"
        elif "bend" in title_lower or "elbow" in title_lower:
            subcat = "Bends & Elbows"
        elif "tee" in title_lower or "cross" in title_lower:
            subcat = "Tees & Crosses"
        elif "coupler" in title_lower or "socket" in title_lower or "bushing" in title_lower or "reducer" in title_lower or "union" in title_lower:
            subcat = "Couplers & Reducers"
        elif "trap" in title_lower or "drain" in title_lower or "gully" in title_lower or "chamber" in title_lower:
            subcat = "Traps & Drainage"
        elif "clamp" in title_lower or "bracket" in title_lower or "clip" in title_lower or "girpi" in title_lower:
            subcat = "Clamps & Fasteners"
        elif "solvent" in title_lower or "cement" in title_lower or "lubricant" in title_lower or "primer" in title_lower:
            subcat = "Solvents & Adhesives"

        matched_img = ""
        min_img_dist = 999999
        row_cy = (ry0 + ry1) / 2
        for img_obj in page_img_items:
            img_is_right = img_obj['cx'] >= 270
            col_match = (is_right == img_is_right)
            ydist = abs(img_obj['cy'] - row_cy)
            dist_score = ydist + (0 if col_match else 250)
            if dist_score < min_img_dist:
                min_img_dist = dist_score
                matched_img = img_obj['path']

        formatted_mrp = mrp
        if mrp not in ["Enquire", "Price on Request"]:
            try:
                num = float(mrp.replace(',', ''))
                formatted_mrp = f"₹{num:,.2f}".replace(".00", "")
            except:
                formatted_mrp = f"₹{mrp}"

        extracted_products.append({
            "page": pno,
            "category": cat_name,
            "category_desc": cat_desc,
            "category_icon": cat_icon,
            "subcategory": subcat,
            "product_name": best_title,
            "size": size_str or "Standard",
            "part_no": part_no,
            "std_pkg": std_pkg,
            "box_qty": box_qty,
            "mrp": formatted_mrp,
            "image": matched_img
        })

print(f"Total extracted products: {len(extracted_products)}")

with open("d:/sridevisanitary/HP-/src/ashirvad_products.json", "w", encoding="utf-8") as f:
    json.dump(extracted_products, f, indent=2)

print("Saved cleanly to d:/sridevisanitary/HP-/src/ashirvad_products.json with accurate prices!")
