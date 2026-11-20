// script.js - Core application engine for Chirag Ganguli's Redesigned Cyber Portfolio

document.addEventListener('DOMContentLoaded', () => {
  // Ensure data is loaded
  if (typeof CHIRAG_DATA === 'undefined') {
    console.error('CHIRAG_DATA not found. Make sure chirag_data.js is loaded.');
    return;
  }

  initHUDClock();
  initThemeToggle();
  initNavigation();
  renderDomains();
  renderExperiences();
  renderPublications();
  initProjectsFilter();
  initCertsFilter();
  renderUtilities();
  initInteractiveQuiz();
  renderTestimonials();
  renderBlogs();
  initTerminal();
  initModals();
});

/* ===================================================================
   1. HUD CLOCK & TELEMETRY
   =================================================================== */
function initHUDClock() {
  const clockEl = document.getElementById('hud-clock');
  const pingEl = document.getElementById('hud-ping');

  function updateTime() {
    const now = new Date();
    const utcStr = now.toISOString().slice(11, 19) + ' UTC';
    if (clockEl) clockEl.textContent = utcStr;
  }

  function simulatePing() {
    if (pingEl) {
      const ping = Math.floor(Math.random() * 8) + 12; // 12-20ms
      pingEl.textContent = `${ping}ms`;
    }
  }

  updateTime();
  setInterval(updateTime, 1000);
  setInterval(simulatePing, 4000);
}

/* ===================================================================
   1.1 THEME TOGGLE (NEWSPAPER LIGHT MODE DEFAULT)
   =================================================================== */
function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  const btnText = document.getElementById('theme-btn-text');
  if (!toggleBtn) return;

  const savedTheme = localStorage.getItem('chirag_theme') || 'light';
  if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    if (btnText) btnText.textContent = 'Light';
    toggleBtn.querySelector('i').className = 'fa-solid fa-sun';
  } else {
    document.documentElement.removeAttribute('data-theme');
    if (btnText) btnText.textContent = 'Dark';
    toggleBtn.querySelector('i').className = 'fa-solid fa-moon';
  }

  toggleBtn.addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('chirag_theme', 'light');
      if (btnText) btnText.textContent = 'Dark';
      toggleBtn.querySelector('i').className = 'fa-solid fa-moon';
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('chirag_theme', 'dark');
      if (btnText) btnText.textContent = 'Light';
      toggleBtn.querySelector('i').className = 'fa-solid fa-sun';
    }
  });
}

/* ===================================================================
   2. NAVIGATION & SMOOTH SCROLLSPY
   =================================================================== */
function initNavigation() {
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');
  const links = document.querySelectorAll('.nav-link');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  links.forEach(link => {
    link.addEventListener('click', () => {
      if (navLinks) navLinks.classList.remove('open');
    });
  });

  // Scrollspy
  window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 100;
      const sectionId = current.getAttribute('id');
      const targetLink = document.querySelector(`.nav-link[href*="${sectionId}"]`);

      if (targetLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          targetLink.classList.add('active');
        } else {
          targetLink.classList.remove('active');
        }
      }
    });
  });
}

/* ===================================================================
   3. RENDER DOMAINS
   =================================================================== */
function renderDomains() {
  const grid = document.getElementById('domains-grid');
  if (!grid) return;

  grid.innerHTML = CHIRAG_DATA.domains.map(d => `
    <div class="domain-card" style="--domain-color: ${d.color};">
      <div class="domain-header">
        <div class="domain-icon-box">
          <i class="fa-solid ${d.icon}"></i>
        </div>
        <span class="domain-badge">${escapeHtml(d.badge)}</span>
      </div>
      <h3 class="domain-title">${escapeHtml(d.title)}</h3>
      <p class="domain-desc">${escapeHtml(d.description)}</p>
      <div class="domain-skills">
        ${d.skills.map(s => `<span class="domain-skill-tag">${escapeHtml(s)}</span>`).join('')}
      </div>
    </div>
  `).join('');
}

/* ===================================================================
   4. RENDER EXPERIENCES TIMELINE
   =================================================================== */
function renderExperiences() {
  const timeline = document.getElementById('timeline-list');
  if (!timeline) return;

  timeline.innerHTML = CHIRAG_DATA.experiences.map(e => `
    <div class="timeline-item">
      <div class="timeline-node"></div>
      <div class="timeline-card">
        <div class="timeline-header">
          <div class="timeline-title-group">
            <img src="${escapeHtml(e.logo)}" alt="${escapeHtml(e.company)}" class="timeline-logo" onerror="this.src='assets/img/siteLogo.png'">
            <div>
              <h3 class="timeline-role">${escapeHtml(e.role)}</h3>
              <div class="timeline-company">${escapeHtml(e.company)}</div>
            </div>
          </div>
          <div class="timeline-meta">
            <span><i class="fa-regular fa-calendar"></i> ${escapeHtml(e.period)}</span>
            <span class="timeline-type-pill">${escapeHtml(e.type)}</span>
          </div>
        </div>
        <div class="timeline-highlight">
          <i class="fa-solid fa-crosshairs"></i> ${escapeHtml(e.highlight)}
        </div>
        <ul class="timeline-bullets">
          ${e.bullets.map(b => `<li>${escapeHtml(b)}</li>`).join('')}
        </ul>
        <div class="timeline-tags">
          ${e.tags.map(t => `<span class="timeline-tag">${escapeHtml(t)}</span>`).join('')}
        </div>
      </div>
    </div>
  `).join('');
}

/* ===================================================================
   5. RENDER PUBLICATIONS & RESEARCH
   =================================================================== */
function renderPublications() {
  const grid = document.getElementById('publications-grid');
  if (!grid) return;

  grid.innerHTML = CHIRAG_DATA.publications.map(p => `
    <div class="pub-card">
      <div class="pub-badge-row">
        <span class="pub-badge">${escapeHtml(p.badge)}</span>
        <span class="pub-year">${escapeHtml(p.year)}</span>
      </div>
      <h3 class="pub-title">${escapeHtml(p.title)}</h3>
      <div class="pub-venue">
        <i class="fa-solid fa-book-bookmark"></i> ${escapeHtml(p.venue)}
      </div>
      <p class="pub-abstract">${escapeHtml(p.abstract)}</p>
      <div class="pub-footer">
        <span class="domain-skill-tag"><i class="fa-solid fa-tag"></i> ${escapeHtml(p.category)}</span>
        <a href="${escapeHtml(p.link)}" target="_blank" rel="noopener noreferrer" class="pub-link">
          Read / Citations <i class="fa-solid fa-arrow-up-right-from-square"></i>
        </a>
      </div>
    </div>
  `).join('');
}

/* ===================================================================
   6. PROJECTS FILTER & STAR MODAL
   =================================================================== */
function initProjectsFilter() {
  const grid = document.getElementById('projects-grid');
  const pills = document.querySelectorAll('.project-filter-pill');
  const searchInput = document.getElementById('project-search');
  if (!grid) return;

  let currentCategory = 'all';
  let searchTerm = '';

  function filterProjects() {
    const filtered = CHIRAG_DATA.projects.filter(p => {
      const matchesCat = (currentCategory === 'all') || (p.category.toLowerCase().includes(currentCategory.toLowerCase()));
      const matchesSearch = !searchTerm || (
        p.title.toLowerCase().includes(searchTerm) ||
        p.summary.toLowerCase().includes(searchTerm) ||
        p.tags.some(t => t.toLowerCase().includes(searchTerm)) ||
        (p.star && Object.values(p.star).some(v => v.toLowerCase().includes(searchTerm)))
      );
      return matchesCat && matchesSearch;
    });

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted); font-family: var(--font-mono);">
          <i class="fa-solid fa-magnifying-glass" style="font-size: 2rem; margin-bottom: 12px; color: var(--accent-cyan);"></i>
          <p>No defense projects match the filter "${escapeHtml(searchTerm)}".</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = filtered.map(p => `
      <div class="project-card" data-id="${p.id}">
        <div class="project-meta-top">
          <span class="project-category">${escapeHtml(p.category)}</span>
          <span class="domain-skill-tag"><i class="fa-solid fa-check"></i> Verified</span>
        </div>
        <h3 class="project-title">${escapeHtml(p.title)}</h3>
        <p class="project-desc">${escapeHtml(p.summary)}</p>
        <div class="project-tags">
          ${p.tags.map(t => `<span class="project-tag">${escapeHtml(t)}</span>`).join('')}
        </div>
        <div class="project-actions">
          <button class="star-btn" onclick="openStarModal('${p.id}')">
            <i class="fa-solid fa-diagram-project"></i> STAR Analysis
          </button>
          ${p.links && p.links[0] ? `
            <a href="${escapeHtml(p.links[0].url)}" target="_blank" rel="noopener noreferrer" class="pub-link">
              ${escapeHtml(p.links[0].text)} <i class="fa-solid fa-arrow-up-right-from-square"></i>
            </a>
          ` : ''}
        </div>
      </div>
    `).join('');
  }

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentCategory = pill.getAttribute('data-cat') || 'all';
      filterProjects();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.trim().toLowerCase();
      filterProjects();
    });
  }

  filterProjects();
}

// Global modal trigger for STAR analysis
window.openStarModal = function(projectId) {
  const project = CHIRAG_DATA.projects.find(p => p.id === projectId);
  if (!project || !project.star) return;

  const modal = document.getElementById('star-modal');
  const titleEl = document.getElementById('modal-project-title');
  const bodyEl = document.getElementById('modal-star-body');

  titleEl.textContent = project.title;

  bodyEl.innerHTML = `
    <div style="margin-bottom: 16px; font-size: 0.92rem; color: var(--text-secondary);">
      ${escapeHtml(project.summary)}
    </div>
    <div class="star-section">
      <div class="star-block situation">
        <div class="star-block-label">📍 SITUATION (CONTEXT)</div>
        <div class="star-block-text">${escapeHtml(project.star.situation || 'Operational deployment requirement.')}</div>
      </div>
      <div class="star-block task">
        <div class="star-block-label">🎯 TASK (OBJECTIVE)</div>
        <div class="star-block-text">${escapeHtml(project.star.task || 'Architect resilient defense capability.')}</div>
      </div>
      <div class="star-block action">
        <div class="star-block-label">⚡ ACTION (EXECUTION & STACK)</div>
        <div class="star-block-text">${escapeHtml(project.star.action || 'Engineered automated pipelines and security controls.')}</div>
      </div>
      <div class="star-block result">
        <div class="star-block-label">🏆 RESULT (IMPACT & METRICS)</div>
        <div class="star-block-text">${escapeHtml(project.star.result || 'Production-verified zero defect resolution.')}</div>
      </div>
    </div>
  `;

  modal.classList.add('active');
};

/* ===================================================================
   7. CERTIFICATES VAULT & FILTER
   =================================================================== */
function initCertsFilter() {
  const grid = document.getElementById('certs-grid');
  const pills = document.querySelectorAll('.cert-filter-pill');
  const searchInput = document.getElementById('cert-search');
  const countEl = document.getElementById('cert-active-count');
  if (!grid) return;

  let currentCategory = 'all';
  let searchTerm = '';

  function filterCerts() {
    const filtered = CHIRAG_DATA.certificates.filter(c => {
      const matchesCat = (currentCategory === 'all') || (c.category.toLowerCase() === currentCategory.toLowerCase());
      const matchesSearch = !searchTerm || (
        c.name.toLowerCase().includes(searchTerm) ||
        c.issuer.toLowerCase().includes(searchTerm) ||
        (c.details && c.details.toLowerCase().includes(searchTerm))
      );
      return matchesCat && matchesSearch;
    });

    if (countEl) countEl.textContent = `${filtered.length} / ${CHIRAG_DATA.certificates.length}`;

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted); font-family: var(--font-mono);">
          <p>No credentials match "${escapeHtml(searchTerm)}".</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = filtered.map(c => `
      <div class="cert-card">
        <div class="cert-badge-row">
          <span class="cert-issuer"><i class="fa-solid fa-award"></i> ${escapeHtml(c.issuer)}</span>
          <span class="cert-category-tag">${escapeHtml(c.category)}</span>
        </div>
        <h4 class="cert-name">${escapeHtml(c.name)}</h4>
        <p class="cert-details">${escapeHtml(c.details || 'Verified professional credential.')}</p>
      </div>
    `).join('');
  }

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentCategory = pill.getAttribute('data-cat') || 'all';
      filterCerts();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.trim().toLowerCase();
      filterCerts();
    });
  }

  filterCerts();
}

/* ===================================================================
   8. UTILITIES & TOOLS
   =================================================================== */
function renderUtilities() {
  const list = document.getElementById('utils-list');
  if (!list) return;

  list.innerHTML = CHIRAG_DATA.utilities.map(u => `
    <div class="util-card">
      <div class="util-header">
        <h4 class="util-title">${escapeHtml(u.name)}</h4>
        <span class="util-badge">${escapeHtml(u.badge)}</span>
      </div>
      <p class="util-desc">${escapeHtml(u.description)}</p>
      <div class="util-metrics">
        <i class="fa-solid fa-microchip text-cyan"></i> ${escapeHtml(u.metrics)}
      </div>
    </div>
  `).join('');
}

/* ===================================================================
   9. INTERACTIVE CYBERSECURITY QUIZ ENGINE
   =================================================================== */
function initInteractiveQuiz() {
  const counterEl = document.getElementById('quiz-counter');
  const questionEl = document.getElementById('quiz-question');
  const optionsEl = document.getElementById('quiz-options');
  const feedbackEl = document.getElementById('quiz-feedback');
  const nextBtn = document.getElementById('quiz-next-btn');
  const scoreBadge = document.getElementById('quiz-score-badge');

  if (!questionEl || !optionsEl) return;

  let currentIndex = 0;
  let score = 0;
  let answered = false;
  const questions = CHIRAG_DATA.quizzes;

  function loadQuestion(index) {
    answered = false;
    const q = questions[index];

    counterEl.textContent = `QUESTION ${index + 1} OF ${questions.length}`;
    questionEl.textContent = q.question;
    feedbackEl.style.display = 'none';
    feedbackEl.innerHTML = '';
    nextBtn.style.display = 'none';

    optionsEl.innerHTML = q.options.map((opt, i) => `
      <button class="quiz-option-btn" data-index="${i}">
        ${String.fromCharCode(65 + i)}. ${escapeHtml(opt)}
      </button>
    `).join('');

    const btns = optionsEl.querySelectorAll('.quiz-option-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        if (answered) return;
        answered = true;

        const selectedIndex = parseInt(btn.getAttribute('data-index'), 10);
        if (selectedIndex === q.correct) {
          btn.classList.add('correct');
          score++;
          scoreBadge.textContent = `SCORE: ${score}/${questions.length}`;
          feedbackEl.innerHTML = `<strong><i class="fa-solid fa-circle-check text-emerald"></i> Correct!</strong> ${escapeHtml(q.explanation)}`;
        } else {
          btn.classList.add('wrong');
          btns[q.correct].classList.add('correct');
          feedbackEl.innerHTML = `<strong><i class="fa-solid fa-circle-xmark" style="color:var(--accent-rose)"></i> Incorrect.</strong> ${escapeHtml(q.explanation)}`;
        }

        feedbackEl.style.display = 'block';
        nextBtn.style.display = 'inline-flex';
        nextBtn.textContent = (currentIndex === questions.length - 1) ? 'View Final Assessment' : 'Next Question ▹';
      });
    });
  }

  nextBtn.addEventListener('click', () => {
    if (currentIndex < questions.length - 1) {
      currentIndex++;
      loadQuestion(currentIndex);
    } else {
      // Quiz Finished
      counterEl.textContent = 'ASSESSMENT COMPLETED';
      questionEl.textContent = `Security Aptitude Evaluation: ${score} / ${questions.length} Correct`;
      optionsEl.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 20px; text-align: center;">
          <h4 style="color: var(--accent-cyan); font-size: 1.2rem; margin-bottom: 8px;">
            ${score >= 4 ? 'Rank: Elite Security Operative 🛡️' : 'Rank: Cyber Defender Apprentice 🔍'}
          </h4>
          <p style="color: var(--text-secondary); font-size: 0.9rem;">
            ${score >= 4 
              ? 'Outstanding technical mastery across Zero-Trust, Swarm Defense algorithms, and Cryptography!' 
              : 'Good knowledge base! Explore Chirag\'s publications and blog archives for deep technical architectures.'}
          </p>
        </div>
      `;
      feedbackEl.style.display = 'none';
      nextBtn.textContent = 'Restart Quiz ↺';
      nextBtn.onclick = () => {
        currentIndex = 0;
        score = 0;
        scoreBadge.textContent = `SCORE: 0/${questions.length}`;
        nextBtn.onclick = null;
        loadQuestion(0);
      };
    }
  });

  loadQuestion(0);
}

/* ===================================================================
   10. TESTIMONIALS & ENDORSEMENTS
   =================================================================== */
function renderTestimonials() {
  const grid = document.getElementById('testimonials-grid');
  if (!grid) return;

  grid.innerHTML = CHIRAG_DATA.testimonials.map(t => `
    <div class="test-card">
      <div class="test-quote">"${escapeHtml(t.quote)}"</div>
      <div class="test-author-row">
        <div>
          <div class="test-author">${escapeHtml(t.author)}</div>
          <div class="test-role">${escapeHtml(t.role)}</div>
        </div>
        <span class="test-badge">${escapeHtml(t.badge)}</span>
      </div>
    </div>
  `).join('');
}

/* ===================================================================
   11. BLOGS & THOUGHT LEADERSHIP
   =================================================================== */
function renderBlogs() {
  const grid = document.getElementById('blogs-grid');
  if (!grid) return;

  grid.innerHTML = CHIRAG_DATA.blogs.map(b => `
    <div class="blog-card">
      <div class="blog-top-row">
        <span><i class="fa-regular fa-clock"></i> ${escapeHtml(b.readTime)}</span>
        <span>${escapeHtml(b.date)}</span>
      </div>
      <h3 class="blog-title">${escapeHtml(b.title)}</h3>
      <p class="blog-summary">${escapeHtml(b.summary)}</p>
      <div class="blog-tags">
        ${b.tags.map(t => `<span class="blog-tag">#${escapeHtml(t)}</span>`).join('')}
      </div>
      <a href="${escapeHtml(b.link)}" target="_blank" rel="noopener noreferrer" class="pub-link" style="margin-top: auto;">
        Read Full Article <i class="fa-solid fa-arrow-up-right-from-square"></i>
      </a>
    </div>
  `).join('');
}

/* ===================================================================
   12. INTERACTIVE CYBER CLI TERMINAL
   =================================================================== */
function initTerminal() {
  const terminal = document.getElementById('terminal-drawer');
  const toggleBtn = document.getElementById('terminal-toggle-btn');
  const closeBtn = document.getElementById('terminal-close-btn');
  const input = document.getElementById('terminal-input');
  const history = document.getElementById('terminal-history');

  if (!terminal || !input) return;

  function toggleTerminal() {
    terminal.classList.toggle('open');
    if (terminal.classList.contains('open')) {
      input.focus();
    }
  }

  if (toggleBtn) toggleBtn.addEventListener('click', toggleTerminal);
  if (closeBtn) closeBtn.addEventListener('click', toggleTerminal);

  // Press ~ or ` or F2 to toggle terminal
  window.addEventListener('keydown', (e) => {
    if (e.key === '`' || e.key === '~') {
      if (document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        toggleTerminal();
      }
    }
    if (e.key === 'Escape' && terminal.classList.contains('open')) {
      terminal.classList.remove('open');
    }
  });

  const commands = {
    help: () => `
Available system commands:
  <span class="text-cyan">whoami</span>        - Inspect Chirag's identity & certifications
  <span class="text-cyan">domains</span>       - Core cybersecurity mastery areas
  <span class="text-cyan">projects</span>      - List all 21 defense & software projects
  <span class="text-cyan">research</span>      - High-impact publications (Nature, IEEE, Springer)
  <span class="text-cyan">certs</span>         - Summary of 47+ verified certifications
  <span class="text-cyan">exp</span>           - Work history (TCS, SECURE CoE, VTF, Police)
  <span class="text-cyan">contact</span>       - Direct communication channels
  <span class="text-cyan">clear</span>         - Purge console screen buffer
    `,
    whoami: () => `
<span class="text-cyan">Chirag Ganguli</span> | Cybersecurity Researcher & Ex-Technical Lead @ TCS
Degrees: B.Tech in CSE (Cyber Security & Forensics) - VIT (Raman Research Awardee)
Elite Accreditations: Certified Ethical Hacker (CEH) • Lean Six Sigma Black Belt (LSSBB)
Email: <a href="mailto:contact@chiragganguli.com" class="text-cyan">contact@chiragganguli.com</a>
    `,
    domains: () => CHIRAG_DATA.domains.map(d => `• <span class="text-cyan">${d.title}</span> (${d.badge})`).join('<br>'),
    projects: () => `Total Projects: 21<br>` + CHIRAG_DATA.projects.map((p, i) => `${i + 1}. [${p.category}] <span class="text-cyan">${p.title}</span>`).join('<br>'),
    research: () => CHIRAG_DATA.publications.map((p, i) => `${i + 1}. <span class="text-cyan">${p.title}</span> (${p.venue})`).join('<br>'),
    certs: () => `Total Credentials: 47+<br>Highlights: CEH, Lean Six Sigma Black Belt, Raman Research Award, 8x Google Cloud Security Badges, NVIDIA CUDA/Deep Learning, TCS Xcelerate Warrior.`,
    exp: () => CHIRAG_DATA.experiences.map(e => `• <span class="text-cyan">${e.role}</span> @ ${e.company} (${e.period})`).join('<br>'),
    contact: () => `
Email: <a href="mailto:contact@chiragganguli.com" class="text-cyan">contact@chiragganguli.com</a>
LinkedIn: <a href="${CHIRAG_DATA.bio.socials.linkedin}" target="_blank" class="text-cyan">chiragganguli.com/links/linkedin</a>
GitHub: <a href="${CHIRAG_DATA.bio.socials.github}" target="_blank" class="text-cyan">chiragganguli.com/links/github</a>
Topmate 1:1 Mentorship: <a href="${CHIRAG_DATA.bio.socials.topmate}" target="_blank" class="text-cyan">topmate.io/chiragganguli</a>
    `,
    clear: () => {
      history.innerHTML = '';
      return '';
    }
  };

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const rawCmd = input.value.trim();
      const cmd = rawCmd.toLowerCase();
      input.value = '';

      if (!cmd) return;

      const cmdRow = document.createElement('div');
      cmdRow.innerHTML = `<span class="terminal-prompt-symbol">chirag@defense-hub:~$</span> ${escapeHtml(rawCmd)}`;
      history.appendChild(cmdRow);

      if (cmd === 'clear') {
        commands.clear();
        return;
      }

      const outputRow = document.createElement('div');
      outputRow.style.color = '#cbd5e1';
      outputRow.style.marginBottom = '10px';

      if (commands[cmd]) {
        outputRow.innerHTML = commands[cmd]();
      } else {
        outputRow.innerHTML = `command not found: "${escapeHtml(rawCmd)}". Type <span class="text-cyan">help</span> for valid directives.`;
      }

      history.appendChild(outputRow);
      history.scrollTop = history.scrollHeight;
    }
  });
}

/* ===================================================================
   13. MODALS & DIGITAL VCARD DOWNLOAD
   =================================================================== */
function initModals() {
  const starModal = document.getElementById('star-modal');
  const closeBtn = document.getElementById('modal-close-btn');

  if (starModal && closeBtn) {
    closeBtn.addEventListener('click', () => {
      starModal.classList.remove('active');
    });

    starModal.addEventListener('click', (e) => {
      if (e.target === starModal) {
        starModal.classList.remove('active');
      }
    });
  }

  // Copy email helper
  window.copyEmail = function() {
    navigator.clipboard.writeText('contact@chiragganguli.com').then(() => {
      alert('Copied contact@chiragganguli.com to clipboard!');
    }).catch(() => {
      prompt('Copy email:', 'contact@chiragganguli.com');
    });
  };

  // Generate & Download vCard
  window.downloadVCard = function() {
    const vCardData = `BEGIN:VCARD
VERSION:3.0
FN:Chirag Ganguli
N:Ganguli;Chirag;;;
TITLE:Cybersecurity Researcher & Certified Ethical Hacker
ORG:Independent / Ex-Tata Consultancy Services
EMAIL;TYPE=INTERNET,PREF:contact@chiragganguli.com
URL:https://chiragganguli.com
NOTE:Raman Research Awardee | Lean Six Sigma Black Belt | Cloud Security Specialist
END:VCARD`;

    const blob = new Blob([vCardData], { type: 'text/vcard;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'Chirag_Ganguli_Security.vcf');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
}

// Utility to escape HTML to prevent XSS
function escapeHtml(str) {
  if (typeof str !== 'string') return str;
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
