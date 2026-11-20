import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update font variables
old_vars = """  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-heading: 'Plus Jakarta Sans', var(--font-main);
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;"""

new_vars = """  --font-main: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-heading: 'Newsreader', Georgia, 'Times New Roman', serif;
  --font-sub: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', 'Courier New', monospace;"""

css = css.replace(old_vars, new_vars)

# 2. Update HUD bar
old_hud = """.hud-bar {
  background: #0f172a; /* Sleek high-contrast dark banner for status */
  color: #f8fafc;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  padding: 7px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 101;
  border-bottom: 2px solid var(--accent-cyan);
}"""

new_hud = """.hud-bar {
  background: #0f172a;
  color: #f8fafc;
  font-family: var(--font-sub);
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 8px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 101;
  border-bottom: 2px solid var(--accent-cyan);
}"""

css = css.replace(old_hud, new_hud)

# 3. Replace generic monospace usages on labels, pills, tags, headers to --font-sub or --font-main
replacements = [
  ("font-family: var(--font-mono);\\n  font-size: 0.78rem;\\n  font-weight: 600;\\n  color: var(--accent-cyan);\\n  margin-bottom: 18px;",
   "font-family: var(--font-sub);\\n  font-size: 0.8rem;\\n  font-weight: 600;\\n  letter-spacing: 0.03em;\\n  color: var(--accent-cyan);\\n  margin-bottom: 18px;"),
   
  ("font-family: var(--font-mono);\\n  font-size: 0.76rem;\\n  font-weight: 600;\\n  color: var(--text-secondary);",
   "font-family: var(--font-sub);\\n  font-size: 0.78rem;\\n  font-weight: 600;\\n  color: var(--text-secondary);"),

  (".section-tag {\\n  display: inline-flex;\\n  align-items: center;\\n  gap: 6px;\\n  font-family: var(--font-mono);",
   ".section-tag {\\n  display: inline-flex;\\n  align-items: center;\\n  gap: 6px;\\n  font-family: var(--font-sub);\\n  letter-spacing: 0.05em;\\n  text-transform: uppercase;"),

  (".domain-badge {\\n  font-family: var(--font-mono);",
   ".domain-badge {\\n  font-family: var(--font-sub);\\n  letter-spacing: 0.03em;"),

  (".pub-badge {\\n  font-family: var(--font-mono);",
   ".pub-badge {\\n  font-family: var(--font-sub);\\n  letter-spacing: 0.03em;"),

  (".project-category {\\n  font-family: var(--font-mono);",
   ".project-category {\\n  font-family: var(--font-sub);\\n  letter-spacing: 0.03em;"),

  (".brand-tag {\\n  font-family: var(--font-mono);",
   ".brand-tag {\\n  font-family: var(--font-sub);\\n  letter-spacing: 0.04em;"),

  (".card-header-bar {\\n  display: flex;\\n  justify-content: space-between;\\n  align-items: center;\\n  font-family: var(--font-mono);",
   ".card-header-bar {\\n  display: flex;\\n  justify-content: space-between;\\n  align-items: center;\\n  font-family: var(--font-sub);\\n  letter-spacing: 0.04em;"),

  (".spec-row {\\n  display: flex;\\n  justify-content: space-between;\\n  align-items: center;\\n  font-family: var(--font-mono);",
   ".spec-row {\\n  display: flex;\\n  justify-content: space-between;\\n  align-items: center;\\n  font-family: var(--font-sub);")
]

for r_from, r_to in replacements:
    r_from_clean = r_from.replace('\\n', '\n')
    r_to_clean = r_to.replace('\\n', '\n')
    css = css.replace(r_from_clean, r_to_clean)

# Also let's tweak .hero-title and .section-title for authentic editorial newspaper typography
css = css.replace(
  ".hero-title {\n  font-family: var(--font-heading);\n  font-size: 3.25rem;\n  font-weight: 800;\n  line-height: 1.12;\n  letter-spacing: -0.035em;",
  ".hero-title {\n  font-family: var(--font-heading);\n  font-size: 3.4rem;\n  font-weight: 700;\n  line-height: 1.14;\n  letter-spacing: -0.02em;"
)

css = css.replace(
  ".section-title {\n  font-family: var(--font-heading);\n  font-size: 2.3rem;\n  font-weight: 800;\n  letter-spacing: -0.025em;",
  ".section-title {\n  font-family: var(--font-heading);\n  font-size: 2.45rem;\n  font-weight: 700;\n  letter-spacing: -0.015em;"
)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated styles.css with Newsreader + Space Grotesk + Manrope typography!')
