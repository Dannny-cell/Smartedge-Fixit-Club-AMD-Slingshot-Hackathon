"""
SmartEdge Copilot v2 — AMD Slingshot Hackathon
A fully humanized AI workspace. Warm, alive, and personal.
"""

import streamlit as st
import plotly.graph_objects as go
import datetime
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import init_db
init_db()

from backend.research import generate_research, answer_followup
from backend.research_db import search_research_notes
from backend.meeting import generate_meeting_summary
from backend.meeting_db import save_meeting_note, list_meeting_notes, list_tasks_for_meeting
from backend.tasks import list_tasks, update_task_status, create_task, get_due_soon
from backend.knowledge_hub import search_knowledge_hub
from backend.analytics_service import (
    get_feature_summary, get_overall_totals, get_usage_over_time, generate_performance_insights,
    get_meeting_sentiment_stats
)
from backend.export_service import export_note_markdown
from backend.database import DB_PATH
from backend.optimizer import generate_optimized_prompt, compare_prompts

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartEdge Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS — warm, human, alive ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;0,9..144,700;1,9..144,400&display=swap');

:root {
  --bg:       #0f0f11;
  --sf:       #17171a;
  --sf2:      #1e1e22;
  --bd:       #2a2a30;
  --bd2:      #353540;
  --amd:      #e8450a;
  --amd2:     #f5841f;
  --amber:    #f0a500;
  --teal:     #00c9a7;
  --lilac:    #a78bfa;
  --sky:      #38bdf8;
  --rose:     #fb7185;
  --text:     #e8e8f0;
  --muted:    #7a7a90;
  --dim:      #404050;
  --r:        14px;
  --rs:       8px;
}
*,*::before,*::after{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Sora',sans-serif!important}
[data-testid="stSidebar"]{background:var(--sf)!important;border-right:1px solid var(--bd)!important}
[data-testid="stSidebar"] *{color:var(--text)!important}
#MainMenu,footer{visibility:hidden}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:2px}

/* Cards */
.card{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:1.3rem 1.5rem;margin-bottom:1rem;transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:var(--bd2);box-shadow:0 4px 24px rgba(0,0,0,.3)}
.ca{border-left:3px solid var(--amd)}
.ct{border-left:3px solid var(--teal)}
.cam{border-left:3px solid var(--amber)}
.cl{border-left:3px solid var(--lilac)}
.csk{border-left:3px solid var(--sky)}

/* Typography */
.eyebrow{font-family:'DM Mono',monospace;font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:.3rem}
.ptitle{font-family:'Fraunces',serif;font-size:2rem;font-weight:700;color:var(--text);line-height:1.15;margin-bottom:.15rem}
.psub{font-size:.875rem;color:var(--muted);margin-bottom:1.6rem;line-height:1.5}

/* KPI */
.kpi{background:var(--sf);border:1px solid var(--bd);border-radius:var(--r);padding:1.1rem 1.3rem;text-align:center}
.kpi-label{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:.45rem}
.kpi-val{font-family:'Fraunces',serif;font-size:1.9rem;font-weight:700;color:var(--text);line-height:1}
.kpi-sub{font-size:.7rem;color:var(--muted);margin-top:.25rem}

/* Tag */
.tag{display:inline-block;font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.06em;text-transform:uppercase;padding:.12rem .48rem;border-radius:99px;border:1px solid;margin-right:.3rem;line-height:1.8}
.ta{color:var(--amd2);border-color:rgba(245,132,31,.35);background:rgba(232,69,10,.08)}
.tt{color:var(--teal);border-color:rgba(0,201,167,.35);background:rgba(0,201,167,.07)}
.tam{color:var(--amber);border-color:rgba(240,165,0,.35);background:rgba(240,165,0,.07)}
.tl{color:var(--lilac);border-color:rgba(167,139,250,.35);background:rgba(167,139,250,.07)}
.tsk{color:var(--sky);border-color:rgba(56,189,248,.35);background:rgba(56,189,248,.07)}
.tr{color:var(--rose);border-color:rgba(251,113,133,.35);background:rgba(251,113,133,.07)}

/* Result item */
.ri{background:var(--sf2);border:1px solid var(--bd);border-radius:var(--rs);padding:.85rem 1rem;margin-bottom:.55rem;transition:border-color .2s}
.ri:hover{border-color:var(--bd2)}
.ri-title{font-weight:600;font-size:.92rem;margin-bottom:.18rem;color:var(--text)}
.ri-meta{font-family:'DM Mono',monospace;font-size:.56rem;color:var(--muted);margin-bottom:.35rem;letter-spacing:.05em}
.ri-body{font-size:.82rem;color:#aaaabb;line-height:1.6}

/* Task */
.tr-row{display:flex;align-items:flex-start;gap:.7rem;background:var(--sf2);border:1px solid var(--bd);border-radius:var(--rs);padding:.75rem .95rem;margin-bottom:.4rem}
.td{width:8px;height:8px;border-radius:50%;flex-shrink:0;margin-top:5px}
.dp{background:var(--amber)}
.dd{background:var(--teal)}
.dc{background:var(--dim)}

/* Insight box */
.ib{background:rgba(232,69,10,.07);border:1px solid rgba(232,69,10,.22);border-radius:var(--rs);padding:.75rem .95rem;font-size:.82rem;color:#d4d4e8;line-height:1.55;margin-bottom:.75rem}

/* Empty state */
.es{text-align:center;padding:2.8rem 2rem;background:var(--sf);border:1px dashed var(--bd2);border-radius:var(--r)}
.es-icon{font-size:2.3rem;margin-bottom:.65rem}
.es-title{font-family:'Fraunces',serif;font-size:1.15rem;font-weight:500;color:var(--muted);margin-bottom:.35rem}
.es-body{font-size:.8rem;color:var(--dim);max-width:340px;margin:0 auto}

/* Progress bar */
.pb-wrap{background:var(--sf2);border-radius:4px;height:6px;overflow:hidden;margin:.25rem 0}
.pb-fill{height:100%;border-radius:4px;transition:width .4s ease}

/* Speed bar */
.sb-wrap{background:var(--sf2);border-radius:3px;height:7px;margin-top:.25rem;overflow:hidden}
.sb-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--teal),var(--sky))}

/* Sidebar */
.sb-brand{padding:1.1rem .9rem .5rem;border-bottom:1px solid var(--bd);margin-bottom:.4rem}
.sb-name{font-family:'Fraunces',serif;font-size:1.25rem;font-weight:700;color:var(--text);line-height:1.1}
.sb-sub{font-family:'DM Mono',monospace;font-size:.56rem;letter-spacing:.12em;color:var(--amd);text-transform:uppercase;margin-top:.2rem}
.nav-sec{font-family:'DM Mono',monospace;font-size:.56rem;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);padding:.45rem .75rem .15rem}

/* AMD hero */
.amd-hero{background:linear-gradient(135deg,rgba(232,69,10,.15) 0%,rgba(245,132,31,.08) 100%);border:1px solid rgba(232,69,10,.22);border-radius:var(--r);padding:1.3rem 1.5rem;margin-bottom:1.3rem;display:flex;align-items:center;gap:1rem}

/* Buttons */
.stButton>button{background:var(--amd)!important;color:white!important;border:none!important;border-radius:var(--rs)!important;font-family:'Sora',sans-serif!important;font-weight:600!important;letter-spacing:.03em!important;font-size:.83rem!important;padding:.48rem 1.1rem!important;transition:background .2s,transform .1s!important}
.stButton>button:hover{background:var(--amd2)!important;transform:translateY(-1px)!important}
.stButton>button:active{transform:translateY(0)!important}

/* Inputs */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--sf2)!important;border:1px solid var(--bd)!important;border-radius:var(--rs)!important;color:var(--text)!important;font-family:'Sora',sans-serif!important;font-size:.86rem!important}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:var(--amd)!important;box-shadow:0 0 0 2px rgba(232,69,10,.15)!important}
.stSelectbox>div>div{background:var(--sf2)!important;border:1px solid var(--bd)!important;border-radius:var(--rs)!important;color:var(--text)!important}
input::placeholder,textarea::placeholder{color:var(--dim)!important}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:var(--sf2)!important;border-radius:var(--rs)!important;padding:3px!important;gap:2px!important;border:1px solid var(--bd)!important}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--muted)!important;border-radius:6px!important;font-family:'Sora',sans-serif!important;font-size:.8rem!important;font-weight:500!important;padding:.38rem .85rem!important;border:none!important}
.stTabs [aria-selected="true"]{background:var(--amd)!important;color:white!important}

hr{border-color:var(--bd)!important}
.stCheckbox label{color:var(--muted)!important;font-size:.83rem!important}
.stRadio label{color:var(--text)!important}
.streamlit-expanderHeader{background:var(--sf2)!important;border:1px solid var(--bd)!important;border-radius:var(--rs)!important;color:var(--text)!important;font-family:'Sora',sans-serif!important}
.streamlit-expanderContent{border:1px solid var(--bd)!important;border-top:none!important;background:var(--sf)!important}
</style>
""", unsafe_allow_html=True)

# ─── Plotly default theme ─────────────────────────────────────────────────────
CHART = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#7a7a90", size=10),
    colorway=["#e8450a","#f5841f","#00c9a7","#38bdf8","#a78bfa","#fb7185","#f0a500"],
    hoverlabel=dict(bgcolor="#1e1e22", font=dict(color="#e8e8f0", family="DM Mono"), bordercolor="#353540"),
    margin=dict(l=8, r=8, t=26, b=8),
    xaxis=dict(gridcolor="#2a2a30", zerolinecolor="#2a2a30", tickfont=dict(size=9)),
    yaxis=dict(gridcolor="#2a2a30", zerolinecolor="#2a2a30", tickfont=dict(size=9)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
)

# ─── Session state ────────────────────────────────────────────────────────────
PAGES = ["Home","Research","Prompt Lab","Meetings","Tasks","Knowledge","Analytics","Slingshot Lab"]
ICONS = {"Home":"🏠","Research":"🔬","Prompt Lab":"⚗️","Meetings":"🎙️","Tasks":"✅","Knowledge":"🧠","Analytics":"📊","Slingshot Lab":"⚡"}
for k,v in [("page","Home"),("research_ctx",None),("research_chat",[]),("opt_result",None),("opt_report",None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-name">SmartEdge<br>Copilot</div>
      <div class="sb-sub">⚡ AMD Slingshot 2025</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="nav-sec">Navigate</div>', unsafe_allow_html=True)

    for p in PAGES:
        is_active = st.session_state.page == p
        if st.button(f"{ICONS[p]}  {p}", key=f"nav_{p}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page = p
            st.rerun()

    st.markdown("---")
    totals_sb = get_overall_totals()
    now_sb = datetime.datetime.now()
    st.markdown(f"""
    <div style="padding:.5rem .75rem">
      <div style="font-family:'DM Mono',monospace;font-size:.56rem;color:var(--dim);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.45rem">Session</div>
      <div style="font-size:.76rem;color:var(--muted);line-height:2.1">
        🕐 {now_sb.strftime("%H:%M, %b %d")}<br>
        🔢 {totals_sb["total_runs"]} AI runs<br>
        💰 ${totals_sb["total_cost"]:.4f} used<br>
        ⚡ Powered by Groq
      </div>
    </div>""", unsafe_allow_html=True)

page = st.session_state.page

# ─── Helper functions ─────────────────────────────────────────────────────────
def hdr(eyebrow, title, sub=""):
    st.markdown(f"""
    <div class="eyebrow">{eyebrow}</div>
    <div class="ptitle">{title}</div>
    {'<div class="psub">' + sub + '</div>' if sub else ''}
    """, unsafe_allow_html=True)

def insight(text, icon="💡"):
    st.markdown(f'<div class="ib"><span style="margin-right:.35rem">{icon}</span>{text}</div>', unsafe_allow_html=True)

def empty(icon, title, body):
    st.markdown(f'<div class="es"><div class="es-icon">{icon}</div><div class="es-title">{title}</div><div class="es-body">{body}</div></div>', unsafe_allow_html=True)

def pbar(pct, color="var(--amd)"):
    pct = max(0, min(100, pct))
    return f'<div class="pb-wrap"><div class="pb-fill" style="width:{pct}%;background:{color}"></div></div>'

def tag_html(label, style="a"):
    return f'<span class="tag t{style}">{label}</span>'


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    now = datetime.datetime.now()
    hour = now.hour
    greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")

    hdr("Your workspace", f"{greeting} 👋", "Here's what's happening across your AI copilot right now.")

    st.markdown(f"""
    <div class="amd-hero">
      <div style="font-size:2.5rem">⚡</div>
      <div>
        <div style="font-family:'Fraunces',serif;font-size:1.05rem;font-weight:600;color:var(--text)">SmartEdge is live and running on Groq's LPU</div>
        <div style="font-size:.78rem;color:var(--muted);margin-top:.2rem">AMD Slingshot Hackathon 2025 · {now.strftime("%A, %B %d")} · All systems go</div>
      </div>
    </div>""", unsafe_allow_html=True)

    totals = get_overall_totals()
    summary = get_feature_summary()
    tasks_all = list_tasks()
    pending = [t for t in tasks_all if t[6]=="pending"]
    done_t  = [t for t in tasks_all if t[6]=="done"]
    due_soon = get_due_soon(3)

    k1,k2,k3,k4,k5 = st.columns(5)
    kpis = [
        (k1,"AI Runs",str(totals["total_runs"]),"total","var(--amd)"),
        (k2,"Tokens",f"{totals['total_tokens']:,}","consumed","var(--sky)"),
        (k3,"Avg Speed",f"{totals['avg_latency_ms']:.0f}ms","per call","var(--teal)"),
        (k4,"Spend",f"${totals['total_cost']:.4f}","USD","var(--amber)"),
        (k5,"Open Tasks",str(len(pending)),f"{len(due_soon)} due soon","var(--lilac)"),
    ]
    for col, lbl, val, sub, clr in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi" style="border-top:2px solid {clr}">
              <div class="kpi-label">{lbl}</div>
              <div class="kpi-val" style="color:{clr}">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        st.markdown('<div class="card ca">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:1.05rem;font-weight:600;margin-bottom:.9rem">🧭 Feature Activity</div>', unsafe_allow_html=True)
        if summary:
            keys   = list(summary.keys())
            labels = [k.replace("_"," ").title() for k in keys]
            runs   = [summary[k]["total_runs"] for k in keys]
            clrs   = ["#e8450a","#f5841f","#00c9a7","#38bdf8","#a78bfa","#fb7185"]
            fig = go.Figure()
            for i,(lbl,r) in enumerate(zip(labels,runs)):
                fig.add_trace(go.Bar(x=[lbl],y=[r],name=lbl,marker_color=clrs[i%len(clrs)],
                    marker_line_width=0,width=.55,
                    hovertemplate=f"<b>{lbl}</b><br>Runs: %{{y}}<extra></extra>"))
            fig.update_layout(**CHART, height=210, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            empty("🧭","No activity yet","Run research or analyze a meeting to see feature activity.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card cam">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:1rem;font-weight:600;margin-bottom:.8rem">📋 Open Tasks</div>', unsafe_allow_html=True)
        if pending:
            for t in pending[:4]:
                tid,src_t,src_id,assignee,desc,deadline,status,created = t
                urg=""
                if deadline:
                    try:
                        dl=datetime.datetime.strptime(deadline,"%Y-%m-%d").date()
                        d=(dl-datetime.date.today()).days
                        urg=f' · <span style="color:{"var(--rose)" if d<=2 else "var(--amber)"};font-size:.62rem">{d}d left</span>'
                    except: pass
                st.markdown(f"""<div class="tr-row"><div class="td dp"></div>
                <div style="flex:1;min-width:0">
                  <div style="font-size:.83rem;color:var(--text);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{desc}</div>
                  <div style="font-family:'DM Mono',monospace;font-size:.56rem;color:var(--muted)">{assignee or "Unassigned"}{urg}</div>
                </div></div>""", unsafe_allow_html=True)
            if len(pending)>4:
                st.markdown(f'<div style="font-size:.72rem;color:var(--muted);text-align:center;margin-top:.3rem">+{len(pending)-4} more</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:.83rem;color:var(--muted)">✨ All caught up!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:1rem;font-weight:600;margin-bottom:.8rem">🚀 Quick Start</div>', unsafe_allow_html=True)
        for icon, lbl, dest in [("🔬","Research a topic","Research"),("🎙️","Analyze a meeting","Meetings"),("⚗️","Optimize a prompt","Prompt Lab"),("⚡","AMD Slingshot Lab","Slingshot Lab")]:
            if st.button(f"{icon} {lbl}", key=f"qs_{dest}", use_container_width=True):
                st.session_state.page = dest
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    col_ins, col_rec = st.columns([2,3])
    with col_ins:
        perf = generate_performance_insights()
        st.markdown('<div class="card ct">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:1rem;font-weight:600;margin-bottom:.8rem">💡 Insights</div>', unsafe_allow_html=True)
        if summary and totals["total_runs"]>0:
            avg = totals["avg_latency_ms"]
            lbl_speed = "fast ⚡" if avg<500 else ("moderate 🟡" if avg<1500 else "slow 🔴")
            insight(f"Average response time is <b>{avg:.0f}ms</b> — {lbl_speed}.", "⚡")
            most_exp = perf.get("most_expensive_feature","")
            if most_exp:
                insight(f"<b>{most_exp.replace('_',' ').title()}</b> is your highest-cost feature.", "💸")
            if totals["total_runs"]>=3:
                insight(f"<b>{totals['total_runs']} AI sessions</b> completed — great momentum!", "🎯")
        else:
            insight("Run your first research query to generate insights.", "🌱")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_rec:
        st.markdown('<div class="card csk">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:1rem;font-weight:600;margin-bottom:.8rem">🔬 Recent Research</div>', unsafe_allow_html=True)
        recent = search_research_notes("")
        if recent:
            for n in recent[:3]:
                preview = n['summary'][:110]+"…" if len(n['summary'])>110 else n['summary']
                st.markdown(f"""<div class="ri">
                  <div class="ri-title">🔍 {n['query']}</div>
                  <div class="ri-meta">{n['created_at'][:16]} · {n['total_tokens']:,} tok · ${n['cost']:.5f}</div>
                  <div class="ri-body">{preview}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:.83rem;color:var(--muted)">No research yet. Head to Research to get started!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="card cl">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:1rem;font-weight:600;margin-bottom:.8rem">🎭 Meeting Sentiment Analysis</div>', unsafe_allow_html=True)
    c_sent1, c_sent2 = st.columns([2,1])
    with c_sent1:
        sent_stats = get_meeting_sentiment_stats()
        if any(sent_stats.values()):
            labels = list(sent_stats.keys())
            values = list(sent_stats.values())
            colors = ["#00c9a7", "#7a7a90", "#fb7185"] # Teal, Muted, Rose
            fig_sent = go.Figure(go.Pie(
                labels=labels, values=values, hole=.6,
                marker=dict(colors=colors, line=dict(color="#17171a", width=2)),
                textfont=dict(family="DM Mono", size=10)
            ))
            fig_sent.update_layout(**CHART, height=220, showlegend=True, margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig_sent, use_container_width=True, config={"displayModeBar":False})
        else:
            empty("🎭", "No sentiment data", "Analyze your first meeting to see emotional trends here.")
    with c_sent2:
        st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
        if any(sent_stats.values()):
            total_s = sum(sent_stats.values())
            pos_p = (sent_stats["Positive"]/total_s)*100
            st.markdown(f"""<div style="text-align:center">
                <div class="kpi-label">Positive Vibes</div>
                <div class="kpi-val" style="color:var(--teal)">{pos_p:.0f}%</div>
                <div class="kpi-sub">across {total_s} meetings</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:.83rem;color:var(--muted);text-align:center">Sentiment metrics will appear here.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RESEARCH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Research":
    hdr("Explore & discover","Research Assistant","Structured AI-powered deep dives, saved automatically to your knowledge base.")

    tab_new, tab_hist = st.tabs(["✨  New Research","📚  Past Notes"])

    with tab_new:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        query = st.text_input("", placeholder="What would you like to explore? e.g. 'How does Groq's LPU architecture work?'", key="rq")
        c1, c2, _ = st.columns([1.6,1,4])
        with c1: run_btn = st.button("✨ Generate Research", key="btn_rq")
        with c2: clear_btn = st.button("Clear", key="btn_rq_clear")
        st.markdown('</div>', unsafe_allow_html=True)

        if clear_btn:
            st.session_state.research_ctx = None
            st.session_state.research_chat = []
            st.rerun()

        if run_btn and query.strip():
            with st.spinner("🔬 Thinking deeply about your topic…"):
                try:
                    result = generate_research(query.strip())
                    st.success("Research complete — saved to your knowledge base!")
                    m = result["metrics"]
                    st.markdown(f"""<div style="display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1rem">
                      {tag_html("Groq","a")}{tag_html(m['model'][:28],"sk")}{tag_html(f"{m['total_tokens']:,} tokens","t")}{tag_html(f"{m['latency_ms']:.0f}ms","am")}{tag_html(f"${m['cost']:.5f}","l")}
                    </div>""", unsafe_allow_html=True)

                    st.markdown('<div class="card ca">', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-family:\'Fraunces\',serif;font-size:1.05rem;font-weight:600;margin-bottom:.7rem">📝 Summary</div><div style="font-size:.9rem;color:#d0d0e0;line-height:1.75">{result["summary"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    ca, cb = st.columns(2)
                    with ca:
                        st.markdown('<div class="card ct"><div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">💡 Key Concepts</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:.86rem;color:#bbbbd0;line-height:1.7;white-space:pre-wrap">{result["key_concepts"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cb:
                        st.markdown('<div class="card cam"><div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">🚀 Applications</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:.86rem;color:#bbbbd0;line-height:1.7;white-space:pre-wrap">{result["applications"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="card cl"><div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">🔗 References</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:.84rem;color:#bbbbd0;line-height:1.7;white-space:pre-wrap">{result["references"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    ctx = f"Topic: {query.strip()}\n\nSummary:\n{result['summary']}\n\nKey Concepts:\n{result['key_concepts']}\n\nApplications:\n{result['applications']}\n\nReferences:\n{result['references']}"
                    st.session_state.research_ctx = ctx
                    st.session_state.research_chat = []
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        if st.session_state.research_ctx:
            st.markdown('<div class="card csk"><div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.8rem">💬 Follow-up Q&A</div>', unsafe_allow_html=True)
            for msg in st.session_state.research_chat:
                is_user = msg["role"]=="user"
                bg = "var(--sf2)" if is_user else "rgba(0,201,167,.07)"
                bd = "var(--bd)" if is_user else "rgba(0,201,167,.22)"
                icon = "🧑" if is_user else "🤖"
                st.markdown(f'<div style="background:{bg};border:1px solid {bd};border-radius:7px;padding:.65rem .85rem;margin-bottom:.45rem"><span style="font-size:.7rem;color:var(--muted);margin-right:.35rem">{icon}</span><span style="font-size:.86rem;color:#d0d0e0;line-height:1.6">{msg["content"]}</span></div>', unsafe_allow_html=True)
            fq = st.text_input("", placeholder="Dig deeper — ask anything about this research…", key="fq")
            if st.button("Ask ✨", key="btn_fq") and (fq or "").strip():
                st.session_state.research_chat.append({"role":"user","content":fq.strip()})
                with st.spinner("Thinking…"):
                    ans = answer_followup(st.session_state.research_ctx, fq.strip())
                st.session_state.research_chat.append({"role":"assistant","content":ans.get("answer","")})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        elif not query.strip():
            empty("🔬","Ready to explore","Type any topic — from quantum computing to marketing strategy — and get a structured, cited research brief in seconds.")

    with tab_hist:
        kw = st.text_input("", placeholder="Search your notes…", key="rh_kw")
        notes = search_research_notes(kw or "")
        if notes:
            st.markdown(f'<div style="font-size:.78rem;color:var(--muted);margin-bottom:.7rem">{len(notes)} note{"s" if len(notes)!=1 else ""}</div>', unsafe_allow_html=True)
            for n in notes:
                with st.expander(f"🔍  {n['query']}   ·   {n['created_at'][:10]}"):
                    st.markdown(f"**Summary:** {n['summary']}")
                    st.markdown(f"**Key Concepts:**\n{n['key_concepts']}")
                    st.caption(f"Model: {n['model']} · {n['total_tokens']:,} tokens · ${n['cost']:.6f} · {n['latency_ms']:.0f}ms")
                    if st.button("📥 Export", key=f"exp_r_{n['id']}"):
                        try:
                            md = export_note_markdown(DB_PATH,"research",n["id"])
                            st.download_button("⬇️ Download .md", md, file_name=f"research_{n['id']}.md", mime="text/markdown", key=f"dl_r_{n['id']}")
                        except Exception as e:
                            st.error(str(e))
        else:
            empty("📚","Nothing here yet","Your research notes will appear here after you run your first query.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PROMPT LAB
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Prompt Lab":
    hdr("Fine-tune your words","Prompt Lab","Optimize prompts for token efficiency, speed, and quality — see exactly what changes and why.")

    cl, cr = st.columns([3,2])
    with cl:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">✍️ Your Prompt</div>', unsafe_allow_html=True)
        raw_prompt = st.text_area("", height=190, placeholder="Paste any prompt you want to improve. Could be a research request, a coding task, a writing brief — anything.", key="opt_raw")
        cb_q = st.checkbox("🔍 Run quality judge comparison", value=False)
        b1, b2 = st.columns(2)
        with b1: btn_opt = st.button("✨ Optimize Prompt", key="btn_opt", use_container_width=True)
        with b2: btn_cmp = st.button("⚖️ Compare Both", key="btn_cmp", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if btn_opt and raw_prompt.strip():
            with st.spinner("🧠 Analyzing and optimizing…"):
                opt = generate_optimized_prompt(raw_prompt.strip())
                st.session_state.opt_result = opt

        if st.session_state.opt_result:
            st.markdown('<div class="card ct">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">✨ Optimized</div>', unsafe_allow_html=True)
            st.text_area("", value=st.session_state.opt_result, height=155, key="opt_view")
            if raw_prompt:
                ow = len(raw_prompt.split()); nw = len(st.session_state.opt_result.split())
                r = (1 - nw/max(ow,1))*100
                if r>0: insight(f"Compressed by <b>{r:.0f}%</b> ({ow} → {nw} words). Shorter = faster + cheaper.", "📉")
            st.markdown('</div>', unsafe_allow_html=True)

        if btn_cmp and raw_prompt.strip():
            with st.spinner("⚖️ Running head-to-head on Groq…"):
                try:
                    report = compare_prompts("optimizer", raw_prompt.strip(), optimized_prompt=st.session_state.opt_result, run_quality_judge=cb_q)
                    st.session_state.opt_report = report
                except Exception as e:
                    st.error(f"Error: {e}")

    with cr:
        st.markdown('<div class="card ca" style="height:fit-content">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.85rem">📊 Comparison Results</div>', unsafe_allow_html=True)
        rep = st.session_state.opt_report
        if rep:
            for metric, rv, ov, pct in [("Tokens",rep.raw.tokens_used,rep.optimized.tokens_used,rep.pct_token_savings),("Latency",f"{rep.raw.latency_ms:.0f}ms",f"{rep.optimized.latency_ms:.0f}ms",rep.pct_latency_improvement),("Cost",f"${rep.raw.cost:.5f}",f"${rep.optimized.cost:.5f}",rep.pct_cost_savings)]:
                arrow="▼" if pct<0 else "▲"
                clr="var(--teal)" if pct<0 else "var(--rose)"
                st.markdown(f"""<div style="border-bottom:1px solid var(--bd);padding:.55rem 0;display:flex;justify-content:space-between;align-items:center">
                  <div style="font-size:.8rem;color:var(--muted)">{metric}</div>
                  <div style="text-align:right">
                    <div style="font-family:'DM Mono',monospace;font-size:.76rem;color:var(--text)">{rv} → {ov}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:.65rem;color:{clr}">{arrow} {abs(pct):.1f}%</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            vc = {"better":"var(--teal)","worse":"var(--rose)","same":"var(--amber)"}.get(rep.verdict,"var(--muted)")
            st.markdown(f"""<div style="margin-top:.85rem;padding:.75rem;background:rgba(0,0,0,.2);border-radius:7px;border:1px solid var(--bd)">
              <div style="font-family:'Fraunces',serif;font-size:.9rem;font-weight:600;color:{vc};margin-bottom:.35rem">Verdict: {rep.verdict.upper()}</div>
              <div style="font-size:.8rem;color:#aaaabb;line-height:1.55">{rep.summary}</div>
            </div>""", unsafe_allow_html=True)
            if rep.recommendations:
                for r2 in rep.recommendations:
                    st.markdown(f'<div style="font-size:.78rem;color:var(--muted);padding:.28rem 0;border-bottom:1px solid var(--bd)">• {r2}</div>', unsafe_allow_html=True)
        else:
            empty("⚖️","Nothing yet","Paste a prompt, optimize it, then compare to see savings.")
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MEETINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Meetings":
    hdr("Never miss a detail","Meeting Intelligence","Paste any transcript — get actions, decisions, risks, sentiment and more in seconds.")

    tab_new, tab_hist = st.tabs(["🎙️  Analyze Meeting","📁  Past Meetings"])

    with tab_new:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        title = st.text_input("", placeholder="Meeting title, e.g. 'Q4 Sprint Planning — Nov 29'", key="mtitle")
        transcript = st.text_area("", height=215, placeholder="Paste the full transcript here.\n\nExample:\nAlex: I think we should ship the auth layer by Friday.\nJordan: Agreed. I'll handle the backend — Sam does frontend.\nAlex: Great. Let's review Thursday at 2pm.", key="mtranscript")
        run_meeting = st.button("🎙️ Analyze Meeting", key="btn_meeting")
        st.markdown('</div>', unsafe_allow_html=True)

        if run_meeting and title.strip() and transcript.strip():
            with st.spinner("Reading your meeting…"):
                try:
                    result = generate_meeting_summary(title.strip(), transcript.strip())
                    m = result["metrics"]
                    st.success(f"Meeting analyzed! Action items extracted and saved as tasks.")
                    st.markdown(f"""<div style="display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1.1rem">
                      {tag_html("Groq","a")}{tag_html(m['model'][:26],"sk")}{tag_html(f"{m['total_tokens']:,} tok","t")}{tag_html(f"{m['latency_ms']:.0f}ms","am")}
                    </div>""", unsafe_allow_html=True)

                    cs, ca = st.columns(2)
                    with cs:
                        st.markdown('<div class="card ca"><div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">📋 Summary</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:.86rem;color:#d0d0e0;line-height:1.72">{result["summary"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with ca:
                        st.markdown('<div class="card ct"><div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.65rem">✅ Action Items</div>', unsafe_allow_html=True)
                        for line in result.get("action_items","").splitlines():
                            if line.strip():
                                st.markdown(f'<div class="tr-row"><div class="td dp"></div><div style="font-size:.83rem;color:#d0d0e0">{line.strip()}</div></div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    c1,c2,c3,c4 = st.columns(4)
                    for col, icon, hd, content, acc in [
                        (c1,"🧭","Key Topics",result.get("key_topics",""),"sk"),
                        (c2,"📅","Deadlines",result.get("deadlines",""),"am"),
                        (c3,"⚠️","Risks",result.get("risks",""),"l"),
                        (c4,"💬","Sentiment",result.get("sentiment",""),"t"),
                    ]:
                        with col:
                            st.markdown(f'<div class="card c{acc}"><div style="font-size:.88rem;font-weight:600;margin-bottom:.55rem;font-family:\'Fraunces\',serif">{icon} {hd}</div><div style="font-size:.78rem;color:#aaaabb;line-height:1.6;white-space:pre-wrap">{content or "None identified."}</div></div>', unsafe_allow_html=True)

                    cr1, cr2 = st.columns(2)
                    with cr1:
                        st.markdown('<div class="card cl"><div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.6rem">🎯 Recommendations</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:.8rem;color:#aaaabb;line-height:1.6;white-space:pre-wrap">{result.get("recommendations","")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cr2:
                        st.markdown('<div class="card csk"><div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.6rem">❓ Follow-up Questions</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:.8rem;color:#aaaabb;line-height:1.6;white-space:pre-wrap">{result.get("followups","")}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        elif run_meeting:
            st.warning("Please enter both a title and a transcript.")
        else:
            if not title.strip() and not transcript.strip():
                insight("Works great with Zoom/Teams transcripts, Google Meet captions, or rough notes. Paste and go.", "💡")

    with tab_hist:
        notes = list_meeting_notes()
        if notes:
            for n in notes:
                mid,tn,sn,ktn,ain,dln,decn,recn,riskn,sentn,spkn,fupn,catn,modn,tokn,latn,costn = n
                with st.expander(f"🎙️  {tn or f'Meeting #{mid}'}   ·   {catn[:10]}"):
                    st.markdown(f"**Summary:** {sn}")
                    cc1,cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**Action Items:**\n{ain}")
                        st.markdown(f"**Topics:**\n{ktn}")
                    with cc2:
                        st.markdown(f"**Deadlines:**\n{dln}")
                        st.markdown(f"**Sentiment:** {sentn}")
                    st.caption(f"Model: {modn} · {tokn:,} tokens · ${costn:.6f} · {latn:.0f}ms")
                    tf = list_tasks_for_meeting(mid)
                    if tf:
                        st.markdown("**Tasks:**")
                        for t in tf:
                            st.markdown(f"- {t[2]} · *{t[1] or 'Unassigned'}* · {t[3] or 'No deadline'} · `{t[4]}`")
                    if st.button("📥 Export", key=f"exp_m_{mid}"):
                        try:
                            md = export_note_markdown(DB_PATH,"meeting",mid)
                            st.download_button("⬇️ Download .md", md, file_name=f"meeting_{mid}.md", mime="text/markdown", key=f"dl_m_{mid}")
                        except Exception as e:
                            st.error(str(e))
        else:
            empty("🎙️","No meetings yet","Analyze a meeting to get a rich structured summary with auto-extracted tasks.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TASKS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Tasks":
    hdr("Stay on top of things","Task Manager","Tasks auto-extracted from meetings, or add your own. Track everything in one place.")

    with st.form("task_form", clear_on_submit=True):
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.65rem">➕ Add a Task</div>', unsafe_allow_html=True)
        tc1,tc2,tc3 = st.columns([3,2,1.5])
        with tc1: new_desc = st.text_input("", placeholder="What needs to get done?", key="tdesc")
        with tc2: new_asn  = st.text_input("", placeholder="Who owns it?", key="tasn")
        with tc3: new_dl   = st.text_input("", placeholder="YYYY-MM-DD", key="tdl")
        if st.form_submit_button("Add Task", use_container_width=True) and new_desc.strip():
            create_task(new_asn, new_desc, new_dl)
            st.success("Task added!")
            st.rerun()

    due_soon = get_due_soon(3)
    if due_soon:
        st.markdown('<div class="card cam">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:.88rem;font-weight:600;color:var(--amber);margin-bottom:.45rem">⏰ {len(due_soon)} task{"s" if len(due_soon)!=1 else ""} due in 3 days</div>', unsafe_allow_html=True)
        for t in due_soon[:3]:
            st.markdown(f'<div style="font-size:.8rem;color:var(--muted)">• {t[4]} · due {t[5]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    sf = st.selectbox("Filter",["All","Pending","Done","Cancelled"],index=0,label_visibility="collapsed")
    tasks = list_tasks(None if sf=="All" else sf.lower())

    if tasks:
        total_t = len(tasks)
        done_t  = sum(1 for t in tasks if t[6]=="done")
        pend_t  = sum(1 for t in tasks if t[6]=="pending")
        pct     = int(done_t/total_t*100) if total_t else 0

        k1,k2,k3 = st.columns(3)
        for col,lbl,val,clr in [(k1,"Total",total_t,"var(--text)"),(k2,"Pending",pend_t,"var(--amber)"),(k3,"Done",done_t,"var(--teal)")]:
            with col:
                st.markdown(f'<div class="kpi"><div class="kpi-label">{lbl}</div><div class="kpi-val" style="color:{clr}">{val}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""<div style="margin:.8rem 0 1.1rem">
          <div style="display:flex;justify-content:space-between;margin-bottom:.25rem">
            <span style="font-size:.72rem;color:var(--muted)">Completion</span>
            <span style="font-family:'DM Mono',monospace;font-size:.68rem;color:var(--teal)">{pct}%</span>
          </div>
          {pbar(pct,"var(--teal)")}
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        for t in tasks:
            tid,src_t,src_id,asn,desc,deadline,status,created = t
            dc = {"pending":"dp","done":"dd","cancelled":"dc"}.get(status,"dp")
            urg=""
            if deadline and status=="pending":
                try:
                    dl=datetime.datetime.strptime(deadline,"%Y-%m-%d").date()
                    d=(dl-datetime.date.today()).days
                    urg=f' · <span style="color:{"var(--rose)" if d<=2 else "var(--amber)"}">{d}d left</span>'
                except: pass
            tc_m, tc_b = st.columns([5,1])
            with tc_m:
                ts = 'style="text-decoration:line-through;color:var(--muted)"' if status=="done" else ""
                st.markdown(f"""<div class="tr-row">
                  <div class="td {dc}"></div>
                  <div style="flex:1;min-width:0">
                    <div {ts} style="font-size:.88rem;color:var(--text)">{desc}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:.56rem;color:var(--muted)">{asn or "Unassigned"} · {deadline or "No deadline"}{urg} · {src_t} #{src_id}</div>
                  </div>
                  <span class="tag {'tt' if status=='done' else 'tam' if status=='pending' else ''}">{status}</span>
                </div>""", unsafe_allow_html=True)
            with tc_b:
                if status=="pending":
                    if st.button("✓", key=f"done_{tid}", help="Mark done"):
                        update_task_status(tid,"done"); st.rerun()
                elif status=="done":
                    if st.button("↩", key=f"reopen_{tid}", help="Reopen"):
                        update_task_status(tid,"pending"); st.rerun()
    else:
        empty("✅","All clear!","No tasks here. Analyze a meeting to auto-extract tasks, or add one manually above.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: KNOWLEDGE HUB
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Knowledge":
    hdr("Your second brain","Knowledge Hub","Search across every research note and meeting summary in one unified place.")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    query_kb = st.text_input("", placeholder="🔎  Search everything — topics, names, decisions, concepts…", key="kb_q")
    st.markdown('</div>', unsafe_allow_html=True)

    if query_kb.strip():
        try:
            results = search_knowledge_hub(DB_PATH, query_kb.strip(), limit=25)
            if results:
                st.markdown(f'<div style="font-size:.78rem;color:var(--muted);margin-bottom:.85rem">Found <b style="color:var(--text)">{len(results)}</b> result{"s" if len(results)!=1 else ""} for <b style="color:var(--amd)">{query_kb}</b></div>', unsafe_allow_html=True)
                for r in results:
                    t_icon = "🔬" if r["type"]=="research" else "🎙️"
                    t_style = "a" if r["type"]=="research" else "sk"
                    cr2, ca2 = st.columns([5,1])
                    with cr2:
                        st.markdown(f"""<div class="ri">
                          <div class="ri-title">{t_icon} {r['title']}</div>
                          <div class="ri-meta">{tag_html(r['type'].upper(), t_style)} ID #{r['id']}</div>
                          <div class="ri-body">{r['preview']}</div>
                        </div>""", unsafe_allow_html=True)
                    with ca2:
                        if st.button("Export", key=f"kb_{r['type']}_{r['id']}"):
                            try:
                                md = export_note_markdown(DB_PATH, r["type"], r["id"])
                                st.download_button("⬇️ .md", md, file_name=f"{r['type']}_{r['id']}.md", mime="text/markdown", key=f"kbdl_{r['type']}_{r['id']}")
                            except Exception as e:
                                st.error(str(e))
            else:
                empty("🔍",f"No results for '{query_kb}'","Try different keywords, or check that you've run some research or meetings first.")
        except Exception as e:
            st.error(f"Search error: {e}")
    else:
        tr = len(search_research_notes(""))
        tm = len(list_meeting_notes())
        k1,k2,k3 = st.columns(3)
        for col,lbl,val,clr in [(k1,"Research Notes",tr,"var(--amd)"),(k2,"Meeting Notes",tm,"var(--sky)"),(k3,"Total Items",tr+tm,"var(--teal)")]:
            with col:
                st.markdown(f'<div class="kpi" style="border-top:2px solid {clr}"><div class="kpi-label">{lbl}</div><div class="kpi-val" style="color:{clr}">{val}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        insight("Your knowledge base grows automatically every time you run research or analyze a meeting. Search it here anytime.", "🧠")
        if tr>0:
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin:.9rem 0 .65rem">Recent items</div>', unsafe_allow_html=True)
            for n in search_research_notes("")[:3]:
                st.markdown(f"""<div class="ri">
                  <div class="ri-title">🔬 {n['query']}</div>
                  <div class="ri-meta">{n['created_at'][:10]} · research</div>
                  <div class="ri-body">{n['summary'][:100]}…</div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Analytics":
    hdr("Under the microscope","Analytics","Historical trends, feature efficiency, and cost patterns — your AI copilot in full detail.")

    totals   = get_overall_totals()
    summary  = get_feature_summary()
    time_data = get_usage_over_time()
    insights  = generate_performance_insights()

    k1,k2,k3,k4 = st.columns(4)
    for col,lbl,val,sub,clr in [(k1,"AI Runs",str(totals["total_runs"]),"all time","var(--amd)"),(k2,"Tokens",f"{totals['total_tokens']:,}","consumed","var(--sky)"),(k3,"Avg Latency",f"{totals['avg_latency_ms']:.0f}ms","per call","var(--teal)"),(k4,"Total Spend",f"${totals['total_cost']:.5f}","USD","var(--amber)")]:
        with col:
            st.markdown(f'<div class="kpi" style="border-top:2px solid {clr}"><div class="kpi-label">{lbl}</div><div class="kpi-val" style="color:{clr}">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab_f, tab_t, tab_m, tab_e = st.tabs(["🏷️  Features","📈  Trends","🤖  Models","💰  Efficiency"])

    with tab_f:
        if summary:
            keys   = list(summary.keys())
            labels = [k.replace("_"," ").title() for k in keys]
            runs   = [summary[k]["total_runs"] for k in keys]
            tokens = [summary[k]["total_tokens"] for k in keys]
            lat    = [summary[k]["avg_latency_ms"] for k in keys]
            cost   = [summary[k]["total_cost"] for k in keys]
            tpr    = [tokens[i]/max(runs[i],1) for i in range(len(keys))]
            clrs   = ["#e8450a","#f5841f","#00c9a7","#38bdf8","#a78bfa","#fb7185"]

            ca2, cb2 = st.columns(2)
            with ca2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.65rem">Tokens/Run vs Latency</div>', unsafe_allow_html=True)
                fig = go.Figure()
                mr = max(runs) if runs else 1
                for i,lbl in enumerate(labels):
                    fig.add_trace(go.Scatter(x=[tpr[i]],y=[lat[i]],mode="markers",name=lbl,
                        marker=dict(size=13+runs[i]/mr*18,color=clrs[i%len(clrs)],opacity=.85,line=dict(color="#17171a",width=1)),
                        hovertemplate=f"<b>{lbl}</b><br>Tokens/run: %{{x:.0f}}<br>Latency: %{{y:.0f}}ms<br>Runs: {runs[i]}<extra></extra>"))
                fig.update_layout(**{**CHART, "xaxis": {**CHART["xaxis"], "title": "Tokens per run"}, "yaxis": {**CHART["yaxis"], "title": "Avg latency (ms)"}}, height=240, showlegend=True)
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            with cb2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.65rem">Cost Share</div>', unsafe_allow_html=True)
                sp = sorted(zip(labels,cost),key=lambda x:x[1],reverse=True)
                fig2 = go.Figure(go.Pie(labels=[p[0] for p in sp],values=[p[1] for p in sp],hole=.56,
                    marker=dict(colors=clrs,line=dict(color="#17171a",width=2)),textfont=dict(family="DM Mono",size=8)))
                fig2.update_layout(**CHART,height=240,showlegend=True)
                st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.75rem">Feature Breakdown</div>', unsafe_allow_html=True)
            hcs = st.columns([3,1,1,1,1])
            for col2,hd in zip(hcs,["Feature","Runs","Tokens","Avg Latency","Cost"]):
                col2.markdown(f'<div style="font-family:\'DM Mono\',monospace;font-size:.56rem;color:var(--dim);letter-spacing:.1em;text-transform:uppercase">{hd}</div>', unsafe_allow_html=True)
            for feat, data in summary.items():
                rcs = st.columns([3,1,1,1,1])
                rcs[0].markdown(f'<span style="font-size:.85rem;color:var(--text)">{feat.replace("_"," ").title()}</span>', unsafe_allow_html=True)
                rcs[1].markdown(f'<span style="font-family:\'DM Mono\',monospace;font-size:.78rem;color:var(--amd)">{data["total_runs"]}</span>', unsafe_allow_html=True)
                rcs[2].markdown(f'<span style="font-family:\'DM Mono\',monospace;font-size:.78rem;color:var(--sky)">{data["total_tokens"]:,}</span>', unsafe_allow_html=True)
                rcs[3].markdown(f'<span style="font-family:\'DM Mono\',monospace;font-size:.78rem;color:var(--teal)">{data["avg_latency_ms"]:.0f}ms</span>', unsafe_allow_html=True)
                rcs[4].markdown(f'<span style="font-family:\'DM Mono\',monospace;font-size:.78rem;color:var(--amber)">${data["total_cost"]:.5f}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            empty("📊","No data yet","Use SmartEdge features to start seeing analytics.")

    with tab_t:
        if time_data:
            dates  = [d["date"] for d in time_data]
            ttok   = [d["total_tokens"] for d in time_data]
            tcost  = [d["total_cost"] for d in time_data]
            cumcost = []
            acc = 0
            for c in tcost:
                acc += c
                cumcost.append(round(acc,8))
            ct1, ct2 = st.columns(2)
            with ct1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.65rem">Token Usage Over Time</div>', unsafe_allow_html=True)
                f3 = go.Figure()
                f3.add_trace(go.Scatter(x=dates,y=ttok,mode="lines+markers",line=dict(color="#e8450a",width=2),
                    marker=dict(size=4,color="#f5841f"),fill="tozeroy",fillcolor="rgba(232,69,10,.07)",
                    hovertemplate="%{x}<br><b>%{y:,} tokens</b><extra></extra>"))
                f3.update_layout(**CHART,height=220)
                st.plotly_chart(f3,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)
            with ct2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.65rem">Cumulative Cost (USD)</div>', unsafe_allow_html=True)
                f4 = go.Figure()
                f4.add_trace(go.Scatter(x=dates,y=cumcost,mode="lines",line=dict(color="#00c9a7",width=2.5),
                    fill="tozeroy",fillcolor="rgba(0,201,167,.07)",
                    hovertemplate="%{x}<br><b>$%{y:.5f}</b><extra></extra>"))
                f4.update_layout(**CHART,height=220)
                st.plotly_chart(f4,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            empty("📈","No time data yet","Use features over multiple days to see trends.")

    with tab_m:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.8rem">Groq Model Speed Reference</div>', unsafe_allow_html=True)
        models_ref = [("llama-3.1-8b-instant",1200,0.000027,"Research, summaries, fast tasks"),("llama-3.3-70b-versatile",300,0.000590,"Complex reasoning, analysis"),("mixtral-8x7b-32768",500,0.000270,"Balanced speed + quality"),("gemma2-9b-it",900,0.000090,"Code, technical writing")]
        max_spd = 1200
        for mid2,spd,c1k,uc in models_ref:
            st.markdown(f"""<div style="padding:.65rem 0;border-bottom:1px solid var(--bd)">
              <div style="display:flex;justify-content:space-between;margin-bottom:.28rem">
                <span style="font-family:'DM Mono',monospace;font-size:.76rem;color:var(--text)">{mid2}</span>
                <span style="font-size:.7rem;color:var(--muted)">{spd:,} t/s</span>
              </div>
              <div class="sb-wrap"><div class="sb-fill" style="width:{int(spd/max_spd*100)}%"></div></div>
              <div style="display:flex;justify-content:space-between;margin-top:.28rem">
                <span style="font-size:.7rem;color:var(--muted)">{uc}</span>
                <span style="font-family:'DM Mono',monospace;font-size:.65rem;color:var(--amber)">${c1k:.6f}/1K tok</span>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_e:
        if summary:
            eff = insights.get("feature_efficiency",{})
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.9rem;font-weight:600;margin-bottom:.85rem">Cost Efficiency by Feature</div>', unsafe_allow_html=True)
            for feat, data in eff.items():
                cr2 = data["cost_per_1k_tokens"]
                mr2 = max(d["cost_per_1k_tokens"] for d in eff.values()) or 1
                bp  = int(cr2/mr2*100)
                st.markdown(f"""<div style="margin-bottom:.9rem">
                  <div style="display:flex;justify-content:space-between;margin-bottom:.25rem">
                    <span style="font-size:.83rem;color:var(--text)">{feat.replace("_"," ").title()}</span>
                    <div>
                      <span style="font-family:'DM Mono',monospace;font-size:.68rem;color:var(--amber)">${cr2:.6f}/1K tok</span>
                      <span style="font-family:'DM Mono',monospace;font-size:.65rem;color:var(--muted);margin-left:.5rem">avg: ${data['avg_cost_per_run']:.6f}</span>
                    </div>
                  </div>
                  {pbar(bp,"var(--amd)")}
                </div>""", unsafe_allow_html=True)
            me = insights.get("most_expensive_feature","")
            sl = insights.get("slowest_feature","")
            if me: insight(f"Most expensive: <b>{me.replace('_',' ').title()}</b>. Slowest: <b>{sl.replace('_',' ').title()}</b>. Consider prompt optimization.", "💡")
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SLINGSHOT LAB
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Slingshot Lab":
    hdr("AMD Slingshot 2025","Performance Lab","Groq's LPU speed advantage — tokenization efficiency, latency benchmarks, and model accuracy under the spotlight.")

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(232,69,10,.18) 0%,rgba(245,132,31,.1) 50%,rgba(56,189,248,.07) 100%);
                border:1px solid rgba(232,69,10,.28);border-radius:16px;padding:1.8rem;margin-bottom:1.4rem;
                display:flex;align-items:center;gap:1.3rem">
      <div style="font-size:3rem;flex-shrink:0">⚡</div>
      <div>
        <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:700;color:var(--text);line-height:1.1">AMD Slingshot Hackathon</div>
        <div style="font-size:.88rem;color:var(--muted);margin-top:.4rem;line-height:1.55">
          SmartEdge Copilot showcases Groq's LPU architecture — delivering up to
          <b style="color:var(--amd)">18× faster</b> inference than GPU-based providers.
          Full observability, token efficiency metrics, and model accuracy tracking built in.
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    tab_b, tab_tok, tab_live, tab_acc = st.tabs(["🏎️  Speed Benchmarks","🔤  Token Efficiency","📡  Live Performance","🎯  Model Accuracy"])

    with tab_b:
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.85rem">Tokens per Second — Groq vs Traditional Providers</div>', unsafe_allow_html=True)
        providers = ["Groq (LPU)","OpenAI GPT-4o","Anthropic Claude 3.5","Google Gemini 1.5","Azure OpenAI"]
        speeds    = [1200,68,82,95,60]
        bclrs     = ["#e8450a","#404055","#404055","#404055","#404055"]

        cb1, cb2 = st.columns([3,2])
        with cb1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            fb = go.Figure(go.Bar(x=speeds,y=providers,orientation="h",marker_color=bclrs,marker_line_width=0,
                text=[f"{s:,} t/s" for s in speeds],textposition="outside",textfont=dict(family="DM Mono",size=9,color="#e8e8f0"),
                hovertemplate="<b>%{y}</b><br>%{x:,} tokens/second<extra></extra>"))
            fb.update_layout(**{**CHART, "xaxis": {**CHART["xaxis"], "title": "Tokens per Second", "range": [0, 1450]}}, height=255, showlegend=False)
            st.plotly_chart(fb,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with cb2:
            st.markdown('<div class="card ca">', unsafe_allow_html=True)
            for prov,spd in zip(providers,speeds):
                ratio = spd/speeds[1]
                rs = f"{ratio:.1f}×" if ratio>=1 else f"{1/ratio:.1f}× slower"
                clr = "var(--amd)" if spd==max(speeds) else "var(--muted)"
                st.markdown(f"""<div style="border-bottom:1px solid var(--bd);padding:.5rem 0;display:flex;justify-content:space-between">
                  <span style="font-size:.8rem;color:var(--text)">{prov}</span>
                  <div style="text-align:right">
                    <span style="font-family:'DM Mono',monospace;font-size:.76rem;color:{clr}">{spd:,}</span>
                    <span style="font-size:.62rem;color:var(--muted);margin-left:.35rem">{rs}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin:1.2rem 0 .75rem">Time to First Token (500 tok prompt)</div>', unsafe_allow_html=True)
        ttft_p = ["Groq (LPU)","OpenAI GPT-4o","Anthropic Claude","Google Gemini","Cohere"]
        ttft_m = [42,480,420,380,520]
        ttft_c = ["#e8450a","#404055","#404055","#404055","#404055"]
        ct1, ct2 = st.columns(2)
        with ct1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            ft = go.Figure(go.Bar(x=ttft_p,y=ttft_m,marker_color=ttft_c,marker_line_width=0,
                text=[f"{t}ms" for t in ttft_m],textposition="outside",textfont=dict(family="DM Mono",size=9,color="#e8e8f0"),
                hovertemplate="<b>%{x}</b><br>TTFT: %{y}ms<extra></extra>"))
            ft.update_layout(**CHART,height=225,showlegend=False,yaxis_title="ms")
            st.plotly_chart(ft,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)
        with ct2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.88rem;font-weight:600;margin-bottom:.75rem">Why Groq is Different</div>', unsafe_allow_html=True)
            for ico,t2,d2 in [("🔧","LPU Architecture","Purpose-built Language Processing Unit — not a repurposed GPU"),("⚡","Deterministic Exec","No batching delays; each token processed in a consistent, predictable cycle"),("💾","On-chip Memory","Weights in SRAM, not HBM — eliminates the memory bandwidth bottleneck"),("🔄","Compiler-first","GroqFlow maps weights to hardware at compile time for zero runtime overhead")]:
                st.markdown(f"""<div style="padding:.45rem 0;border-bottom:1px solid var(--bd)">
                  <div style="font-size:.8rem;font-weight:600;color:var(--text);margin-bottom:.12rem">{ico} {t2}</div>
                  <div style="font-size:.73rem;color:var(--muted);line-height:1.5">{d2}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_tok:
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.75rem">Token Efficiency Analyzer</div>', unsafe_allow_html=True)
        insight("Fewer tokens = faster responses + lower cost. SmartEdge's Prompt Optimizer systematically reduces token usage while preserving quality.", "🔤")
        cl2, cr2 = st.columns([3,2])
        with cl2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            sample = st.text_area("", height=150, placeholder="Paste any prompt to analyze its efficiency…\n\nTry: 'Please kindly provide me with a comprehensive and detailed explanation of how neural networks work, including all the important concepts and ideas that are relevant to understanding the topic fully.'", key="tok_input")
            if st.button("🔤 Analyze & Optimize", key="btn_tok") and sample.strip():
                with st.spinner("Analyzing tokens and optimizing…"):
                    opt2 = generate_optimized_prompt(sample.strip())
                words_raw = sample.split()
                words_opt = opt2.split()
                tok_raw = int(len(words_raw)*1.33)
                tok_opt = int(len(words_opt)*1.33)
                sav_pct = (1 - tok_opt/max(tok_raw,1))*100
                ka,kb,kc = st.columns(3)
                for col3,lbl3,val3,clr3 in [(ka,"Raw",tok_raw,"var(--rose)"),(kb,"Optimized",tok_opt,"var(--teal)"),(kc,"Saved",f"{sav_pct:.0f}%","var(--amd)")]:
                    with col3:
                        st.markdown(f'<div class="kpi" style="border-top:2px solid {clr3}"><div class="kpi-label">{lbl3}</div><div class="kpi-val" style="color:{clr3}">{val3}</div></div>', unsafe_allow_html=True)
                st.markdown(f"""<div style="margin:.75rem 0">
                  <div style="font-size:.7rem;color:var(--muted);margin-bottom:.22rem">Raw</div>
                  {pbar(100,"var(--rose)")}
                  <div style="font-size:.7rem;color:var(--muted);margin:.22rem 0">Optimized</div>
                  {pbar(max(0,100-sav_pct),"var(--teal)")}
                </div>""", unsafe_allow_html=True)
                st.text_area("Optimized:", value=opt2, height=100, key="tok_opt")
            st.markdown('</div>', unsafe_allow_html=True)

        with cr2:
            st.markdown('<div class="card ct">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.88rem;font-weight:600;margin-bottom:.75rem">💡 Efficiency Principles</div>', unsafe_allow_html=True)
            for tip, desc_t in [("Remove filler words","Delete 'please', 'kindly', 'could you' — they add tokens without adding meaning."),("Be direct","Replace 'Can you provide an explanation of X' with 'Explain X'."),("Set output length","Add 'in 3 bullets' or 'max 150 words' — constrains tokens predictably."),("Avoid repetition","Don't restate context already in the system prompt."),("Use structure","Explicit output format instructions reduce back-and-forth iterations.")]:
                st.markdown(f"""<div style="padding:.45rem 0;border-bottom:1px solid var(--bd)">
                  <div style="font-size:.8rem;font-weight:600;color:var(--text);margin-bottom:.12rem">✓ {tip}</div>
                  <div style="font-size:.73rem;color:var(--muted);line-height:1.5">{desc_t}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_live:
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.75rem">Live Session Performance</div>', unsafe_allow_html=True)
        totals2  = get_overall_totals()
        time_d2  = get_usage_over_time()
        if totals2["total_runs"]>0:
            avg2 = totals2["avg_latency_ms"]
            ss = ("🟢 Excellent","var(--teal)") if avg2<400 else (("🟡 Good","var(--amber)") if avg2<1000 else ("🔴 Slow","var(--rose)"))
            tps_est = totals2["total_tokens"]/max(totals2["total_runs"],1) * (1000/max(avg2,1))
            c1p,c2p,c3p = st.columns(3)
            with c1p: st.markdown(f'<div class="card" style="border-top:2px solid {ss[1]};text-align:center"><div class="kpi-label">Speed Status</div><div style="font-family:\'Fraunces\',serif;font-size:1.5rem;font-weight:700;color:{ss[1]}">{ss[0]}</div><div class="kpi-sub">{avg2:.0f}ms avg</div></div>', unsafe_allow_html=True)
            with c2p: st.markdown(f'<div class="card" style="border-top:2px solid var(--amd);text-align:center"><div class="kpi-label">Est. Throughput</div><div style="font-family:\'Fraunces\',serif;font-size:1.5rem;font-weight:700;color:var(--amd)">{tps_est:.0f}</div><div class="kpi-sub">tokens/sec</div></div>', unsafe_allow_html=True)
            c1k = (totals2["total_cost"]/max(totals2["total_tokens"],1))*1000
            with c3p: st.markdown(f'<div class="card" style="border-top:2px solid var(--amber);text-align:center"><div class="kpi-label">Cost/1K Tokens</div><div style="font-family:\'Fraunces\',serif;font-size:1.5rem;font-weight:700;color:var(--amber)">${c1k:.5f}</div><div class="kpi-sub">USD</div></div>', unsafe_allow_html=True)
            if time_d2:
                st.markdown('<div class="card" style="margin-top:.9rem">', unsafe_allow_html=True)
                st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.88rem;font-weight:600;margin-bottom:.65rem">Session Timeline</div>', unsafe_allow_html=True)
                fl = go.Figure()
                fl.add_trace(go.Scatter(x=[d["date"] for d in time_d2],y=[d["total_tokens"] for d in time_d2],
                    mode="lines+markers",line=dict(color="#e8450a",width=2.5),marker=dict(color="#f5841f",size=5),
                    fill="tozeroy",fillcolor="rgba(232,69,10,.09)",hovertemplate="%{x}<br><b>%{y:,} tokens</b><extra></extra>"))
                fl.update_layout(**CHART,height=195)
                st.plotly_chart(fl,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            empty("📡","No live data yet","Run some AI features to see real-time performance here.")

    with tab_acc:
        st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.95rem;font-weight:600;margin-bottom:.75rem">Model Quality vs Speed Trade-off</div>', unsafe_allow_html=True)
        insight("SmartEdge uses Groq's llama-3.1-8b-instant by default — sub-500ms responses with strong accuracy for research and summarization. The quality judge in Prompt Lab scores outputs 1–10.", "🎯")
        ca3, cb3 = st.columns(2)
        with ca3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            mn  = ["llama-3.1-8b-instant","mixtral-8x7b","llama-3.3-70b","gemma2-9b"]
            qsc = [7.8, 8.2, 9.1, 7.5]
            ssc = [9.5, 7.0, 4.5, 8.0]
            acc_c = ["#e8450a","#f5841f","#00c9a7","#38bdf8"]
            fa = go.Figure()
            for i,m2 in enumerate(mn):
                fa.add_trace(go.Scatter(x=[ssc[i]],y=[qsc[i]],mode="markers+text",name=m2,
                    text=[m2.split("-")[0].title()],textposition="top center",textfont=dict(size=8,color="#e8e8f0"),
                    marker=dict(size=18,color=acc_c[i],opacity=.85,line=dict(color="#17171a",width=1)),
                    hovertemplate=f"<b>{m2}</b><br>Quality: {qsc[i]}/10<br>Speed: {ssc[i]}/10<extra></extra>"))
            fa.update_layout(**{**CHART, "xaxis": {**CHART["xaxis"], "title": "Speed (10=fastest)", "range": [3, 11]}, "yaxis": {**CHART["yaxis"], "title": "Quality (10=best)", "range": [6, 10]}}, height=255, showlegend=False)
            st.plotly_chart(fa,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with cb3:
            st.markdown('<div class="card cl">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Fraunces\',serif;font-size:.88rem;font-weight:600;margin-bottom:.8rem">Recommended by Use Case</div>', unsafe_allow_html=True)
            for use, mr, rat, clr in [("Research queries","llama-3.1-8b-instant","⚡ Fast + accurate","t"),("Meeting analysis","mixtral-8x7b-32768","📋 Rich structure","am"),("Prompt optimization","llama-3.1-8b-instant","💰 Cost efficient","a"),("Complex reasoning","llama-3.3-70b","🎯 Highest quality","l")]:
                st.markdown(f"""<div style="padding:.6rem 0;border-bottom:1px solid var(--bd)">
                  <div style="font-size:.8rem;font-weight:600;color:var(--text)">{use}</div>
                  <div style="margin:.18rem 0">{tag_html(mr, clr)}</div>
                  <div style="font-size:.7rem;color:var(--muted)">{rat}</div>
                </div>""", unsafe_allow_html=True)
            eff_data = generate_performance_insights().get("feature_efficiency",{})
            if eff_data:
                avg_c = sum(d["cost_per_1k_tokens"] for d in eff_data.values())/max(len(eff_data),1)
                insight(f"Your actual avg efficiency: <b>${avg_c:.6f}</b>/1K tokens.", "💰")
            st.markdown('</div>', unsafe_allow_html=True)
