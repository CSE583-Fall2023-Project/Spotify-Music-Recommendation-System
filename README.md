# Generating Personalized Music Recommendations and Historical Music Insights

Juntong Wu, Denkie Yan, Chesie Yu

<br>

## User Stories

### **Story 1: Abby, Music Producer**
Abby, an enthusiastic music producer, seeks a system for exploring music trends from the past century and getting personalized recommendations from Spotify.  She aims to enrich her understanding of music genres and styles evolution, which aids her career.

### **Story 2: Mike, Truck Driver**
Mike is always on the road –  he needs music to make his long drives more enjoyable.  Mike is looking for a simple music recommendation tool where he could input his favorite songs and receive a playlist tailored for his driving hours.   

### **Story 3: Tina, Marketing Manager at Spotify**
To expand Spotify’s market reach, Tina needs access to customer insights.  She would love to understand market trends and improve personalized music recommendations based on customer feedback.    

### **Story 4: Dave, A Professor at UW**  
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

- As dummy data is used, real user privacy concerns are non-existent.
- The system is designed to educate users about musical diversity and the evolution of music.
- Personalized recommendations should offer a mix of popular and lesser-known music to enrich the user's experience.
- The system should be capable of illustrating complex data (e.g., audio features, historical trends) in an accessible and user-friendly manner.


<br>


## Data Source

### Spotify Dataset (Content Filtering)

- **Features:** song_id, song_name, artists_name, artist_id, year, genre, release_date, duration_ms, acousticness, valence, danceability, energy, explicit, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, popularity


### Dummy Data for Users

- **Features:** user_id, user_name, …


### Dummy Data for User-Songs (Collaborative Filtering)

- **Features:** user_id, song_id, listening_cnt


### Dummy Data for User-Friends (Collaborative Filtering)

- **Features:** user_id, friend_id


### Dummy Data for Artists

- **Features:** artist_id, artist_name


<br>


## Deliverables

- **Data Understanding by Visualization and EDA:** HTML file
- **Predictions:** Top 10 new songs/artists recommended
- **EDA:** Top songs/artists in users’ and friends’ history, favorite genres, audio features, and word cloud with favorite song names
