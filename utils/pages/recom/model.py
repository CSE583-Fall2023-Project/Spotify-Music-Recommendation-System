import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from surprise import SVD, Dataset, Reader
from surprise.model_selection import GridSearchCV
from collections import defaultdict


class RecommendationModel:
    def __init__(self, user_songs_path, user_friends_path):
        self.user_songs = pd.read_csv(user_songs_path)
        self.user_friends = pd.read_csv(user_friends_path)
        self.algo = None

    def train(self):
        scaler = MinMaxScaler()
        self.user_songs['listening_count_normalized'] = scaler.fit_transform(self.user_songs[['listening_count']])
        reader = Reader(rating_scale=(0, 1))

        # Load the dataset from DataFrame
        data = Dataset.load_from_df(self.user_songs[['user_id', 'song_id', 'listening_count_normalized']], reader)

        param_grid = {"n_epochs": [5, 10], "lr_all": [0.002, 0.005], "reg_all": [0.4, 0.6]}
        gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)
        gs.fit(data)

        print("Best RMSE score:", gs.best_score["rmse"])
        print("Best parameters set:", gs.best_params["rmse"])

        self.algo = gs.best_estimator["rmse"]
        trainset = data.build_full_trainset()
        self.algo.fit(trainset)

    def predict(self):
        if self.algo is None:
            raise ValueError("Model not trained yet. Call train() before your make predictions")
        trainset = self.algo.trainset
        anti_testset = trainset.build_anti_testset()
        predictions = self.algo.test(anti_testset)
        return predictions

    def get_top_n_songs(self, predictions, n):
        playlist = defaultdict(list)
        for user_id, item_id, true_r, est, _ in predictions:
            playlist[user_id].append((item_id, est))

        for user_id, list_cnt in playlist.items():
            list_cnt.sort(key=lambda x: x[1], reverse=True)
            playlist[user_id] = list_cnt[:n]

        for user_id in playlist:
            if len(playlist[user_id]) < n:
                friends_top_songs = self.get_friends_top_songs(user_id,
                                                               playlist,
                                                               n - len(playlist[user_id]))
                playlist[user_id].extend(friends_top_songs)

        return playlist

    # Function to get top songs from friends
    def get_friends_top_songs(self, user_id, playlist, n):
        friends_songs = []
        friends_ids = self.user_friends[self.user_friends['user_id'] == user_id]['friend_id'].tolist()

        for friend_id in friends_ids:
            if friend_id in playlist:
                friends_songs.extend(playlist[friend_id])

        friends_songs.sort(key=lambda x: x[1], reverse=True)
        return [song_id for song_id, _ in friends_songs[:n]]



