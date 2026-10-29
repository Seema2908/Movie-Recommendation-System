# 🎬 MovZone
### Discover Your Next Favorite.

<p align="center">
  <strong>A Smart, Content-Based Movie Recommendation System</strong>
</p>

<p align="center">
  <a href="https://movzone.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_Live_Demo-MovZone-738044?style=for-the-badge" alt="Live Demo"/>
  </a>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Machine_Learning-TF--IDF-596B3D?style=for-the-badge" alt="Machine Learning"/>
</p>

---

## 🌐 Live Demo

### 🍿 [Explore MovZone →](https://movzone.streamlit.app/)

Discover movies similar to your favorites through an interactive, cinematic movie discovery experience.

---

## ✨ About the Project

**MovZone** is a movie recommendation web application built with Python, Machine Learning, and Streamlit. It helps users discover movies based on their content, including genres, keywords, cast, director, and plot overview.

Using **TF-IDF vectorization** and **cosine similarity**, MovZone identifies movies with similar characteristics and presents recommendations in a user-friendly interface.

Whether you're looking for your next favorite movie or exploring films in a particular language, MovZone makes movie discovery simple and engaging.

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🎬 Movie Recommendations | Find movies similar to a selected title. |
| 🧠 Content-Based Filtering | Uses TF-IDF and cosine similarity to calculate movie similarity. |
| 🌐 Language Filter | Filter the movie selection list by original language. |
| 🖼️ Movie Posters | Browse available movie posters visually. |
| 📌 Watchlist | Keep track of movies you want to watch. |
| 🎨 Olive Noir UI | Dark charcoal, olive accents, and ivory text. |
| 📱 Responsive Interface | A modern layout designed for different screen sizes. |

## ⚙️ How It Works

```text
Movie Metadata
      │
      ▼
Data Cleaning & Feature Combination
      │
      ▼
Genres + Keywords + Cast + Director + Overview
      │
      ▼
       TF-IDF
      │
      ▼
Cosine Similarity Matrix
      │
      ▼
Find Similar Movies
      │
      ▼
Recommendations in Streamlit
```

1. **Data preparation:** Relevant movie attributes are combined into a single text representation.
2. **Feature extraction:** TF-IDF converts movie descriptions into numerical vectors.
3. **Similarity calculation:** Cosine similarity measures the similarity between movies.
4. **Recommendation:** The system ranks movies by similarity to the selected title.
5. **Presentation:** Streamlit displays recommendations and available poster images.

## 🛠️ Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/>
</p>

- **Language:** Python
- **Data processing:** Pandas, NumPy
- **Machine learning:** Scikit-learn
- **Recommendation technique:** TF-IDF, cosine similarity
- **Model loading:** Joblib
- **Web application:** Streamlit
- **Version control:** Git and GitHub
- **Large-file storage:** Git LFS

## 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── data/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── movie_posters.csv
│
├── artifacts/
│   ├── movies_clean.pkl
│   └── similarity.pkl
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Seema2908/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### 2. Create and activate a virtual environment (optional)

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Git LFS files

Ensure Git LFS is installed, then run:

```bash
git lfs install
git lfs pull
```

This downloads the large similarity artifact tracked through Git LFS.

### 5. Launch MovZone

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to explore the application.

## 📊 Dataset

This project uses the **TMDB 5000 Movies Dataset**, containing movie metadata used to build the content-based recommendation system.

A separate `movie_posters.csv` file maps movies to poster URLs. Poster availability depends on the image URLs remaining accessible.

## 🎓 What I Learned

- Applying text vectorization techniques to movie metadata.
- Using cosine similarity for content-based recommendations.
- Preparing and processing structured datasets with Python.
- Integrating a machine learning model into a Streamlit web application.
- Managing model artifacts with Joblib and Git LFS.
- Deploying an interactive application using Streamlit Community Cloud.

## 🔮 Future Enhancements

- Improve movie search and discovery.
- Expand poster coverage and image-loading reliability.
- Introduce hybrid recommendation techniques.
- Explore user ratings and personalized recommendations.

## 👩‍💻 Author

**Seema Timmanagoudar**

[![GitHub](https://img.shields.io/badge/GitHub-Seema2908-181717?style=for-the-badge&logo=github)](https://github.com/Seema2908)

---

<p align="center">
  Made with ❤️ and Python
  <br/>
  <strong>MovZone — Discover Your Next Favorite.</strong>
  <br/><br/>
  <a href="https://movzone.streamlit.app/">🚀 Launch MovZone</a>
</p>
