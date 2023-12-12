# Generating Personalized Music Recommendations and Historical Music Insights

Team Member: Juntong Wu, Denkie Yan, Chesie Yu

<br>

## 🎶 Background

In the dynamic and diverse world of music streaming and discovery, our project aims to offer a **unique personalized and enriching experience that caters to the tastes of individual users**.  At the core of this objective is the desire to not only provide music recommendations but to do so in a way that is insightful and resonates with each user’s unique music journey.  

The scope of this project emcompasses **three major aspects**：

**Inform Historical Music Insights**: uncovering the story of music behind the data. Leveraging the Spotify music dataset, we will discover and illustrate interesting patterns and trends through interactive visualization dashboards with customizable controls. 

**Provide Personalized Recommendations**: based on user behavioral preferences and potentially social networks, improving listening experience through understanding then predicting the unique tastes of each user.  

**Create engaging interactive user-friendly interface**: users can explore the rich history of contemporary music and discover new personal favorites through this *prototype app*. This tool is designed to create a music discovery experience that is not only entertaining but also informative and personalized.  

<br>

## Organization of the Project 

The project has the following structure:
```
Spotify-Music-Recommendation-System (master)
|      # All the graphics, stylesheets, and scripts used in the project
|----- assets
|     |
|      # All spotify datasets   
|----- data
|     |  
|      # Design Documents
|----- doc
|     |      component-spec.md
|     |      functional-spec.md
|     |      technology-review.pdf
|     |      technology-review.pptx
|     | 
|      # All images used in this project
|----- image
|     |
|      # Body of displayed page 
|----- pages
|     |      about.py
|     |      explore.py
|     |      home.py
|     |      login.py
|     |      recom.py
|     |
|      # Preprocess Data 
|----- preprocess
|     |
|      # All the functionality tests for this project
|----- tests
|     |      _init_.py
|     |      test_database.py
|     |      test_login.py
|     |      test_recom.py
|     |      test_visual.py
|     |
|      # All the functionality and callcacks for pages
|----- utils
|     |----- pages
|     |      |----- explore
|     |      |      |      callbacks.py
|     |      |      |      visuals.py
|     |      |----- login
|     |      |      |      callbacks.py
|     |      |      |      usermatch.py
|     |      |----- recom
|     |      |      |      callbacks.py
|     |      |      |      model.py
|     |      |      |      playlist.py
|     |      |      |      profile.py
|     |----- database.py
|     |----- music_reco_sys_db.sqlit
|     |----- page_template.py
|     |
|      # Environmental file
|----- environment.yml
|     |
|      # Main file; run this to start the app
|----- app.py
|     |
|      # README file
|     README.md

```

## Data

This [**Spotify Dataset**](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset/code) contains 170,653 songs released from 1921 to 2020 from Spotify. For the purpose of research, we have modified the original data  by renaming fields and adding identification and genre information. [Click here for more infomation](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/blob/main/doc/functional-spec.md). 


Original datasets include data for artists, genres, years, and Spotify data. The newly added dummy datasets include data for User-Songs, User-Friends, and User-Friends. All project data is stored as CSV files in the [data](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/tree/main/data) file.

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

Denkie Yan -- denkie@uw.edu

Chesie Yu -- cyu909@uw.edu

<br>