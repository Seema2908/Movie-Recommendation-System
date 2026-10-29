from pathlib import Path
import html
import joblib

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------
# CineMatch — Olive Noir
# UI redesign only. The recommendation model/artifacts stay
# unchanged: movies_clean.pkl + similarity.pkl.
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="CineMatch | Olive Noir",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------- Theme -------------------------
st.markdown(
    """
    <style>
    :root {
        --olive-bg: #171A12;
        --olive-panel: #202419;
        --olive-card: #25291D;
        --olive-border: #3B412C;
        --olive-accent: #A6B85B;
        --olive-accent-dark: #899B43;
        --olive-ivory: #F4F0E5;
        --olive-muted: #B9B9A7;
        --olive-soft: #D9D8C9;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--olive-bg);
        color: var(--olive-ivory);
    }
    [data-testid="stHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        background: transparent !important;
    }
    [data-testid="stToolbar"] {
        right: 1rem;
    }
    [data-testid="stAppViewContainer"] > .main {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(166,184,91,.12), transparent 34%),
            radial-gradient(ellipse at 100% 24%, rgba(137,155,67,.07), transparent 30%),
            var(--olive-bg);
    }
    .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 3.5rem;
    }
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
        color: var(--olive-ivory);
    }
    .muted { color: var(--olive-muted) !important; }
    .eyebrow {
        color: var(--olive-accent);
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: 2.3px;
        text-transform: uppercase;
    }
    .brand-row {
        display: flex;
        align-items: center;
        gap: 13px;
        margin-top: .8rem;
        margin-bottom: 1.35rem;
        animation: riseIn .6s ease both;
    }
    .brand-icon {
        width: 52px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--olive-accent);
        color: var(--olive-bg);
        border-radius: 15px;
        font-size: 27px;
        box-shadow: 0 8px 24px rgba(166,184,91,.15);
    }
    .brand-name {
        color: var(--olive-ivory);
        font-size: clamp(2rem, 3.2vw, 2.7rem);
        line-height: 1.05;
        font-weight: 950;
        letter-spacing: 2px;
    }
    .brand-tagline {
        color: var(--olive-accent);
        font-size: .75rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 5px;
    }
    .hero {
        padding: .9rem 0 .55rem;
        animation: riseIn .7s ease both;
    }
    .hero-title {
        font-size: clamp(2.1rem, 4.3vw, 3.8rem);
        line-height: 1.04;
        letter-spacing: -1.4px;
        font-weight: 900;
        color: var(--olive-ivory);
        margin: 9px 0 12px;
        max-width: 780px;
    }
    .hero-title span { color: var(--olive-accent); }
    .hero-copy {
        color: var(--olive-muted);
        font-size: 1rem;
        line-height: 1.6;
        max-width: 660px;
        margin-bottom: .65rem;
    }
    .search-label {
        color: var(--olive-accent);
        font-size: .78rem;
        font-weight: 850;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 1.15rem 0 .7rem;
    }
    div[data-baseweb="select"] {
        font-size: 1.08rem;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--olive-border) !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, rgba(37,41,29,.78), rgba(32,36,25,.68));
        padding: 1.5rem 1.4rem 1rem !important;
        box-shadow: 0 18px 45px rgba(0,0,0,.12);
    }
    /* Make the actual select control match the primary button height. */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #171A12 !important;
        border: 1px solid #50583A !important;
        border-radius: 12px !important;
        min-height: 64px !important;
        height: 64px !important;
        max-height: 64px !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        font-size: 1.08rem !important;
        box-sizing: border-box !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"] {
        min-height: 62px !important;
        height: 62px !important;
        max-height: 62px !important;
        align-items: center !important;
        box-sizing: border-box !important;
    }
    div[data-baseweb="select"] * { color: var(--olive-ivory) !important; }
    div[data-baseweb="select"] > div:hover { border-color: var(--olive-accent) !important; }
    .stButton > button[kind="primary"],
    [data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #A6B85B, #899B43);
        color: #171A12;
        border: 1px solid #A6B85B;
        border-radius: 12px;
        min-height: 56px !important;
        height: 56px !important;
        max-height: 56px !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        line-height: 1.2 !important;
        box-sizing: border-box !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        letter-spacing: .2px;
        transition: transform .22s ease, box-shadow .22s ease, filter .22s ease;
        box-shadow: 0 7px 20px rgba(166,184,91,.13);
    }
    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.08);
        transform: translateY(-2px);
        box-shadow: 0 11px 27px rgba(166,184,91,.22);
    }
    .stButton > button:not([kind="primary"]) {
        background: #25291D;
        color: var(--olive-ivory);
        border: 1px solid var(--olive-border);
        border-radius: 10px;
        transition: all .2s ease;
    }
    .stButton > button:not([kind="primary"]):hover {
        border-color: var(--olive-accent);
        color: var(--olive-accent);
        transform: translateY(-1px);
    }
    .section-heading {
        margin: 2.5rem 0 1.2rem;
        animation: riseIn .5s ease both;
    }
    .section-intro {
        color: var(--olive-muted);
        font-size: clamp(1rem, 1.7vw, 1.25rem);
        line-height: 1.25;
        font-weight: 650;
        margin: 10px 0 3px;
    }
    .section-title {
        color: var(--olive-ivory);
        font-size: clamp(1.6rem, 3.5vw, 2.5rem);
        line-height: 1.15;
        font-weight: 850;
        letter-spacing: -.8px;
        margin: 0 0 9px;
        overflow-wrap: anywhere;
    }
    .selected-movie-title { color: var(--olive-accent); }
    .section-copy { color: var(--olive-muted); line-height: 1.65; }
    .movie-card {
        overflow: hidden;
        height: 100%;
        margin-bottom: 10px;
        background: var(--olive-panel);
        border: 1px solid var(--olive-border);
        border-radius: 15px;
        box-shadow: 0 7px 20px rgba(0,0,0,.13);
        transition: transform .28s ease, border-color .28s ease, box-shadow .28s ease;
        animation: cardIn .55s ease both;
    }
    .movie-card:hover {
        transform: translateY(-7px) rotate(-.25deg);
        border-color: var(--olive-accent);
        box-shadow: 0 15px 32px rgba(0,0,0,.3);
    }
    .poster-wrap {
        width: 100%;
        overflow: hidden;
        background: #303522;
    }
    .poster {
        display: block;
        width: 100%;
        aspect-ratio: 2 / 3;
        object-fit: cover;
        transition: transform .4s ease, filter .4s ease;
    }
    .movie-card:hover .poster { transform: scale(1.045); filter: saturate(1.06); }
    .poster-fallback {
        display: flex;
        flex-direction: column;
        gap: 9px;
        justify-content: center;
        align-items: center;
        text-align: center;
        aspect-ratio: 2 / 3;
        padding: 12px;
        color: var(--olive-muted);
        background: linear-gradient(145deg, #303522, #202419);
    }
    .poster-fallback .clapper { font-size: 2.2rem; }
    .card-body { padding: 13px 13px 15px; }
    .movie-number {
        color: var(--olive-accent);
        font-size: .67rem;
        letter-spacing: 1.5px;
        font-weight: 850;
        margin-bottom: 8px;
    }
    .movie-title {
        color: var(--olive-ivory);
        font-size: .93rem;
        line-height: 1.4;
        font-weight: 750;
        overflow-wrap: anywhere;
        min-height: 2.6em;
    }
    .watchlist-pill {
        display: inline-block;
        margin-top: 9px;
        padding: 4px 8px;
        border-radius: 20px;
        background: rgba(166,184,91,.12);
        color: var(--olive-accent);
        font-size: .68rem;
        font-weight: 800;
    }
    .footer {
        margin-top: 3rem;
        border-top: 1px solid var(--olive-border);
        padding-top: 1.2rem;
        color: var(--olive-muted);
        font-size: .8rem;
    }
    @keyframes riseIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes cardIn {
        from { opacity: 0; transform: translateY(12px) scale(.985); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    @media (max-width: 1050px) {
        .block-container { padding-left: 1.4rem; padding-right: 1.4rem; }
    }
    @media (max-width: 640px) {
        .block-container { padding: 1rem .85rem 2rem; }
        [data-testid="stVerticalBlockBorderWrapper"] { padding: 1rem .8rem .8rem !important; }
        .brand-row { margin-bottom: 1.5rem; }
        .hero { padding-top: .5rem; }
        .hero-title { letter-spacing: -.8px; font-size: clamp(2rem, 9vw, 3rem); }
        .hero-copy { font-size: .94rem; line-height: 1.55; margin-bottom: .4rem; }
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div { min-height: 64px !important; height: 64px !important; }
        [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"] { min-height: 62px !important; height: 62px !important; }
        .stButton > button[kind="primary"],
        [data-testid="stButton"] > button[kind="primary"] { min-height: 56px !important; height: 56px !important; max-height: 56px !important; }
        .stButton > button[kind="primary"],
        [data-testid="stButton"] > button[kind="primary"] { font-size: 1.12rem !important; }
        .search-label { margin-top: 1rem; }
        .movie-title { font-size: .85rem; }
        .card-body { padding: 10px; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation: none !important; transition: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------- Load artifacts -------------------
@st.cache_resource
def load_model_artifacts():
    movies_path = ARTIFACTS_DIR / "movies_clean.pkl"
    similarity_path = ARTIFACTS_DIR / "similarity.pkl"

    if not movies_path.exists() or not similarity_path.exists():
        missing = []
        if not movies_path.exists():
            missing.append(str(movies_path))
        if not similarity_path.exists():
            missing.append(str(similarity_path))
        raise FileNotFoundError(
            "Missing recommendation artifact(s): " + ", ".join(missing)
        )

    # joblib.load supports joblib-compressed artifacts and ordinary
    # pickle-compatible artifacts. This avoids assuming both files were
    # written specifically with pickle.dump().
    movies_frame = joblib.load(movies_path)
    similarity_matrix = joblib.load(similarity_path)

    return movies_frame, similarity_matrix


try:
    movies, similarity = load_model_artifacts()
except Exception as error:
    st.error(f"Could not load the existing recommendation model: {error}")
    st.info(
        "Check that artifacts/movies_clean.pkl and "
        "artifacts/similarity.pkl exist next to app.py."
    )
    st.stop()


# ------------------------ Poster data --------------------
@st.cache_data
def load_poster_lookup():
    poster_file = DATA_DIR / "movie_posters.csv"
    if not poster_file.exists():
        return {}

    poster_frame = pd.read_csv(poster_file)
    required_columns = {"title", "poster_url"}
    if not required_columns.issubset(poster_frame.columns):
        return {}

    poster_frame = poster_frame.dropna(subset=["title", "poster_url"]).copy()
    poster_frame["title"] = poster_frame["title"].astype(str).str.strip()
    poster_frame["poster_url"] = poster_frame["poster_url"].astype(str).str.strip()
    poster_frame = poster_frame[
        poster_frame["poster_url"].str.startswith(("https://", "http://"))
    ]
    poster_frame = poster_frame.drop_duplicates(subset=["title"], keep="first")
    return dict(zip(poster_frame["title"], poster_frame["poster_url"]))


poster_lookup = load_poster_lookup()


# ---------------- Original-language metadata ----------------
LANGUAGE_NAMES = {
    "ar": "Arabic", "bn": "Bengali", "cn": "Chinese", "cs": "Czech",
    "da": "Danish", "de": "German", "el": "Greek", "en": "English",
    "es": "Spanish", "fa": "Persian", "fi": "Finnish", "fr": "French",
    "he": "Hebrew", "hi": "Hindi", "hu": "Hungarian", "id": "Indonesian",
    "it": "Italian", "ja": "Japanese", "ka": "Georgian", "kn": "Kannada",
    "ko": "Korean", "ml": "Malayalam", "mr": "Marathi", "ms": "Malay",
    "nl": "Dutch", "no": "Norwegian", "pl": "Polish", "pt": "Portuguese",
    "ro": "Romanian", "ru": "Russian", "sv": "Swedish", "ta": "Tamil",
    "te": "Telugu", "th": "Thai", "tr": "Turkish", "uk": "Ukrainian",
    "ur": "Urdu", "vi": "Vietnamese", "xx": "Unknown",
}


@st.cache_data
def load_original_language_lookup():
    # Prefer the original TMDB dataset because the cleaned recommendation
    # artifact may only contain title/tags. This metadata does not alter the model.
    source_csv = DATA_DIR / "tmdb_5000_movies.csv"
    source_frame = None

    if source_csv.exists():
        try:
            source_frame = pd.read_csv(
                source_csv,
                usecols=lambda column: column in {"title", "original_language"},
            )
        except Exception:
            source_frame = None

    if source_frame is None and "original_language" in movies.columns:
        source_frame = movies[["title", "original_language"]].copy()

    if source_frame is None or not {"title", "original_language"}.issubset(source_frame.columns):
        return {}

    source_frame = source_frame.dropna(subset=["title", "original_language"]).copy()
    source_frame["title"] = source_frame["title"].astype(str).str.strip()
    source_frame["original_language"] = (
        source_frame["original_language"].astype(str).str.strip().str.lower()
    )
    source_frame = source_frame.drop_duplicates(subset=["title"], keep="first")
    return dict(zip(source_frame["title"], source_frame["original_language"]))


original_language_lookup = load_original_language_lookup()


# ---------------- Existing recommendation logic -----------
# This function uses the saved similarity matrix as before.
# Do not retrain or modify the TF-IDF/cosine-similarity model.
def recommend_movies(movie_title, number_of_recommendations=5):
    title_matches = movies.index[movies["title"].astype(str) == movie_title].tolist()
    if not title_matches:
        return []

    movie_index = title_matches[0]
    similarity_scores = list(enumerate(similarity[movie_index]))
    similarity_scores = sorted(
        similarity_scores, key=lambda item: item[1], reverse=True
    )

    recommendations = []
    for index, score in similarity_scores[1:]:
        recommended_title = str(movies.iloc[index]["title"])
        if recommended_title != movie_title and recommended_title not in recommendations:
            recommendations.append(recommended_title)
        if len(recommendations) >= number_of_recommendations:
            break

    return recommendations


# ---------------------- Hero / search --------------------
st.markdown(
    """
    <div class="brand-row">
        <div class="brand-icon">🎬</div>
        <div>
            <div class="brand-name">CINEMATCH</div>
            <div class="brand-tagline">YOUR PERSONAL FILM DISCOVERY ENGINE</div>
        </div>
    </div>

    <div class="hero">
        <div class="eyebrow">THE NEXT GREAT FILM IS CLOSER THAN YOU THINK</div>
        <div class="hero-title">
            Find your next<br><span>obsession.</span>
        </div>
        <div class="hero-copy">
            One film you love. Five new worlds to explore.
            Discover movies with a similar vibe, powered by content-based recommendations.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

all_movie_titles = movies["title"].dropna().astype(str).unique().tolist()
titles_by_lower = {title.casefold(): title for title in all_movie_titles}

# Put familiar/popular titles first when they exist in this dataset.
featured_movie_order = [
    "The Dark Knight",
    "Inception",
    "Interstellar",
    "Avatar",
    "The Avengers",
    "Titanic",
    "The Lord of the Rings: The Return of the King",
    "Iron Man",
    "The Matrix",
    "Fight Club",
    "Forrest Gump",
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight Rises",
    "Pulp Fiction",
    "The Wolf of Wall Street",
    "Guardians of the Galaxy",
    "The Martian",
    "Harry Potter and the Philosopher's Stone",
    "Deadpool",
    "Jurassic Park",
    "Gladiator",
    "The Hunger Games",
    "Toy Story",
    "Finding Nemo",
]
featured_titles = [
    titles_by_lower[title.casefold()]
    for title in featured_movie_order
    if title.casefold() in titles_by_lower
]
featured_lower = {title.casefold() for title in featured_titles}
remaining_titles = sorted(
    [title for title in all_movie_titles if title.casefold() not in featured_lower],
    key=str.casefold,
)
ordered_movie_titles = featured_titles + remaining_titles

if "cine_recommendations" not in st.session_state:
    st.session_state.cine_recommendations = []
if "cine_selected_movie" not in st.session_state:
    st.session_state.cine_selected_movie = None
if "cine_watchlist" not in st.session_state:
    st.session_state.cine_watchlist = []

# Use readable names in the dropdown while retaining TMDB's language codes internally.
language_codes = sorted({
    original_language_lookup[title]
    for title in all_movie_titles
    if title in original_language_lookup and original_language_lookup[title]
})
language_options = ["All languages"] + [
    f"{LANGUAGE_NAMES.get(code, code.upper())} ({code.upper()})"
    for code in language_codes
]
language_value_to_code = {
    f"{LANGUAGE_NAMES.get(code, code.upper())} ({code.upper()})": code
    for code in language_codes
}

with st.container(border=True):
    language_col, search_col, button_col = st.columns(
        [1.45, 3.7, 1.5],
        vertical_alignment="bottom",
    )

    with language_col:
        selected_language_label = st.selectbox(
            "Original language",
            options=language_options,
            index=0,
            key="cine_language_filter",
            help="Filter the movie list by the film's original language.",
        )

    selected_language_code = language_value_to_code.get(selected_language_label)

    if selected_language_code:
        filtered_movie_titles = [
            title for title in ordered_movie_titles
            if original_language_lookup.get(title) == selected_language_code
        ]
    else:
        filtered_movie_titles = ordered_movie_titles

    with search_col:
        selected_movie = st.selectbox(
            "Search or select a movie",
            options=filtered_movie_titles,
            index=None,
            placeholder="Start typing a movie title...",
            label_visibility="visible",
            key=f"cine_movie_selector_{selected_language_code or 'all'}",
        )

    with button_col:
        recommend_clicked = st.button(
            "✦ Find My Movies",
            type="primary",
            use_container_width=True,
        )

    if not original_language_lookup:
        st.caption(
            "Language filtering needs data/tmdb_5000_movies.csv with "
            "title and original_language columns. The rest of CineMatch still works."
        )
    elif selected_language_code and not filtered_movie_titles:
        st.caption("No movies were found for this language in the current dataset.")

if recommend_clicked:
    if not selected_movie:
        st.warning("Choose a movie first, then discover your next favourites.")
    else:
        with st.spinner("Finding movies with a similar vibe..."):
            st.session_state.cine_recommendations = recommend_movies(selected_movie, 5)
            st.session_state.cine_selected_movie = selected_movie


# -------------------- Recommendation cards ----------------
recommendations = st.session_state.cine_recommendations
current_movie = st.session_state.cine_selected_movie

if current_movie and recommendations:
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="section-intro">Because you loved</div>
            <div class="section-title selected-movie-title">{html.escape(str(current_movie))}.</div>
            <div class="section-copy">
                Five picks for your next movie night.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Native Streamlit columns keep the cards usable and interactive.
    card_columns = st.columns(5, gap="medium")
    for position, (column, title) in enumerate(zip(card_columns, recommendations), start=1):
        safe_title = html.escape(str(title))
        poster_url = poster_lookup.get(title)

        with column:
            if poster_url:
                poster_html = (
                    f'<div class="poster-wrap">'
                    f'<img class="poster" src="{html.escape(poster_url, quote=True)}" '
                    f'alt="{safe_title}" loading="lazy"></div>'
                )
            else:
                poster_html = (
                    '<div class="poster-fallback">'
                    '<div class="clapper">🎞️</div>'
                    '<div>Poster coming soon</div>'
                    '</div>'
                )

            is_saved = title in st.session_state.cine_watchlist
            saved_pill = '<span class="watchlist-pill">✓ IN WATCHLIST</span>' if is_saved else ""

            # Keep the HTML card on one line so Markdown does not
            # interpret indented closing tags as a code block.
            card_html = (
                '<div class="movie-card">'
                + poster_html
                + '<div class="card-body">'
                + f'<div class="movie-number">MOVIE {position:02d}</div>'
                + f'<div class="movie-title">{safe_title}</div>'
                + saved_pill
                + '</div></div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

            button_label = "✓ Saved" if is_saved else "＋ Watchlist"
            if st.button(
                button_label,
                key=f"watchlist_{position}_{title}",
                use_container_width=True,
                disabled=is_saved,
            ):
                st.session_state.cine_watchlist.append(title)
                st.rerun()

elif current_movie and not recommendations:
    st.warning("No recommendations were found for this title. Try another movie.")

# Automatically scroll to the recommendation heading after clicking Find My Movies.
if recommend_clicked and current_movie and recommendations:
    components.html(
        """
        <script>
        function scrollToCineMatchRecommendations() {
            const doc = window.parent.document;
            const nodes = Array.from(doc.querySelectorAll('[data-testid="stMarkdownContainer"]'));
            const target = nodes.find(node =>
                node.innerText && node.innerText.includes('Because you loved')
            );
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        setTimeout(scrollToCineMatchRecommendations, 350);
        setTimeout(scrollToCineMatchRecommendations, 900);
        </script>
        """,
        height=0,
    )

# ----------------------- Watchlist ------------------------
if st.session_state.cine_watchlist:
    st.markdown(
        """
        <div class="section-heading">
            <div class="eyebrow">YOUR SAVED PICKS</div>
            <div class="section-title">Movie-night shortlist.</div>
            <div class="section-copy">Your watchlist stays available while this app session is open.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    watchlist_columns = st.columns([4, 1])
    with watchlist_columns[0]:
        for saved_title in st.session_state.cine_watchlist:
            st.markdown(
                f'<div style="padding:10px 0;border-bottom:1px solid #3B412C;color:#F4F0E5;">'
                f'🎬 &nbsp; {html.escape(str(saved_title))}</div>',
                unsafe_allow_html=True,
            )
    with watchlist_columns[1]:
        if st.button("Clear watchlist", use_container_width=True):
            st.session_state.cine_watchlist = []
            st.rerun()

st.markdown(
    """
    <div class="footer">
        <span style="color:#A6B85B;font-weight:800;letter-spacing:1.5px;">CINEMATCH</span>
        &nbsp; · &nbsp; Made for curious movie lovers
     </div>
    """,
    unsafe_allow_html=True,
)
