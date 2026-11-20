import json
import re
from bs4 import BeautifulSoup

def clean(t):
    if not t: return ''
    return re.sub(r'\s+', ' ', t).strip()

data = {}

# 1. Experiences
with open('scraped_pages/experiences.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

experiences = []
# Each section or card
for exp in soup.find_all(['div', 'li'], class_=lambda c: c and any(k in str(c) for k in ['experience-item', 'exp', 'work', 'timeline', 'item'])):
    t = clean(exp.get_text())
    if len(t) > 30:
        experiences.append(t)

# Also let's extract structured roles:
structured_exp = [
    {
        "role": "Technical Lead",
        "company": "Tata Consultancy Services (TCS)",
        "period": "September 2024 - April 2026",
        "description": "Proven experience in managing international client relations, cross-functional engineering teams, and enterprise architectural delivery. Directed product development and security posture across core enterprise platforms.",
        "skills": ["Leadership", "Cloud Architecture", "DevSecOps", "High-Reliability Engineering"]
    },
    {
        "role": "Technical Lead / Product Development Specialist",
        "company": "Tata Consultancy Services (TCS)",
        "period": "August 2023 - September 2024",
        "description": "Spearheaded technical development, cartridge development, defect reduction initiatives, and timely delivery of enterprise solutions.",
        "skills": ["Technical Architecture", "Software Engineering", "Defect Resolution", "Mentorship"]
    },
    {
        "role": "Project Intern - Application Developer",
        "company": "Tata Consultancy Services (TCS)",
        "period": "January 2023 - August 2023",
        "description": "Engineered enterprise application modules, automated workflows, and developed scalable web and software services.",
        "skills": ["Application Development", "Automation", "Full Stack"]
    },
    {
        "role": "Member - Advisor",
        "company": "SECURE - The Centre of Excellence in Cyber Security",
        "period": "October 2022 - October 2023",
        "description": "Provided strategic advisory on threat modeling, cyber security infrastructure, vulnerability mitigation, and nature-inspired defense research.",
        "skills": ["Cyber Security Advisory", "Nature-Inspired Defense", "Vulnerability Research"]
    },
    {
        "role": "Cyber Security Intern (Tech Development & Assessment)",
        "company": "SECURE - The Centre of Excellence in Cyber Security",
        "period": "June 2021 - October 2022",
        "description": "Conducted vulnerability assessment, network penetration testing, and security tooling evaluation.",
        "skills": ["VAPT", "Network Security", "Security Tooling"]
    },
    {
        "role": "Identity & Accounts Management Team Lead / Intern",
        "company": "Virtually Testing Foundation",
        "period": "May 2022 - August 2022",
        "description": "Managed Active Directory, IAM protocols, role-based access control (RBAC), and user account lifecycles.",
        "skills": ["Active Directory", "IAM", "RBAC", "Access Governance"]
    },
    {
        "role": "Penetration Testing Intern & Cloud Security Associate",
        "company": "Virtually Testing Foundation",
        "period": "June 2021 - December 2021",
        "description": "Conducted automated and manual cloud audits, perimeter scans, and offensive penetration tests.",
        "skills": ["Cloud Security", "Offensive Pentesting", "Perimeter Defense"]
    },
    {
        "role": "Teaching Assistant - Digital Forensics",
        "company": "Vellore Institute of Technology (VIT)",
        "period": "August 2021 - December 2021",
        "description": "Assisted in the 'Principles of Digital Forensics' course. Guided undergraduate students through memory forensics, file system analysis, and network packet forensics.",
        "skills": ["Digital Forensics", "Incident Investigation", "Pedagogy"]
    },
    {
        "role": "Community Facilitator",
        "company": "Google Crowdsource",
        "period": "November 2022 - August 2023",
        "description": "Community-driven facilitation for AI/ML dataset evaluation and algorithmic training.",
        "skills": ["Community Building", "AI Data Ops"]
    },
    {
        "role": "Microsoft Learn Student Ambassador",
        "company": "Microsoft",
        "period": "September 2019 - December 2022",
        "description": "Evangelized cloud computing (Azure), developer tools, and hosted hands-on cybersecurity workshops.",
        "skills": ["Azure Cloud", "Developer Relations", "Tech Workshops"]
    },
    {
        "role": "Front-End Developer (Cyber Security Initiative)",
        "company": "Madhya Pradesh Police",
        "period": "May 2020 - June 2020",
        "description": "Developed web interfaces for public cyber hygiene awareness and crime reporting initiatives.",
        "skills": ["Cyber Hygiene", "Web Development", "Public Advisory"]
    }
]
data['experiences'] = structured_exp

# 2. Extract Projects
with open('scraped_pages/projects.html', 'r', encoding='utf-8') as f:
    psoup = BeautifulSoup(f.read(), 'html.parser')

projects_raw = []
for sec in psoup.find_all(['div', 'article', 'li'], class_=lambda c: c and ('project' in str(c) or 'card' in str(c))):
    title_tag = sec.find(['h2', 'h3', 'h4', 'strong'])
    p_tags = sec.find_all('p')
    links = [a.get('href') for a in sec.find_all('a', href=True)]
    if title_tag:
        title = clean(title_tag.get_text())
        desc = " ".join([clean(p.get_text()) for p in p_tags if clean(p.get_text()) != title])
        if len(title) > 2 and title != "Projects":
            projects_raw.append({"title": title, "desc": desc, "links": links})

# Deduplicate
seen = set()
clean_projects = []
for p in projects_raw:
    if p['title'] not in seen and len(p['title']) > 2:
        seen.add(p['title'])
        clean_projects.append(p)

data['projects'] = clean_projects
print(f"Extracted {len(clean_projects)} projects.")

# 3. Extract Certificates
with open('scraped_pages/certificates.html', 'r', encoding='utf-8') as f:
    csoup = BeautifulSoup(f.read(), 'html.parser')

certs_raw = []
for h2 in csoup.find_all(['h2', 'h3']):
    title = clean(h2.get_text())
    if title and not title.startswith('$') and len(title) > 3:
        # find sibling p
        p = h2.find_next_sibling('p')
        desc = clean(p.get_text()) if p else ''
        certs_raw.append({"name": title, "details": desc})

# Deduplicate certs
c_seen = set()
clean_certs = []
for c in certs_raw:
    if c['name'] not in c_seen:
        c_seen.add(c['name'])
        clean_certs.append(c)

data['certificates'] = clean_certs
print(f"Extracted {len(clean_certs)} certificates/achievements.")

# 4. Publications
with open('scraped_pages/publications.html', 'r', encoding='utf-8') as f:
    pub_soup = BeautifulSoup(f.read(), 'html.parser')

pubs = [
    {
        "title": "Post-Quantum Cryptography and Nature-Inspired Cyber Defense: Strategic Readiness and Adaptive Techniques for Next-Gen Threat Response",
        "venue": "IEEE Access",
        "category": "Quantum & Nature-Inspired Defense",
        "description": "Comprehensive analysis of quantum threat landscapes, lattice-based cryptography, and bio-inspired adaptive defense mechanisms for post-quantum resilience.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Nature-inspired swarm optimization paradigms for securing semantic web frameworks against DDoS attacks: a computational approach",
        "venue": "Scientific Reports (Nature Publishing Group)",
        "category": "Bio-Inspired Cyber Defense",
        "description": "Novel defense mechanism utilizing Swarm Intelligence algorithms to detect and throttle high-volume distributed semantic DDoS assaults.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Adaptive Network Sustainability and Defense Based on Artificial Bees Colony Optimization Algorithm for Nature Inspired Cyber Security",
        "venue": "Computer Systems Science & Engineering (Tech Science Press)",
        "category": "Swarm Intelligence & Networks",
        "description": "Applied Artificial Bee Colony (ABC) metaheuristic to dynamically route traffic, isolate compromised nodes, and maintain network stability under cyber attack.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Data-Driven Approach to Network Intrusion Detection System Using Modified Artificial Bee Colony Algorithm for Nature-Inspired Cybersecurity",
        "venue": "Springer - Applied Machine Learning and Data Analytics",
        "category": "NIDS & Machine Learning",
        "description": "Integrated modified ABC algorithm for hyperparameter optimization and feature selection in anomaly-based Network Intrusion Detection Systems.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Adaptive Artificial Bee Colony Algorithm for Nature-Inspired Cyber Defense",
        "venue": "MDPI Systems",
        "category": "Bio-Inspired Cybersecurity",
        "description": "Self-adapting swarm colony model capable of self-healing and dynamic defense configuration against zero-day and polymorphism attacks.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Design and implementation of adaptive network stabilization based on artificial bees colony optimization for nature inspired cyber security",
        "venue": "Journal of King Saud University - Computer and Information Sciences",
        "category": "Network Stabilization",
        "description": "Algorithmic implementation and testbed verification for real-time grid and network stabilization against hostile intrusion.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Adaptive Network Stabilization based on Artificial Bees Colony Optimization for Nature inspired Cyber Security",
        "venue": "Copyright Office, Government of India (IP / Registered Research)",
        "category": "Intellectual Property / Copyright",
        "description": "Formally registered intellectual property for bio-inspired cyber defense optimization architecture.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Enhanced Artificial Bees Colonization Algorithm for Adaptive Nature-Inspired Cyber Defense",
        "venue": "Copyright Office, Government of India (IP / Registered Research)",
        "category": "Intellectual Property / Copyright",
        "description": "Second formal IP registration for advanced adaptive heuristics in cyber threat counter-measures.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "Cyber Attack Evaluation Dataset for Deep Packet Inspection and Analysis",
        "venue": "Data in Brief / IEEE DataPort / Mendeley Data",
        "category": "Open Security Datasets",
        "description": "Publicly released benchmark dataset consisting of thousands of annotated packet traces for intrusion detection, deep packet inspection, and ML-based threat modeling.",
        "link": "https://publications.chiragganguli.com"
    },
    {
        "title": "A Nature-Inspired Approach to Cryptology",
        "venue": "Special Mentions In Academic Textbooks & Digital Resilience Monograph",
        "category": "Book Contribution / Chapters",
        "description": "Authorial chapter exploring biological mimicry, genetic algorithms, and evolutionary principles applied to cryptographic key generation and entropy pools.",
        "link": "https://publications.chiragganguli.com"
    }
]
data['publications'] = pubs

# 5. Testimonials
testimonials = [
    {
        "author": "Dr. Shishir Kumar Shandilya",
        "role": "Faculty - School of Data Science & Forecasting, Devi Ahilya University",
        "text": "I have had the privilege of mentoring Chirag, who was an exceptional student during his time at VIT. Highly dedicated, insightful, and always pushing the boundaries of research in nature-inspired cyber security.",
        "tag": "Research Mentor"
    },
    {
        "author": "Milind Lakkad",
        "role": "Chief Human Resources Officer, Tata Consultancy Services",
        "text": "In appreciation of your outstanding contribution to the organisation, you are awarded the On The Spot Award. You are an inspiration to your peers. Congratulations on becoming an Xcelerate Warrior.",
        "tag": "Leadership & Awards"
    },
    {
        "author": "Shubhangi Singh",
        "role": "Product Engineer - TCS",
        "text": "Working with you has been a great experience—your technical depth, leadership, and proactive problem-solving made a profound impact on the entire team.",
        "tag": "Colleague"
    },
    {
        "author": "Sujay Ghosh",
        "role": "Technical Architect - TCS",
        "text": "I truly enjoyed working with you. Wishing you great success in all your future endeavours. A silent killer, Brilliant Performer, always dependable. Highly talented, sharp focussed. A shining star in the making.",
        "tag": "Technical Leadership"
    },
    {
        "author": "Pradipta Ghosh",
        "role": "Operations Head - TCS",
        "text": "Wish you all the very best Chirag. You are an amazing talent. Keep growing.",
        "tag": "Executive Leadership"
    },
    {
        "author": "Rajesh Sundaresan",
        "role": "Project Lead - TCS",
        "text": "Your excellence and brilliance have always made for a stunning performance at work. Raise the bar with your hard work and continue setting milestones.",
        "tag": "Project Leadership"
    },
    {
        "author": "Abbas Mehdi",
        "role": "Product Engineer - TCS",
        "text": "I admire your growth-mindset and dedication towards continuous learning. You are an asset for our team and an inspiration for anyone passionate about cybersecurity.",
        "tag": "Peer Review"
    },
    {
        "author": "Suraj Kumar",
        "role": "Product Engineer - TCS",
        "text": "Thank you for your guidance and support. It's been memorable working alongside someone who is so brilliant in coding and debugging with endless patience.",
        "tag": "Engineering Peer"
    }
]
data['testimonials'] = testimonials

# 6. Blogs
blogs = [
    {
        "title": "The 2026 AI Paradigm Shift: How Verifiable Reasoning, GRPO, and Inference Scaling Rewrote the Rules",
        "tags": ["AI", "GRPO", "InferenceScaling", "CyberAI"],
        "date": "2026",
        "summary": "The artificial intelligence landscape of 2026 marks a historic inflection point in computational history. Deep dive into verifiable reasoning engines, Group Relative Policy Optimization (GRPO), and inference compute economics.",
        "link": "https://blogs.chiragganguli.com"
    },
    {
        "title": "The 'Agentic Web' Just Killed Traditional Software (And Nobody’s Paying Attention)",
        "tags": ["Agentic AI", "Web Architecture", "Security Posture"],
        "date": "2026",
        "summary": "Every couple of years, the tech industry experiences an extinction-level UX event. Examining autonomous agent protocols, machine-to-machine APIs, and the new threat vectors emerging in the agentic era.",
        "link": "https://blogs.chiragganguli.com"
    },
    {
        "title": "Engineering the Real-Time Social Graph: A Comprehensive Architectural Analysis of Instant Messaging",
        "tags": ["System Design", "Distributed Systems", "End-to-End Encryption"],
        "date": "2025",
        "summary": "Architectural breakdown of high-throughput websocket clusters, cryptographic ratcheting (Signal Protocol), and persistent distributed state in instant messaging backends.",
        "link": "https://blogs.chiragganguli.com"
    }
]
data['blogs'] = blogs

# 7. Utilities & Tools
utilities = [
    {
        "name": "VulnForge Report Generator",
        "desc": "Automated engine to compile structured, CVSS-compliant Vulnerability Assessment & Penetration Testing (VAPT) reports with remediation roadmaps.",
        "category": "Cybersecurity Tool",
        "status": "Production"
    },
    {
        "name": "Reaction Time Test",
        "desc": "Precision latency tester measuring human neural-to-digital reaction speed with millisecond accuracy.",
        "category": "Interactive Utility",
        "status": "Live"
    },
    {
        "name": "IOU Debt & Ledger Tracker",
        "desc": "Lightweight cryptographic ledger and balance tracker for decentralized mutual accounting.",
        "category": "Utility App",
        "status": "Live"
    },
    {
        "name": "Deadline & Milestone Tracker",
        "desc": "Minimalist sprint countdown and deliverable timer optimized for high-pressure engineering deadlines.",
        "category": "Productivity",
        "status": "Live"
    },
    {
        "name": "Orbit Subscriptions & SaaS Audit",
        "desc": "Privacy-focused subscription monitor to prevent credential sprawl and untracked recurring spend.",
        "category": "Security & Finance",
        "status": "Live"
    }
]
data['utilities'] = utilities

# 8. Interactive Quizzes
data['quizzes'] = [
    {
        "title": "Cybersecurity Fundamentals Quiz",
        "desc": "Test your knowledge of OSI layer security, public-key cryptography, symmetric ciphers, and common network attack vectors.",
        "questions_count": 10,
        "difficulty": "Intermediate"
    },
    {
        "title": "VAPT & Threat Hunting Challenge",
        "desc": "Hands-on scenarios covering SQLi, SSRF, XSS, Buffer Overflows, and SIEM log correlation.",
        "questions_count": 15,
        "difficulty": "Advanced"
    },
    {
        "title": "Cloud Security & IAM Hardening",
        "desc": "Assess real-world cloud posture scenarios across AWS IAM, GCP BeyondCorp Zero-Trust, and Kubernetes RBAC.",
        "questions_count": 12,
        "difficulty": "Expert"
    }
]

# 9. Core Bio & Domains
data['bio'] = {
    "name": "Chirag Ganguli",
    "handle": "@chirag_ganguli",
    "email": "contact@chiragganguli.com",
    "location": "India",
    "roles": [
        "Cybersecurity Researcher",
        "Certified Ethical Hacker (CEH)",
        "Lean Six Sigma Black Belt (LSSBB)",
        "Technical Lead (Ex-TCS)"
    ],
    "education": {
        "degree": "B.Tech in Computer Science and Engineering",
        "institution": "Vellore Institute of Technology (VIT)",
        "honors": "Raman Research Award (2023-2024)"
    },
    "summary": "Chirag Ganguli is an accomplished Cybersecurity Researcher, Certified Ethical Hacker (CEH), and Lean Six Sigma Black Belt (LSSBB) holding a B.Tech in CSE from Vellore Institute of Technology (VIT). He specializes in Security Automation, Cloud Security Infrastructure, Governance Risk & Compliance (GRC), VAPT, and pioneering research in Nature-Inspired Cyber Defense (Swarm Optimization & Artificial Bee Colony algorithms). Previously Technical Lead at Tata Consultancy Services (TCS) and Advisor at SECURE CoE.",
    "domains": [
        {
            "name": "Cloud Security & Infrastructure",
            "icon": "cloud-shield",
            "desc": "Architecture and hardening across AWS, Google Cloud, and Azure. Specialized in BeyondCorp Zero-Trust, IAM least-privilege policies, VPC security perimeters, and Kubernetes hardening."
        },
        {
            "name": "Nature-Inspired Cyber Defense",
            "icon": "dna",
            "desc": "Groundbreaking published research utilizing Swarm Intelligence, Artificial Bee Colony (ABC) algorithms, and bio-inspired evolutionary heuristics for real-time intrusion mitigation and DDoS defense."
        },
        {
            "name": "Vulnerability Assessment & Pentesting (VAPT)",
            "icon": "terminal",
            "desc": "Offensive security assessments, web application security (OWASP Top 10), perimeter penetration testing, threat hunting, and automated vulnerability scanning."
        },
        {
            "name": "Security Automation & DevSecOps",
            "icon": "cpu",
            "desc": "Integrating SAST/DAST into CI/CD pipelines, custom security orchestration tooling, automated incident triage, and defect reduction workflows."
        },
        {
            "name": "Governance, Risk & Compliance (GRC)",
            "icon": "shield-check",
            "desc": "Aligning enterprise operations with ISO 27001, NIST CSF, PCI-DSS, and GDPR frameworks combined with Lean Six Sigma Black Belt process optimization."
        },
        {
            "name": "Digital Forensics & Post-Quantum Cryptography",
            "icon": "binary",
            "desc": "Memory forensics, packet trace forensics (deep packet inspection datasets), and strategic post-quantum cryptographic migration."
        }
    ],
    "social_links": {
        "LinkedIn": "https://chiragganguli.com/links/linkedin",
        "GitHub": "https://chiragganguli.com/links/github",
        "Twitter": "https://chiragganguli.com/links/twitter",
        "YouTube": "https://yt.chiragganguli.com/chirag",
        "Topmate": "https://topmate.io/chiragganguli",
        "TryHackMe": "https://chiragganguli.com/links/thm",
        "Instagram": "https://chiragganguli.com/links/instagram",
        "Email": "mailto:contact@chiragganguli.com"
    }
}

with open('chirag_complete_profile.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Saved complete structured data to chirag_complete_profile.json successfully!")
