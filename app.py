from __future__ import annotations

import base64
import json
import html
from pathlib import Path

import streamlit.components.v1 as components
import streamlit as st
from recommender import load_quiz_questions, recommend


st.set_page_config(
    page_title="寻找此刻与你精神同频的舞蹈作品",
    page_icon="💃",
    layout="centered",
)


def image_file_to_data_uri(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


INTRO_BACKGROUND_URI = image_file_to_data_uri(
    "/Users/cn/Downloads/Gemini_Generated_Image_vyzehhvyzehhvyze.png"
)
QUIZ_BACKGROUND_URI = image_file_to_data_uri(
    "/Users/cn/Downloads/Gemini_Generated_Image_sc8a45sc8a45sc8a (1).png"
)

st.markdown(
    """
    <style>
    :root {
        --bg-warm: #d9eef7;
        --bg-warm-deep: #bddff0;
        --card-cream: rgba(250, 254, 255, 0.72);
        --line-soft: rgba(116, 143, 163, 0.14);
        --text-main: #5b7388;
        --text-blue: #6d87a1;
        --text-soft: #7d96aa;
        --result-orange: #e7b188;
        --result-orange-deep: #d89f73;
        --chip-cream: rgba(255, 255, 255, 0.82);
        --button-blue: #7f9cb7;
    }
    html,
    body,
    #root {
        min-height: 100%;
        height: auto !important;
        margin: 0;
        background: var(--bg-warm);
        overflow-x: hidden;
    }
    html {
        scroll-behavior: smooth;
    }
    body {
        overflow-y: auto !important;
    }
    .stApp {
        position: relative;
        min-height: 100vh !important;
        overflow: visible !important;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.04)),
            url("__QUIZ_BG__");
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        color: var(--text-main);
        font-family: "Avenir Next", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", sans-serif;
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: -10% -6%;
        pointer-events: none;
        background:
            linear-gradient(115deg, transparent 28%, rgba(255, 255, 255, 0.18) 48%, transparent 68%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.16), transparent 42%, rgba(255, 255, 255, 0.08) 74%, transparent);
        filter: blur(30px);
        opacity: 0.42;
        animation: hazeDrift 24s ease-in-out infinite alternate;
        z-index: 0;
    }
    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background: radial-gradient(circle at center, rgba(255, 255, 255, 0.18), transparent 56%);
        opacity: 0.7;
        z-index: 0;
    }
    .block-container {
        max-width: 680px;
        padding-top: 1.25rem;
        padding-bottom: 3rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
        position: relative;
        z-index: 1;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        min-height: 100vh !important;
        height: auto !important;
        overflow: visible !important;
    }
    [data-testid="stToolbar"],
    [data-testid="stHeader"] {
        background: transparent;
    }
    header,
    footer,
    #MainMenu,
    [data-testid="stToolbar"] {
        display: none !important;
    }
    .stage-hero {
        position: relative;
        max-width: 35rem;
        min-height: calc(100svh - 3rem);
        margin: 0 auto 1rem auto;
        padding: 1rem 1rem 1.4rem 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        overflow: hidden;
        border-radius: 34px;
        background:
            radial-gradient(circle at center, rgba(255, 255, 255, 0.12), transparent 38%),
            url("__INTRO_BG__");
        background-size: cover;
        background-position: center;
        box-shadow:
            inset 0 0 0 1px rgba(255, 255, 255, 0.24),
            0 20px 44px rgba(110, 145, 170, 0.16);
    }
    .stage-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: radial-gradient(circle at center, rgba(255, 255, 255, 0.12), transparent 48%);
        opacity: 0.9;
    }
    .stage-hero-inner {
        position: relative;
        z-index: 1;
        max-width: 20rem;
        padding: 0 0.2rem;
    }
    .stage-eyebrow {
        color: rgba(109, 135, 156, 0.78);
        font-size: 0.74rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .stage-title {
        color: var(--text-blue);
        font-size: clamp(1.92rem, 7vw, 2.35rem);
        line-height: 1.14;
        font-weight: 640;
        margin: 0;
        text-wrap: balance;
        text-shadow: 0 0 26px rgba(255, 255, 255, 0.36);
    }
    .stage-title,
    .stage-title * {
        color: var(--text-blue) !important;
    }
    .stage-copy {
        margin: 1rem auto 0 auto;
        color: #678195;
        font-size: 1rem;
        line-height: 1.88;
        text-align: center;
        max-width: 20rem;
        text-shadow: 0 0 18px rgba(255, 255, 255, 0.28);
    }
    .stage-copy p {
        margin: 0 0 0.72rem 0;
    }
    .stage-cta-wrap {
        margin-top: 1.45rem;
        display: flex;
        justify-content: center;
    }
    .stage-cta {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.45rem;
        min-width: 11.25rem;
        padding: 0.92rem 1.4rem;
        border-radius: 999px;
        text-decoration: none;
        color: #fffaf5;
        background: linear-gradient(180deg, rgba(136, 164, 188, 0.98) 0%, rgba(122, 149, 172, 0.98) 100%);
        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.32),
            0 0 18px rgba(255, 255, 255, 0.48),
            0 14px 28px rgba(109, 131, 151, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.34);
        font-size: 0.99rem;
        font-weight: 680;
        animation: breathePulse 2.8s ease-in-out infinite;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stage-cta:hover {
        color: #fffaf5;
        transform: translateY(-1px) scale(1.035);
        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.4),
            0 0 26px rgba(255, 255, 255, 0.62),
            0 18px 32px rgba(109, 131, 151, 0.24);
    }
    .stage-cta:focus,
    .stage-cta:active {
        color: #fffaf5;
    }
    @keyframes hazeDrift {
        0% {
            transform: translate3d(-1.2%, -0.6%, 0) scale(1);
        }
        100% {
            transform: translate3d(1.1%, 0.8%, 0) scale(1.03);
        }
    }
    @keyframes breathePulse {
        0%,
        100% {
            transform: translateY(0) scale(1);
            box-shadow: 0 14px 26px rgba(109, 131, 151, 0.18);
        }
        50% {
            transform: translateY(-1px) scale(1.025);
            box-shadow: 0 18px 32px rgba(109, 131, 151, 0.24);
        }
    }
    @keyframes stageRise {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .result-card {
        padding: 0.95rem 1rem;
        border: 1px solid rgba(181, 135, 93, 0.16);
        border-radius: 18px;
        background: rgba(255, 250, 244, 0.94);
        margin-bottom: 1rem;
        box-shadow: 0 10px 24px rgba(177, 126, 84, 0.07);
    }
    .result-panel {
        padding: 1.15rem 1.15rem 1.25rem 1.15rem;
        border-radius: 24px;
        margin-top: 1rem;
        background: linear-gradient(180deg, rgba(231, 177, 136, 0.92) 0%, rgba(219, 159, 114, 0.94) 100%);
        border: 1px solid rgba(181, 126, 84, 0.18);
        box-shadow: 0 14px 30px rgba(174, 121, 77, 0.10);
    }
    .result-card-primary {
        background: rgba(255, 248, 239, 0.94);
        border-color: rgba(176, 125, 86, 0.22);
    }
    .result-card-secondary {
        background: rgba(255, 246, 235, 0.9);
    }
    .result-panel-title {
        color: #fff7ed;
        font-size: 1.24rem;
        font-weight: 640;
        margin: 0 0 0.85rem 0;
    }
    .result-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
        margin-top: 0.7rem;
    }
    .result-card-title {
        color: var(--text-blue);
        font-size: 1.03rem;
        font-weight: 680;
        margin: 0;
    }
    .result-meta {
        color: var(--text-soft);
        font-size: 0.92rem;
        line-height: 1.6;
        margin-top: 0.25rem;
    }
    .work-still-wrap {
        margin: 0.75rem 0 0.9rem 0;
        border-radius: 16px;
        overflow: hidden;
        background: rgba(250, 242, 231, 0.88);
        border: 1px solid rgba(181, 135, 93, 0.14);
    }
    .work-still-wrap a {
        display: block;
        line-height: 0;
    }
    .work-still {
        display: block;
        width: 100%;
        max-height: 340px;
        object-fit: cover;
    }
    .result-inline-label {
        color: #695a4d;
        font-weight: 700;
    }
    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.25rem;
    }
    .chip {
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        background: var(--chip-cream);
        border: 1px solid rgba(136, 141, 145, 0.16);
        font-size: 0.86rem;
        color: #60686f;
    }
    .small-note {
        color: var(--text-soft);
        font-size: 0.93rem;
        line-height: 1.55;
    }
    .intro-copy {
        color: #6d859b;
        font-size: 0.97rem;
        line-height: 1.8;
        margin-top: 0.8rem;
        max-width: 42rem;
    }
    .section-title {
        color: var(--text-blue);
        font-size: 1.18rem;
        font-weight: 640;
        margin: 0.2rem 0 0.85rem 0;
    }
    .question-anchor {
        scroll-margin-top: 6rem;
    }
    .question-stage-shell {
        margin: 1rem 0 0.7rem 0;
        padding: 0.82rem 0.95rem 0.76rem 0.95rem;
        border: 1px solid rgba(122, 149, 169, 0.14);
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.42);
        box-shadow: 0 16px 28px rgba(122, 149, 169, 0.08);
        animation: stageRise 0.42s ease-out both;
    }
    .question-stage-kicker {
        color: rgba(104, 130, 152, 0.64);
        font-size: 0.76rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0;
    }
    .question-heading {
        display: flex;
        align-items: flex-start;
        gap: 0.62rem;
        margin: 0.55rem 0 0.3rem 0;
    }
    .question-number {
        flex: 0 0 auto;
        color: #9b785a;
        font-family: "Bradley Hand", "Segoe Print", "Noteworthy", "Comic Sans MS", cursive;
        font-size: 1.72rem;
        line-height: 1;
        font-weight: 700;
        transform: rotate(-4deg);
        margin-top: 0.02rem;
    }
    .question-heading-text {
        color: var(--text-blue);
        font-size: 1.12rem;
        font-weight: 650;
        line-height: 1.55;
        margin: 0;
    }
    .question-stage-title {
        color: var(--text-blue);
        font-size: 1.05rem;
        font-weight: 640;
        line-height: 1.5;
    }
    .question-stage-note {
        color: var(--text-soft);
        font-size: 0.92rem;
        line-height: 1.6;
        margin-top: 0.18rem;
    }
    .mbti-dimension-label {
        color: var(--text-main);
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0.1rem 0 0.35rem 0;
    }
    .result-copy {
        color: #695a4d;
        line-height: 1.75;
    }
    h2, h3, h4 {
        color: var(--text-blue) !important;
        letter-spacing: 0;
    }
    p, li, label, div {
        letter-spacing: 0;
    }
    div[data-testid="stWidgetLabel"] p {
        color: var(--text-blue);
        font-size: 1.12rem;
        font-weight: 640;
        line-height: 1.55;
    }
    div[data-testid="stRadio"] label p,
    div[data-testid="stCheckbox"] label p {
        color: var(--text-main);
        font-size: 0.96rem;
        font-weight: 500;
    }
    div[data-testid="stCaptionContainer"] p {
        color: var(--text-soft);
        font-size: 0.94rem;
        line-height: 1.65;
    }
    div[data-testid="stRadio"] {
        margin-bottom: 1.2rem;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        border-radius: 16px;
        border: 1px solid rgba(122, 149, 169, 0.12);
        background: rgba(255, 255, 255, 0.76);
        transition:
            transform 0.18s ease,
            background-color 0.18s ease,
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        transform: translateY(-1px);
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        transform: scale(0.985);
        background: rgba(229, 243, 252, 0.98);
        border-color: rgba(124, 147, 167, 0.42);
        box-shadow: 0 9px 18px rgba(124, 147, 167, 0.12);
    }
    div[data-testid="stCheckbox"] {
        margin: 0.25rem 0 0.8rem 0;
    }
    div[data-testid="stButton"] button {
        background: linear-gradient(180deg, #93afc8 0%, var(--button-blue) 100%);
        color: #fffaf5;
        border: none;
        border-radius: 999px;
        min-height: 3rem;
        font-size: 0.99rem;
        font-weight: 680;
        box-shadow: 0 0 18px rgba(255, 255, 255, 0.34), 0 10px 18px rgba(109, 131, 151, 0.14);
        animation: breathePulse 2.8s ease-in-out infinite;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(180deg, #88a6c0 0%, #6f8da8 100%);
    }
    div[data-testid="stColumn"] {
        padding: 0 0.35rem;
    }
    @media (max-width: 900px) {
        .result-grid {
            grid-template-columns: 1fr;
        }
        .block-container {
            padding-top: 0.95rem;
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }
        .stage-hero {
            min-height: calc(100svh - 2.2rem);
            padding: 0.8rem 0.72rem 1.1rem 0.72rem;
        }
        .stage-title {
            font-size: 1.88rem;
        }
        .stage-copy {
            font-size: 0.94rem;
            line-height: 1.76;
        }
        .stage-hero-inner {
            max-width: 18rem;
        }
        .stage-cta {
            min-width: 10.9rem;
            padding: 0.86rem 1.22rem;
        }
    }
    </style>
    """.replace("__INTRO_BG__", INTRO_BACKGROUND_URI).replace("__QUIZ_BG__", QUIZ_BACKGROUND_URI),
    unsafe_allow_html=True,
)


def render_tag_chips(tags: list[str]) -> None:
    if not tags:
        return
    chips = "".join(f"<span class='chip'>{tag}</span>" for tag in tags)
    st.markdown(f"<div class='chip-row'>{chips}</div>", unsafe_allow_html=True)


def build_tag_chips_html(tags: list[str]) -> str:
    if not tags:
        return ""
    chips = "".join(
        f"<span class='chip'>{html.escape(tag)}</span>" for tag in tags
    )
    return f"<div class='chip-row'>{chips}</div>"


def build_work_image_html(image_url: str, title: str, source_url: str = "") -> str:
    if not image_url:
        return ""
    safe_image_url = html.escape(image_url, quote=True)
    safe_title = html.escape(title)
    safe_source_url = html.escape(source_url, quote=True)
    img = f'<img class="work-still" src="{safe_image_url}" alt="{safe_title} 剧照" loading="lazy" />'
    if source_url:
        return (
            '<div class="work-still-wrap">'
            f'<a href="{safe_source_url}" target="_blank" rel="noopener noreferrer">{img}</a>'
            "</div>"
        )
    return f'<div class="work-still-wrap">{img}</div>'


def render_recommendation_deck(results: list[dict], mbti_note: str = "") -> None:
    cards: list[dict[str, str]] = []
    for index, result in enumerate(results[:3]):
        work = result["work"]
        relation_summary = result["summary"].strip()
        if index == 0 and mbti_note:
            relation_summary = f"{relation_summary} {mbti_note}".strip()
        cards.append(
            {
                "rank_label": "最符合的推荐" if index == 0 else f"推荐 {index + 1}",
                "title": work.title,
                "creator": work.row.get("主创", ""),
                "intro": work.row.get("简介", ""),
                "image_url": work.row.get("剧照链接", ""),
                "image_source": work.row.get("剧照来源", ""),
                "note": relation_summary,
            }
        )

    payload = json.dumps(cards, ensure_ascii=False)
    deck_html = """
    <style>
      html, body {
        margin: 0;
        padding: 0;
        background: transparent;
        font-family: "Avenir Next", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      }
      .deck-scene {
        position: relative;
        overflow: hidden;
        border-radius: 36px;
        padding: 1rem 0.85rem 1.6rem 0.85rem;
        background: radial-gradient(circle at center, #DAF2F7 0%, #A4D5E6 80%);
        box-shadow:
          inset 0 0 0 1px rgba(255,255,255,0.38),
          0 24px 54px rgba(91, 130, 158, 0.14);
      }
      .deck-scene::before {
        content: "";
        position: absolute;
        inset: -10% -8%;
        background:
          radial-gradient(circle at 22% 18%, rgba(255,255,255,0.65), transparent 20%),
          radial-gradient(circle at 82% 14%, rgba(255,255,255,0.34), transparent 18%),
          radial-gradient(circle at 50% 82%, rgba(255,255,255,0.28), transparent 24%);
        filter: blur(18px);
        opacity: 0.9;
        pointer-events: none;
      }
      .deck-ornament {
        position: absolute;
        inset: 0;
        pointer-events: none;
        opacity: 0.46;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 1800'%3E%3Cg fill='none' stroke='rgba(255,255,255,0.92)' stroke-width='3' stroke-linecap='round'%3E%3Cpath d='M103 380c57-19 115 3 154 52 36 44 48 103 30 152'/%3E%3Cpath d='M126 307c48 22 88 61 109 112'/%3E%3Cpath d='M1014 304c-56 27-98 74-112 131'/%3E%3Cpath d='M952 353c42 25 73 67 79 116'/%3E%3Cpath d='M138 1286c44-35 105-52 160-39 53 13 100 56 120 109'/%3E%3Cpath d='M998 1248c-34 24-64 57-80 97-17 43-17 94-1 137'/%3E%3Cpath d='M208 879c112 12 208-70 244-164'/%3E%3Cpath d='M736 210c39 95 142 161 247 163'/%3E%3Cpath d='M582 1448c49-54 70-129 55-201'/%3E%3Cpath d='M444 177c25 70 86 126 160 148'/%3E%3C/g%3E%3C/svg%3E");
        background-size: cover;
        background-position: center;
        transition: transform 0.28s ease-out;
      }
      .deck-header {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 1rem;
        color: #315069;
        margin: 0 0 1rem 0;
        padding: 0 0.25rem;
      }
      .deck-title {
        font-size: 1.16rem;
        line-height: 1.45;
        font-weight: 650;
        margin: 0;
      }
      .deck-counter {
        font-size: 0.94rem;
        letter-spacing: 0.08em;
        color: rgba(49, 80, 105, 0.68);
        white-space: nowrap;
      }
      .deck-caption {
        position: relative;
        z-index: 2;
        margin: -0.15rem 0.25rem 1rem 0.25rem;
        font-size: 0.94rem;
        line-height: 1.82;
        color: rgba(49, 80, 105, 0.84);
      }
      .deck-shell {
        position: relative;
        min-height: 43.5rem;
        max-width: 31.5rem;
        margin: 0 auto;
      }
      .deck-stack {
        position: relative;
        height: 39.5rem;
        cursor: pointer;
      }
      .deck-pager {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.48rem;
        margin-top: 0.9rem;
      }
      .pantone-card {
        position: absolute;
        inset: 0;
        background: var(--paper, rgba(252,249,243,0.98));
        border: 1px solid rgba(218, 225, 231, 0.9);
        box-shadow: 0 22px 44px rgba(102, 138, 165, 0.14);
        overflow: hidden;
        transform-origin: center top;
        transition: transform 0.45s ease, opacity 0.35s ease, box-shadow 0.35s ease;
      }
      .pantone-card::after {
        content: "";
        position: absolute;
        top: 1rem;
        left: 50%;
        width: 8.75rem;
        height: 1.02rem;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(218, 226, 232, 0.98);
        box-shadow: 0 3px 8px rgba(123, 143, 161, 0.08);
      }
      .pantone-card.is-front {
        opacity: 1;
        z-index: 3;
        transform: translate3d(0, 0, 0) rotate(-0.6deg) scale(1);
      }
      .pantone-card.is-middle {
        opacity: 1;
        z-index: 2;
        transform: translate3d(0.45rem, 1.05rem, 0) rotate(0.3deg) scale(0.975);
      }
      .pantone-card.is-back {
        opacity: 1;
        z-index: 1;
        transform: translate3d(-0.45rem, 2.1rem, 0) rotate(-0.2deg) scale(0.95);
      }
      .pantone-card.is-hidden {
        opacity: 0;
        z-index: 0;
        transform: translate3d(0, 3rem, 0) rotate(0deg) scale(0.91);
        pointer-events: none;
      }
      .card-inner {
        position: relative;
        display: grid;
        grid-template-rows: auto auto minmax(12rem, 1fr);
        height: 100%;
        padding: 1.35rem 1.05rem 1.05rem 1.05rem;
      }
      .card-rank {
        position: relative;
        z-index: 1;
        margin-top: 1rem;
        margin-bottom: 0.72rem;
        font-size: 0.8rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: rgba(71, 95, 118, 0.76);
      }
      .card-art {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.88);
        border: 12px solid rgba(249, 247, 242, 0.98);
        box-shadow: inset 0 0 0 1px rgba(220, 227, 234, 0.88);
        padding: 0.48rem;
        min-height: 15rem;
      }
      .card-art img,
      .card-art-fallback {
        display: block;
        width: 100%;
        height: auto;
        max-height: 18.6rem;
        object-fit: contain;
        background: linear-gradient(180deg, #d9eef6, #c3e1ee);
      }
      .card-art-fallback {
        min-height: 15rem;
      }
      .card-swatch {
        position: relative;
        z-index: 1;
        margin-top: 0.72rem;
        padding: 1rem 0.95rem 1.05rem 0.95rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.16), rgba(255,255,255,0.04)), var(--swatch, #dbeef5);
        color: var(--ink, #22384e);
        border: 1px solid rgba(255,255,255,0.24);
      }
      .card-title {
        margin: 0;
        font-size: 1.82rem;
        line-height: 1.16;
        font-weight: 650;
        color: var(--ink, #22384e);
      }
      .card-creator {
        margin-top: 0.45rem;
        font-size: 0.9rem;
        line-height: 1.55;
        color: rgba(34, 56, 78, 0.84);
      }
      .card-intro {
        margin-top: 0.72rem;
        font-size: 0.93rem;
        line-height: 1.72;
        color: rgba(34, 56, 78, 0.88);
      }
      .pager-dot {
        width: 0.58rem;
        height: 0.58rem;
        border: none;
        border-radius: 999px;
        background: rgba(126, 162, 187, 0.38);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.48);
        transition: transform 0.18s ease, background-color 0.18s ease;
        cursor: pointer;
      }
      .pager-dot.is-active {
        background: rgba(109, 135, 161, 0.92);
        transform: scale(1.18);
      }
      @media (max-width: 640px) {
        .deck-scene {
          padding: 0.95rem 0.58rem 1.38rem 0.58rem;
          border-radius: 30px;
        }
        .deck-header {
          margin-bottom: 0.65rem;
        }
        .deck-caption {
          margin: -0.08rem 0.18rem 0.78rem 0.18rem;
          font-size: 0.88rem;
          line-height: 1.74;
        }
        .deck-shell {
          min-height: 38rem;
          max-width: 100%;
        }
        .deck-stack {
          height: 34rem;
        }
        .pantone-card::after {
          width: 7.4rem;
        }
        .card-inner {
          grid-template-rows: auto auto minmax(10.8rem, 1fr);
          padding: 1.18rem 0.86rem 0.92rem 0.86rem;
        }
        .card-title {
          font-size: 1.5rem;
        }
        .card-art img,
        .card-art-fallback {
          max-height: 14.8rem;
        }
        .card-creator {
          font-size: 0.84rem;
        }
        .card-intro {
          font-size: 0.86rem;
          line-height: 1.62;
        }
      }
    </style>
    <div class="deck-scene" id="deck-scene">
      <div class="deck-ornament" id="deck-ornament" aria-hidden="true"></div>
      <div class="deck-header">
        <p class="deck-title">第三幕 · 三张与你同频的舞台色卡</p>
        <div class="deck-counter" id="deck-counter">1 / 3</div>
      </div>
      <p class="deck-caption" id="deck-caption"></p>
      <div class="deck-shell">
        <div class="deck-stack" id="deck-stack"></div>
        <div class="deck-pager" id="deck-pager"></div>
      </div>
    </div>
    <script>
      const cards = __PAYLOAD__;
      const stackEl = document.getElementById("deck-stack");
      const counterEl = document.getElementById("deck-counter");
      const captionEl = document.getElementById("deck-caption");
      const pagerEl = document.getElementById("deck-pager");
      const ornamentEl = document.getElementById("deck-ornament");
      const sceneEl = document.getElementById("deck-scene");
      let activeIndex = 0;

      function escapeHtml(text) {
        return String(text || "")
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#39;");
      }

      function hexToRgb(hex) {
        const normalized = (hex || "").replace("#", "");
        if (normalized.length !== 6) {
          return { r: 220, g: 238, b: 245 };
        }
        return {
          r: parseInt(normalized.slice(0, 2), 16),
          g: parseInt(normalized.slice(2, 4), 16),
          b: parseInt(normalized.slice(4, 6), 16),
        };
      }

      function mixColor(a, b, weight) {
        return {
          r: Math.round(a.r * (1 - weight) + b.r * weight),
          g: Math.round(a.g * (1 - weight) + b.g * weight),
          b: Math.round(a.b * (1 - weight) + b.b * weight),
        };
      }

      function rgbToCss(color) {
        return `rgb(${color.r}, ${color.g}, ${color.b})`;
      }

      function luminance(color) {
        return (0.2126 * color.r) + (0.7152 * color.g) + (0.0722 * color.b);
      }

      function buildPalette(baseColor) {
        const white = { r: 255, g: 255, b: 255 };
        const liftedBase = luminance(baseColor) < 116
          ? mixColor(baseColor, white, 0.58)
          : mixColor(baseColor, white, 0.26);
        const inkBase = mixColor(liftedBase, { r: 23, g: 36, b: 52 }, 0.82);
        const swatch = mixColor(liftedBase, white, 0.24);
        const paper = mixColor(liftedBase, { r: 252, g: 249, b: 243 }, 0.84);
        const ink = luminance(swatch) > 188 ? inkBase : mixColor(swatch, { r: 14, g: 26, b: 39 }, 0.82);
        return {
          swatch: rgbToCss(swatch),
          paper: rgbToCss(paper),
          ink: rgbToCss(ink),
        };
      }

      async function extractPalette(imageUrl, fallbackHex) {
        const fallback = buildPalette(hexToRgb(fallbackHex));
        if (!imageUrl) {
          return fallback;
        }
        try {
          const image = new Image();
          image.crossOrigin = "anonymous";
          image.referrerPolicy = "no-referrer";
          const loaded = await new Promise((resolve, reject) => {
            image.onload = () => resolve(image);
            image.onerror = reject;
            image.src = imageUrl;
          });
          const canvas = document.createElement("canvas");
          canvas.width = 28;
          canvas.height = 28;
          const ctx = canvas.getContext("2d", { willReadFrequently: true });
          if (!ctx) {
            return fallback;
          }
          ctx.drawImage(loaded, 0, 0, canvas.width, canvas.height);
          const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
          let totalR = 0;
          let totalG = 0;
          let totalB = 0;
          let count = 0;
          for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            const alpha = data[i + 3];
            if (alpha < 32) {
              continue;
            }
            if (Math.max(r, g, b) < 40) {
              continue;
            }
            if (r > 245 && g > 245 && b > 245) {
              continue;
            }
            totalR += r;
            totalG += g;
            totalB += b;
            count += 1;
          }
          if (!count) {
            return fallback;
          }
          return buildPalette({
            r: Math.round(totalR / count),
            g: Math.round(totalG / count),
            b: Math.round(totalB / count),
          });
        } catch (error) {
          return fallback;
        }
      }

      function buildArt(card) {
        const img = `<img src="${escapeHtml(card.image_url)}" alt="${escapeHtml(card.title)} 剧照" loading="lazy" />`;
        if (!card.image_url) {
          return `<div class="card-art"><div class="card-art-fallback"></div></div>`;
        }
        if (card.image_source) {
          return `<a class="card-art" href="${escapeHtml(card.image_source)}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()">${img}</a>`;
        }
        return `<div class="card-art">${img}</div>`;
      }

      function buildCard(card, index) {
        const distance = (index - activeIndex + cards.length) % cards.length;
        const className =
          distance === 0 ? "is-front" :
          distance === 1 ? "is-middle" :
          distance === 2 ? "is-back" : "is-hidden";
        const paletteStyle = `--swatch:${card.palette.swatch};--paper:${card.palette.paper};--ink:${card.palette.ink};`;
        return `
          <article class="pantone-card ${className}" style="${paletteStyle}">
            <div class="card-inner">
              <div class="card-rank">${escapeHtml(card.rank_label)}</div>
              ${buildArt(card)}
              <div class="card-swatch">
                <h3 class="card-title">《${escapeHtml(card.title)}》</h3>
                <div class="card-creator">主创：${escapeHtml(card.creator || "待补充")}</div>
                <div class="card-intro">${escapeHtml(card.intro)}</div>
              </div>
            </div>
          </article>
        `;
      }

      function renderDeck() {
        stackEl.innerHTML = cards.map((card, index) => buildCard(card, index)).join("");
        counterEl.textContent = `${activeIndex + 1} / ${cards.length}`;
        if (captionEl) {
          captionEl.textContent = cards[activeIndex]?.note || "";
        }
        if (pagerEl) {
          pagerEl.innerHTML = cards.map((card, index) => (
            `<button class="pager-dot ${index === activeIndex ? "is-active" : ""}" type="button" data-index="${index}" aria-label="查看第 ${index + 1} 张推荐"></button>`
          )).join("");
          pagerEl.querySelectorAll(".pager-dot").forEach((dot) => {
            dot.addEventListener("click", (event) => {
              event.stopPropagation();
              activeIndex = Number(dot.getAttribute("data-index") || 0);
              renderDeck();
            });
          });
        }
      }

      function bindParallax() {
        sceneEl.addEventListener("pointermove", (event) => {
          const rect = sceneEl.getBoundingClientRect();
          const x = (event.clientX - rect.left) / rect.width - 0.5;
          const y = (event.clientY - rect.top) / rect.height - 0.5;
          ornamentEl.style.transform = `translate(${x * 12}px, ${y * 12}px)`;
        });
        sceneEl.addEventListener("pointerleave", () => {
          ornamentEl.style.transform = "translate(0px, 0px)";
        });
      }

      async function initDeck() {
        if (!cards.length) {
          stackEl.innerHTML = "";
          counterEl.textContent = "0 / 0";
          return;
        }
        const fallbackColors = ["#d7edf5", "#c7dff1", "#dce9df"];
        const palettes = await Promise.all(
          cards.map((card, index) => extractPalette(card.image_url, fallbackColors[index % fallbackColors.length]))
        );
        cards.forEach((card, index) => {
          card.palette = palettes[index];
        });
        renderDeck();
        bindParallax();
      }

      stackEl.addEventListener("click", () => {
        activeIndex = (activeIndex + 1) % cards.length;
        renderDeck();
      });

      initDeck();
    </script>
    """.replace("__PAYLOAD__", payload)
    components.html(deck_html, height=900, scrolling=False)


def get_stage_mode() -> str:
    query_params = getattr(st, "query_params", None)
    if query_params is not None:
        stage = query_params.get("stage", "")
        if isinstance(stage, list):
            stage = stage[0] if stage else ""
        return str(stage)

    legacy_params = st.experimental_get_query_params()
    stage = legacy_params.get("stage", [""])
    if isinstance(stage, list):
        return stage[0] if stage else ""
    return str(stage)


MBTI_DIMENSION_OPTIONS = (
    ("Q1_ei", "E / I", [("Q1_A", "E"), ("Q1_B", "I")]),
    ("Q1_sn", "S / N", [("Q1_D", "S"), ("Q1_C", "N")]),
    ("Q1_tf", "T / F", [("Q1_E", "T"), ("Q1_F", "F")]),
    ("Q1_jp", "P / J", [("Q1_H", "P"), ("Q1_G", "J")]),
)

MBTI_WARMTH = {
    "E": "你常常会被舞台的流动感、人与人之间的张力和现场能量很快点亮。",
    "I": "你更容易在安静处进入作品，也更擅长听见那些细微却长尾的情绪回声。",
    "S": "你会信任具体的身体、场景和细节，喜欢作品真正落在可触摸的生活质地上。",
    "N": "你天生会追随意象、象征和余味，常常在别人还没说出口的地方先感到什么。",
    "T": "你会在感受之外留意结构、逻辑和编排如何成立，对作品的骨架很敏感。",
    "F": "你特别在意情感有没有被真诚地递出来，也很容易和人物命运建立连接。",
    "J": "你会偏爱完整、稳定、收束有力的表达，喜欢作品在秩序里慢慢长出力量。",
    "P": "你会被开放、流动、带一点未知感的表达吸引，喜欢作品保留呼吸和空白。",
}


def collect_mbti_answer() -> str | list[str] | None:
    unsure = st.checkbox("我不确定", key="Q1_unsure")
    if unsure:
        for key, _, _ in MBTI_DIMENSION_OPTIONS:
            if key in st.session_state:
                st.session_state[key] = None
        return "Q1_I"

    labels = {
        "Q1_A": "E",
        "Q1_B": "I",
        "Q1_D": "S",
        "Q1_C": "N",
        "Q1_E": "T",
        "Q1_F": "F",
        "Q1_H": "P",
        "Q1_G": "J",
    }
    selected_options: list[str] = []
    for field_key, dimension_label, option_pairs in MBTI_DIMENSION_OPTIONS:
        st.markdown(
            f"<div class='mbti-dimension-label'>{dimension_label}</div>",
            unsafe_allow_html=True,
        )
        option_ids = [item[0] for item in option_pairs]
        current_value = st.session_state.get(field_key)
        default_index = option_ids.index(current_value) if current_value in option_ids else None
        selected = st.radio(
            " ",
            option_ids,
            index=default_index,
            horizontal=True,
            format_func=lambda option_id, mapping=labels: mapping[option_id],
            key=field_key,
            label_visibility="collapsed",
        )
        if selected:
            selected_options.append(selected)

    return selected_options


def mbti_code_from_answers(answer_value: str | list[str] | None) -> str:
    if answer_value == "Q1_I":
        return ""
    option_ids = answer_value if isinstance(answer_value, list) else []
    option_to_letter = {
        "Q1_A": "E",
        "Q1_B": "I",
        "Q1_D": "S",
        "Q1_C": "N",
        "Q1_E": "T",
        "Q1_F": "F",
        "Q1_H": "P",
        "Q1_G": "J",
    }
    letters = [option_to_letter[option_id] for option_id in option_ids if option_id in option_to_letter]
    if len(letters) != 4:
        return ""
    return "".join(letters)


def mbti_match_note(mbti_code: str, work_title: str, matched_tags: list[str]) -> str:
    if not mbti_code:
        return ""
    dimensions = [MBTI_WARMTH[letter] for letter in mbti_code]
    tag_text = "、".join(matched_tags[:3]) if matched_tags else "你这次的观看偏好"
    return (
        f"作为 {mbti_code} 的你，"
        f"{dimensions[0]}{dimensions[1]}{dimensions[2]}{dimensions[3]}"
        f"所以像《{work_title}》这种带着 {tag_text} 气质的作品，"
        "往往会更容易让你觉得被接住，也更容易走进你的心里。"
    )


QUESTION_STAGES = [
    {
        "title": "第 1 阶段 · 身体初醒",
        "note": "先让最轻的两个信号亮起来，页面会在你完成这一组后自然向下生长。",
        "question_ids": ("Q1", "Q2"),
    },
    {
        "title": "第 2 阶段 · 感官展开",
        "note": "这一段会在前一组完成后优雅展开，让你继续往下走。",
        "question_ids": ("Q3", "Q4"),
    },
    {
        "title": "第 3 阶段 · 身体语汇",
        "note": "把你更偏爱的身体质地和听觉牵引找出来。",
        "question_ids": ("Q5", "Q6"),
    },
    {
        "title": "第 4 阶段 · 题材偏向",
        "note": "如果你更靠近中国题材，这一段会继续长出地域气质的判断。",
        "question_ids": ("Q7", "Q8"),
    },
    {
        "title": "第 5 阶段 · 精神落点",
        "note": "最后三题会把今晚的观看坐标慢慢收束起来。",
        "question_ids": ("Q9", "Q10", "Q11"),
    },
]


def render_intro_section() -> None:
    st.markdown(
        f"""
        <section class="stage-hero">
            <div class="stage-hero-inner">
                <div class="stage-eyebrow">第一幕 · 剧场入口</div>
                <h1 class="stage-title" style="color: var(--text-blue) !important;">寻找此刻与你精神同频的舞蹈作品</h1>
                <div class="stage-copy">
                    <p>堆叠的学业与周而复始的事务，常常让我们忘记了肉身的温度与呼吸。</p>
                    <p>花 2 分钟跟随直觉，从优雅的古典芭蕾到大写意的东方舞剧，</p>
                    <p>找出此时此刻，最契合你灵魂的那一部作品。</p>
                </div>
                <div class="stage-cta-wrap">
                    <a class="stage-cta" href="?stage=quiz#questionnaire">🪐 步入舞台</a>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def is_answer_complete(question_id: str) -> bool:
    answer_value = st.session_state.get(question_id)
    if question_id == "Q1":
        if answer_value == "Q1_I":
            return True
        return isinstance(answer_value, list) and len(answer_value) == 4
    return bool(answer_value)


def active_question_ids(question_ids: tuple[str, ...]) -> list[str]:
    visible_ids: list[str] = []
    for question_id in question_ids:
        if question_id == "Q8" and st.session_state.get("Q7") != "Q7_A":
            continue
        visible_ids.append(question_id)
    return visible_ids


def render_question_heading(question_id: str, question_text: str) -> None:
    question_number = "".join(ch for ch in question_id if ch.isdigit()) or question_id
    st.markdown(
        (
            "<div class='question-heading'>"
            f"<span class='question-number'>{html.escape(question_number)}</span>"
            f"<div class='question-heading-text'>{html.escape(question_text)}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_standard_question(question) -> None:
    render_question_heading(question.question_id, question.question_text)
    option_ids = [option.option_id for option in question.options]
    option_text_map = {
        option.option_id: option.option_text for option in question.options
    }
    current_value = st.session_state.get(question.question_id)
    default_index = option_ids.index(current_value) if current_value in option_ids else None
    st.radio(
        question.question_text,
        option_ids,
        index=default_index,
        format_func=lambda option_id, mapping=option_text_map: mapping[option_id],
        key=question.question_id,
        label_visibility="collapsed",
    )


def render_question_stage(
    stage_index: int,
    question_ids: tuple[str, ...],
    questions_by_id: dict[str, object],
) -> bool:
    visible_ids = active_question_ids(question_ids)
    if not visible_ids:
        return True

    stage = QUESTION_STAGES[stage_index]
    st.markdown(
        f"""
        <div class="question-stage-shell">
            <div class="question-stage-kicker">第 {stage_index + 1} 阶段 / 5</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for question_id in visible_ids:
        question = questions_by_id[question_id]
        if question_id == "Q1":
            render_question_heading(question.question_id, question.question_text)
            st.caption("四组二选一；如果你暂时不想判断，也可以直接选“我不确定”。")
            st.session_state["Q1"] = collect_mbti_answer()
        else:
            render_standard_question(question)

    return all(is_answer_complete(question_id) for question_id in visible_ids)


def main() -> None:
    if st.session_state.get("Q7") != "Q7_A" and "Q8" in st.session_state:
        st.session_state.pop("Q8")

    render_intro_section()
    if get_stage_mode() != "quiz":
        return

    questions = load_quiz_questions()
    st.markdown('<div id="questionnaire" class="question-anchor"></div>', unsafe_allow_html=True)

    questions_by_id = {question.question_id: question for question in questions}
    st.markdown('<div class="section-title">第二幕 · 身体探索</div>', unsafe_allow_html=True)

    stages_completed = True
    for stage_index, stage in enumerate(QUESTION_STAGES):
        if not stages_completed:
            break
        stages_completed = render_question_stage(
            stage_index=stage_index,
            question_ids=stage["question_ids"],
            questions_by_id=questions_by_id,
        )

    all_visible_question_ids: list[str] = []
    for stage in QUESTION_STAGES:
        all_visible_question_ids.extend(active_question_ids(stage["question_ids"]))

    all_visible_complete = all(
        is_answer_complete(question_id) for question_id in all_visible_question_ids
    )
    if all_visible_complete:
        if st.button("🎟️ 铸造专属剧场门票", use_container_width=True):
            st.session_state["show_recommendation"] = True
    else:
        st.session_state.pop("show_recommendation", None)

    if st.session_state.get("show_recommendation") and all_visible_complete:
        q1_answer = st.session_state.get("Q1")
        if isinstance(q1_answer, list) and len(q1_answer) not in {0, 4}:
            st.warning("第一题的 MBTI 部分最好四组都选完；如果暂时拿不准，也可以直接选“我不确定”。")
            return

        visible_questions = [
            questions_by_id[question_id]
            for question_id in all_visible_question_ids
        ]
        selected_answers = {}
        for question in visible_questions:
            question_id = question.question_id
            answer_value = st.session_state.get(question_id)
            if isinstance(answer_value, list) and answer_value:
                selected_answers[question_id] = answer_value
            elif isinstance(answer_value, str) and answer_value:
                selected_answers[question_id] = answer_value
        recommendation_payload = recommend(selected_answers, top_n=3)
        results = recommendation_payload["results"]
        profile = recommendation_payload["profile"]

        st.markdown('<div class="section-title">你的观看画像</div>', unsafe_allow_html=True)
        render_tag_chips([item["tag"] for item in profile[:8]])

        if not results:
            st.info("这一轮还没有算出结果，我们可以继续补充作品库。")
            return

        top_result = results[0]
        first_work = top_result["work"]
        mbti_code = mbti_code_from_answers(st.session_state.get("Q1"))
        mbti_note = mbti_match_note(mbti_code, first_work.title, top_result["matched_tags"])

        render_recommendation_deck(results, mbti_note)

        with st.expander("看看这次推荐是怎么得出来的"):
            st.write("问卷的大部分题目会先转成标签，再和作品库里的情绪、风格、主题、观看人格标签去做匹配。")
            st.write("Q4 的观看门槛单独计算，所以“入门 / 中级 / 高级”不会混进普通标签里。")
            st.write("Q7 会额外考虑你是更想看中国题材还是外国题材，避免整体气质对了但文化来源跑偏。")
            st.write("Q8 只会在你选择中国题材后出现，用来继续分辨在地文化的气质方向。")
            for result in results:
                work = result["work"]
                st.markdown(f"**{work.title}**")
                render_tag_chips(result["matched_tags"][:6])
                for hit in result["question_hits"][:3]:
                    tags_text = " / ".join(hit["tags"])
                    st.write(f"- {hit['option_text']} -> {tags_text}")


if __name__ == "__main__":
    main()
