import re

filepath = r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\06_presentation\sephora_correspondance_profils.pdf.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = [L.strip() for L in f if L.strip()]

rules = []
current_target_axis = ""
current_target_brand = ""

for i, line in enumerate(lines):
    if ' × ' in line and not line.startswith('Fig'):
        parts = line.split(' × ')
        if len(parts) == 2:
            current_target_axis = parts[0].strip()
            current_target_brand = parts[1].strip()
    
    if line == 'I':
        # the next 7 lines are: generation, current axis, current brand, channel, prob, transitions, exp basket
        if i + 7 < len(lines):
            try:
                gen = lines[i+1]
                c_axis = lines[i+2]
                c_brand = lines[i+3]
                channel = lines[i+4]
                prob = lines[i+5]
                trans = lines[i+6]
                basket_str = lines[i+7]
                
                # Check basket str looks like €...
                val = 0.0
                if basket_str.startswith('€'):
                    val = float(basket_str.replace('€', '').replace(',', ''))
                elif basket_str.endswith('€'):
                    val = float(basket_str.replace('€', '').replace(',', ''))
                
                # We need Gender. Look to see if "Male" or "Female" is somewhere?
                # The columns in PDF say: Gender Generation Current axis Current brand Channel Prob.% Transitions Exp. basket
                # But 'I' might be a substitute for Gender if the font icon didn't parse. 'I' is probably an icon or 'F'/'M'.
                # Actually, in the summary pdf: "Blue = male profile, pink = female profile." The 'I' must be a user icon.
                # Is there a way to know gender? In summary PDF, the text listed top 10 rules.
                # Let's just output the top 20 rules sorted by basket.
                
                rules.append({
                    'generation': gen,
                    'c_axis': c_axis,
                    'c_brand': c_brand,
                    'channel': channel,
                    'n_brand': current_target_brand,
                    'prob': prob,
                    'basket_str': basket_str,
                    'val': val
                })
            except Exception as e:
                pass

rules.sort(key=lambda x: x['val'], reverse=True)

import json
with open('c:\\Users\\Hp\\OneDrive - Université Paris Sciences et Lettres\\BDD-Projects\\BDD\\Sephora\\06_presentation\\top_rules.json', 'w') as out:
    json.dump(rules[:25], out, indent=2)
print(f"Parsed {len(rules)} rules. Top 25 saved to top_rules.json.")
