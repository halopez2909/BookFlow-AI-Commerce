import os

BASE = "frontend-bookflow/src"

css = r"""@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg: #0A0908;
  --bg-2: #111009;
  --bg-card: #161410;
  --bg-card-hover: #1E1B16;
  --bg-glass: rgba(14,12,10,0.92);
  --text: #F5F0E8;
  --text-2: #A89880;
  --text-3: #6B5E4E;
  --accent: #C9A84C;
  --accent-dim: rgba(201,168,76,0.1);
  --accent-glow: rgba(201,168,76,0.2);
  --accent-2: #E8C97A;
  --green: #4A7C59;
  --green-light: rgba(74,124,89,0.15);
  --red: #8B3A3A;
  --red-light: rgba(139,58,58,0.15);
  --border: rgba(201,168,76,0.1);
  --border-strong: rgba(201,168,76,0.22);
  --shadow: 0 2px 8px rgba(0,0,0,0.5);
  --shadow-md: 0 8px 32px rgba(0,0,0,0.6);
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.7);
  --font-display: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --r: 6px;
  --r-lg: 12px;
  --transition: all 0.28s cubic-bezier(0.4,0,0.2,1);
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  font-family:var(--font-body);
  background:var(--bg);
  color:var(--text);
  -webkit-font-smoothing:antialiased;
  min-height:100vh;
  background-image:
    radial-gradient(ellipse 80% 40% at 10% 0%,rgba(201,168,76,0.05) 0%,transparent 70%),
    radial-gradient(ellipse 60% 40% at 90% 100%,rgba(201,168,76,0.04) 0%,transparent 70%);
}
#root{min-height:100vh;display:flex;flex-direction:column;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border-strong);border-radius:2px;}
::selection{background:var(--accent-dim);color:var(--accent-2);}
h1,h2,h3{font-family:var(--font-display);line-height:1.15;}
a{color:var(--accent);text-decoration:none;transition:var(--transition);}

/* NAVBAR */
.navbar{
  position:sticky;top:0;z-index:100;
  background:var(--bg-glass);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
  padding:0 clamp(16px,4vw,64px);
  height:68px;
  display:flex;align-items:center;justify-content:space-between;
}
.navbar-brand{
  font-family:var(--font-display);
  font-size:26px;font-weight:600;
  color:var(--text);letter-spacing:0.02em;
  cursor:pointer;transition:var(--transition);
  display:flex;align-items:center;gap:8px;
}
.navbar-brand:hover{color:var(--accent-2);}
.navbar-brand span{color:var(--accent);}
.navbar-brand::before{
  content:'';width:6px;height:6px;
  background:var(--accent);border-radius:50%;
  box-shadow:0 0 8px var(--accent);
}
.navbar-actions{display:flex;align-items:center;gap:4px;}
.navbar-link{
  font-size:13px;font-weight:500;
  color:var(--text-2);
  padding:7px 14px;border-radius:var(--r);
  background:transparent;border:none;cursor:pointer;
  font-family:var(--font-body);
  transition:var(--transition);
  letter-spacing:0.03em;
  position:relative;
}
.navbar-link:hover{color:var(--text);background:var(--accent-dim);}
.navbar-link.active{color:var(--accent);}
.navbar-link.active::after{
  content:'';position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);
  width:24px;height:1px;background:var(--accent);
  box-shadow:0 0 6px var(--accent);
}

/* CART BADGE */
.cart-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:18px;height:18px;border-radius:50%;
  background:var(--accent);color:var(--bg);
  font-size:10px;font-weight:700;
  margin-left:6px;
  animation:badgePop 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes badgePop{from{transform:scale(0);}to{transform:scale(1);}}

/* ADMIN NAV */
.admin-nav{
  background:var(--bg-2);
  border-bottom:1px solid var(--border);
  padding:0 clamp(16px,4vw,48px);
  display:flex;align-items:center;gap:4px;height:48px;
}
.admin-nav-btn{
  font-size:12px;font-weight:500;color:var(--text-3);
  padding:6px 14px;border-radius:var(--r);
  background:transparent;border:none;cursor:pointer;
  font-family:var(--font-body);transition:var(--transition);
  text-decoration:none;display:inline-flex;align-items:center;
  letter-spacing:0.04em;text-transform:uppercase;
}
.admin-nav-btn:hover{background:var(--accent-dim);color:var(--text-2);}
.admin-nav-btn.active{background:var(--accent-dim);color:var(--accent);}

/* PAGE */
.page{max-width:1320px;margin:0 auto;padding:clamp(32px,5vw,64px) clamp(16px,4vw,48px);}

/* BUTTONS */
.btn{
  font-family:var(--font-body);font-size:13px;font-weight:600;
  padding:10px 20px;border-radius:var(--r);border:none;
  cursor:pointer;transition:var(--transition);
  display:inline-flex;align-items:center;gap:8px;
  letter-spacing:0.04em;text-transform:uppercase;
  position:relative;overflow:hidden;
}
.btn::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(rgba(255,255,255,0.05),rgba(255,255,255,0));
  opacity:0;transition:var(--transition);
}
.btn:hover::after{opacity:1;}
.btn-primary{
  background:var(--accent);color:var(--bg);
  box-shadow:0 0 20px var(--accent-glow);
}
.btn-primary:hover{
  background:var(--accent-2);
  box-shadow:0 0 30px var(--accent-glow),0 4px 16px rgba(201,168,76,0.3);
  transform:translateY(-1px);
}
.btn-primary:active{transform:translateY(0);}
.btn-primary:disabled{opacity:0.4;cursor:not-allowed;transform:none;box-shadow:none;}
.btn-ghost{
  background:transparent;color:var(--text-2);
  border:1px solid var(--border-strong);
}
.btn-ghost:hover{background:var(--accent-dim);color:var(--accent);border-color:var(--accent);}
.btn-sm{font-size:11px;padding:6px 12px;}

/* INPUTS */
input,select{
  font-family:var(--font-body);font-size:14px;
  background:var(--bg-card);
  border:1px solid var(--border);color:var(--text);
  border-radius:var(--r);padding:10px 14px;
  outline:none;transition:var(--transition);width:100%;
}
input:focus,select:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-dim),0 0 12px var(--accent-glow);
}
input::placeholder{color:var(--text-3);}

/* BADGES */
.badge{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 10px;border-radius:20px;
  font-size:10px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;
}
.badge-enriched{background:rgba(74,124,89,0.2);color:#6DBF8A;border:1px solid rgba(74,124,89,0.3);}
.badge-basic{background:rgba(107,94,78,0.2);color:var(--text-3);border:1px solid var(--border);}
.badge-available{background:rgba(74,124,89,0.2);color:#6DBF8A;border:1px solid rgba(74,124,89,0.3);}

/* BOOK GRID */
.books-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:20px;}
@media(max-width:480px){.books-grid{grid-template-columns:repeat(2,1fr);gap:12px;}}

/* BOOK CARD */
.book-card{
  background:var(--bg-card);
  border:1px solid var(--border);
  border-radius:var(--r-lg);overflow:hidden;cursor:pointer;
  transition:var(--transition);display:flex;flex-direction:column;
  position:relative;
}
.book-card::before{
  content:'';position:absolute;inset:0;border-radius:var(--r-lg);
  background:linear-gradient(135deg,rgba(201,168,76,0.08),transparent);
  opacity:0;transition:var(--transition);pointer-events:none;
}
.book-card:hover{
  border-color:var(--border-strong);
  box-shadow:var(--shadow-md),0 0 20px var(--accent-glow);
  transform:translateY(-4px);
}
.book-card:hover::before{opacity:1;}
.book-card-img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block;}
.book-card-placeholder{
  width:100%;aspect-ratio:2/3;
  background:linear-gradient(135deg,var(--bg-2),var(--bg-card-hover));
  display:flex;align-items:center;justify-content:center;
  font-family:var(--font-display);font-size:42px;font-weight:300;
  color:var(--accent);font-style:italic;border-bottom:1px solid var(--border);
}
.book-card-body{padding:16px;flex:1;display:flex;flex-direction:column;gap:6px;}
.book-card-title{
  font-family:var(--font-display);font-size:15px;font-weight:600;
  color:var(--text);line-height:1.3;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.book-card-author{font-size:12px;color:var(--text-3);font-style:italic;}
.book-card-footer{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:10px;flex-wrap:wrap;gap:4px;}
.book-price{font-size:14px;font-weight:600;color:var(--accent);letter-spacing:0.02em;}
.book-price-na{font-size:12px;color:var(--text-3);font-style:italic;}

/* SKELETON */
@keyframes shimmer{
  0%{background-position:-400px 0}
  100%{background-position:400px 0}
}
.skeleton{
  background:linear-gradient(90deg,var(--bg-card) 25%,var(--bg-card-hover) 50%,var(--bg-card) 75%);
  background-size:800px 100%;
  animation:shimmer 1.8s infinite;
  border-radius:var(--r);
}
.skeleton-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;}
.skeleton-img{aspect-ratio:2/3;width:100%;}
.skeleton-line{height:12px;margin:10px 14px 0;}
.skeleton-line.short{width:60%;}
.skeleton-line.xshort{width:40%;margin-bottom:14px;}

/* FILTER BAR */
.filter-bar{display:flex;gap:12px;margin-bottom:32px;flex-wrap:wrap;align-items:flex-end;}
.filter-group{display:flex;flex-direction:column;gap:6px;}
.filter-label{font-size:10px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.1em;}
.range-row{display:flex;gap:8px;align-items:center;}

/* EMPTY STATE */
.empty-state{text-align:center;padding:80px 24px;}
.empty-state-icon{font-size:48px;margin-bottom:16px;opacity:0.3;}
.empty-state p{color:var(--text-2);margin-top:8px;font-family:var(--font-display);font-size:18px;}

/* CATALOG HERO */
.catalog-hero{margin-bottom:48px;position:relative;}
.catalog-hero h1{
  font-size:clamp(2.5rem,6vw,5rem);
  font-weight:300;color:var(--text);
  letter-spacing:-0.02em;
  background:linear-gradient(135deg,var(--text) 60%,var(--accent) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.catalog-hero p{color:var(--text-3);font-size:15px;margin-top:8px;letter-spacing:0.04em;}

/* DETAIL LAYOUT */
.detail-layout{display:grid;grid-template-columns:320px 1fr;gap:56px;align-items:start;}
@media(max-width:768px){.detail-layout{grid-template-columns:1fr;}}
.detail-img{width:100%;border-radius:var(--r-lg);box-shadow:var(--shadow-lg);object-fit:cover;}
.detail-img-placeholder{
  width:100%;aspect-ratio:2/3;border-radius:var(--r-lg);
  background:linear-gradient(135deg,var(--bg-2),var(--bg-card));
  display:flex;align-items:center;justify-content:center;
  font-family:var(--font-display);font-size:80px;font-weight:300;
  color:var(--accent);border:1px solid var(--border);font-style:italic;
}
.detail-meta{display:flex;flex-direction:column;gap:24px;}
.detail-title{font-size:clamp(2rem,4vw,3rem);font-weight:300;color:var(--text);}
.detail-author{font-size:16px;color:var(--text-2);font-style:italic;}
.detail-description{font-size:15px;line-height:1.8;color:var(--text-2);}
.detail-price-box{
  background:linear-gradient(135deg,rgba(201,168,76,0.08),rgba(201,168,76,0.04));
  border:1px solid var(--border-strong);
  border-radius:var(--r-lg);padding:20px 24px;
  position:relative;overflow:hidden;
}
.detail-price-box::before{
  content:'';position:absolute;top:-50%;right:-20%;
  width:120px;height:120px;border-radius:50%;
  background:radial-gradient(var(--accent-glow),transparent 70%);
  pointer-events:none;
}
.detail-price-value{font-size:32px;font-weight:300;color:var(--accent);font-family:var(--font-display);letter-spacing:-0.02em;}
.detail-price-explanation{font-size:12px;color:var(--text-3);margin-top:6px;line-height:1.5;}
.detail-attrs{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}
.detail-attr{background:var(--bg-2);border:1px solid var(--border);border-radius:var(--r);padding:12px 16px;}
.detail-attr-label{font-size:10px;font-weight:600;color:var(--text-3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;}
.detail-attr-value{font-size:13px;font-weight:500;color:var(--text-2);}

/* RECOMMENDATIONS */
.recs-section{margin-top:64px;padding-top:48px;border-top:1px solid var(--border);}
.recs-section h2{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:300;color:var(--text);margin-bottom:28px;}

/* LOGIN */
.login-page{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;}
@media(max-width:768px){.login-page{grid-template-columns:1fr;}}
.login-left{
  background:var(--bg-2);display:flex;align-items:center;justify-content:center;
  padding:48px;position:relative;overflow:hidden;
}
.login-left::before{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse at 30% 40%,rgba(201,168,76,0.08) 0%,transparent 60%),
    radial-gradient(ellipse at 70% 80%,rgba(201,168,76,0.05) 0%,transparent 50%);
}
.login-left-content{position:relative;z-index:1;text-align:center;}
.login-logo{font-family:var(--font-display);font-size:52px;font-weight:300;color:var(--text);letter-spacing:0.04em;}
.login-logo span{color:var(--accent);}
.login-tagline{font-size:15px;color:var(--text-3);margin-top:16px;line-height:1.7;max-width:300px;font-style:italic;}
.login-right{display:flex;align-items:center;justify-content:center;padding:48px;background:var(--bg);}
.login-form-container{width:100%;max-width:380px;}
.login-tabs{display:flex;gap:0;margin-bottom:32px;background:var(--bg-2);border-radius:var(--r);padding:4px;border:1px solid var(--border);}
.login-tab{
  flex:1;padding:9px;border-radius:var(--r);border:none;cursor:pointer;
  font-family:var(--font-body);font-weight:600;font-size:12px;
  text-transform:uppercase;letter-spacing:0.08em;transition:var(--transition);
}
.login-tab.active{background:var(--accent);color:var(--bg);box-shadow:0 0 16px var(--accent-glow);}
.login-tab:not(.active){background:transparent;color:var(--text-3);}
.login-tab:not(.active):hover{color:var(--text-2);}
.login-form-title{font-family:var(--font-display);font-size:30px;font-weight:300;margin-bottom:6px;color:var(--text);}
.login-form-subtitle{color:var(--text-3);font-size:13px;margin-bottom:28px;font-style:italic;}
.login-field{margin-bottom:18px;}
.login-label{display:block;font-size:10px;font-weight:600;color:var(--text-3);margin-bottom:8px;letter-spacing:0.1em;text-transform:uppercase;}
.login-error{background:var(--red-light);border:1px solid var(--red);color:#E8A0A0;padding:10px 14px;border-radius:var(--r);font-size:13px;margin-bottom:16px;}
.login-success{background:var(--green-light);border:1px solid var(--green);color:#8DBF9E;padding:10px 14px;border-radius:var(--r);font-size:13px;margin-bottom:16px;}
.login-submit{width:100%;padding:12px;font-size:13px;margin-top:8px;justify-content:center;}
.login-back{text-align:center;margin-top:24px;font-size:13px;color:var(--text-3);}

/* TABLES */
.table-wrap{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden;}
table{width:100%;border-collapse:collapse;}
th{
  text-align:left;padding:14px 18px;
  font-size:10px;font-weight:600;color:var(--text-3);
  text-transform:uppercase;letter-spacing:0.1em;
  border-bottom:1px solid var(--border);background:var(--bg-2);
}
td{padding:16px 18px;font-size:13px;border-bottom:1px solid var(--border);color:var(--text-2);vertical-align:middle;}
tr:last-child td{border-bottom:none;}
tr{transition:var(--transition);}
tr:hover td{background:var(--accent-dim);color:var(--text);}

/* PAGE HEADER */
.page-header{margin-bottom:32px;}
.page-header h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:300;margin-bottom:6px;}
.page-header p{color:var(--text-3);font-size:14px;font-style:italic;}

/* LOAD MORE */
.load-more{text-align:center;margin-top:48px;}
.books-count{text-align:center;color:var(--text-3);font-size:13px;margin-top:16px;letter-spacing:0.06em;}

/* ANIMATIONS */
@keyframes fadeUp{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
.fade-up{animation:fadeUp 0.5s cubic-bezier(0.4,0,0.2,1) both;}
.fade-in{animation:fadeIn 0.4s ease both;}

/* STATUS BADGES */
.status-badge{display:inline-flex;align-items:center;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;}
.status-pending{background:rgba(201,168,76,0.15);color:var(--accent);border:1px solid rgba(201,168,76,0.3);}
.status-confirmed{background:rgba(74,124,89,0.15);color:#6DBF8A;border:1px solid rgba(74,124,89,0.3);}
.status-shipped{background:rgba(100,100,200,0.15);color:#9090E8;border:1px solid rgba(100,100,200,0.3);}
.status-delivered{background:rgba(74,124,89,0.2);color:#6DBF8A;border:1px solid rgba(74,124,89,0.4);}
.status-cancelled{background:rgba(139,58,58,0.15);color:#E8A0A0;border:1px solid rgba(139,58,58,0.3);}

/* CART */
.cart-summary{
  background:var(--bg-card);border:1px solid var(--border-strong);
  border-radius:var(--r-lg);padding:24px;position:sticky;top:88px;
}
.cart-total-line{
  display:flex;justify-content:space-between;
  font-size:20px;font-family:var(--font-display);font-weight:400;
  border-top:1px solid var(--border);padding-top:16px;margin-top:16px;
}
.cart-total-amount{color:var(--accent);}

/* ASSISTANT */
.assistant-container{
  background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--r-lg);overflow:hidden;
  display:flex;flex-direction:column;
}
.message-bubble{
  max-width:75%;padding:12px 18px;border-radius:16px;
  font-size:14px;line-height:1.6;
  animation:fadeUp 0.3s cubic-bezier(0.4,0,0.2,1);
}
.message-user{
  background:linear-gradient(135deg,var(--accent),var(--copper));
  color:var(--bg);margin-left:auto;
  border-bottom-right-radius:4px;
}
.message-assistant{
  background:var(--bg-2);color:var(--text);border:1px solid var(--border);
  border-bottom-left-radius:4px;
}
.message-sources{font-size:11px;color:var(--text-3);margin-top:4px;font-style:italic;letter-spacing:0.04em;}
.thinking-dots{display:flex;gap:4px;padding:16px 20px;}
.thinking-dot{
  width:6px;height:6px;border-radius:50%;background:var(--accent);
  animation:thinking 1.4s infinite;
}
.thinking-dot:nth-child(2){animation-delay:0.2s;}
.thinking-dot:nth-child(3){animation-delay:0.4s;}
@keyframes thinking{
  0%,80%,100%{transform:scale(0.8);opacity:0.4;}
  40%{transform:scale(1.1);opacity:1;}
}

/* PRICING ADMIN */
.pricing-status-ia{background:rgba(201,168,76,0.15);color:var(--accent);border:1px solid rgba(201,168,76,0.3);}
.pricing-status-adjusted{background:rgba(74,124,89,0.15);color:#6DBF8A;border:1px solid rgba(74,124,89,0.3);}
.pricing-status-pending{background:rgba(107,94,78,0.2);color:var(--text-3);border:1px solid var(--border);}

/* DIVIDER */
.gold-divider{height:1px;background:linear-gradient(90deg,transparent,var(--accent-glow),transparent);margin:48px 0;}

/* RESPONSIVE */
@media(max-width:768px){
  .navbar{padding:0 16px;}
  .page{padding:24px 16px;}
  .detail-layout{grid-template-columns:1fr;}
  .books-grid{grid-template-columns:repeat(2,1fr);}
}

/* SCROLLBAR */
* { scrollbar-width: thin; scrollbar-color: var(--border-strong) var(--bg); }
"""

files = {}
files["index.css"] = css

# Updated NavBar
files["components/shared/NavBar.tsx"] = """import React, { useContext } from 'react'
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

  function handleLogout() {
    dispatch({ type: 'LOGOUT' })
    navigate('/catalog')
  }

  const isActive = (path: string) => location.pathname.startsWith(path)

  return (
    <nav className="navbar">
      <span className="navbar-brand" onClick={() => navigate('/catalog')}>
        <span>Book</span>Flow
      </span>
      <div className="navbar-actions">
        <button className={`navbar-link ${isActive('/catalog') ? 'active' : ''}`} onClick={() => navigate('/catalog')}>
          Catálogo
        </button>
        <button className={`navbar-link ${isActive('/assistant') ? 'active' : ''}`} onClick={() => navigate('/assistant')}>
          Asistente
        </button>
        <button className={`navbar-link ${isActive('/cart') ? 'active' : ''}`} onClick={() => navigate('/cart')}>
          Carrito
          {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
        </button>
        {state.isAuthenticated && (
          <button className={`navbar-link ${isActive('/orders') ? 'active' : ''}`} onClick={() => navigate('/orders')}>
            Pedidos
          </button>
        )}
        {state.isAuthenticated ? (
          <button className="btn btn-ghost btn-sm" onClick={handleLogout} style={{ marginLeft: 8 }}>Salir</button>
        ) : (
          <button className="btn btn-ghost btn-sm" onClick={() => navigate('/login')} style={{ marginLeft: 8 }}>Admin</button>
        )}
      </div>
    </nav>
  )
}
"""

# Updated Login
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
        setSuccess('Cuenta creada. Ahora puedes iniciar sesión.')
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
        <div className="login-left-content fade-up">
          <div className="login-logo">Book<span>Flow</span></div>
          <p className="login-tagline">Plataforma inteligente de comercio de libros con inteligencia artificial.</p>
          <div style={{ marginTop: 48, display: 'flex', flexDirection: 'column', gap: 12 }}>
            {['Catálogo enriquecido con IA', 'Precios sugeridos en tiempo real', 'Asistente conversacional', 'Recomendaciones personalizadas'].map(f => (
              <div key={f} style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--text-3)', fontSize: 13 }}>
                <span style={{ width: 4, height: 4, borderRadius: '50%', background: 'var(--accent)', flexShrink: 0, boxShadow: '0 0 6px var(--accent)' }} />
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
          <h2 className="login-form-title">{mode === 'login' ? 'Bienvenido' : 'Nueva cuenta'}</h2>
          <p className="login-form-subtitle">{mode === 'login' ? 'Accede a tu cuenta para continuar' : 'Crea tu cuenta para explorar'}</p>
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
              {loading ? (mode === 'login' ? 'Ingresando...' : 'Registrando...') : (mode === 'login' ? 'Iniciar Sesión' : 'Crear Cuenta')}
            </button>
          </form>
          <div className="login-back"><a href="/catalog">Explorar catálogo público →</a></div>
        </div>
      </div>
    </div>
  )
}
"""

# CatalogPage
files["pages/catalog/CatalogPage.tsx"] = """import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCatalog } from '../../hooks/useCatalog'
import BookCard from '../../components/catalog/BookCard'
import SkeletonCard from '../../components/catalog/SkeletonCard'
import FilterBar from '../../components/catalog/FilterBar'
import EmptyState from '../../components/shared/EmptyState'

export default function CatalogPage() {
  const navigate = useNavigate()
  const { data, isLoading, isError, refetch, filters, setFilters, fetchNextPage } = useCatalog()
  const [titleInput, setTitleInput] = useState('')

  function handleTitleChange(v: string) {
    setTitleInput(v)
    setFilters({ ...filters, title: v })
  }

  return (
    <div className="page">
      <div className="catalog-hero fade-up">
        <h1>Nuestra Colección</h1>
        <p>{data?.total ? `${data.total} títulos disponibles · enriquecidos con inteligencia artificial` : 'Descubre libros con precios y datos enriquecidos por IA'}</p>
      </div>

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
              <div key={book.id} className="fade-up" style={{ animationDelay: `${Math.min(i * 0.05, 0.5)}s` }}>
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

# AssistantPage
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

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend() {
    if (!input.trim() || isLoading) return
    const q = input.trim()
    setInput('')
    await sendMessage(q)
    inputRef.current?.focus()
  }

  return (
    <div className="page fade-up" style={{ maxWidth: 800 }}>
      <div className="page-header">
        <h1>Asistente BookFlow</h1>
        <p>Consulta precios, disponibilidad y descripción de cualquier libro</p>
      </div>

      <div className="assistant-container" style={{ height: 'calc(100vh - 340px)', minHeight: 400 }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: 24, display: 'flex', flexDirection: 'column', gap: 16 }}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', padding: 48, color: 'var(--text-3)' }}>
              <div style={{ fontSize: 48, marginBottom: 16, opacity: 0.4 }}>◎</div>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: 20, color: 'var(--text-2)', marginBottom: 8 }}>¿En qué puedo ayudarte?</p>
              <p style={{ fontSize: 13, marginBottom: 28 }}>Pregunta sobre precios, disponibilidad o descripción de libros</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' }}>
                {SUGGESTIONS.map(s => (
                  <button key={s} className="btn btn-ghost btn-sm" onClick={() => { setInput(s); inputRef.current?.focus(); }}
                    style={{ fontSize: 12, letterSpacing: '0.02em', textTransform: 'none' }}>
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
                <div className="message-sources" style={{ marginLeft: msg.role === 'user' ? 0 : 4 }}>
                  Fuentes: {msg.sources.join(', ')}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div style={{ display: 'flex', alignItems: 'flex-start' }}>
              <div className="message-bubble message-assistant" style={{ padding: 0 }}>
                <div className="thinking-dots">
                  <div className="thinking-dot" />
                  <div className="thinking-dot" />
                  <div className="thinking-dot" />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div style={{ padding: '16px 24px', borderTop: '1px solid var(--border)', display: 'flex', gap: 10, background: 'var(--bg-2)' }}>
          <input ref={inputRef} type="text" value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="¿Cuánto cuesta Don Quixote?"
            style={{ flex: 1, background: 'var(--bg-card)' }}
            disabled={isLoading}
          />
          <button className="btn btn-primary" onClick={handleSend} disabled={isLoading || !input.trim()}
            style={{ flexShrink: 0 }}>
            Enviar
          </button>
        </div>
      </div>
    </div>
  )
}
"""

# CartPage
files["pages/cart/CartPage.tsx"] = """import React, { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useCart, useUpdateCartItem, useRemoveCartItem, useClearCart } from '../../hooks/useCart'
import { useCreateOrder } from '../../hooks/useOrders'

export default function CartPage() {
  const { state } = useContext(AuthContext)
  const navigate = useNavigate()
  const customerId = state.user?.email || 'guest-001'
  const { data: cart, isLoading } = useCart(customerId)
  const updateItem = useUpdateCartItem()
  const removeItem = useRemoveCartItem()
  const clearCart = useClearCart()
  const createOrder = useCreateOrder()
  const [confirming, setConfirming] = useState(false)

  async function handleConfirmOrder() {
    if (!cart || cart.items.length === 0) return
    if (!state.isAuthenticated) { navigate('/login'); return }
    setConfirming(true)
    try {
      const orderItems = cart.items.map(item => ({
        book_id: item.book_id, quantity: item.quantity,
        unit_price: item.unit_price, title: item.book_id,
      }))
      const order = await createOrder.mutateAsync({
        customer_id: customerId, items: orderItems, notes: 'Pedido desde carrito',
      })
      await clearCart.mutateAsync(customerId)
      navigate('/orders/' + order.id)
    } catch (e: any) {
      alert(e?.response?.data?.detail?.message || 'Error al crear el pedido')
    } finally { setConfirming(false) }
  }

  if (!state.isAuthenticated && (!cart || cart.items.length === 0)) {
    return (
      <div className="page" style={{ textAlign: 'center', padding: '80px 24px' }}>
        <div style={{ fontSize: 48, marginBottom: 16, opacity: 0.3, fontFamily: 'var(--font-display)' }}>◎</div>
        <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 300, marginBottom: 8 }}>Tu carrito está vacío</h2>
        <p style={{ color: 'var(--text-3)', marginBottom: 24 }}>Explora el catálogo y agrega libros a tu carrito</p>
        <button className="btn btn-primary" onClick={() => navigate('/catalog')}>Explorar catálogo</button>
      </div>
    )
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 80, color: 'var(--text-3)' }}>Cargando carrito...</div>

  const items = cart?.items || []
  const total = cart?.total || 0

  return (
    <div className="page fade-up">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 32 }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontWeight: 300, fontSize: 'clamp(2rem,4vw,3rem)' }}>Mi Carrito</h1>
        {items.length > 0 && (
          <button className="btn btn-ghost btn-sm" onClick={() => clearCart.mutate(customerId)}>Vaciar</button>
        )}
      </div>

      {items.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 64 }}>
          <p style={{ color: 'var(--text-3)', fontFamily: 'var(--font-display)', fontSize: 20 }}>El carrito está vacío</p>
          <button className="btn btn-primary" onClick={() => navigate('/catalog')} style={{ marginTop: 20 }}>Ir al catálogo</button>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24, alignItems: 'flex-start' }}>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Libro</th><th>Precio</th><th>Cantidad</th><th>Subtotal</th><th></th></tr>
              </thead>
              <tbody>
                {items.map(item => (
                  <tr key={item.id}>
                    <td style={{ fontWeight: 500, color: 'var(--text)', maxWidth: 200 }}>{item.book_id}</td>
                    <td style={{ color: 'var(--text-2)' }}>${Number(item.unit_price).toLocaleString('es-CO')}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <button className="btn btn-ghost btn-sm" style={{ width: 28, padding: '4px 8px' }}
                          onClick={() => { if (item.quantity > 1) updateItem.mutate({ itemId: item.id, quantity: item.quantity - 1, customerId }) }}>−</button>
                        <span style={{ minWidth: 24, textAlign: 'center', fontWeight: 600 }}>{item.quantity}</span>
                        <button className="btn btn-ghost btn-sm" style={{ width: 28, padding: '4px 8px' }}
                          onClick={() => updateItem.mutate({ itemId: item.id, quantity: item.quantity + 1, customerId })}>+</button>
                      </div>
                    </td>
                    <td style={{ fontWeight: 600, color: 'var(--accent)', fontFamily: 'var(--font-display)', fontSize: 16 }}>
                      ${Number(item.subtotal).toLocaleString('es-CO')}
                    </td>
                    <td>
                      <button className="btn btn-ghost btn-sm" style={{ color: 'var(--red)', borderColor: 'var(--red-light)' }}
                        onClick={() => removeItem.mutate({ itemId: item.id, customerId })}>✕</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="cart-summary">
            <h3 style={{ fontFamily: 'var(--font-display)', fontWeight: 400, fontSize: 22, marginBottom: 20 }}>Resumen</h3>
            <div style={{ color: 'var(--text-3)', fontSize: 13, marginBottom: 8 }}>
              {items.length} {items.length === 1 ? 'título' : 'títulos'}
            </div>
            <div className="cart-total-line">
              <span>Total</span>
              <span className="cart-total-amount">${Number(total).toLocaleString('es-CO')} COP</span>
            </div>
            <button className="btn btn-primary" style={{ width: '100%', marginTop: 20, justifyContent: 'center' }}
              onClick={handleConfirmOrder} disabled={confirming}>
              {confirming ? 'Procesando...' : 'Confirmar Pedido'}
            </button>
            {!state.isAuthenticated && (
              <p style={{ fontSize: 12, color: 'var(--text-3)', marginTop: 12, textAlign: 'center', fontStyle: 'italic' }}>
                Debes <a href="/login" style={{ color: 'var(--accent)' }}>iniciar sesión</a> para confirmar
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
"""

# OrdersPage
files["pages/orders/OrdersPage.tsx"] = """import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'
import { useOrders } from '../../hooks/useOrders'
import api from '../../services/apiClient'

const STATUS: Record<string, string> = {
  pending: 'status-pending', confirmed: 'status-confirmed',
  shipped: 'status-shipped', delivered: 'status-delivered', cancelled: 'status-cancelled',
}
const STATUS_LABELS: Record<string, string> = {
  pending: 'Pendiente', confirmed: 'Confirmado',
  shipped: 'Enviado', delivered: 'Entregado', cancelled: 'Cancelado',
}

export default function OrdersPage() {
  const { state } = useContext(AuthContext)
  const navigate = useNavigate()
  const customerId = state.user?.email || 'guest-001'
  const { data: orders, isLoading, refetch } = useOrders(customerId)

  if (!state.isAuthenticated) {
    return (
      <div className="page" style={{ textAlign: 'center', padding: '80px 24px' }}>
        <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 300 }}>Inicia sesión para ver tus pedidos</h2>
        <button className="btn btn-primary" onClick={() => navigate('/login')} style={{ marginTop: 24 }}>Iniciar sesión</button>
      </div>
    )
  }

  if (isLoading) return <div className="page" style={{ textAlign: 'center', padding: 80, color: 'var(--text-3)' }}>Cargando pedidos...</div>

  async function handleCancel(orderId: string) {
    if (!confirm('¿Cancelar este pedido?')) return
    try { await api.put('/api/orders/' + orderId + '/status', { status: 'cancelled' }); refetch() }
    catch (e: any) { alert(e?.response?.data?.detail || 'No se pudo cancelar') }
  }

  return (
    <div className="page fade-up">
      <div className="page-header">
        <h1>Mis Pedidos</h1>
        <p>Historial completo de tus compras</p>
      </div>
      {!orders || orders.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 64 }}>
          <p style={{ color: 'var(--text-3)', fontFamily: 'var(--font-display)', fontSize: 20 }}>No tienes pedidos aún</p>
          <button className="btn btn-primary" onClick={() => navigate('/catalog')} style={{ marginTop: 20 }}>Ir al catálogo</button>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>ID</th><th>Estado</th><th>Total</th><th>Fecha</th><th>Acciones</th></tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id} style={{ cursor: 'pointer' }} onClick={() => navigate('/orders/' + order.id)}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--text-3)' }}>{order.id.slice(0, 8)}...</td>
                  <td><span className={`status-badge ${STATUS[order.status] || ''}`}>{STATUS_LABELS[order.status] || order.status}</span></td>
                  <td style={{ fontFamily: 'var(--font-display)', fontSize: 16, color: 'var(--accent)', fontWeight: 400 }}>
                    ${order.total_amount.toLocaleString('es-CO')} COP
                  </td>
                  <td style={{ color: 'var(--text-3)', fontSize: 12 }}>{new Date(order.created_at).toLocaleDateString('es-CO')}</td>
                  <td style={{ display: 'flex', gap: 8 }} onClick={e => e.stopPropagation()}>
                    <span style={{ color: 'var(--accent)', fontSize: 13 }}>Ver →</span>
                    {order.status === 'pending' && (
                      <button className="btn btn-ghost btn-sm" style={{ color: '#E8A0A0', borderColor: 'var(--red-light)', fontSize: 11 }}
                        onClick={() => handleCancel(order.id)}>Cancelar</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
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

print("\nRediseno completado!")
