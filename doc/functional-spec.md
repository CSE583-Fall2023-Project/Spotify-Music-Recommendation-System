<h1 align="center">🎵 Generating Personalized Music Recommendations and Historical Music Insights 🎵</h1>

<p align="center">
  <img src="../image/banner-2048.png" alt="Music Exploration">
</p>
<h2 align="center"> Functional Specification 💽</h2>



## 🎶 Background  

<p> 
<strong>Music is dynamic</strong> – the history of music is the history of human culture; each era presents its own story through its distinct styles and genres.  <strong>Music is diverse</strong> – each genre is characterized by its unique blends of composition elements, varying in rhythms, scales, harmonies, and structures.  <strong>Music tells us about ourselves.</strong>  Our music taste is shaped by our surroundings and exposures, by a mix of cultural influences, popular trends, and personal experiences.    
</p>
<p> 
In the dynamic and diverse world of music streaming and discovery, our project aims to offer a <strong>unique personalized and enriching experience that caters to the tastes of individual users</strong>.  At the core of this objective is the desire to not only provide music recommendations but to do so in a way that is insightful and resonates with each user’s unique music journey.  
</p>
<p> 
The scope of this project emcompasses three major aspects.  First, we hope to <strong>inform the historical music insights</strong>, uncovering the story of music behind the data.  Leveraging the Spotify music dataset, we will discover and illustrate interesting patterns and trends through interactive visualization dashboards with customizable controls.   Second, we want to <strong>provide personalized recommendations</strong> based on user behavioral preferences and potentially social networks, improving listening experience through understanding then predicting the unique tastes of each user.  Ultimately, we want to create a platform where users can explore the rich history of contemporary music and discover new personal favorites, all within <strong>an engaging interactive user-friendly interface</strong>.  We aim to create a music discovery experience that is not only enjoyable but also insightful and personal.  
</p>



## 🌟 User Stories

<details>
<summary><b>Story 1: Abby, Music Producer</b></summary>
<p>
Abby, an enthusiastic music producer, seeks a system for exploring music trends from the past century and getting personalized recommendations from Spotify.  She aims to enrich her understanding of music genres and styles evolution, which aids her career.
</p>
</details>
<details>
<summary><b>Story 2: Mike, Truck Driver</b></summary>
<p>
Mike is always on the road –  he needs music to make his long drives more enjoyable.  Mike is looking for a simple music recommendation tool where he could input his favorite songs and receive a playlist tailored for his driving hours.  
</p>
</details>
<details>
<summary><b>Story 3: Tina, Marketing Manager at Spotify</b></summary>
<p>
To expand Spotify’s market reach, Tina needs access to customer insights.  She would love to understand market trends and improve personalized music recommendations based on customer feedback.    
</p>
</details>
<details>
<summary><b>Story 4: Dave, Professor at UW</b></summary>
<p>
Dave is a professor at the University of Washington who loves music.  Tired of repeating his current playlist, Dave is looking for fresh and exciting music recommendations.  He seeks a personalized music discovery experience to find new songs that align with his tastes, ultimately boosting his happiness (?).   
</p>
</details>


<br>


## ✅ Acceptance Criteria

- <span style="color: green">The system allows users to create a profile detailing their music preferences.</span>
- <span style="color: green">Personalized recommendations should span songs and artists, informed by user history and broader trends.</span>
- <span style="color: green">The system should offer insights into music evolution from 1921 to 2020.</span>
- <span style="color: green">Users can explore the audio features of music to understand what shapes their preferences.</span>
- <span style="color: green">The system should provide visualizations of music trends and audio features alongside recommendations.</span>
- <span style="color: green">The recommendations should adapt with the user's feedback.</span>


<br>


## 🎭 Use Case

<details>
<summary><b>Use Case 1: User Browsing Historical Music Trends and Listening to Samples</b></summary>
<div class="use-case-content">
    <p>The user visits the music exploration platform with the intent to browse and understand historical music trends without logging in. The platform presents a timeline feature where the user can navigate through different eras of music, listening to samples, and viewing trend data.</p>
    <ul class="use-case-list">
      <li>User lands on the home page and starts their journey of music exploration without logging in.</li>
      <li>User selects a time period of interest to explore music trends.</li>
      <li>The system displays a variety of metrics and data visualization representing the musical landscape of the selected time.</li>
      <li>User can listen to sample tracks, add songs to their profile, and learn about influential artists and genres.</li>
    </ul>
  </div>
</details>

<details>
<summary><b>Use Case 2: User Receiving Music Profile with Personalized Music Recommendations </b></summary>
<div class="use-case-content">
    <p>The user aims to receive personalized music profile with recommendations tailored to their tastes. The system analyzes the user's listening history, friends' favorite tracks, and artist preferences to generate a custom playlist.</p>
    <ul class="use-case-list">
      <li>The system has gathered sufficient data on user preferences and historical music trends.</li>
      <li>User logs in from the home page.</li>
      <li>The system pulls the user's listening history and stated preferences. </li>
      <li>The system employs an algorithm to find and recommend new music matching the user's preferences.</li>
      <li>User receives personalized music profile, inclusing a curated playlist which they can save, modify, and rate.</li>
      <li>The music profile offers insightful analytics on the user's preferred music features, sheds light on favored genres, and pinpoints the time periods that resonate most with their musical sensibilities. </li>
      <li>User discovers the current favorites within the user's friend circle through a social listening window. </li>
      <li>User saves their personalized music profile as pdf in their local devices.</li>
      <li>The system refines its recommendations based on user feedback and interaction with the playlist.</li>
    </ul>
  </div>
</details>

**Exemptions:**

- If the user is not in the internal database, the system generates error messages.
- If the system cannot generate recommendations due to a lack of data, it offers a guided journey through music history to help define their preferences.

**Frequency of Use:**

Users can engage with the system daily or as often as they seek new music.

<br>

## 📜 Business Rules

- <span style="color: blue">The use of dummy data in the system eliminates concerns regarding actual user privacy.</span>
- <span style="color: blue">The system is designed to inform users about the broad spectrum and evolution of music genres.</span>
- <span style="color: blue">The personalized recommendations should offer a mix of popular hits and niche songs to enrich the user’s experience.</span>
- <span style="color: blue">The system should be capable of illustrating complex data (e.g., audio features, historical trends) in an accessible and user-friendly manner.</span>


<br>


## 📊 Data Source

### Spotify Dataset (Content Filtering)

This data set contains 170,653 songs released from 1921 to 2020 from Spotify. For the purpose of research, we have modified the original data [(check it here)](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset/code) by renaming fields and adding identification and genre information. Typical features include:

- **Track Information:** Such as song ID, song name, and artist names. This would include metadata about the tracks.
- **Audio Features:** Data points like acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, and valence, which are standard Spotify API audio features that describe the qualities of a track.
- **Popularity Metrics:** The dataset might include a popularity score for each track, which is a metric used by Spotify to determine how often tracks are played and how recent those plays are.
- **Temporal Data:** Information about the release date of each track and the year they were released.
- **Identification Data:** Unique identifiers for each song (song ID) and each artist (artist ID).

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>song_id</td>
    <td>Unique identifier for each song</td>
  </tr>
  <tr>
    <td>song_name</td>
    <td>Title of the song</td>
  </tr>
  <tr>
    <td>artists_name</td>
    <td>Name of the artist(s) who performed the song</td>
  </tr>
  <tr>
    <td>artist_id</td>
    <td>Unique identifier for each artist</td>
  </tr>
  <tr>
    <td>year</td>
    <td>Release year of the song</td>
  </tr>
  <tr>
    <td>genre</td>
    <td>Music genre of the song</td>
  </tr>
  <tr>
    <td>release_date</td>
    <td>The date when the song was released</td>
  </tr>
  <tr>
    <td>duration_ms</td>
    <td>Duration of the song in milliseconds</td>
  </tr>
  <tr>
    <td>acousticness</td>
    <td>A measure of the acoustical quality of the song</td>
  </tr>
  <tr>
    <td>valence</td>
    <td>A measure of the musical positiveness conveyed by a song</td>
  </tr>
  <tr>
    <td>danceability</td>
    <td>A measure of how suitable a track is for dancing</td>
  </tr>
  <tr>
    <td>energy</td>
    <td>A measure of intensity and activity in a song</td>
  </tr>
  <tr>
    <td>explicit</td>
    <td>Indicates whether the song contains explicit content</td>
  </tr>
  <tr>
    <td>instrumentalness</td>
    <td>Indicates the likelihood of a song being instrumental</td>
  </tr>
  <tr>
    <td>key</td>
    <td>The key the track is in</td>
  </tr>
  <tr>
    <td>liveness</td>
    <td>Detects the presence of an audience in the recording</td>
  </tr>
  <tr>
    <td>loudness</td>
    <td>Overall loudness of a track in decibels</td>
  </tr>
  <tr>
    <td>mode</td>
    <td>Modality of the track (major or minor)</td>
  </tr>
  <tr>
    <td>speechiness</td>
    <td>A measure of the presence of spoken words in a track</td>
  </tr>
  <tr>
    <td>tempo</td>
    <td>The overall estimated tempo of a track in beats per minute</td>
  </tr>
  <tr>
    <td>popularity</td>
    <td>The popularity indicator of the track</td>
  </tr>
</table>

### Dummy Data for Users

This data set contains 2,000 synthesized users. The profile photos were generated using stable-diffusion-v1-5 [(check it here)](https://huggingface.co/runwayml/stable-diffusion-v1-5) with prompts "{user['first_name']} {user['last_name']} at the age of {str(user['age'])} with gender being {user['sex']}".

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>user_id</td>
    <td>Unique identifier for each user</td>
  </tr>
  <tr>
    <td>first_name</td>
    <td>First name of the user</td>
  </tr>
  <tr>
    <td>last_name</td>
    <td>Last name of the user</td>
  </tr>
  <tr>
    <td>age</td>
    <td>Age of the user</td>
  </tr>
  <tr>
    <td>sex</td>
    <td>Sex of the user</td>
  </tr>
  <tr>
    <td>profile_photo</td>
    <td>Photo of the user</td>
  </tr>
</table>

### Dummy Data for User-Songs (Collaborative Filtering)

This data set contains 10,000 synthesized user-songs relations that shows how frequently a user listens to a song, i.e. tuples [user, song, listening count].  

**avg. 50% songs most listened by each user (listening count > 10)**

**avg. each song has 5 users who listened** 

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>user_id</td>
    <td>Unique identifier for each user</td>
  </tr>
  <tr>
    <td>song_id</td>
    <td>Unique identifier for each song</td>
  </tr>
  <tr>
    <td>listening_cnt</td>
    <td>Record of the total number of times a user listens to a song</td>
  </tr>
</table>

### Dummy Data for User-Friends (Collaborative Filtering)

This data set contains 12,000 bi-directional synthesized friend relations between users in the database, i.e. 24,000 (user_i, user_j) pairs. 

**min. 3 friend relations per user** 

**max. 20 friend relations per user**

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>user_id</td>
    <td>Unique identifier for each user</td>
  </tr>
  <tr>
    <td>friend_id</td>
    <td>Unique identifier for each friend of a user (who is also a user)</td>
  </tr>
</table>
