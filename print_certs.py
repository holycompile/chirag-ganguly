import json

with open('chirag_complete_profile.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for i, c in enumerate(d['certificates'], 1):
    print(f"{i}. {c['name']} | {c['details'][:60]}...")
