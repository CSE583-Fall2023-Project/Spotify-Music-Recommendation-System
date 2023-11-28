<h1 align="center">🎵 Generating Personalized Music Recommendations and Historical Music Insights 🎵</h1>

<p align="center">
  <img src="../image/banner-2048.png" alt="Music Exploration">
</p>
<h2 align="center"> Component Specification 💡</h2>



## 👩‍💻 Software Components

### Data Manager

<details>
<summary><b>Functionality</b></summary>
<p>This component manages all interactions with datasets including Spotify Dataset, Dummy User Data, User-Songs, and User-Friends data. It executes queries, filters, and aggregates data to meet various requirements.</p>
</details>

<table>
  <tr>
    <th colspan="2" style="text-align:center;background-color:#4CAF50;color:white;">Data Manager Process Flow</th>
  </tr>
  <tr>
    <td style="background-color:#f2f2f2;text-align:center;"><b>Inputs</b></td>
    <td style="background-color:#f2f2f2;text-align:center;"><b>Outputs</b></td>
  </tr>
  <tr>
    <td>Queries and requests for data handling</td>
    <td rowspan="2" style="vertical-align:middle;text-align:center;">Structured data outputs (e.g., data frames)</td>
  </tr>
  <tr>
    <td>Ranging from individual user profiles to complex friend connection networks</td>
  </tr>
</table>


### Recommendation Engine

<details>
<summary ><b>Functionality</b></summary>
<p>The core of the system is the Recommendation Engine, which utilizes collaborative and content-based filtering to produce music suggestions. It takes into account user preferences, listening habits, and social connections to generate relevant song and artist recommendations.</p>
</details>
<table>
  <tr>
    <th colspan="2" style="text-align:center;background-color:#4CAF50;color:white;">Recommendation Engine Process Flow</th>
  </tr>
  <tr>
    <td style="background-color:#f2f2f2;text-align:center;"><b>Inputs</b></td>
    <td style="background-color:#f2f2f2;text-align:center;"><b>Outputs</b></td>
  </tr>
  <tr>
    <td>Listening histories, genre preferences, artist selections, and social listening trends from the Data Manager.</td>
    <td rowspan="2" style="vertical-align:middle;text-align:center;">A personalized playlist of songs and artists, customized to users' music preferences.</td>
  </tr>
</table>


### Visualization Manager

<details>
<summary><b>Functionality</b></summary>
<p>This component focuses on creating visual narratives from data, by transforming data into visualizations that highlights music trends, listening behaviors, and audio feature analysis, to engage and inform the users.</p>
</details>

<table>
  <tr>
    <th colspan="2" style="text-align:center;background-color:#4CAF50;color:white;">Visualization Manager Process Flow</th>
  </tr>
  <tr>
    <td style="background-color:#f2f2f2;text-align:center;"><b>Inputs</b></td>
    <td style="background-color:#f2f2f2;text-align:center;"><b>Outputs</b></td>
  </tr>
  <tr>
    <td>Data encompassing popularity metrics, user behavior, and audio features provided by the Data Manager.</td>
    <td rowspan="2" style="vertical-align:middle;text-align:center;">A dashboard of visual aids such as charts, graphs, and timelines to illustrate the evolution of music, characteristics of songs, and personalized listening behaviors.</td>
  </tr>
</table>


<br> 


## 🧬 Use Cases and Interactions  

### Use Case 1: Exploring Historical Music Trends

<details>
<summary><b>Process Flow</b></summary>
<div class="use-case-content">
  <p>The process flow is designed to guide the user through a seamless and educational journey in music discovery:</p>
  <ol class="use-case-list">
    <li><span class="step">User Access:</span> Upon accessing the platform, the user is introduced to a dashboard highlighting various music exploration features.</li>
    <li><span class="step">Trend Selection:</span> The user selects a time period or genre to explore historical music trends.</li>
    <li><span class="step">Data Retrieval:</span> The Data Manager queries the database for relevant historical data.</li>
    <li><span class="step">Trend Analysis:</span> The retrieved data is processed to highlight key trends and significant musical milestones.</li>
    <li><span class="step">Visual Representation:</span> The Visualization Manager generates interactive charts and graphs that depict the evolution of music during the chosen period or within the selected genre.</li>
    <li><span class="step">Interactive Learning:</span> The user interacts with the visual data, discovering influential artists, landmark albums, and pivotal songs.</li>
    <li><span class="step">Feedback Mechanism:</span> The user can provide feedback or save their historical exploration to their profile for future reference.</li>
  </ol>
</div>
</details>

### Use Case 2: Generating User Profile with Personalized Music Recommendations

<details>
<summary><b>Process Flow</b></summary>
<div class="use-case-content">
  <p>The process flow is designed to guide the user through a seamless and educational journey in music discovery:</p>
  <ol class="use-case-list">
    <li><span class="step">User Login:</span> Initiates a data fetch from the Data Manager.</li>
    <li><span class="step">Data Analysis:</span> The user's data is channeled to the Recommendation Engine.</li>
    <li><span class="step">Generating Recommendations:</span> A tailored music profile is constructed, featuring a selection of songs and artists.</li>
    <li><span class="step">Visual Analytics:</span> The Visualization Manager concurrently receives data to manifest user-specific music preference analytics.</li>
    <li><span class="step">Output Presentation:</span> Users are greeted with an all-encompassing music profile, inclusive of a custom playlist and visual data insights.</li>
  </ol>
</div>
</details>


<br> 


## 📝 Preliminary Plan

<blockquote>
Having defined the business problem and drafted the design specifications tailored to these requirements, the following plan outlines the remaining stages in the development process, with the aim to deliver a robust and user-centered final product.   
</blockquote>

- **Develop the Data Manager**: Clean and organize the data so that it is accessible and usable.  
- **Build the Recommendation Engine**: Develop the recommendation system using content/collaborative filtering.
- **Design the Visualization Manager**: Create interactive visualization dashboards from EDA. 
- **Integrate Components**: Combine all components together into one system.  
- **User Interface Development**: Design a user-friendly interface for users to interact with the application.      
- **Testing and Iteration**: Conduct tests on the code to verify that it meets the defined requirements and make adjustments accordingly.   
- **Documentation and Training**: Create end-user documentation to help users  understand how to use the tool.    
- **Launch and Monitor**: Make the tool available to users (deploy the software to production environment); maintain and update the tool if needed.   
