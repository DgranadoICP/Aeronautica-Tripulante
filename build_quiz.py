import json
import sys

with open('questions_final.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('explanations.json', 'r', encoding='utf-8') as f:
    explanations = json.load(f)

questions_js = json.dumps(questions, ensure_ascii=False)
explanations_js = json.dumps(explanations, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Examen Tripulante de Cabina</title>
<style>
:root {
  --bg: #f5f5f7;
  --card: #ffffff;
  --text: #1d1d1f;
  --text2: #6e6e73;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --green: #34c759;
  --red: #ff3b30;
  --orange: #ff9500;
  --border: #d2d2d7;
  --track: #e5e5ea;
  --option-bg: #f5f5f7;
  --toast-bg: #1d1d1f;
  --accent-tint: rgba(0,113,227,0.10);
  --accent-tint-strong: rgba(0,113,227,0.18);
  --green-tint: rgba(52,199,89,0.10);
  --green-tint-strong: rgba(52,199,89,0.15);
  --red-tint: rgba(255,59,48,0.10);
  --orange-tint: rgba(255,149,0,0.10);
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --radius: 16px;
}

:root[data-theme="dark"] {
  --bg: #000000;
  --card: #1c1c1e;
  --text: #f5f5f7;
  --text2: #98989d;
  --accent: #0a84ff;
  --accent-hover: #409cff;
  --green: #30d158;
  --red: #ff453a;
  --orange: #ff9f0a;
  --border: #38383a;
  --track: #2c2c2e;
  --option-bg: #2c2c2e;
  --toast-bg: #2c2c2e;
  --accent-tint: rgba(10,132,255,0.18);
  --accent-tint-strong: rgba(10,132,255,0.30);
  --green-tint: rgba(48,209,88,0.18);
  --green-tint-strong: rgba(48,209,88,0.22);
  --red-tint: rgba(255,69,58,0.18);
  --orange-tint: rgba(255,159,10,0.18);
  --shadow: 0 2px 14px rgba(0,0,0,0.4);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* HEADER */
.header {
  text-align: center;
  padding: 40px 20px 20px;
}

.header h1 {
  font-size: 2em;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.header p {
  color: var(--text2);
  font-size: 1.1em;
}

/* HOME SCREEN */
.home-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin: 24px 0;
}

.stat-card {
  background: var(--card);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: var(--shadow);
}

.stat-card .number {
  font-size: 1.8em;
  font-weight: 700;
  color: var(--accent);
}

.stat-card .label {
  font-size: 0.8em;
  color: var(--text2);
  margin-top: 4px;
}

.rounds-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 24px 0;
}

.round-card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.round-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}

.round-card.completed {
  border-color: var(--green);
}

.round-card.in-progress {
  border-color: var(--orange);
}

.round-card .round-progress {
  margin-top: 12px;
  font-size: 0.95em;
  font-weight: 600;
  color: var(--orange);
}

.round-card .progress-mini {
  height: 4px;
  background: var(--track);
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.round-card .progress-mini-fill {
  height: 100%;
  background: var(--orange);
  border-radius: 2px;
}

.restart-round-link {
  display: block;
  width: 100%;
  text-align: center;
  background: none;
  border: none;
  color: var(--text2);
  font-size: 0.85em;
  font-weight: 500;
  cursor: pointer;
  padding: 8px;
  margin-bottom: 12px;
  text-decoration: underline;
}

.restart-round-link:hover { color: var(--red); }

.round-card .round-number {
  font-size: 0.85em;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.round-card .round-title {
  font-size: 1.3em;
  font-weight: 700;
  margin: 6px 0;
}

.round-card .round-info {
  font-size: 0.85em;
  color: var(--text2);
}

.round-card .round-score {
  margin-top: 12px;
  font-size: 1.1em;
  font-weight: 600;
  color: var(--green);
}

.round-card .round-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--green);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  display: none;
}

.round-card.completed .round-badge { display: flex; }
.round-card.in-progress .round-badge {
  display: flex;
  background: var(--orange);
}

.shuffle-btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 16px;
}

.shuffle-btn:hover { background: var(--accent-hover); }

.reset-btn {
  display: block;
  width: 100%;
  padding: 14px;
  background: transparent;
  color: var(--red);
  border: 1px solid var(--red);
  border-radius: 12px;
  font-size: 0.95em;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
}

/* QUIZ SCREEN */
.quiz-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1.1em;
  color: var(--accent);
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.quiz-progress-text {
  font-size: 0.9em;
  color: var(--text2);
  font-weight: 500;
}

.quiz-score-live {
  font-size: 0.9em;
  font-weight: 600;
  color: var(--accent);
}

.progress-bar-container {
  width: 100%;
  height: 6px;
  background: var(--track);
  border-radius: 3px;
  margin-bottom: 24px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--accent);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.category-tag {
  display: inline-block;
  padding: 4px 12px;
  background: var(--accent-tint);
  color: var(--accent);
  border-radius: 20px;
  font-size: 0.8em;
  font-weight: 600;
  margin-bottom: 16px;
}

.question-card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 28px;
  box-shadow: var(--shadow);
  margin-bottom: 20px;
}

.question-text {
  font-size: 1.1em;
  font-weight: 500;
  line-height: 1.5;
  margin-bottom: 24px;
  color: var(--text);
}

.feedback-card .fb-text { color: var(--text); }
.review-item .ri-q { color: var(--text); }

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: var(--option-bg);
  border: 2px solid transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  font-size: 0.95em;
  line-height: 1.4;
  color: var(--text);
  font-family: inherit;
  width: 100%;
}

.option-btn:hover:not(.disabled) {
  border-color: var(--accent);
  background: var(--accent-tint);
}

.option-btn .option-letter {
  min-width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--card);
  border: 2px solid var(--border);
  color: var(--text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85em;
  flex-shrink: 0;
}

.option-btn.correct {
  border-color: var(--green);
  background: var(--green-tint);
}

.option-btn.correct .option-letter {
  background: var(--green);
  border-color: var(--green);
  color: white;
}

.option-btn.wrong {
  border-color: var(--red);
  background: var(--red-tint);
}

.option-btn.wrong .option-letter {
  background: var(--red);
  border-color: var(--red);
  color: white;
}

.option-btn.disabled { pointer-events: none; }
.option-btn.dimmed { opacity: 0.5; }

.feedback-card {
  border-radius: 12px;
  padding: 20px;
  margin-top: 16px;
  animation: slideUp 0.3s ease;
  line-height: 1.5;
}

.feedback-card.correct-fb {
  background: var(--green-tint);
  border-left: 4px solid var(--green);
}

.feedback-card.wrong-fb {
  background: var(--red-tint);
  border-left: 4px solid var(--red);
}

.feedback-card .fb-title {
  font-weight: 700;
  font-size: 1em;
  margin-bottom: 8px;
}

.feedback-card.correct-fb .fb-title { color: var(--green); }
.feedback-card.wrong-fb .fb-title { color: var(--red); }

.feedback-card .fb-text {
  font-size: 0.95em;
  color: var(--text);
}

.next-btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05em;
  font-weight: 600;
  cursor: pointer;
  margin-top: 20px;
  transition: background 0.2s;
}

.next-btn:hover { background: var(--accent-hover); }

/* RESULTS SCREEN */
.results-card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 40px 28px;
  box-shadow: var(--shadow);
  text-align: center;
  margin: 20px 0;
}

.results-score-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  margin: 0 auto 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  position: relative;
}

.results-score-circle .big-number {
  font-size: 2.8em;
  line-height: 1;
}

.results-score-circle .out-of {
  font-size: 0.9em;
  opacity: 0.7;
}

.results-score-circle.excellent { background: var(--green-tint-strong); color: var(--green); }
.results-score-circle.good { background: var(--accent-tint); color: var(--accent); }
.results-score-circle.average { background: var(--orange-tint); color: var(--orange); }
.results-score-circle.poor { background: var(--red-tint); color: var(--red); }

.results-message {
  font-size: 1.3em;
  font-weight: 600;
  margin-bottom: 8px;
}

.results-detail {
  color: var(--text2);
  margin-bottom: 24px;
}

.results-breakdown {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 24px 0;
}

.breakdown-item {
  padding: 16px;
  border-radius: 12px;
  background: var(--bg);
}

.breakdown-item .bi-number {
  font-size: 1.5em;
  font-weight: 700;
}

.breakdown-item .bi-label {
  font-size: 0.8em;
  color: var(--text2);
}

.breakdown-item.correct-bi .bi-number { color: var(--green); }
.breakdown-item.wrong-bi .bi-number { color: var(--red); }

.review-section {
  margin-top: 24px;
  text-align: left;
}

.review-section h3 {
  font-size: 1.1em;
  margin-bottom: 12px;
  color: var(--text);
}

.review-item {
  background: var(--card);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 8px;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--red);
}

.review-item .ri-q {
  font-size: 0.9em;
  font-weight: 500;
  margin-bottom: 6px;
}

.review-item .ri-answer {
  font-size: 0.85em;
  color: var(--text2);
}

.review-item .ri-correct {
  font-size: 0.85em;
  color: var(--green);
  font-weight: 600;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.hidden { display: none !important; }

/* THEME TOGGLE */
.theme-toggle {
  position: fixed;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  box-shadow: var(--shadow);
  transition: transform 0.15s ease, background 0.2s, border-color 0.2s;
  -webkit-tap-highlight-color: transparent;
}
.theme-toggle:hover { transform: scale(1.05); }
.theme-toggle:active { transform: scale(0.94); }
.theme-toggle svg { display: block; }
.theme-toggle .icon-sun { display: none; }
.theme-toggle .icon-moon { display: block; }
:root[data-theme="dark"] .theme-toggle .icon-sun { display: block; }
:root[data-theme="dark"] .theme-toggle .icon-moon { display: none; }

/* SESSION BAR */
.session-bar {
  background: var(--card);
  border-radius: 12px;
  padding: 14px 16px;
  margin: 16px 0;
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.session-info { flex: 1; min-width: 0; }
.session-label {
  font-size: 0.72em;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}
.session-code {
  font-size: 1.15em;
  font-weight: 700;
  font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
  color: var(--accent);
  letter-spacing: 0.05em;
  margin-top: 2px;
}
.session-actions { display: flex; gap: 8px; }
.session-btn {
  padding: 8px 14px;
  background: var(--accent-tint);
  color: var(--accent);
  border: none;
  border-radius: 8px;
  font-size: 0.85em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.session-btn:hover { background: var(--accent-tint-strong); }
.session-btn.outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
}
.session-btn.outline:hover { background: var(--bg); }
.sync-indicator {
  font-size: 0.72em;
  color: var(--text2);
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
}
.sync-indicator .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--green);
}
.sync-indicator.syncing .dot { background: var(--orange); animation: pulse 1s infinite; }
.sync-indicator.error .dot { background: var(--red); }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }

/* MODAL */
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 100; padding: 20px;
}
.modal {
  background: var(--card);
  border-radius: var(--radius);
  padding: 28px;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0,0,0,0.25);
}
.modal h3 { font-size: 1.3em; font-weight: 700; margin-bottom: 8px; }
.modal p { color: var(--text2); font-size: 0.95em; margin-bottom: 16px; line-height: 1.45; }
.modal input {
  width: 100%;
  padding: 14px;
  border: 2px solid var(--border);
  border-radius: 12px;
  font-size: 1em;
  font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
  margin-bottom: 16px;
  background: var(--bg);
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: center;
}
.modal input:focus { outline: none; border-color: var(--accent); }
.modal-actions { display: flex; gap: 8px; }
.modal-actions button {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  border: none;
  font-size: 0.95em;
  font-weight: 600;
  cursor: pointer;
}
.modal-actions .cancel { background: transparent; border: 1px solid var(--border); color: var(--text); }
.modal-actions .confirm { background: var(--accent); color: white; }
.modal-error { color: var(--red); font-size: 0.85em; margin-top: -8px; margin-bottom: 12px; min-height: 18px; }

.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--toast-bg);
  color: white;
  padding: 12px 22px;
  border-radius: 24px;
  font-size: 0.9em;
  font-weight: 500;
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  animation: slideUp 0.3s ease;
  z-index: 200;
  max-width: 90%;
  text-align: center;
}

/* Responsive */
@media (max-width: 600px) {
  .home-stats { grid-template-columns: repeat(3, 1fr); }
  .rounds-grid { grid-template-columns: 1fr; }
  .header h1 { font-size: 1.6em; }
  .question-card { padding: 20px; }
  .results-breakdown { grid-template-columns: 1fr 1fr; }
}
</style>
<script>
// Theme init — runs before paint to avoid flash
(function(){
  try {
    var stored = localStorage.getItem('tcq_theme');
    var theme = (stored === 'light' || stored === 'dark')
      ? stored
      : (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
  } catch(e) {}
})();
</script>
</head>
<body>

<button class="theme-toggle" onclick="toggleTheme()" aria-label="Cambiar tema">
  <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </svg>
  <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="4"/>
    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
  </svg>
</button>

<div class="container">
  <!-- HOME SCREEN -->
  <div id="home-screen">
    <div class="header">
      <h1>Tripulante de Cabina</h1>
      <p>Guía de estudio para licencia</p>
    </div>

    <div class="session-bar">
      <div class="session-info">
        <div class="session-label">Tu código de sesión</div>
        <div class="session-code" id="session-code">—</div>
        <div class="sync-indicator" id="sync-indicator">
          <span class="dot"></span>
          <span id="sync-text">Local</span>
        </div>
      </div>
      <div class="session-actions">
        <button class="session-btn" onclick="copyCode()">Copiar</button>
        <button class="session-btn outline" onclick="openRecoverModal()">Recuperar</button>
      </div>
    </div>

    <div class="home-stats">
      <div class="stat-card">
        <div class="number" id="total-questions">''' + str(len(questions)) + r'''</div>
        <div class="label">Preguntas</div>
      </div>
      <div class="stat-card">
        <div class="number" id="rounds-completed">0/6</div>
        <div class="label">Rondas</div>
      </div>
      <div class="stat-card">
        <div class="number" id="avg-score">--</div>
        <div class="label">Promedio</div>
      </div>
    </div>

    <div class="rounds-grid" id="rounds-grid"></div>

    <button class="shuffle-btn" onclick="shuffleDay()">Mezclar preguntas del día</button>
    <button class="reset-btn" onclick="resetAll()">Reiniciar todo</button>
  </div>

  <!-- QUIZ SCREEN -->
  <div id="quiz-screen" class="hidden">
    <div class="quiz-header">
      <button class="back-btn" onclick="goHome()">← Rondas</button>
      <span class="quiz-progress-text" id="progress-text">1 / 100</span>
      <span class="quiz-score-live" id="score-live">0 pts</span>
    </div>
    <div class="progress-bar-container">
      <div class="progress-bar" id="progress-bar"></div>
    </div>
    <button class="restart-round-link" onclick="restartRound()">↻ Reiniciar esta ronda</button>
    <div id="question-area"></div>
  </div>

  <!-- RESULTS SCREEN -->
  <div id="results-screen" class="hidden"></div>
</div>

<div id="modal-container"></div>
<div id="toast-container"></div>

<script>
const ALL_QUESTIONS = ''' + questions_js + r''';

const EXPLANATIONS = ''' + explanations_js + r''';

function getExplanation(q) {
  const id = String(q.id);
  if (EXPLANATIONS[id]) return EXPLANATIONS[id];

  const correct = q.correct;
  const correctText = q[correct] || '';
  return `La respuesta correcta es la opción ${correct}: ${correctText}.`;
}

/* Old pattern-matching removed — all explanations now in EXPLANATIONS dict */

// THEME
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('tcq_theme', next); } catch(e) {}
}

// PANTRY SYNC CONFIG
const PANTRY_ID = 'b6e26746-6952-467b-b17e-06c78cbd1375';
const PANTRY_BASE = `https://getpantry.cloud/apiv1/pantry/${PANTRY_ID}/basket`;
const SESSION_WORDS = ['VUELO','PILOTO','AVION','CABINA','TRIPU','RUTA','TORRE','AEREO','DESPEGUE','VECTOR'];

// STATE
let state = {
  rounds: [],
  currentRound: -1,
  currentQ: 0,
  score: 0,
  answered: false,
  scores: [null,null,null,null,null,null],
  answers: [[],[],[],[],[],[]],
  sessionCode: null
};

let syncTimer = null;
let lastSyncStatus = 'local';

function generateSessionCode() {
  const word = SESSION_WORDS[Math.floor(Math.random() * SESSION_WORDS.length)];
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let suffix = '';
  for (let i = 0; i < 4; i++) suffix += chars[Math.floor(Math.random() * chars.length)];
  return `${word}-${suffix}`;
}

function loadState() {
  try {
    const s = localStorage.getItem('tcq_state');
    if (s) state = JSON.parse(s);
  } catch(e) {}
  if (!state.sessionCode) state.sessionCode = generateSessionCode();
}

function saveState() {
  localStorage.setItem('tcq_state', JSON.stringify(state));
  scheduleSync();
}

function setSyncStatus(status, text) {
  lastSyncStatus = status;
  const ind = document.getElementById('sync-indicator');
  const txt = document.getElementById('sync-text');
  if (!ind || !txt) return;
  ind.classList.remove('syncing','error');
  if (status === 'syncing') ind.classList.add('syncing');
  if (status === 'error') ind.classList.add('error');
  txt.textContent = text;
}

function scheduleSync() {
  if (syncTimer) clearTimeout(syncTimer);
  syncTimer = setTimeout(() => syncToPantry(), 2000);
}

async function syncToPantry() {
  if (!state.sessionCode) return;
  setSyncStatus('syncing', 'Sincronizando…');
  try {
    const payload = {
      rounds: state.rounds,
      scores: state.scores,
      answers: state.answers,
      currentRound: state.currentRound,
      currentQ: state.currentQ,
      score: state.score,
      updatedAt: Date.now()
    };
    const r = await fetch(`${PANTRY_BASE}/${state.sessionCode}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    setSyncStatus('ok', 'Sincronizado');
  } catch (e) {
    console.error('Sync failed', e);
    setSyncStatus('error', 'Sin conexión');
  }
}

async function loadFromPantry(code) {
  const r = await fetch(`${PANTRY_BASE}/${code}`);
  if (r.status === 400) throw new Error('Código no encontrado');
  if (!r.ok) throw new Error('HTTP ' + r.status);
  const data = await r.json();
  return data;
}

function copyCode() {
  if (!state.sessionCode) return;
  const code = state.sessionCode;
  navigator.clipboard?.writeText(code).then(() => {
    showToast(`Código ${code} copiado`);
  }).catch(() => {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = code;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); showToast(`Código ${code} copiado`); } catch(e) { showToast('No se pudo copiar'); }
    document.body.removeChild(ta);
  });
}

function showToast(msg) {
  const c = document.getElementById('toast-container');
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  c.appendChild(t);
  setTimeout(() => t.remove(), 2500);
}

function openRecoverModal() {
  const c = document.getElementById('modal-container');
  c.innerHTML = `
    <div class="modal-backdrop" onclick="if(event.target===this)closeModal()">
      <div class="modal">
        <h3>Recuperar progreso</h3>
        <p>Ingresa tu código de sesión para cargar tu progreso desde otro dispositivo.</p>
        <input type="text" id="recover-input" placeholder="VUELO-A3K2" maxlength="20" autocomplete="off" autocapitalize="characters">
        <div class="modal-error" id="recover-error"></div>
        <div class="modal-actions">
          <button class="cancel" onclick="closeModal()">Cancelar</button>
          <button class="confirm" onclick="doRecover()">Cargar</button>
        </div>
      </div>
    </div>
  `;
  setTimeout(() => {
    const input = document.getElementById('recover-input');
    if (input) {
      input.focus();
      input.addEventListener('keydown', e => { if (e.key === 'Enter') doRecover(); });
    }
  }, 50);
}

function closeModal() {
  document.getElementById('modal-container').innerHTML = '';
}

async function doRecover() {
  const input = document.getElementById('recover-input');
  const err = document.getElementById('recover-error');
  const code = (input.value || '').trim().toUpperCase();
  if (!code) { err.textContent = 'Ingresa un código.'; return; }
  if (code === state.sessionCode) { err.textContent = 'Ese ya es tu código actual.'; return; }
  err.textContent = 'Cargando…';
  try {
    const data = await loadFromPantry(code);
    if (!data || !data.rounds) throw new Error('Datos inválidos');
    state.rounds = data.rounds || [];
    state.scores = data.scores || [null,null,null,null,null,null];
    state.answers = data.answers || [[],[],[],[],[],[]];
    state.currentRound = -1;
    state.currentQ = 0;
    state.score = 0;
    state.answered = false;
    state.sessionCode = code;
    localStorage.setItem('tcq_state', JSON.stringify(state));
    closeModal();
    document.getElementById('session-code').textContent = code;
    showToast('Progreso recuperado');
    renderHome();
    setSyncStatus('ok', 'Sincronizado');
  } catch (e) {
    err.textContent = 'No se encontró ese código. Verifica e intenta de nuevo.';
  }
}

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function shuffleDay() {
  const shuffled = shuffleArray(ALL_QUESTIONS);
  const rounds = [];
  const totalPerRound = 100;

  // Distribute: first 5 rounds get ~100, round 6 gets remaining + some repeats
  for (let r = 0; r < 5; r++) {
    rounds.push(shuffled.slice(r * totalPerRound, (r + 1) * totalPerRound));
  }

  // Round 6: remaining questions + random fill to reach 100
  const remaining = shuffled.slice(500);
  const needed = totalPerRound - remaining.length;
  const fill = shuffleArray(ALL_QUESTIONS).slice(0, needed);
  rounds.push([...remaining, ...fill]);

  state.rounds = rounds;
  state.scores = [null,null,null,null,null,null];
  state.answers = [[],[],[],[],[],[]];
  state.currentRound = -1;
  saveState();
  renderHome();
}

function resetAll() {
  if (!confirm('¿Seguro que quieres reiniciar todo el progreso? Tu código de sesión se mantiene.')) return;
  const keepCode = state.sessionCode;
  state = { rounds: [], currentRound: -1, currentQ: 0, score: 0, answered: false, scores: [null,null,null,null,null,null], answers: [[],[],[],[],[],[]], sessionCode: keepCode };
  saveState();
  renderHome();
}

function renderHome() {
  document.getElementById('home-screen').classList.remove('hidden');
  document.getElementById('quiz-screen').classList.add('hidden');
  document.getElementById('results-screen').classList.add('hidden');

  const grid = document.getElementById('rounds-grid');
  grid.innerHTML = '';

  const completed = state.scores.filter(s => s !== null).length;
  document.getElementById('rounds-completed').textContent = `${completed}/6`;

  const validScores = state.scores.filter(s => s !== null);
  const avg = validScores.length > 0 ? Math.round(validScores.reduce((a,b) => a+b, 0) / validScores.length) : '--';
  document.getElementById('avg-score').textContent = avg;

  for (let i = 0; i < 6; i++) {
    const card = document.createElement('div');
    const isCompleted = state.scores[i] !== null;
    const answerCount = (state.answers[i] || []).length;
    const inProgress = !isCompleted && answerCount > 0;

    card.className = 'round-card' + (isCompleted ? ' completed' : (inProgress ? ' in-progress' : ''));

    const hasQuestions = state.rounds.length > 0 && state.rounds[i] && state.rounds[i].length > 0;
    const qCount = hasQuestions ? state.rounds[i].length : 100;

    let statusText, extraHtml = '';
    if (isCompleted) {
      statusText = 'Ronda completada';
      extraHtml = `<div class="round-score">${state.scores[i]}/${qCount}</div>`;
    } else if (inProgress) {
      const pct = Math.round((answerCount / qCount) * 100);
      statusText = `Continuar donde lo dejaste`;
      extraHtml = `
        <div class="round-progress">${answerCount} / ${qCount} respondidas</div>
        <div class="progress-mini"><div class="progress-mini-fill" style="width:${pct}%"></div></div>
      `;
    } else {
      statusText = hasQuestions ? 'Lista para iniciar' : 'Mezcla las preguntas primero';
    }

    const badgeIcon = inProgress ? '⏵' : '✓';

    card.innerHTML = `
      <div class="round-badge">${badgeIcon}</div>
      <div class="round-number">Ronda ${i + 1}</div>
      <div class="round-title">${qCount} preguntas</div>
      <div class="round-info">${statusText}</div>
      ${extraHtml}
    `;

    if (isCompleted) {
      card.onclick = () => showResults(i);
    } else if (hasQuestions) {
      card.onclick = () => startRound(i);
    }

    grid.appendChild(card);
  }
}

function startRound(roundIndex) {
  state.currentRound = roundIndex;

  // Detect resume vs fresh start
  const existing = state.answers[roundIndex] || [];
  const hasProgress = existing.length > 0 && state.scores[roundIndex] === null;

  if (hasProgress) {
    // Resume: continue from next unanswered question
    state.currentQ = existing.length;
    state.score = existing.filter(a => a.isCorrect).length;
  } else {
    // Fresh start
    state.currentQ = 0;
    state.score = 0;
    state.answers[roundIndex] = [];
  }
  state.answered = false;
  saveState();

  document.getElementById('home-screen').classList.add('hidden');
  document.getElementById('quiz-screen').classList.remove('hidden');
  document.getElementById('results-screen').classList.add('hidden');

  renderQuestion();
}

function restartRound() {
  if (state.currentRound < 0) return;
  if (!confirm('¿Seguro que quieres reiniciar esta ronda? Se borrará el progreso de esta ronda solamente.')) return;
  const r = state.currentRound;
  state.answers[r] = [];
  state.scores[r] = null;
  state.currentQ = 0;
  state.score = 0;
  state.answered = false;
  saveState();
  renderQuestion();
}

function renderQuestion() {
  const round = state.rounds[state.currentRound];
  const q = round[state.currentQ];
  const total = round.length;

  document.getElementById('progress-text').textContent = `${state.currentQ + 1} / ${total}`;
  document.getElementById('score-live').textContent = `${state.score} pts`;
  document.getElementById('progress-bar').style.width = `${((state.currentQ) / total) * 100}%`;

  const area = document.getElementById('question-area');

  const options = [];
  if (q.A) options.push({letter: 'A', text: q.A});
  if (q.B) options.push({letter: 'B', text: q.B});
  if (q.C) options.push({letter: 'C', text: q.C});
  if (q.D) options.push({letter: 'D', text: q.D});
  if (q.E) options.push({letter: 'E', text: q.E});

  area.innerHTML = `
    <span class="category-tag">${q.category}</span>
    <div class="question-card">
      <div class="question-text">${q.question}</div>
      <div class="options-list" id="options-list">
        ${options.map(o => `
          <button class="option-btn" onclick="selectAnswer('${o.letter}')" data-letter="${o.letter}">
            <span class="option-letter">${o.letter}</span>
            <span>${o.text}</span>
          </button>
        `).join('')}
      </div>
      <div id="feedback-area"></div>
    </div>
  `;

  state.answered = false;
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function selectAnswer(letter) {
  if (state.answered) return;
  state.answered = true;

  const round = state.rounds[state.currentRound];
  const q = round[state.currentQ];
  const isCorrect = letter === q.correct;

  if (isCorrect) state.score++;

  state.answers[state.currentRound].push({
    qId: q.id,
    selected: letter,
    correct: q.correct,
    isCorrect: isCorrect
  });
  saveState();

  // Mark options
  const btns = document.querySelectorAll('.option-btn');
  btns.forEach(btn => {
    const l = btn.dataset.letter;
    btn.classList.add('disabled');
    if (l === q.correct) btn.classList.add('correct');
    else if (l === letter && !isCorrect) btn.classList.add('wrong');
    else btn.classList.add('dimmed');
  });

  document.getElementById('score-live').textContent = `${state.score} pts`;

  // Show feedback
  const explanation = getExplanation(q);
  const fbArea = document.getElementById('feedback-area');

  if (isCorrect) {
    fbArea.innerHTML = `
      <div class="feedback-card correct-fb">
        <div class="fb-title">¡Correcto!</div>
        <div class="fb-text">${explanation}</div>
      </div>
      <button class="next-btn" onclick="nextQuestion()">
        ${state.currentQ < round.length - 1 ? 'Siguiente pregunta →' : 'Ver resultados'}
      </button>
    `;
  } else {
    fbArea.innerHTML = `
      <div class="feedback-card wrong-fb">
        <div class="fb-title">Incorrecto</div>
        <div class="fb-text">La respuesta correcta es <strong>${q.correct}</strong>: ${q[q.correct]}.<br><br>${explanation}</div>
      </div>
      <button class="next-btn" onclick="nextQuestion()">
        ${state.currentQ < round.length - 1 ? 'Siguiente pregunta →' : 'Ver resultados'}
      </button>
    `;
  }
}

function nextQuestion() {
  const round = state.rounds[state.currentRound];
  state.currentQ++;

  if (state.currentQ >= round.length) {
    finishRound();
    return;
  }

  renderQuestion();
}

function finishRound() {
  state.scores[state.currentRound] = state.score;
  saveState();
  showResults(state.currentRound);
}

function showResults(roundIndex) {
  document.getElementById('home-screen').classList.add('hidden');
  document.getElementById('quiz-screen').classList.add('hidden');
  document.getElementById('results-screen').classList.remove('hidden');

  const score = state.scores[roundIndex];
  const total = state.rounds[roundIndex].length;
  const wrong = total - score;
  const pct = Math.round((score / total) * 100);

  let grade, msg;
  if (pct >= 90) { grade = 'excellent'; msg = '¡Excelente!'; }
  else if (pct >= 70) { grade = 'good'; msg = '¡Buen trabajo!'; }
  else if (pct >= 50) { grade = 'average'; msg = 'Puedes mejorar'; }
  else { grade = 'poor'; msg = 'Necesitas estudiar más'; }

  const wrongAnswers = state.answers[roundIndex].filter(a => !a.isCorrect);

  let reviewHtml = '';
  if (wrongAnswers.length > 0) {
    reviewHtml = `
      <div class="review-section">
        <h3>Preguntas incorrectas (${wrongAnswers.length})</h3>
        ${wrongAnswers.map(a => {
          const q = ALL_QUESTIONS.find(qq => qq.id === a.qId) || state.rounds[roundIndex].find(qq => qq.id === a.qId);
          if (!q) return '';
          return `
            <div class="review-item">
              <div class="ri-q">${q.question}</div>
              <div class="ri-answer">Tu respuesta: ${a.selected} - ${q[a.selected] || '?'}</div>
              <div class="ri-correct">Correcta: ${a.correct} - ${q[a.correct] || '?'}</div>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  document.getElementById('results-screen').innerHTML = `
    <div class="header">
      <h1>Ronda ${roundIndex + 1}</h1>
    </div>
    <div class="results-card">
      <div class="results-score-circle ${grade}">
        <div class="big-number">${score}</div>
        <div class="out-of">/ ${total}</div>
      </div>
      <div class="results-message">${msg}</div>
      <div class="results-detail">${pct}% de acierto</div>
      <div class="results-breakdown">
        <div class="breakdown-item correct-bi">
          <div class="bi-number">${score}</div>
          <div class="bi-label">Correctas</div>
        </div>
        <div class="breakdown-item wrong-bi">
          <div class="bi-number">${wrong}</div>
          <div class="bi-label">Incorrectas</div>
        </div>
      </div>
    </div>
    ${reviewHtml}
    <button class="shuffle-btn" onclick="goHome()">← Volver a rondas</button>
  `;

  window.scrollTo({top: 0, behavior: 'smooth'});
}

function goHome() {
  renderHome();
}

// INIT
loadState();
document.getElementById('session-code').textContent = state.sessionCode;
if (state.rounds.length === 0) {
  shuffleDay();
} else {
  renderHome();
}
setSyncStatus('ok', 'Sincronizado');
// Initial sync to upload current state to Pantry (in case it's a new session)
setTimeout(() => syncToPantry(), 500);
</script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html ({len(html)} bytes)")
print(f"Questions embedded: {len(questions)}")
