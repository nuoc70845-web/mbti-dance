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


BASE_DIR = Path(__file__).resolve().parent

INTRO_BACKGROUND_URI = image_file_to_data_uri(
    str(BASE_DIR / "assets" / "intro-bg.png")
)
QUIZ_BACKGROUND_URI = image_file_to_data_uri(
    str(BASE_DIR / "assets" / "quiz-bg.png")
)

st.markdown(
    """
    <style>
    :root {
        --bg-warm: #e8f0f3;
        --bg-warm-deep: #d4e3e8;
        --card-cream: rgba(252, 249, 247, 0.78);
        --line-soft: rgba(139, 138, 149, 0.16);
        --text-main: #60707d;
        --text-blue: #71889b;
        --text-soft: #8995a3;
        --text-ink: #5f6177;
        --accent-rose: #d59ca3;
        --accent-sage: #94b0a7;
        --accent-gold: #d5af8d;
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
            radial-gradient(circle at 14% 14%, rgba(247, 233, 237, 0.26), transparent 28%),
            radial-gradient(circle at 84% 12%, rgba(229, 241, 244, 0.18), transparent 24%),
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
        max-width: 38rem;
        min-height: calc(100svh - 2.6rem);
        margin: 0 auto 1rem auto;
        padding: 1.2rem 1.1rem 1.5rem 1.1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        overflow: hidden;
        border-radius: 38px;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0.08)),
            url("__INTRO_BG__");
        background-size: cover;
        background-position: center top;
        box-shadow:
            inset 0 0 0 1px rgba(255, 255, 255, 0.24),
            0 24px 52px rgba(120, 136, 153, 0.18);
    }
    .stage-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(247, 235, 239, 0.40) 54%, rgba(233, 244, 247, 0.22)),
            radial-gradient(circle at center, rgba(255, 255, 255, 0.1), transparent 48%);
        opacity: 0.96;
    }
    .stage-hero::after {
        content: "";
        position: absolute;
        right: -3.4rem;
        bottom: -3.2rem;
        width: 14rem;
        height: 14rem;
        border-radius: 50%;
        pointer-events: none;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.42), rgba(233, 210, 221, 0.16) 52%, transparent 74%);
        filter: blur(6px);
        opacity: 0.92;
    }
    .stage-hero-inner {
        position: relative;
        z-index: 1;
        max-width: 25rem;
        padding: 0 0.2rem;
    }
    .stage-eyebrow {
        color: rgba(140, 120, 132, 0.78);
        font-size: 0.74rem;
        letter-spacing: 0.26em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .stage-title-wrap {
        display: grid;
        gap: 0.5rem;
    }
    .stage-title-prelude {
        margin: 0;
        color: rgba(123, 108, 118, 0.78);
        font-size: 0.84rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }
    .stage-title {
        margin: 0;
        text-wrap: balance;
        text-shadow: 0 0 26px rgba(255, 255, 255, 0.36);
    }
    .stage-title-top,
    .stage-title-main {
        display: block;
        font-family: "Iowan Old Style", "Palatino Linotype", "Songti SC", "STSong", serif;
    }
    .stage-title-top {
        color: var(--text-ink);
        font-size: clamp(1.36rem, 5vw, 1.62rem);
        line-height: 1.18;
        font-weight: 540;
        letter-spacing: 0.06em;
    }
    .stage-title-main {
        margin-top: 0;
        font-size: clamp(2.2rem, 8vw, 3rem);
        line-height: 1.06;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: #516579;
    }
    .stage-title-accent {
        background: linear-gradient(135deg, var(--accent-rose) 0%, #799596 56%, var(--accent-gold) 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
    }
    .stage-copy-panel {
        margin-top: 1.25rem;
        padding: 1rem 1rem 1.05rem 1rem;
        border-radius: 24px;
        background: rgba(255, 250, 248, 0.62);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 14px 30px rgba(136, 146, 162, 0.10);
    }
    .stage-copy {
        margin: 0;
        color: #69707d;
        font-size: 0.99rem;
        line-height: 1.86;
        text-align: left;
        max-width: none;
        text-shadow: none;
    }
    .stage-copy p {
        margin: 0 0 0.66rem 0;
    }
    .stage-copy p:last-child {
        margin-bottom: 0;
    }
    .stage-copy strong {
        color: #816775;
        font-weight: 650;
    }
    .stage-quote {
        margin-top: 0.8rem;
        color: rgba(131, 114, 126, 0.88);
        font-size: 0.9rem;
        letter-spacing: 0.04em;
    }
    .stage-trail {
        margin-top: 0.95rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.48rem;
    }
    .stage-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.34rem 0.72rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(220, 206, 211, 0.56);
        color: #7b6975;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        box-shadow: 0 8px 16px rgba(151, 136, 150, 0.08);
    }
    .stage-cta-wrap {
        margin-top: 1.5rem;
        display: flex;
        justify-content: center;
    }
    .stage-cta {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.45rem;
        min-width: 11.7rem;
        padding: 0.96rem 1.45rem;
        border-radius: 999px;
        text-decoration: none;
        color: #fffaf5;
        background: linear-gradient(135deg, rgba(229, 192, 206, 0.98) 0%, rgba(164, 196, 216, 0.98) 100%);
        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.32),
            0 0 20px rgba(255, 255, 255, 0.46),
            0 16px 28px rgba(145, 164, 187, 0.2);
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
            0 18px 32px rgba(145, 164, 187, 0.24);
    }
    .stage-cta:focus,
    .stage-cta:active {
        color: #fffaf5;
    }
    .stage-cta-note {
        margin-top: 0.78rem;
        color: rgba(113, 109, 123, 0.82);
        font-size: 0.85rem;
        letter-spacing: 0.04em;
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
    @keyframes mistSceneExit {
        0%, 76% {
            opacity: 1;
            visibility: visible;
        }
        100% {
            opacity: 0;
            visibility: hidden;
        }
    }
    @keyframes mistDriftFront {
        0% {
            opacity: 1;
            transform: scale(1.08) translate3d(0, 0, 0);
        }
        100% {
            opacity: 0;
            transform: scale(1.28) translate3d(0, -8%, 0);
        }
    }
    @keyframes mistDriftBack {
        0% {
            opacity: 0.92;
            transform: scale(1.02) translate3d(0, 0, 0);
        }
        100% {
            opacity: 0;
            transform: scale(1.16) translate3d(0, 10%, 0);
        }
    }
    @keyframes mistCopyFade {
        0%, 54% {
            opacity: 0.94;
            transform: translateY(0);
        }
        100% {
            opacity: 0;
            transform: translateY(-10px);
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
    .question-scene {
        position: relative;
        padding-bottom: 0.8rem;
        animation: stageRise 0.42s ease-out both;
    }
    .question-scene-shell {
        margin: 0.35rem 0 0.85rem 0;
        padding: 1rem 1rem 0.92rem 1rem;
        border: 1px solid rgba(122, 149, 169, 0.14);
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.42);
        box-shadow: 0 18px 32px rgba(122, 149, 169, 0.08);
        backdrop-filter: blur(12px);
    }
    .question-scene-kicker {
        color: rgba(104, 130, 152, 0.62);
        font-size: 0.76rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .question-scene-note {
        color: var(--text-soft);
        font-size: 0.94rem;
        line-height: 1.7;
    }
    .question-heading {
        display: flex;
        align-items: flex-start;
        gap: 0.62rem;
        margin: 0.85rem 0 0.3rem 0;
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
    .mbti-dimension-label {
        color: var(--text-main);
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0.1rem 0 0.35rem 0;
    }
    .scene-back-bar {
        max-width: 680px;
        margin: 0 auto 0.85rem auto;
        display: flex;
        justify-content: flex-start;
    }
    .scene-back-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.85rem;
        height: 2.85rem;
        border-radius: 999px;
        text-decoration: none;
        color: rgba(255, 255, 255, 0.98) !important;
        font-size: 1.38rem;
        line-height: 1;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.34);
        box-shadow: 0 12px 26px rgba(126, 152, 179, 0.16);
        backdrop-filter: blur(14px);
        transition: transform 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease;
    }
    .scene-back-link:hover {
        transform: translateY(-1px);
        background: rgba(255, 255, 255, 0.18);
        box-shadow: 0 14px 28px rgba(126, 152, 179, 0.2);
    }
    .mist-transition {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 30;
        overflow: hidden;
        animation: mistSceneExit 1.85s ease forwards;
    }
    .mist-transition::before,
    .mist-transition::after {
        content: "";
        position: absolute;
        inset: -14%;
        background:
            radial-gradient(circle at 18% 34%, rgba(255, 255, 255, 0.92), transparent 18%),
            radial-gradient(circle at 76% 22%, rgba(255, 255, 255, 0.78), transparent 19%),
            radial-gradient(circle at 64% 74%, rgba(255, 255, 255, 0.8), transparent 22%),
            radial-gradient(circle at 34% 70%, rgba(246, 251, 255, 0.74), transparent 24%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(236, 246, 252, 0.68));
        filter: blur(28px);
    }
    .mist-transition::before {
        animation: mistDriftFront 1.85s cubic-bezier(0.2, 0.78, 0.2, 1) forwards;
    }
    .mist-transition::after {
        opacity: 0.78;
        filter: blur(40px);
        animation: mistDriftBack 1.85s cubic-bezier(0.2, 0.78, 0.2, 1) forwards;
    }
    .mist-copy {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: rgba(109, 128, 149, 0.86);
        font-size: 1.04rem;
        letter-spacing: 0.08em;
        animation: mistCopyFade 1.3s ease forwards;
    }
    .result-copy {
        color: #695a4d;
        line-height: 1.75;
    }
    .results-back-bar {
        max-width: 680px;
        margin: 0 auto 0.85rem auto;
        display: flex;
        justify-content: flex-start;
    }
    .results-back-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.85rem;
        height: 2.85rem;
        border-radius: 999px;
        text-decoration: none;
        color: rgba(255, 255, 255, 0.98) !important;
        font-size: 1.38rem;
        line-height: 1;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.34);
        box-shadow: 0 12px 26px rgba(126, 152, 179, 0.16);
        backdrop-filter: blur(14px);
        transition: transform 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease;
    }
    .results-back-link:hover {
        transform: translateY(-1px);
        background: rgba(255, 255, 255, 0.18);
        box-shadow: 0 14px 28px rgba(126, 152, 179, 0.2);
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
        background: linear-gradient(135deg, rgba(229, 192, 206, 0.98) 0%, rgba(164, 196, 216, 0.98) 100%);
        color: #fffaf5;
        border: none;
        border-radius: 999px;
        min-height: 3rem;
        font-size: 0.99rem;
        font-weight: 680;
        box-shadow: 0 0 18px rgba(255, 255, 255, 0.34), 0 12px 20px rgba(145, 164, 187, 0.20);
        animation: breathePulse 2.8s ease-in-out infinite;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #e6c2cf 0%, #a7c8de 100%);
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
            padding: 0.88rem 0.72rem 1.14rem 0.72rem;
        }
        .stage-title-top {
            font-size: 1.2rem;
        }
        .stage-title-main {
            font-size: 2rem;
        }
        .stage-hero-inner {
            max-width: 20rem;
        }
        .stage-copy-panel {
            margin-top: 1.05rem;
            padding: 0.92rem 0.86rem 0.98rem 0.86rem;
        }
        .stage-copy {
            font-size: 0.93rem;
            line-height: 1.78;
        }
        .stage-quote,
        .stage-cta-note {
            font-size: 0.82rem;
        }
        .stage-pill {
            font-size: 0.76rem;
            padding: 0.3rem 0.64rem;
        }
        .stage-cta {
            min-width: 10.9rem;
            padding: 0.88rem 1.22rem;
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
            relation_summary = f"{mbti_note} {relation_summary}".strip()
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
        isolation: isolate;
        border-radius: 36px;
        padding: 1rem 0.85rem 1.6rem 0.85rem;
        background: radial-gradient(circle at center, #DAF2F7 0%, #A4D5E6 80%);
        box-shadow:
          inset 0 0 0 1px rgba(255,255,255,0.38),
          0 24px 54px rgba(91, 130, 158, 0.14);
      }
      .curtain-overlay {
        position: absolute;
        inset: 0;
        z-index: 6;
        overflow: hidden;
        background: radial-gradient(circle at center, rgba(228, 240, 248, 0.28), rgba(171, 201, 223, 0.18) 58%, rgba(132, 164, 195, 0.14));
        animation: curtainOverlayExit 0.35s ease 1.9s forwards;
      }
      .curtain-panel {
        position: absolute;
        top: -2%;
        bottom: -2%;
        width: 54%;
        box-shadow:
          inset -1px 0 0 rgba(255,255,255,0.42),
          0 18px 34px rgba(95, 132, 167, 0.16);
      }
      .curtain-panel::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
          repeating-linear-gradient(
            90deg,
            rgba(255,255,255,0.14) 0,
            rgba(255,255,255,0.14) 18px,
            rgba(118, 151, 183, 0.10) 18px,
            rgba(118, 151, 183, 0.10) 38px
          ),
          linear-gradient(180deg, rgba(255,255,255,0.26), transparent 22%, rgba(108, 141, 176, 0.12) 72%, rgba(91, 125, 160, 0.18));
      }
      .curtain-left {
        left: 0;
        background: linear-gradient(90deg, rgba(178, 207, 228, 0.99) 0%, rgba(157, 189, 215, 0.98) 58%, rgba(134, 168, 198, 0.98) 100%);
        transform-origin: left center;
        animation: curtainOpenLeft 1.25s cubic-bezier(0.2, 0.82, 0.22, 1) 0.48s forwards;
      }
      .curtain-right {
        right: 0;
        background: linear-gradient(270deg, rgba(178, 207, 228, 0.99) 0%, rgba(157, 189, 215, 0.98) 58%, rgba(134, 168, 198, 0.98) 100%);
        transform-origin: right center;
        animation: curtainOpenRight 1.25s cubic-bezier(0.2, 0.82, 0.22, 1) 0.48s forwards;
      }
      .curtain-center-glow {
        position: absolute;
        left: 50%;
        top: 8%;
        bottom: 8%;
        width: 16%;
        transform: translateX(-50%);
        background: radial-gradient(circle at center, rgba(255,255,255,0.56), rgba(255,255,255,0.10) 62%, transparent 76%);
        filter: blur(10px);
        opacity: 0.9;
        animation: curtainGlowFade 1s ease 0.9s forwards;
      }
      .curtain-copy {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.52rem;
        text-align: center;
        color: #f8fcff;
        text-shadow: 0 4px 18px rgba(88, 122, 158, 0.28);
        animation: curtainCopyFade 0.45s ease 1.12s forwards;
      }
      .curtain-copy-eyebrow {
        font-size: 0.76rem;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        opacity: 0.92;
      }
      .curtain-copy-title {
        font-size: 1.32rem;
        line-height: 1.45;
        font-weight: 650;
        letter-spacing: 0.06em;
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
        opacity: 0;
        animation: deckContentReveal 0.62s ease 1.18s forwards;
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
        opacity: 0;
        animation: deckContentReveal 0.62s ease 1.28s forwards;
      }
      .deck-shell {
        position: relative;
        max-width: 31.5rem;
        margin: 0 auto;
        opacity: 0;
        animation: deckContentReveal 0.72s ease 1.36s forwards;
      }
      .deck-viewport {
        overflow: hidden;
        border-radius: 34px;
        padding: 0.18rem;
        cursor: grab;
        touch-action: pan-y;
        user-select: none;
      }
      .deck-viewport.is-dragging {
        cursor: grabbing;
      }
      .deck-track {
        display: flex;
        align-items: stretch;
        will-change: transform;
      }
      .deck-slide {
        flex: 0 0 100%;
        min-width: 100%;
        box-sizing: border-box;
        padding: 0 0.08rem 0.18rem 0.08rem;
      }
      .deck-pager {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.48rem;
        margin-top: 0.9rem;
        opacity: 0;
        animation: deckContentReveal 0.62s ease 1.48s forwards;
      }
      .deck-hint {
        position: relative;
        z-index: 2;
        margin-top: 0.72rem;
        text-align: center;
        font-size: 0.84rem;
        line-height: 1.55;
        color: rgba(49, 80, 105, 0.68);
        letter-spacing: 0.04em;
        opacity: 0;
        animation: deckContentReveal 0.62s ease 1.56s forwards;
      }
      .pantone-card {
        position: relative;
        display: block;
        background: var(--paper, rgba(252,249,243,0.98));
        border: 1px solid rgba(218, 225, 231, 0.9);
        box-shadow: 0 22px 44px rgba(102, 138, 165, 0.14);
        overflow: hidden;
        border-radius: 30px;
      }
      .pantone-card::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(180deg, rgba(255,255,255,0.08), transparent 18%, rgba(255,255,255,0.12) 100%);
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
        border-radius: 22px;
        overflow: hidden;
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
      @keyframes curtainOpenLeft {
        0% {
          transform: translateX(0);
        }
        100% {
          transform: translateX(-108%);
        }
      }
      @keyframes curtainOpenRight {
        0% {
          transform: translateX(0);
        }
        100% {
          transform: translateX(108%);
        }
      }
      @keyframes curtainCopyFade {
        0%,
        55% {
          opacity: 1;
          transform: translateY(0);
        }
        100% {
          opacity: 0;
          transform: translateY(-12px);
        }
      }
      @keyframes curtainGlowFade {
        0%,
        45% {
          opacity: 0.92;
        }
        100% {
          opacity: 0;
        }
      }
      @keyframes curtainOverlayExit {
        0%,
        88% {
          opacity: 1;
          visibility: visible;
        }
        100% {
          opacity: 0;
          visibility: hidden;
        }
      }
      @keyframes deckContentReveal {
        0% {
          opacity: 0;
          transform: translateY(14px);
        }
        100% {
          opacity: 1;
          transform: translateY(0);
        }
      }
      @media (max-width: 640px) {
        .deck-scene {
          padding: 0.95rem 0.58rem 1.38rem 0.58rem;
          border-radius: 30px;
        }
        .curtain-copy-title {
          font-size: 1.08rem;
          line-height: 1.52;
        }
        .curtain-copy-eyebrow {
          font-size: 0.72rem;
          letter-spacing: 0.18em;
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
          max-width: 100%;
        }
        .deck-viewport {
          border-radius: 28px;
          padding: 0.12rem;
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
      <div class="curtain-overlay" aria-hidden="true">
        <div class="curtain-panel curtain-left"></div>
        <div class="curtain-panel curtain-right"></div>
        <div class="curtain-center-glow"></div>
        <div class="curtain-copy">
          <div class="curtain-copy-eyebrow">第三幕即将开启</div>
          <div class="curtain-copy-title">专属作品正在缓缓显现</div>
        </div>
      </div>
      <div class="deck-ornament" id="deck-ornament" aria-hidden="true"></div>
      <div class="deck-header">
        <p class="deck-title">第三幕 · 三张与你同频的舞台色卡</p>
        <div class="deck-counter" id="deck-counter">1 / 3</div>
      </div>
      <p class="deck-caption" id="deck-caption"></p>
      <div class="deck-shell">
        <div class="deck-viewport" id="deck-viewport">
          <div class="deck-track" id="deck-track"></div>
        </div>
        <div class="deck-pager" id="deck-pager"></div>
        <div class="deck-hint">向左轻轻滑动，继续看下一张作品卡。</div>
      </div>
    </div>
    <script>
      const cards = __PAYLOAD__;
      const viewportEl = document.getElementById("deck-viewport");
      const trackEl = document.getElementById("deck-track");
      const counterEl = document.getElementById("deck-counter");
      const captionEl = document.getElementById("deck-caption");
      const pagerEl = document.getElementById("deck-pager");
      const ornamentEl = document.getElementById("deck-ornament");
      const sceneEl = document.getElementById("deck-scene");
      let activeIndex = 0;
      let dragOffset = 0;
      let dragStartX = 0;
      let isDragging = false;
      let suppressClick = false;

      function setFrameHeight() {
        const height = Math.ceil(document.documentElement.scrollHeight);
        window.parent.postMessage(
          {
            isStreamlitMessage: true,
            type: "streamlit:setFrameHeight",
            height,
          },
          "*"
        );
      }

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

      function buildCard(card) {
        const paletteStyle = `--swatch:${card.palette.swatch};--paper:${card.palette.paper};--ink:${card.palette.ink};`;
        return `
          <div class="deck-slide">
            <article class="pantone-card" style="${paletteStyle}">
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
          </div>
        `;
      }

      function currentX(event) {
        if (event.touches && event.touches.length) {
          return event.touches[0].clientX;
        }
        if (event.changedTouches && event.changedTouches.length) {
          return event.changedTouches[0].clientX;
        }
        return event.clientX || 0;
      }

      function syncDeck(animate = true) {
        const width = viewportEl.getBoundingClientRect().width;
        trackEl.style.transition = animate ? "transform 0.46s cubic-bezier(0.22, 1, 0.36, 1)" : "none";
        trackEl.style.transform = `translate3d(${(-activeIndex * width) + dragOffset}px, 0, 0)`;
        counterEl.textContent = `${activeIndex + 1} / ${cards.length}`;
        captionEl.textContent = cards[activeIndex]?.note || "";
        pagerEl.querySelectorAll(".pager-dot").forEach((dot, index) => {
          dot.classList.toggle("is-active", index === activeIndex);
        });
        requestAnimationFrame(setFrameHeight);
      }

      function goTo(index) {
        activeIndex = Math.max(0, Math.min(index, cards.length - 1));
        dragOffset = 0;
        syncDeck(true);
      }

      function renderPager() {
        pagerEl.innerHTML = cards.map((card, index) => (
          `<button class="pager-dot ${index === activeIndex ? "is-active" : ""}" type="button" data-index="${index}" aria-label="查看第 ${index + 1} 张推荐"></button>`
        )).join("");
        pagerEl.querySelectorAll(".pager-dot").forEach((dot) => {
          dot.addEventListener("click", (event) => {
            event.stopPropagation();
            goTo(Number(dot.getAttribute("data-index") || 0));
          });
        });
      }

      function bindImageHeightSync() {
        trackEl.querySelectorAll("img").forEach((img) => {
          if (img.complete) {
            return;
          }
          img.addEventListener("load", () => requestAnimationFrame(setFrameHeight), { once: true });
          img.addEventListener("error", () => requestAnimationFrame(setFrameHeight), { once: true });
        });
      }

      function renderDeck() {
        trackEl.innerHTML = cards.map((card) => buildCard(card)).join("");
        renderPager();
        bindImageHeightSync();
        syncDeck(false);
      }

      function handleDragStart(event) {
        if (cards.length <= 1) {
          return;
        }
        isDragging = true;
        suppressClick = false;
        dragStartX = currentX(event);
        dragOffset = 0;
        viewportEl.classList.add("is-dragging");
        trackEl.style.transition = "none";
        if (event.pointerId !== undefined && viewportEl.setPointerCapture) {
          viewportEl.setPointerCapture(event.pointerId);
        }
      }

      function handleDragMove(event) {
        if (!isDragging) {
          return;
        }
        dragOffset = currentX(event) - dragStartX;
        if (Math.abs(dragOffset) > 10) {
          suppressClick = true;
        }
        if ((activeIndex === 0 && dragOffset > 0) || (activeIndex === cards.length - 1 && dragOffset < 0)) {
          dragOffset *= 0.35;
        }
        syncDeck(false);
      }

      function handleDragEnd(event) {
        if (!isDragging) {
          return;
        }
        const threshold = Math.min(96, viewportEl.clientWidth * 0.18);
        if (dragOffset <= -threshold && activeIndex < cards.length - 1) {
          activeIndex += 1;
        } else if (dragOffset >= threshold && activeIndex > 0) {
          activeIndex -= 1;
        }
        dragOffset = 0;
        isDragging = false;
        viewportEl.classList.remove("is-dragging");
        if (event && event.pointerId !== undefined && viewportEl.releasePointerCapture) {
          try {
            viewportEl.releasePointerCapture(event.pointerId);
          } catch (error) {
            // Ignore release failures from canceled drags.
          }
        }
        syncDeck(true);
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
          trackEl.innerHTML = "";
          counterEl.textContent = "0 / 0";
          captionEl.textContent = "";
          requestAnimationFrame(setFrameHeight);
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

      viewportEl.addEventListener("pointerdown", handleDragStart);
      viewportEl.addEventListener("pointermove", handleDragMove);
      viewportEl.addEventListener("pointerup", handleDragEnd);
      viewportEl.addEventListener("pointercancel", handleDragEnd);
      viewportEl.addEventListener("lostpointercapture", handleDragEnd);
      viewportEl.addEventListener("click", (event) => {
        if (suppressClick) {
          event.preventDefault();
          event.stopPropagation();
          suppressClick = false;
        }
      }, true);
      window.addEventListener("resize", () => syncDeck(false));

      initDeck();
    </script>
    """.replace("__PAYLOAD__", payload)
    components.html(deck_html, height=1080, scrolling=False)


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


def set_stage_mode(stage: str) -> None:
    query_params = getattr(st, "query_params", None)
    if query_params is not None:
        query_params.clear()
        if stage:
            query_params["stage"] = stage
        return

    if stage:
        st.experimental_set_query_params(stage=stage)
    else:
        st.experimental_set_query_params()


def render_intro_section() -> None:
    st.markdown(
        f"""
        <section class="stage-hero">
            <div class="stage-hero-inner">
                <div class="stage-eyebrow">第一幕 · 剧场入口</div>
                <div class="stage-title-wrap">
                    <h1 class="stage-title">
                        <span class="stage-title-top">寻找此刻与你</span>
                        <span class="stage-title-main stage-title-accent">精神同频的舞蹈作品</span>
                    </h1>
                </div>
                <div class="stage-copy-panel">
                    <div class="stage-copy">
                        <p>堆叠的学业与周而复始的事务，常常让我们忘记了肉身的温度与呼吸。</p>
                        <p><strong>花 2 分钟跟随直觉</strong>，从优雅的古典芭蕾到大写意的东方舞剧，慢慢找出此时此刻最契合你灵魂的一部作品。</p>
                    </div>
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
    if question_id == "Q1":
        answer_value = st.session_state.get(question_id)
        return isinstance(answer_value, list) and len(answer_value) > 0
    return bool(st.session_state.get(question_id))

def render_question_heading(question_text: str, question_number: int | str) -> None:
    st.markdown(
        (
            "<div class='question-heading'>"
            f"<span class='question-number'>{html.escape(str(question_number))}</span>"
            f"<div class='question-heading-text'>{html.escape(question_text)}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_standard_question(question, question_number: int | str) -> None:
    render_question_heading(question.question_text, question_number)
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


def render_q1_multiselect(question, question_number: int | str) -> None:
    render_question_heading(question.question_text, question_number)
    st.caption("这题最多可选四项；如果选“我不确定”，就不用再选其他项。")

    current_value = st.session_state.get(question.question_id)
    selected_ids = current_value[:] if isinstance(current_value, list) else []
    selected_set = set(selected_ids)
    unknown_option_id = next(
        (option.option_id for option in question.options if option.option_text.strip() == "我不确定"),
        "",
    )

    updated_selection: list[str] = []
    normal_selected_count = 0

    for option in question.options:
        option_id = option.option_id
        is_unknown = option_id == unknown_option_id
        is_checked = option_id in selected_set
        disabled = False
        if is_unknown and normal_selected_count > 0:
            disabled = True
        if not is_unknown and unknown_option_id in selected_set:
            disabled = True
        if not is_unknown and option_id not in selected_set and normal_selected_count >= 4:
            disabled = True

        checked = st.checkbox(
            option.option_text,
            value=is_checked,
            key=f"{question.question_id}__{option_id}",
            disabled=disabled,
        )

        if checked:
            if is_unknown:
                updated_selection = [option_id]
                normal_selected_count = 0
                break
            if len(updated_selection) < 4:
                updated_selection.append(option_id)
                normal_selected_count += 1

    st.session_state[question.question_id] = updated_selection


def render_quiz_transition() -> None:
    st.markdown(
        """
        <div class="mist-transition" aria-hidden="true">
            <div class="mist-copy">穿过白色迷雾，第二幕正在慢慢展开</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz_scene(question_count: int) -> None:
    st.markdown(
        f"""
        <div class="scene-back-bar">
            <a class="scene-back-link" href="?" aria-label="返回第一幕">←</a>
        </div>
        <div id="questionnaire" class="question-anchor"></div>
        <section class="question-scene">
            <div class="question-scene-shell">
                <div class="question-scene-kicker">第二幕 · 身体探索</div>
                <div class="section-title">让直觉一次走完整段路</div>
                <div class="question-scene-note">白雾散开以后，今晚的观看坐标会在这 {question_count} 道题里慢慢显影。跟着第一反应往下走就好。</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def build_selected_answers(visible_questions: list[object]) -> dict[str, str | list[str]]:
    selected_answers: dict[str, str | list[str]] = {}
    for question in visible_questions:
        question_id = question.question_id
        answer_value = st.session_state.get(question_id)
        if isinstance(answer_value, list) and answer_value:
            selected_answers[question_id] = answer_value
        elif isinstance(answer_value, str) and answer_value:
            selected_answers[question_id] = answer_value
    return selected_answers


def main() -> None:
    stage_mode = get_stage_mode()
    show_results_stage = stage_mode == "results"
    show_quiz_stage = stage_mode == "quiz"
    previous_stage_mode = st.session_state.get("_last_stage_mode", "")
    show_quiz_transition_once = show_quiz_stage and previous_stage_mode != "quiz"

    if not show_quiz_stage and not show_results_stage:
        render_intro_section()
        st.session_state["_last_stage_mode"] = stage_mode

    if stage_mode not in {"quiz", "results"}:
        st.session_state["_last_stage_mode"] = stage_mode
        return

    questions = load_quiz_questions()
    question_number_map = {
        question.question_id: index for index, question in enumerate(questions, start=1)
    }
    all_visible_complete = all(is_answer_complete(question.question_id) for question in questions)
    visible_questions = list(questions)

    if show_results_stage:
        st.markdown(
            """
            <div class="results-back-bar">
                <a class="results-back-link" href="?stage=quiz#questionnaire" aria-label="返回前两幕">←</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not all_visible_complete:
            st.info("先完成前两幕，我们再一起拉开第三幕的幕布。")
            return

        selected_answers = build_selected_answers(visible_questions)
        recommendation_payload = recommend(selected_answers, top_n=3)
        results = recommendation_payload["results"]
        profile = recommendation_payload["profile"]

        st.markdown('<div class="section-title">你的观看画像</div>', unsafe_allow_html=True)
        render_tag_chips([item["tag"] for item in profile[:8]])

        if not results:
            st.info("这一轮还没有算出结果，我们可以继续补充作品库。")
            return

        render_recommendation_deck(results)

        with st.expander("看看这次推荐是怎么得出来的"):
            st.write("问卷的大部分题目会先转成标签，再和作品库里的情绪、风格、主题、观看人格标签去做匹配。")
            st.write("Q4 的观看门槛单独计算，所以“入门 / 中级 / 高级”不会混进普通标签里。")
            for result in results:
                work = result["work"]
                st.markdown(f"**{work.title}**")
                render_tag_chips(result["matched_tags"][:6])
                for hit in result["question_hits"][:3]:
                    tags_text = " / ".join(hit["tags"])
                    st.write(f"- {hit['option_text']} -> {tags_text}")
        return

    if show_quiz_transition_once:
        render_quiz_transition()
    render_quiz_scene(len(questions))

    for question in questions:
        if question.question_id == "Q1":
            render_q1_multiselect(
                question,
                question_number=question_number_map.get(question.question_id, question.question_id),
            )
        else:
            render_standard_question(
                question,
                question_number=question_number_map.get(question.question_id, question.question_id),
            )

    if all_visible_complete:
        if st.button("🎟️ 铸造专属剧场门票", use_container_width=True):
            set_stage_mode("results")
            st.rerun()

    st.session_state["_last_stage_mode"] = stage_mode


if __name__ == "__main__":
    main()
