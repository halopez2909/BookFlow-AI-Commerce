import os

BASE = "frontend-bookflow/src"
files = {}

# ── EPIC index.css ────────────────────────────────────────────────────
files["index.css"] = r"""@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,700;1,300;1,400&family=Outfit:wght@200;300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg: #080706;
  --bg-2: #0E0C0A;
  --bg-card: #141210;
  --bg-card-hover: #1C1916;
  --bg-glass: rgba(10,8,6,0.92);
  --text: #F0EAE0;
  --text-2: #9E8E7A;
  --text-3: #5C4E3E;
  --accent: #C8A45A;
  --accent-dim: rgba(200,164,90,0.1);
  --accent-glow: rgba(200,164,90,0.22);
  --accent-2: #E2C07A;
  --accent-3: #8B6914;
  --green: #3D7A52;
  --green-light: rgba(61,122,82,0.15);
  --red: #7A3535;
  --red-light: rgba(122,53,53,0.15);
  --border: rgba(200,164,90,0.1);
  --border-strong: rgba(200,164,90,0.22);
  --shadow: 0 2px 12px rgba(0,0,0,0.6);
  --shadow-md: 0 8px 40px rgba(0,0,0,0.65);
  --shadow-lg: 0 20px 80px rgba(0,0,0,0.75);
  --shadow-accent: 0 0 40px rgba(200,164,90,0.18);
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Outfit', system-ui, sans-serif;
  --font-mono: 'DM Mono', monospace;
  --r: 8px;
  --r-lg: 14px;
  --r-xl: 24px;
  --ease: cubic-bezier(0.4,0,0.2,1);
  --ease-spring: cubic-bezier(0.34,1.56,0.64,1);
  --ease-slow: cubic-bezier(0.65,0,0.35,1);
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  font-family:var(--font-body);
  background:var(--bg);
  color:var(--text);
  -webkit-font-smoothing:antialiased;
  min-height:100vh;
  overflow-x:hidden;
}
#root{min-height:100vh;display:flex;flex-direction:column;}

::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border-strong);border-radius:2px;}
::selection{background:var(--accent-dim);color:var(--accent-2);}
h1,h2,h3{font-family:var(--font-display);line-height:1.15;}
a{color:var(--accent);text-decoration:none;}

/* ── NAVBAR ─────────────── */
.navbar{
  position:fixed;top:0;left:0;right:0;z-index:200;
  background:var(--bg-glass);
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border-bottom:1px solid var(--border);
  padding:0 clamp(16px,4vw,64px);
  height:64px;display:flex;align-items:center;justify-content:space-between;
  transition:all 0.4s var(--ease);
}
.navbar-brand{
  font-family:var(--font-display);font-size:24px;font-weight:400;
  color:var(--text);cursor:pointer;
  display:flex;align-items:center;gap:10px;
  letter-spacing:0.04em;
}
.navbar-brand-dot{
  width:8px;height:8px;border-radius:50%;
  background:var(--accent);
  box-shadow:0 0 10px var(--accent),0 0 20px var(--accent-glow);
  animation:pulse 3s infinite;
}
@keyframes pulse{
  0%,100%{box-shadow:0 0 10px var(--accent),0 0 20px var(--accent-glow);}
  50%{box-shadow:0 0 16px var(--accent),0 0 32px var(--accent-glow),0 0 48px rgba(200,164,90,0.1);}
}
.navbar-brand span{color:var(--accent);}
.navbar-actions{display:flex;align-items:center;gap:2px;}
.navbar-link{
  font-size:12px;font-weight:500;color:var(--text-2);
  padding:7px 14px;border-radius:var(--r);
  background:transparent;border:none;cursor:pointer;
  font-family:var(--font-body);
  transition:all 0.2s var(--ease);
  letter-spacing:0.08em;text-transform:uppercase;
  position:relative;
}
.navbar-link:hover{color:var(--text);background:var(--accent-dim);}
.navbar-link.active{color:var(--accent);}
.navbar-link.active::after{
  content:'';position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);
  width:20px;height:1px;background:var(--accent);
  box-shadow:0 0 8px var(--accent);
}
.cart-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:17px;height:17px;border-radius:50%;
  background:var(--accent);color:var(--bg);
  font-size:9px;font-weight:700;margin-left:5px;
  animation:badgePop 0.4s var(--ease-spring);
}
@keyframes badgePop{from{transform:scale(0) rotate(-180deg);}to{transform:scale(1) rotate(0deg);}}

/* ── ADMIN NAV ─────────── */
.admin-nav{
  background:var(--bg-2);border-bottom:1px solid var(--border);
  padding:0 clamp(16px,4vw,48px);
  display:flex;align-items:center;gap:4px;height:46px;
  margin-top:64px;
}
.admin-nav-btn{
  font-size:11px;font-weight:500;color:var(--text-3);
  padding:6px 14px;border-radius:var(--r);
  background:transparent;border:none;cursor:pointer;
  font-family:var(--font-body);transition:all 0.2s var(--ease);
  text-decoration:none;display:inline-flex;align-items:center;
  letter-spacing:0.08em;text-transform:uppercase;
}
.admin-nav-btn:hover{background:var(--accent-dim);color:var(--text-2);}
.admin-nav-btn.active{background:var(--accent-dim);color:var(--accent);}

/* ── PAGE ─────────────── */
.page{max-width:1400px;margin:0 auto;padding:clamp(24px,4vw,56px) clamp(16px,4vw,48px);padding-top:calc(64px + clamp(24px,4vw,56px));}

/* ── BUTTONS ──────────── */
.btn{
  font-family:var(--font-body);font-size:12px;font-weight:600;
  padding:10px 22px;border-radius:var(--r);border:none;
  cursor:pointer;transition:all 0.25s var(--ease);
  display:inline-flex;align-items:center;gap:8px;
  letter-spacing:0.08em;text-transform:uppercase;
  position:relative;overflow:hidden;
}
.btn-primary{
  background:var(--accent);color:var(--bg);
  box-shadow:0 0 0 rgba(200,164,90,0);
}
.btn-primary:hover{
  background:var(--accent-2);
  box-shadow:0 0 24px var(--accent-glow),0 4px 16px rgba(200,164,90,0.25);
  transform:translateY(-2px);
}
.btn-primary:active{transform:translateY(0);}
.btn-primary:disabled{opacity:0.35;cursor:not-allowed;transform:none;box-shadow:none;}
.btn-ghost{
  background:transparent;color:var(--text-2);
  border:1px solid var(--border-strong);
}
.btn-ghost:hover{background:var(--accent-dim);color:var(--accent);border-color:var(--accent);}
.btn-sm{font-size:10px;padding:6px 12px;}

/* ── INPUTS ──────────── */
input,select{
  font-family:var(--font-body);font-size:13px;
  background:var(--bg-card);border:1px solid var(--border);
  color:var(--text);border-radius:var(--r);padding:10px 14px;
  outline:none;transition:all 0.2s var(--ease);width:100%;
}
input:focus,select:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-dim);
}
input::placeholder{color:var(--text-3);}

/* ── BADGES ──────────── */
.badge{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 10px;border-radius:20px;
  font-size:9px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;
}
.badge-enriched{background:rgba(61,122,82,0.2);color:#7AC99A;border:1px solid rgba(61,122,82,0.3);}
.badge-basic{background:rgba(92,78,62,0.2);color:var(--text-3);border:1px solid var(--border);}
.badge-available{background:rgba(61,122,82,0.2);color:#7AC99A;border:1px solid rgba(61,122,82,0.3);}

/* ── METRICS DASHBOARD ── */
.metrics-grid{
  display:grid;grid-template-columns:repeat(4,1fr);gap:16px;
  margin-bottom:48px;
}
@media(max-width:900px){.metrics-grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:480px){.metrics-grid{grid-template-columns:repeat(2,1fr);gap:10px;}}

.metric-card{
  background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:20px 22px;
  position:relative;overflow:hidden;
  transition:all 0.3s var(--ease);
  cursor:default;
}
.metric-card::before{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--accent),transparent);
  opacity:0;transition:opacity 0.3s var(--ease);
}
.metric-card:hover{border-color:var(--border-strong);transform:translateY(-2px);box-shadow:var(--shadow-md);}
.metric-card:hover::before{opacity:1;}
.metric-label{font-size:10px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;}
.metric-value{font-family:var(--font-display);font-size:32px;font-weight:300;color:var(--text);line-height:1;}
.metric-sub{font-size:11px;color:var(--text-3);margin-top:6px;font-style:italic;}
.metric-icon{position:absolute;top:18px;right:18px;font-size:20px;opacity:0.15;}
.metric-accent{color:var(--accent);}

/* ── LIBRARY GATE ANIMATION ── */
.library-gate{
  position:fixed;inset:0;z-index:500;
  display:flex;align-items:center;justify-content:center;
  background:var(--bg);
  pointer-events:auto;
}
.gate-left,.gate-right{
  position:absolute;top:0;bottom:0;width:50%;
  background:var(--bg-2);
  display:flex;align-items:center;justify-content:center;
  overflow:hidden;
}
.gate-left{left:0;border-right:1px solid var(--border);}
.gate-right{right:0;border-left:1px solid var(--border);}
.gate-left::before,.gate-right::before{
  content:'';position:absolute;inset:0;
  background:repeating-linear-gradient(
    0deg,transparent,transparent 40px,
    rgba(200,164,90,0.03) 40px,rgba(200,164,90,0.03) 41px
  );
}
.gate-text{
  font-family:var(--font-display);font-size:clamp(2rem,6vw,5rem);
  font-weight:300;color:var(--accent);letter-spacing:0.2em;
  font-style:italic;opacity:0.4;
  position:relative;z-index:1;
}
.gate-left .gate-text{transform:translateX(-20px);}
.gate-right .gate-text{transform:translateX(20px);}
.gate-center{
  position:relative;z-index:10;text-align:center;
  display:flex;flex-direction:column;align-items:center;gap:24px;
}
.gate-logo{
  font-family:var(--font-display);font-size:clamp(2.5rem,7vw,6rem);
  font-weight:300;color:var(--text);letter-spacing:0.06em;
  animation:fadeUp 0.8s var(--ease) both;
}
.gate-logo span{color:var(--accent);}
.gate-tagline{
  font-size:14px;color:var(--text-3);letter-spacing:0.16em;
  text-transform:uppercase;font-weight:300;
  animation:fadeUp 0.8s var(--ease) 0.2s both;
}
.gate-btn{
  animation:fadeUp 0.8s var(--ease) 0.5s both;
  position:relative;
}
.gate-btn::after{
  content:'';position:absolute;inset:-4px;border-radius:var(--r);
  border:1px solid var(--accent-glow);
  animation:gateRing 2s ease infinite;
}
@keyframes gateRing{
  0%{opacity:0;transform:scale(1);}
  50%{opacity:1;}
  100%{opacity:0;transform:scale(1.15);}
}
.gate-open .gate-left{animation:slideLeft 0.9s var(--ease-slow) both;}
.gate-open .gate-right{animation:slideRight 0.9s var(--ease-slow) both;}
.gate-open .gate-center{animation:gateCenter 0.4s var(--ease) both;}
@keyframes slideLeft{to{transform:translateX(-100%);}}
@keyframes slideRight{to{transform:translateX(100%);}}
@keyframes gateCenter{to{opacity:0;transform:scale(1.1);}}
.gate-hidden{display:none;}

/* ── CATALOG HERO ─────── */
.catalog-hero{
  margin-bottom:40px;
  display:flex;align-items:flex-end;justify-content:space-between;
  gap:20px;flex-wrap:wrap;
}
.catalog-hero-title{
  font-size:clamp(2.5rem,5vw,4.5rem);font-weight:300;
  color:var(--text);letter-spacing:-0.02em;
}
.catalog-hero-title em{color:var(--accent);font-style:italic;}
.catalog-hero-sub{
  color:var(--text-3);font-size:13px;
  letter-spacing:0.08em;text-transform:uppercase;
  margin-top:6px;font-weight:300;
}

/* ── FILTER BAR ─────── */
.filter-bar{
  display:flex;gap:12px;margin-bottom:36px;
  flex-wrap:wrap;align-items:flex-end;
  padding:20px;background:var(--bg-card);
  border:1px solid var(--border);border-radius:var(--r-lg);
}
.filter-group{display:flex;flex-direction:column;gap:6px;}
.filter-label{font-size:9px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.12em;}
.range-row{display:flex;gap:8px;align-items:center;}

/* ── BOOK GRID ─────── */
.books-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
  gap:24px;
}
@media(max-width:600px){.books-grid{grid-template-columns:repeat(2,1fr);gap:14px;}}

/* ── BOOK CARD ─────── */
.book-card{
  background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--r-lg);overflow:hidden;cursor:pointer;
  transition:all 0.35s var(--ease);
  display:flex;flex-direction:column;
  position:relative;
}
.book-card::after{
  content:'';position:absolute;inset:0;border-radius:var(--r-lg);
  background:linear-gradient(135deg,rgba(200,164,90,0.07),transparent 60%);
  opacity:0;transition:opacity 0.35s var(--ease);pointer-events:none;
}
.book-card:hover{
  border-color:var(--border-strong);
  box-shadow:var(--shadow-md),var(--shadow-accent);
  transform:translateY(-6px) scale(1.01);
}
.book-card:hover::after{opacity:1;}
.book-card-img-wrap{position:relative;overflow:hidden;}
.book-card-img{
  width:100%;aspect-ratio:2/3;object-fit:cover;display:block;
  transition:transform 0.6s var(--ease-slow);
}
.book-card:hover .book-card-img{transform:scale(1.06);}
.book-card-placeholder{
  width:100%;aspect-ratio:2/3;
  background:linear-gradient(160deg,var(--bg-2) 0%,var(--bg-card-hover) 100%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;
  font-family:var(--font-display);font-size:48px;font-weight:300;
  color:var(--accent);font-style:italic;border-bottom:1px solid var(--border);
  transition:all 0.4s var(--ease);
}
.book-card:hover .book-card-placeholder{background:linear-gradient(160deg,var(--bg-card-hover) 0%,var(--bg-2) 100%);}
.book-card-shine{
  position:absolute;top:0;left:-100%;width:60%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(200,164,90,0.08),transparent);
  transition:left 0.6s var(--ease-slow);
}
.book-card:hover .book-card-shine{left:150%;}
.book-card-body{padding:16px;flex:1;display:flex;flex-direction:column;gap:6px;}
.book-card-title{
  font-family:var(--font-display);font-size:15px;font-weight:400;
  color:var(--text);line-height:1.35;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.book-card-author{font-size:11px;color:var(--text-3);font-style:italic;letter-spacing:0.02em;}
.book-card-footer{
  display:flex;justify-content:space-between;align-items:center;
  margin-top:auto;padding-top:12px;border-top:1px solid var(--border);
  flex-wrap:wrap;gap:4px;
}
.book-price{font-size:13px;font-weight:600;color:var(--accent);letter-spacing:0.02em;font-family:var(--font-mono);}
.book-price-na{font-size:11px;color:var(--text-3);font-style:italic;}

/* ── SKELETON ─────── */
@keyframes shimmer{
  0%{background-position:-600px 0}100%{background-position:600px 0}
}
.skeleton{
  background:linear-gradient(90deg,var(--bg-card) 25%,rgba(200,164,90,0.05) 50%,var(--bg-card) 75%);
  background-size:1200px 100%;animation:shimmer 2s infinite;border-radius:var(--r);
}
.skeleton-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;}
.skeleton-img{aspect-ratio:2/3;width:100%;}
.skeleton-line{height:12px;margin:10px 14px 0;}
.skeleton-line.short{width:60%;}
.skeleton-line.xshort{width:40%;margin-bottom:14px;}

/* ── EMPTY STATE ─────── */
.empty-state{text-align:center;padding:80px 24px;}
.empty-state p{color:var(--text-2);margin-top:8px;font-family:var(--font-display);font-size:20px;font-style:italic;}

/* ── DETAIL LAYOUT ─────── */
.detail-layout{display:grid;grid-template-columns:300px 1fr;gap:56px;align-items:start;}
@media(max-width:768px){.detail-layout{grid-template-columns:1fr;}}
.detail-img-wrap{position:relative;}
.detail-img{
  width:100%;border-radius:var(--r-lg);
  box-shadow:var(--shadow-lg),var(--shadow-accent);
  object-fit:cover;
  transition:transform 0.5s var(--ease);
}
.detail-img:hover{transform:scale(1.02);}
.detail-img-placeholder{
  width:100%;aspect-ratio:2/3;border-radius:var(--r-lg);
  background:linear-gradient(135deg,var(--bg-2),var(--bg-card));
  display:flex;align-items:center;justify-content:center;
  font-family:var(--font-display);font-size:80px;font-weight:300;
  color:var(--accent);border:1px solid var(--border);font-style:italic;
}
.detail-meta{display:flex;flex-direction:column;gap:24px;}
.detail-title{font-size:clamp(1.8rem,4vw,3rem);font-weight:300;color:var(--text);letter-spacing:-0.01em;}
.detail-author{font-size:16px;color:var(--text-2);font-style:italic;}
.detail-description{font-size:14px;line-height:1.85;color:var(--text-2);}
.detail-price-box{
  background:linear-gradient(135deg,rgba(200,164,90,0.08),rgba(200,164,90,0.03));
  border:1px solid var(--border-strong);border-radius:var(--r-lg);padding:22px 26px;
  position:relative;overflow:hidden;
}
.detail-price-box::after{
  content:'';position:absolute;top:-30px;right:-30px;
  width:100px;height:100px;border-radius:50%;
  background:radial-gradient(var(--accent-glow),transparent 70%);
  pointer-events:none;
}
.detail-price-label{font-size:10px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.12em;margin-bottom:6px;}
.detail-price-value{font-size:36px;font-weight:300;color:var(--accent);font-family:var(--font-display);letter-spacing:-0.02em;}
.detail-price-explanation{font-size:12px;color:var(--text-3);margin-top:8px;line-height:1.6;font-style:italic;}
.detail-attrs{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}
.detail-attr{background:var(--bg-2);border:1px solid var(--border);border-radius:var(--r);padding:12px 16px;transition:all 0.2s var(--ease);}
.detail-attr:hover{border-color:var(--border-strong);}
.detail-attr-label{font-size:9px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;}
.detail-attr-value{font-size:13px;font-weight:400;color:var(--text-2);}

/* ── LOGIN ─────── */
.login-page{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;}
@media(max-width:768px){.login-page{grid-template-columns:1fr;}}
.login-left{
  background:var(--bg-2);display:flex;align-items:center;justify-content:center;
  padding:48px;position:relative;overflow:hidden;
}
.login-left::before{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse at 25% 35%,rgba(200,164,90,0.07) 0%,transparent 55%),
    radial-gradient(ellipse at 75% 75%,rgba(200,164,90,0.04) 0%,transparent 50%);
}
.login-bg-lines{
  position:absolute;inset:0;overflow:hidden;opacity:0.04;
}
.login-bg-lines::before{
  content:'';position:absolute;inset:-50%;
  background:repeating-linear-gradient(
    45deg,transparent,transparent 80px,
    rgba(200,164,90,1) 80px,rgba(200,164,90,1) 81px
  );
}
.login-left-content{position:relative;z-index:1;text-align:center;}
.login-logo{font-family:var(--font-display);font-size:clamp(3rem,6vw,5rem);font-weight:300;color:var(--text);letter-spacing:0.06em;}
.login-logo span{color:var(--accent);}
.login-tagline{font-size:14px;color:var(--text-3);margin-top:16px;line-height:1.8;max-width:300px;font-style:italic;}
.login-features{margin-top:40px;display:flex;flex-direction:column;gap:12px;}
.login-feature{display:flex;align-items:center;gap:12px;color:var(--text-3);font-size:13px;}
.login-feature-dot{width:4px;height:4px;border-radius:50%;background:var(--accent);flex-shrink:0;box-shadow:0 0 6px var(--accent);}
.login-right{display:flex;align-items:center;justify-content:center;padding:48px;background:var(--bg);}
.login-form-container{width:100%;max-width:380px;}
.login-tabs{display:flex;gap:0;margin-bottom:32px;background:var(--bg-2);border-radius:var(--r);padding:4px;border:1px solid var(--border);}
.login-tab{
  flex:1;padding:9px;border-radius:var(--r);border:none;cursor:pointer;
  font-family:var(--font-body);font-weight:600;font-size:11px;
  text-transform:uppercase;letter-spacing:0.1em;transition:all 0.25s var(--ease);
}
.login-tab.active{background:var(--accent);color:var(--bg);box-shadow:0 0 20px var(--accent-glow);}
.login-tab:not(.active){background:transparent;color:var(--text-3);}
.login-tab:not(.active):hover{color:var(--text-2);}
.login-form-title{font-family:var(--font-display);font-size:28px;font-weight:300;margin-bottom:6px;color:var(--text);}
.login-form-subtitle{color:var(--text-3);font-size:13px;margin-bottom:28px;font-style:italic;}
.login-field{margin-bottom:18px;}
.login-label{display:block;font-size:9px;font-weight:600;color:var(--text-3);margin-bottom:8px;letter-spacing:0.12em;text-transform:uppercase;}
.login-error{background:var(--red-light);border:1px solid var(--red);color:#E8A0A0;padding:10px 14px;border-radius:var(--r);font-size:13px;margin-bottom:16px;}
.login-success{background:var(--green-light);border:1px solid var(--green);color:#8DBF9E;padding:10px 14px;border-radius:var(--r);font-size:13px;margin-bottom:16px;}
.login-submit{width:100%;padding:12px;font-size:12px;margin-top:8px;justify-content:center;}
.login-back{text-align:center;margin-top:24px;font-size:13px;color:var(--text-3);}

/* ── TABLES ─────── */
.table-wrap{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;}
table{width:100%;border-collapse:collapse;}
th{
  text-align:left;padding:14px 20px;
  font-size:9px;font-weight:600;color:var(--text-3);
  text-transform:uppercase;letter-spacing:0.12em;
  border-bottom:1px solid var(--border);background:var(--bg-2);
}
td{padding:16px 20px;font-size:13px;border-bottom:1px solid var(--border);color:var(--text-2);vertical-align:middle;}
tr:last-child td{border-bottom:none;}
tr{transition:background 0.2s var(--ease);}
tr:hover td{background:var(--accent-dim);color:var(--text);}

/* ── PAGE HEADER ─── */
.page-header{margin-bottom:36px;}
.page-header h1{font-size:clamp(1.8rem,4vw,3rem);font-weight:300;margin-bottom:6px;}
.page-header p{color:var(--text-3);font-size:13px;font-style:italic;letter-spacing:0.04em;}

/* ── LOAD MORE ─── */
.load-more{text-align:center;margin-top:56px;}
.books-count{text-align:center;color:var(--text-3);font-size:12px;margin-top:16px;letter-spacing:0.08em;text-transform:uppercase;}

/* ── STATUS BADGES ─── */
.status-badge{display:inline-flex;align-items:center;padding:4px 12px;border-radius:20px;font-size:10px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;}
.status-pending{background:rgba(200,164,90,0.15);color:var(--accent);border:1px solid rgba(200,164,90,0.3);}
.status-confirmed{background:rgba(61,122,82,0.15);color:#7AC99A;border:1px solid rgba(61,122,82,0.3);}
.status-shipped{background:rgba(100,100,220,0.15);color:#9090E8;border:1px solid rgba(100,100,220,0.3);}
.status-delivered{background:rgba(61,122,82,0.2);color:#7AC99A;border:1px solid rgba(61,122,82,0.4);}
.status-cancelled{background:rgba(122,53,53,0.15);color:#E8A0A0;border:1px solid rgba(122,53,53,0.3);}

/* ── CART ─── */
.cart-summary{
  background:var(--bg-card);border:1px solid var(--border-strong);
  border-radius:var(--r-lg);padding:24px;position:sticky;top:88px;
}
.cart-total-line{
  display:flex;justify-content:space-between;
  font-size:20px;font-family:var(--font-display);font-weight:300;
  border-top:1px solid var(--border);padding-top:16px;margin-top:16px;
}
.cart-total-amount{color:var(--accent);}

/* ── ASSISTANT ─── */
.assistant-container{
  background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--r-lg);overflow:hidden;display:flex;flex-direction:column;
}
.message-bubble{
  max-width:76%;padding:12px 18px;border-radius:16px;
  font-size:14px;line-height:1.65;
  animation:msgIn 0.3s var(--ease-spring);
}
@keyframes msgIn{from{opacity:0;transform:translateY(8px) scale(0.97);}to{opacity:1;transform:none;}}
.message-user{
  background:linear-gradient(135deg,var(--accent),var(--accent-3));
  color:var(--bg);margin-left:auto;border-bottom-right-radius:4px;
}
.message-assistant{
  background:var(--bg-2);color:var(--text);border:1px solid var(--border);
  border-bottom-left-radius:4px;
}
.message-sources{font-size:10px;color:var(--text-3);margin-top:4px;font-style:italic;letter-spacing:0.04em;}
.thinking-dots{display:flex;gap:5px;padding:14px 18px;}
.thinking-dot{
  width:6px;height:6px;border-radius:50%;background:var(--accent);
  animation:thinking 1.4s infinite;
}
.thinking-dot:nth-child(2){animation-delay:0.2s;}
.thinking-dot:nth-child(3){animation-delay:0.4s;}
@keyframes thinking{
  0%,80%,100%{transform:scale(0.7);opacity:0.35;}
  40%{transform:scale(1.2);opacity:1;box-shadow:0 0 8px var(--accent);}
}

/* ── ANIMATIONS ─── */
@keyframes fadeUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
@keyframes scaleIn{from{opacity:0;transform:scale(0.94);}to{opacity:1;transform:scale(1);}}
.fade-up{animation:fadeUp 0.55s var(--ease) both;}
.fade-in{animation:fadeIn 0.4s var(--ease) both;}
.scale-in{animation:scaleIn 0.4s var(--ease-spring) both;}

/* ── RECS ─── */
.recs-section{margin-top:72px;padding-top:48px;border-top:1px solid var(--border);}
.recs-section h2{font-size:clamp(1.4rem,3vw,2rem);font-weight:300;color:var(--text);margin-bottom:24px;font-style:italic;}

/* ── RESPONSIVE ─── */
@media(max-width:768px){
  .navbar{padding:0 16px;}
  .page{padding:16px;padding-top:80px;}
  .metrics-grid{grid-template-columns:repeat(2,1fr);}
  .detail-layout{grid-template-columns:1fr;}
}
*{scrollbar-width:thin;scrollbar-color:var(--border-strong) var(--bg);}
"""

# ── LibraryGate component ─────────────────────────────────────────────
files["components/shared/LibraryGate.tsx"] = """import React, { useState, useEffect } from 'react'

interface Props { onOpen: () => void }

export default function LibraryGate({ onOpen }: Props) {
  const [opening, setOpening] = useState(false)

  function handleOpen() {
    setOpening(true)
    setTimeout(onOpen, 900)
  }

  return (
    <div className={`library-gate ${opening ? 'gate-open' : ''}`}>
      <div className="gate-left">
        <div className="login-bg-lines" />
        <div className="gate-text">Book</div>
      </div>
      <div className="gate-right">
        <div className="login-bg-lines" />
        <div className="gate-text">Flow</div>
      </div>
      <div className="gate-center">
        <div className="gate-logo">Book<span>Flow</span></div>
        <div className="gate-tagline">Librería de Comercio Inteligente</div>
        <button className="btn btn-primary gate-btn" onClick={handleOpen} style={{ fontSize: 13, letterSpacing: '0.12em', padding: '14px 32px' }}>
          Explorar Colección
        </button>
      </div>
    </div>
  )
}
"""

# ── MetricsDashboard component ────────────────────────────────────────
files["components/catalog/MetricsDashboard.tsx"] = """import React from 'react'

interface Props {
  total: number
  enriched: number
  withPrice: number
  avgPrice: number
}

export default function MetricsDashboard({ total, enriched, withPrice, avgPrice }: Props) {
  const enrichedPct = total > 0 ? Math.round((enriched / total) * 100) : 0
  const pricedPct = total > 0 ? Math.round((withPrice / total) * 100) : 0

  return (
    <div className="metrics-grid fade-up" style={{ animationDelay: '0.1s' }}>
      <div className="metric-card">
        <div className="metric-label">Total Títulos</div>
        <div className="metric-value metric-accent">{total.toLocaleString('es-CO')}</div>
        <div className="metric-sub">En el catálogo activo</div>
        <div className="metric-icon">◎</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Enriquecidos con IA</div>
        <div className="metric-value">{enrichedPct}<span style={{ fontSize: 18, color: 'var(--text-3)' }}>%</span></div>
        <div className="metric-sub">{enriched} de {total} títulos</div>
        <div className="metric-icon">✦</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Con Precio IA</div>
        <div className="metric-value">{pricedPct}<span style={{ fontSize: 18, color: 'var(--text-3)' }}>%</span></div>
        <div className="metric-sub">{withPrice} títulos valuados</div>
        <div className="metric-icon">◈</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Precio Promedio</div>
        <div className="metric-value" style={{ fontSize: 24 }}>${avgPrice > 0 ? Math.round(avgPrice / 1000) + 'K' : '—'}</div>
        <div className="metric-sub">COP · Sugerido por IA</div>
        <div className="metric-icon">❋</div>
      </div>
    </div>
  )
}
"""

# ── Updated CatalogPage ───────────────────────────────────────────────
files["pages/catalog/CatalogPage.tsx"] = """import React, { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCatalog } from '../../hooks/useCatalog'
import BookCard from '../../components/catalog/BookCard'
import SkeletonCard from '../../components/catalog/SkeletonCard'
import FilterBar from '../../components/catalog/FilterBar'
import EmptyState from '../../components/shared/EmptyState'
import LibraryGate from '../../components/shared/LibraryGate'
import MetricsDashboard from '../../components/catalog/MetricsDashboard'

const GATE_KEY = 'bookflow_gate_seen'

export default function CatalogPage() {
  const navigate = useNavigate()
  const [gateOpen, setGateOpen] = useState(() => sessionStorage.getItem(GATE_KEY) === '1')
  const [titleInput, setTitleInput] = useState('')
  const { data, isLoading, isError, refetch, filters, setFilters, fetchNextPage } = useCatalog()

  function handleGateOpen() {
    sessionStorage.setItem(GATE_KEY, '1')
    setGateOpen(true)
  }

  function handleTitleChange(v: string) {
    setTitleInput(v)
    setFilters({ ...filters, title: v })
  }

  const metrics = useMemo(() => {
    if (!data?.items) return { enriched: 0, withPrice: 0, avgPrice: 0 }
    const items = data.items
    const enriched = items.filter(b => b.enriched_flag).length
    const priced = items.filter(b => b.suggested_price && b.suggested_price > 0)
    const avgPrice = priced.length > 0 ? priced.reduce((s, b) => s + (b.suggested_price || 0), 0) / priced.length : 0
    return { enriched, withPrice: priced.length, avgPrice }
  }, [data?.items])

  if (!gateOpen) return <LibraryGate onOpen={handleGateOpen} />

  return (
    <div className="page">
      <div className="catalog-hero fade-up">
        <div>
          <h1 className="catalog-hero-title">Nuestra <em>Colección</em></h1>
          <p className="catalog-hero-sub">
            {data?.total ? `${data.total} títulos · inteligencia artificial aplicada` : 'Catálogo enriquecido con IA'}
          </p>
        </div>
      </div>

      {!isLoading && data && (
        <MetricsDashboard
          total={data.total}
          enriched={metrics.enriched}
          withPrice={metrics.withPrice}
          avgPrice={metrics.avgPrice}
        />
      )}

      <FilterBar
        title={titleInput} onTitleChange={handleTitleChange}
        minPrice={filters.min_price} maxPrice={filters.max_price}
        onMinPriceChange={v => setFilters({ ...filters, min_price: v })}
        onMaxPriceChange={v => setFilters({ ...filters, max_price: v })}
        available={filters.available} onAvailableChange={v => setFilters({ ...filters, available: v })}
      />

      {isError && <EmptyState message="No se pudo cargar el catálogo." onRetry={() => refetch()} />}
      {isLoading && (
        <div className="books-grid">{Array.from({ length: 12 }).map((_, i) => <SkeletonCard key={i} />)}</div>
      )}
      {!isLoading && !isError && data?.items?.length === 0 && <EmptyState message="No se encontraron libros." />}
      {!isLoading && !isError && data?.items && data.items.length > 0 && (
        <>
          <div className="books-grid">
            {data.items.map((book, i) => (
              <div key={book.id} className="fade-up scale-in" style={{ animationDelay: `${Math.min(i * 0.04, 0.6)}s` }}>
                <BookCard book={book} onClick={() => navigate('/catalog/' + book.id)} />
              </div>
            ))}
          </div>
          {data.items.length < data.total && (
            <div className="load-more">
              <button className="btn btn-ghost" onClick={fetchNextPage}>Cargar más títulos</button>
            </div>
          )}
          <div className="books-count">{data.items.length} de {data.total} títulos</div>
        </>
      )}
    </div>
  )
}
"""

# ── Updated BookCard ──────────────────────────────────────────────────
files["components/catalog/BookCard.tsx"] = """import React from 'react'
import type { Book } from '../../utils/types'
import EnrichmentBadge from './EnrichmentBadge'
import PriceSummary from './PriceSummary'

type Props = { book: Book; onClick?: () => void }

export default function BookCard({ book, onClick }: Props) {
  const initials = book.title.split(' ').slice(0, 2).map((w: string) => w[0]).join('').toUpperCase()
  return (
    <div className="book-card" onClick={onClick}>
      <div className="book-card-img-wrap">
        <div className="book-card-shine" />
        {book.cover_url
          ? <img className="book-card-img" src={book.cover_url} alt={book.title} loading="lazy"
              onError={(e) => { const t = e.currentTarget as HTMLImageElement; t.style.display = 'none'; const p = t.nextElementSibling as HTMLElement; if (p) p.style.display = 'flex'; }} />
          : null}
        <div className="book-card-placeholder" style={{ display: book.cover_url ? 'none' : 'flex' }}>
          {initials}
        </div>
      </div>
      <div className="book-card-body">
        <EnrichmentBadge isEnriched={book.enriched_flag} />
        <div className="book-card-title">{book.title}</div>
        <div className="book-card-author">{book.author}</div>
        <div className="book-card-footer">
          <PriceSummary suggestedPrice={book.suggested_price} />
          {book.published_flag && <span className="badge badge-available">Disponible</span>}
        </div>
      </div>
    </div>
  )
}
"""

# ── Updated NavBar ────────────────────────────────────────────────────
files["components/shared/NavBar.tsx"] = """import React, { useContext, useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useCart } from '../../hooks/useCart'

export default function NavBar() {
  const { state, dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const location = useLocation()
  const customerId = state.user?.email || 'guest-001'
  const { data: cart } = useCart(customerId)
  const cartCount = cart?.items?.length || 0
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  const isActive = (path: string) => location.pathname.startsWith(path)

  return (
    <nav className="navbar" style={{ boxShadow: scrolled ? '0 4px 32px rgba(0,0,0,0.4)' : 'none' }}>
      <span className="navbar-brand" onClick={() => navigate('/catalog')}>
        <span className="navbar-brand-dot" />
        Book<span>Flow</span>
      </span>
      <div className="navbar-actions">
        {[
          { path: '/catalog', label: 'Catálogo' },
          { path: '/assistant', label: 'Asistente' },
        ].map(({ path, label }) => (
          <button key={path} className={`navbar-link ${isActive(path) ? 'active' : ''}`} onClick={() => navigate(path)}>
            {label}
          </button>
        ))}
        <button className={`navbar-link ${isActive('/cart') ? 'active' : ''}`} onClick={() => navigate('/cart')}>
          Carrito {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
        </button>
        {state.isAuthenticated && (
          <button className={`navbar-link ${isActive('/orders') ? 'active' : ''}`} onClick={() => navigate('/orders')}>
            Pedidos
          </button>
        )}
        {state.isAuthenticated ? (
          <button className="btn btn-ghost btn-sm" onClick={() => { dispatch({ type: 'LOGOUT' }); navigate('/catalog'); }} style={{ marginLeft: 8 }}>
            Salir
          </button>
        ) : (
          <button className="btn btn-ghost btn-sm" onClick={() => navigate('/login')} style={{ marginLeft: 8 }}>
            Admin
          </button>
        )}
      </div>
    </nav>
  )
}
"""

# ── Updated Login ─────────────────────────────────────────────────────
files["pages/Login.tsx"] = """import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/apiClient'
import { AuthContext } from '../context/AuthContext'

export default function Login() {
  const { dispatch } = useContext(AuthContext)
  const navigate = useNavigate()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null); setSuccess(null); setLoading(true)
    try {
      if (mode === 'login') {
        const { data } = await api.post('/api/auth/login', { email, password })
        dispatch({ type: 'LOGIN', payload: { token: data.access_token, user: data } })
        navigate('/catalog', { replace: true })
      } else {
        await api.post('/api/auth/register', { email, password, role: 'user' })
        setSuccess('Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
        setMode('login')
      }
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : mode === 'login' ? 'Credenciales incorrectas' : 'Error al registrarse')
    } finally { setLoading(false) }
  }

  return (
    <div className="login-page">
      <div className="login-left">
        <div className="login-bg-lines" />
        <div className="login-left-content fade-up">
          <div className="login-logo">Book<span>Flow</span></div>
          <p className="login-tagline">Plataforma inteligente de comercio de libros con inteligencia artificial aplicada.</p>
          <div className="login-features">
            {['Catálogo enriquecido con IA', 'Precios sugeridos en tiempo real', 'Asistente conversacional', 'Recomendaciones personalizadas'].map(f => (
              <div key={f} className="login-feature">
                <span className="login-feature-dot" />
                {f}
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="login-right">
        <div className="login-form-container fade-up">
          <div className="login-tabs">
            <button className={`login-tab ${mode === 'login' ? 'active' : ''}`} onClick={() => { setMode('login'); setError(null); setSuccess(null); }}>
              Iniciar Sesión
            </button>
            <button className={`login-tab ${mode === 'register' ? 'active' : ''}`} onClick={() => { setMode('register'); setError(null); setSuccess(null); }}>
              Registrarse
            </button>
          </div>
          <h2 className="login-form-title">{mode === 'login' ? 'Bienvenido' : 'Nueva Cuenta'}</h2>
          <p className="login-form-subtitle">{mode === 'login' ? 'Accede para gestionar el sistema' : 'Crea tu cuenta para explorar'}</p>
          {success && <div className="login-success">{success}</div>}
          <form onSubmit={handleSubmit}>
            <div className="login-field">
              <label className="login-label">Correo electrónico</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} required placeholder="tu@email.com" />
            </div>
            <div className="login-field">
              <label className="login-label">Contraseña</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} required placeholder="••••••••" />
            </div>
            {error && <div className="login-error">{error}</div>}
            <button type="submit" disabled={loading} className="btn btn-primary login-submit">
              {loading ? '...' : mode === 'login' ? 'Iniciar Sesión' : 'Crear Cuenta'}
            </button>
          </form>
          <div className="login-back"><a href="/catalog">← Explorar catálogo público</a></div>
        </div>
      </div>
    </div>
  )
}
"""

# ── Updated AssistantPage ─────────────────────────────────────────────
files["pages/assistant/AssistantPage.tsx"] = """import React, { useState, useRef, useEffect } from 'react'
import { useAssistant } from '../../hooks/useAssistant'

const SESSION_ID = 'session-' + Math.random().toString(36).slice(2, 9)
const SUGGESTIONS = [
  '¿Cuánto cuesta Don Quixote?',
  '¿Está disponible 1984?',
  'Libros de George Orwell',
  'Cuéntame sobre The Great Gatsby',
]

export default function AssistantPage() {
  const { messages, isLoading, sendMessage } = useAssistant(SESSION_ID)
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  async function handleSend() {
    if (!input.trim() || isLoading) return
    const q = input.trim(); setInput('')
    await sendMessage(q)
    inputRef.current?.focus()
  }

  return (
    <div className="page fade-up" style={{ maxWidth: 860 }}>
      <div className="page-header">
        <h1>Asistente <em style={{ fontStyle: 'italic', color: 'var(--accent)' }}>BookFlow</em></h1>
        <p>Consulta precios, disponibilidad y descripción de cualquier título</p>
      </div>
      <div className="assistant-container" style={{ height: 'calc(100vh - 360px)', minHeight: 420 }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: 28, display: 'flex', flexDirection: 'column', gap: 16 }}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', padding: '48px 24px', color: 'var(--text-3)' }}>
              <div style={{ fontSize: 40, marginBottom: 16, opacity: 0.2, fontFamily: 'var(--font-display)', fontStyle: 'italic' }}>◎</div>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: 22, color: 'var(--text-2)', fontWeight: 300, marginBottom: 8 }}>¿En qué puedo ayudarte?</p>
              <p style={{ fontSize: 13, marginBottom: 28, letterSpacing: '0.04em' }}>Pregunta sobre precios, disponibilidad o descripción</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' }}>
                {SUGGESTIONS.map(s => (
                  <button key={s} className="btn btn-ghost btn-sm" onClick={() => { setInput(s); inputRef.current?.focus(); }}
                    style={{ textTransform: 'none', letterSpacing: '0.02em', fontSize: 12 }}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <div className={`message-bubble ${msg.role === 'user' ? 'message-user' : 'message-assistant'}`}>
                {msg.content}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div className="message-sources" style={{ marginLeft: msg.role === 'assistant' ? 4 : 0 }}>
                  Fuentes: {msg.sources.join(', ')}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div style={{ display: 'flex' }}>
              <div className="message-bubble message-assistant" style={{ padding: 0 }}>
                <div className="thinking-dots">
                  <div className="thinking-dot" /><div className="thinking-dot" /><div className="thinking-dot" />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
        <div style={{ padding: '16px 24px', borderTop: '1px solid var(--border)', display: 'flex', gap: 10, background: 'var(--bg-2)' }}>
          <input ref={inputRef} type="text" value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="¿Cuánto cuesta Don Quixote?" style={{ flex: 1 }} disabled={isLoading} />
          <button className="btn btn-primary" onClick={handleSend} disabled={isLoading || !input.trim()} style={{ flexShrink: 0 }}>
            Enviar
          </button>
        </div>
      </div>
    </div>
  )
}
"""

# Write all files
for path, content in files.items():
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: {path}")

print("\nRediseno epico completado!")
