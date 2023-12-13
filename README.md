# Generating Personalized Music Recommendations and Historical Music Insights

[![Python Package using Conda](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/actions/workflows/python-package-conda.yml)

**Contributors: Juntong Wu, Chesie Yu, Denkie Yan**

<br>

## 🎶 Background

In the dynamic and diverse world of music, our project aims to offer a personalized and enriching experience that caters to the tastes of individual users.  Despite currently in its prototype phase and utilizing synthesized user data, the goal of this project goes beyond music recommendation. It preludes a fully-fledged application that resonates with the unique music journeys of real-world users.  

The scope of this project emcompasses **two major aspects**：

- **Inform historical music insights through interactive dashboard**

- **Provide personalized recommendations based on user preferences and social networks**  

<br>

## Organization of the Project 

The project has the following structure:
```
Spotify-Music-Recommendation-System (main)
|   
|   # App-related directories and files
|--- app
|    |   # All the graphics, stylesheets, and scripts used in the project
|    |--- assets
|    |
|    |   # All datasets used; in .csv format
|    |--- data
|    |
|    |   # Body of displayed page
|    |--- pages
|    |    |   about.py
|    |    |   explore.py
|    |    |   home.py
|    |    |   login.py
|    |    |   recom.py
|    |
|    |   # All the functionality tests for this project
|    |--- tests
|    |    |   _init_.py
|    |    |   test_database.py
|    |    |   test_login.py
|    |    |   test_recom.py
|    |    |   test_visual.py
|    |
|    |   # All the functionality and callbacks for pages
|    |--- utils
|    |    |--- pages
|    |    |    |--- explore
|    |    |    |    |   callbacks.py
|    |    |    |    |   visuals.py
|    |    |    |--- login
|    |    |    |    |   callbacks.py
|    |    |    |    |   usermatch.py
|    |    |    |--- recom
|    |    |    |    |   callbacks.py
|    |    |    |    |   model.py
|    |    |    |    |   playlist.py
|    |    |    |    |   profile.py
|    |    |    database.py
|    |    |    spotipy_db.sqlite
|    |    |    page_template.py
|    |
|    |   # Main file; run this to start the app
|    |--- app.py
|    |
|    |   # Script to execute specific functions
|    |--- play.py
|    |
|    |   # SQLite database file
|    |--- spotipy_db.sqlite
|
|   # Design documents
|--- doc
|    |   component-spec.md
|    |   functional-spec.md
|    |   technology-review.pdf
|    |   project-presentation.pdf
|
|   # Images used in docs and readme
|--- image
|
|   # Code for data preprocessing
|--- preprocess
|
|   # Environmental file
|--- environment.yml
|
|   # README file
|--- README.md
```

## Data

This [Spotify Dataset](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset/code) contains 170,653 songs released from 1921 to 2020 from Spotify. To adapt to our research objectives, we have curated the dataset by renaming certain fields and enriching it with additional identification and genre details. [Click here for more infomation](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/doc/functional-spec.md). 


The original Spotify datasets covered a range of features, including songs, artists, genres, years, along with various music attributes. Our project expanded it by creating dummy datasets encompassing Users, User-Songs, and User-Friends. These datasets are avaliable as CSV files in the [data](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/tree/main/app/data) folder. To enhance the user experience with visually appealing elements, each user has been assigned a unique, anime-style profile photo generated through the [Diffusion model](https://huggingface.co/docs/diffusers/index).

<br>

## Install and Execute Recommondation System User Interface
- Installation of package dependency: 

    ```conda env create -f environment.yml```

- In command line, execute ```python app.py``` to start the application. Navigate through http://127.0.0.1:5000/ to access the web page.

<br>

## User Interface Example

**Home Page of the User Interface**
![Home Page](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/image/01-landing.png)

**Charateristic of a Song**
![Characteristic of a Song](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/image/03-explore-radar.png)

**Music Trend**
![Trend of Music](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/image/03-explore-trend.png)

**User Login Interface**
![User Login](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/image/04-login.png)

**PlayList Recommendation**
![Playlist Recommendation](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/image/05-recom.png)

<br>

## Contacts
Juntong Wu -- juntongw@uw.edu

Chesie Yu -- cyu909@uw.edu

Denkie Yan -- denkie@uw.edu

<br>