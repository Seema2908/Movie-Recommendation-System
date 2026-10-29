import pandas as pd
from pathlib import Path

# Public dataset with TMDB movie IDs and poster image URLs.
DATASET_NAME = "ROSCOSMOS/Movie-Poster-WebURL-Dataset-1874-2025"

DATA_DIR = Path("data")
MOVIES_FILE = DATA_DIR / "tmdb_5000_movies.csv"
OUTPUT_FILE = DATA_DIR / "movie_posters.csv"


def main():
    if not MOVIES_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find {MOVIES_FILE}. Run this script from your project root."
        )

    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency. Install it with:\n"
            "pip install datasets pandas pyarrow"
        ) from exc

    movies = pd.read_csv(MOVIES_FILE, usecols=["id", "title"])
    movies["id"] = pd.to_numeric(movies["id"], errors="coerce")
    movies = movies.dropna(subset=["id"]).copy()
    movies["id"] = movies["id"].astype("int64")

    target_ids = set(movies["id"].tolist())
    matched_rows = []

    print("Loading public poster metadata in streaming mode...")
    print("This may take a while because the source contains over 800,000 records.")

    # Stream the source instead of downloading the entire dataset into memory.
    dataset = load_dataset(DATASET_NAME, split="train", streaming=True)

    for row in dataset:
        raw_id = row.get("tmdb_id")
        url = row.get("web_url")

        try:
            movie_id = int(raw_id)
        except (TypeError, ValueError):
            continue

        if movie_id in target_ids and isinstance(url, str) and url.startswith("http"):
            matched_rows.append({
                "movie_id": movie_id,
                "poster_url": url.strip(),
            })

    # Prefer one URL per movie ID. Keep the first valid URL found.
    poster_data = pd.DataFrame(matched_rows, columns=["movie_id", "poster_url"])
    if not poster_data.empty:
        poster_data = poster_data.drop_duplicates(subset=["movie_id"], keep="first")

    result = movies.rename(columns={"id": "movie_id"})
    result = result.merge(poster_data, on="movie_id", how="left")
    result["poster_url"] = result["poster_url"].fillna("")
    result["poster_path"] = result["poster_url"].apply(
        lambda url: url.split("/t/p/w500", 1)[-1]
        if "/t/p/w500" in url else ""
    )
    result = result[["movie_id", "title", "poster_path", "poster_url"]]
    result.to_csv(OUTPUT_FILE, index=False)

    total = len(result)
    matched = int(result["poster_url"].ne("").sum())
    print(f"\nCreated: {OUTPUT_FILE}")
    print(f"Movies in your dataset: {total}")
    print(f"Movies matched to a poster URL: {matched}")
    print(f"Movies without a matched URL: {total - matched}")
    print("\nSample matched rows:")
    print(result[result["poster_url"].ne("")].head(10).to_string(index=False))
    print(
        "\nNote: matching by TMDB ID is safer than matching by title. "
        "Still, open a few sample URLs to confirm they load before using them in Streamlit."
    )


if __name__ == "__main__":
    main()
