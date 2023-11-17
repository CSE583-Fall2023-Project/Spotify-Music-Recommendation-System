# Generating Personalized Music Recommendations and Historical Music Insights

Juntong Wu, Denkie Yan, Chesie Yu

<br>

## 🎶 Background  

**Music is dynamic** – the history of music is the history of human culture; each era presents its own story through its distinct styles and genres.  **Music is diverse** – each genre is characterized by its unique blends of composition elements, varying in rhythms, scales, harmonies, and structures.  **Music tells us about ourselves.**  Our music taste is shaped by our surroundings and exposures, by a mix of cultural influences, popular trends, and personal experiences.    

In the dynamic and diverse world of music streaming and discovery, our project aims to offer a **unique personalized and enriching experience that caters to the tastes of individual users**.  At the core of this objective is the desire to not only provide music recommendations but to do so in a way that is insightful and resonates with each user’s unique music journey.  

The scope of this project emcompasses three major aspects.  First, we hope to **inform the historical music insights**, uncovering the story of music behind the data.  Leveraging the Spotify music dataset, we will discover and illustrate interesting patterns and trends through interactive visualization dashboards with customizable controls.   Second, we want to **provide personalized recommendations** based on user behavioral preferences and potentially social networks, improving listening experience through understanding then predicting the unique tastes of each user.  Ultimately, we aim to create a platform where users can explore the rich history of contemporary music and discover new personal favorites, all within **an engaging interactive user-friendly interface**.  This tool is designed to create a music discovery experience that is not only entertaining but also informative and personalized.  


<br>


## User Stories

### **Story 1: Abby, Music Producer**
Abby, an enthusiastic music producer, seeks a system for exploring music trends from the past century and getting personalized recommendations from Spotify.  She aims to enrich her understanding of music genres and styles evolution, which aids her career.

### **Story 2: Mike, Truck Driver**
Mike is always on the road –  he needs music to make his long drives more enjoyable.  Mike is looking for a simple music recommendation tool where he could input his favorite songs and receive a playlist tailored for his driving hours.   

### **Story 3: Tina, Marketing Manager at Spotify**
To expand Spotify’s market reach, Tina needs access to customer insights.  She would love to understand market trends and improve personalized music recommendations based on customer feedback.    

### **Story 4: Dave, Professor at UW**  
Dave is a professor at the University of Washington who loves music.  Tired of repeating his current playlist, Dave is looking for fresh and exciting music recommendations.  He seeks a personalized music discovery experience to find new songs that align with his tastes, ultimately boosting his happiness (?).    


<br>


## Acceptance Criteria

- The system allows users to create a profile detailing their music preferences.
- Personalized recommendations should span songs and artists, informed by user history and broader trends.
- The system should offer insights into music evolution from 1921 to 2020.
- Users can explore the audio features of music to understand what shapes their preferences.
- The system should provide visualizations of music trends and audio features alongside recommendations.
- The recommendations should adapt as the user's tastes evolve and as they interact with historical and audio feature explorations.


<br>


## Use Case

**Use Case Name:** Generating Personalized Music Recommendations and Historical Music Insights  
**Actors:** User, Music Exploration System  
**Preconditions:** The user has an active profile within the system and the system has gathered sufficient data on user preferences and historical music trends.


### Basic Flow

1. The user lands on the home page.
2. The user is presented with insights into music trends over the last 100 years and interactive tools to explore song audio features.
3. The user logs into their profile and jumps to the recommendation page.
4. The system pulls the user's listening history and stated preferences.
5. The recommendation engine proposes song and artist recommendations based on content filtering.
6. The system integrates collaborative filtering data, considering user-friend listening patterns.
7. The user can filter insights and recommendations by year, genre, artist, audio features, or friends’ selection.


### Postconditions

- The user gains a broader understanding of music evolution and their personal tastes.
- The system refines its recommendation algorithms based on user engagement with both songs and educational content.


### Exceptions

- If the user is not in the internal database, the system generates error messages.
- If the system cannot generate recommendations due to a lack of data, it offers a guided journey through music history to help define their preferences.

**Frequency of Use:** Users can engage with the system daily or as often as they seek new music.


<br>


## Business Rules

- The use of dummy data in the system eliminates concerns regarding actual user privacy.   
- The system is designed to inform users about the broad spectrum and evolution of music genres.   
- The personalized recommendations should offer a mix of popular hits and niche songs to enrich the user’s experience.  
- The system should be capable of illustrating complex data (e.g., audio features, historical trends) in an accessible and user-friendly manner.   


<br>


## Data Source

### Spotify Dataset (Content Filtering)

- **Features:** song_id, song_name, artists_name, artist_id, year, genre, release_date, duration_ms, acousticness, valence, danceability, energy, explicit, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, popularity


### Dummy Data for Users

- **Features:** user_id, first_name, last_name, age, sex, profile_photo    


### Dummy Data for User-Songs (Collaborative Filtering)

- **Features:** user_id, song_id, listening_cnt


### Dummy Data for User-Friends (Collaborative Filtering)

- **Features:** user_id, friend_id


### Dummy Data for Artists

- **Features:** artist_id, artist_name


<br>


## Deliverables

Interactive user interface that presents historical music insights and provides personalized music recommendations         

- **Historical Music Insights:** EDA + Visualization (music evolution, popular songs/genres, genre characteristics, etc.) in an HTML file      
- **Personalized Music Recommendations:** Predict the top 10 songs and artists based on listening history and user preferences   
- **User Music Profile:** Top songs/artists in users’ and friends’ history, favorite genres, audio features, and word cloud with favorite song names   
