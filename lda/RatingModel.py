import numpy as np
from DataProcessor import DataLoader
from scipy.sparse import csr_matrix


class RatingModel:

    def __init__(self, ratings_filename='../Data/ratings.npz', n_hidden_factors=10):
        self.data = DataLoader.ratings_data(ratings_filename)
        n_users, n_items = self.data.shape
        self.corpus_ix = (self.data > 0).toarray()

        self.alpha = 0.0
        self.beta_user = np.zeros(n_users)
        self.beta_item = np.zeros(n_items)
        self.gamma_user = np.zeros((n_users, n_hidden_factors))
        self.gamma_item = np.zeros((n_items, n_hidden_factors))
        self.predicted_rating = None

    def get_predicted_ratings(self):
        self.predicted_rating = self.alpha + self.beta_user[:, None] + \
              self.beta_item + np.dot(self.gamma_user, self.gamma_item.transpose())
        self.predicted_rating[np.logical_not(self.corpus_ix)] = 0

    def get_rating_error(self):
        corpus_ix = self.data.nonzero()
        return np.sum(np.square(self.predicted_rating - self.data))
