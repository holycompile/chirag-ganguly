import json

with open('extracted_projects_clean.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)

print('=== ALL 21 PROJECTS ===')
for i, p in enumerate(projects, 1):
    print(f"{i}. {p['title']}")

with open('chirag_complete_profile.json', 'r', encoding='utf-8') as f:
    profile = json.load(f)

profile['projects'] = projects

with open('chirag_complete_profile.json', 'w', encoding='utf-8') as f:
    json.dump(profile, f, indent=2)

print('Updated chirag_complete_profile.json with all 21 projects!')
