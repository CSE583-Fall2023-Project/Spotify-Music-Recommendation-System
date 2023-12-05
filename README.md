# Generating Personalized Music Recommendations and Historical Music Insights

Team Member: Juntong Wu, Denkie Yan, Chesie Yu
[Github Link](https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System/tree/main)
<br> 

## Background

**Music is dynamic** – the history of music is the history of human culture; each era presents its own story through its distinct styles and genres.  **Music is diverse** – each genre is characterized by its unique blends of composition elements, varying in rhythms, scales, harmonies, and structures.  **Music tells us about ourselves.**  Our music taste is shaped by our surroundings and exposures, by a mix of cultural influences, popular trends, and personal experiences.    

In the dynamic and diverse world of music streaming and discovery, our project aims to offer a **unique personalized and enriching experience that caters to the tastes of individual users**.  At the core of this objective is the desire to not only provide music recommendations but to do so in a way that is insightful and resonates with each user’s unique music journey.  

The scope of this project emcompasses three major aspects.  First, we hope to **inform the historical music insights**, uncovering the story of music behind the data.  Leveraging the Spotify music dataset, we will discover and illustrate interesting patterns and trends through interactive visualization dashboards with customizable controls.   Second, we want to **provide personalized recommendations** based on user behavioral preferences and potentially social networks, improving listening experience through understanding then predicting the unique tastes of each user.  Ultimately, we aim to create a platform where users can explore the rich history of contemporary music and discover new personal favorites, all within **an engaging interactive user-friendly interface**.  This tool is designed to create a music discovery experience that is not only entertaining but also informative and personalized.  

<br>

## Organization of the Project 

The project has the following structure:
```
Spotify-Music-Recommendation-System (master)
|     .git
|     .github
|     .idea
|     .gitignore
|     README.md
|     app.py
|     environment.yml
|     music_reco_sys_db.sqlite
|
|----- assets
|     |      Design Specification.md
|     |      
|----- data
|     |      data_by_artist.csv
|     |      data_by_genres.csv
|     |      data_by_years.csv
|     |      data_w_genres.csv
|     |      spotify_data.csv
|     |      user_friends.csv
|     |      user_songs.csv
|     |      users.csv
|     |  
|----- doc
|     |      component-spec.md
|     |      functional-spec.md
|     |      technology-review.pdf
|     |      technology-review.pptx
|     | 
|----- image
|     |      banner-2048.png
|     |      project profie.png
|     | 
|----- pages
|     |      about.py
|     |      explore.py
|     |      home.py
|     |      login.py
|     |      recom.py
|     |
|----- preprocess
|     |      00-explore.ipynb
|     |      01-eda.ipynb
|     |      02-viz.ipynb
|     |      03-reco.ipynb
|     |      04-dashboard.ipynb
|     |      05-app.ipynb
|     |      Collaborative Filtering.ipynb
|     |      dummy_data.ipynb
|     |      generate_dummy-user-pics.ipynb
|     |      spotify-data-preprcessing.ipynb
|     |      knn_recommender.py
|     |
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
|     |----- music_reco_sys_db.sqlite
|     |----- page_template.py
```

## Data

Spotify Data Set
   

<br>

## Execution of Recommondation System

Upload images and explain steps   


<br>


## Deliverables

Interactive user interface that presents historical music insights and provides personalized music recommendations         

- **Historical Music Insights:** EDA + Visualization (music evolution, popular songs/genres, genre characteristics, etc.) in an HTML file      
- **Personalized Music Recommendations:** Predict the top 10 songs and artists based on listening history and user preferences   
- **User Music Profile:** Top songs/artists in users’ and friends’ history, favorite genres, audio features, and word cloud with favorite song names   

## Acknowledgements

Thank you!

<br>

## Contacts

Questions? Comments? 

<br>