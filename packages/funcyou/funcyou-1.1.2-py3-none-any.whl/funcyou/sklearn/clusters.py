import random
from itertools import product
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn import cluster, mixture, metrics


__all__ = ["models", "ClusterRandomzedSearch", "params"]

# Models for clustering algorithms to be used in the search process
models = {
    "kmeans": cluster.KMeans(),
    "ap": cluster.AffinityPropagation(),
    "gmm": mixture.GaussianMixture(),
    "bgmm": mixture.BayesianGaussianMixture(),
    "meanshift": cluster.MeanShift(),
    "dbscan": cluster.DBSCAN(),
    "spectral": cluster.SpectralClustering(),
    "agg": cluster.AgglomerativeClustering(),
    "birch": cluster.Birch(),
    "hdbscan": cluster.HDBSCAN(),
    "optics": cluster.OPTICS(),
    "bkmeans": cluster.BisectingKMeans(),
    "mini_batch_kmeans": cluster.MiniBatchKMeans(),
}


class ClusterRandomizedSearch:
    def __init__(
        self,
        model,
        param_distributions,
        n_iter=10,
        scoring="silhouette_score",
        random_state=None,
    ):
        """
        Initializes an instance of the class with the provided model, parameter distributions, and optional arguments.
        Sets up the scoring, random state, results, combinations, used combinations, n_iter, and model name attributes.

        Args:
            model:sklearn model: The model to be used for clustering.
            param_distributions:dict : A dictionary of parameter distributions for the model.
            n_iter (optional):int : The number of iterations for the search. Defaults to 10.
            scoring (optional):list : The scoring metric(s) to be used for evaluation. Defaults to 'silhouette_score'.
                            values: [silhouette_score', 'davies_bouldin_score', 'calinski_harabasz_score']
                            first metric will be used to score as best params and model.
            random_state (optional): The random seed for reproducibility.

        Returns:
            None

        Raises:
            ValueError: If scoring is not a string or a list of strings.

        Example:
            ```
            model = MyModel()
            param_distributions = {'param1': [1, 2, 3], 'param2': [4, 5, 6]}
            search = Search(model, param_distributions, n_iter=5, scoring='accuracy')
            ```
        """

        self.model = model
        self.param_distributions = param_distributions

        if isinstance(scoring, str):
            scoring = [scoring]
        elif not isinstance(scoring, list):
            raise ValueError(
                f"Scoring must be a string or a list of strings. Values can be {self.get_scorer()}"
            )

        self.scoring = scoring
        self.random_state = random_state
        self.results = []
        self.combinations = self.get_all_combinations(self.param_distributions)
        random.shuffle(self.combinations)
        self.used_combinations = set()
        self.n_iter = min(n_iter, len(self.combinations))
        self.model_name = model.__class__.__name__

    def fit(self, X):
        np.random.seed(self.random_state)
        for _ in range(self.n_iter):
            params = self.combinations.pop()

            try:
                model = self.model.set_params(**params)
                labels = model.fit_predict(X)
            except Exception as e:
                print("Model: ", self.model_name)
                print("Params: ", params)
                raise e

            self.n_clusters_ = np.unique(labels).size

            all_scores = {}
            for scoring_ in self.scoring:
                score = self._evaluate_score(X, labels, scoring_)
                all_scores.update(score)
            self.results.append(
                {
                    "params": params,
                    "name": self.model_name,
                    "n_clusters": self.n_clusters_,
                    **all_scores,
                }
            )

        self.best_result = max(
            self.results, default=np.nan, key=lambda x: x[self.scoring[0]]
        )

    @property
    def best_params_(self):
        return self.best_result["params"]

    @property
    def best_scores_(self):
        return {i: self.best_result[i] for i in self.scoring}

    @property
    def best_estimators_(self):
        return self.model.set_params(**self.best_params_)

    @property
    def n_clusters_(self):
        return self.best_result["n_clusters"]

    def get_all_combinations(self, parameter_dict):
        parameter_names = list(parameter_dict.keys())
        parameter_values = list(parameter_dict.values())

        combinations = list(product(*parameter_values))
        return [dict(zip(parameter_names, combo)) for combo in combinations]

    def get_scorer(self):
        return {"silhouette_score", "davies_bouldin_score", "calinski_harabasz_score"}

    def _evaluate_score(self, X, labels, scoring):
        if self.n_clusters_ == 1:
            score = np.nan
        elif scoring == "silhouette_score":
            score = silhouette_score(X, labels)
        elif scoring == "davies_bouldin_score":
            score = metrics.davies_bouldin_score(X, labels)
        elif scoring == "calinski_harabasz_score":
            score = metrics.calinski_harabasz_score(X, labels)
        else:
            raise ValueError(f"Invalid scoring metric: {scoring}")

        return {scoring: score}

    def results_(self):
        results_df = pd.DataFrame(self.results)
        param_columns = list(self.param_distributions.keys())
        for param_column in param_columns:
            results_df[f"param_{param_column}"] = results_df["params"].apply(
                lambda x: x[param_column]
            )

        return results_df


params = {
    "ap": {
        "damping": [
            0.5,
            0.55444444,
            0.60888889,
            0.66333333,
            0.71777778,
            0.77222222,
            0.82666667,
            0.88111111,
            0.93555556,
            0.99,
        ],
        "convergence_iter": [10, 12, 14, 16, 18, 20, 22, 24, 15],
        "affinity": ["euclidean"],
    },
    "kmeans": {
        "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "init": ["k-means++", "random"],
        "n_init": ["auto"],
        "tol": [0.001, 0.01, 0.1],
    },
    "meanshift": {
        "bandwidth": {},
    },
    "dbscan": {
        #         'eps':[0.51, 0.6, 0.7, 0.8, 0.9, 0.99],
        "eps": [
            0.5,
            0.55555556,
            0.61111111,
            0.66666667,
            0.72222222,
            0.77777778,
            0.83333333,
            0.88888889,
            0.94444444,
            1.0,
        ],
        "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
    },
    "spectral": {
        "eigen_solver": ["arpack", "lobpcg"],
        "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "n_init": [5, 7, 9, 11, 13, 15, 17, 19],
        "gamma": [0.5, 0.665, 0.831, 0.996, 1.162, 1.327, 1.493, 1.658, 1.824, 1.99],
        #         'affinity':['rbf', 'nearest_neighbors', 'precomputed_nearest_neighbors'],
        "n_neighbors": [5, 7, 9, 11, 13, 15, 17, 19],
    },
    "agg": {
        "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        #         'metric': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine'],
        "linkage": ["ward", "complete", "average", "single"],
        "compute_distances": [True, False],
    },
    "hdbscan": {
        "min_cluster_size": [10, 15, 20],
        "min_samples": [None, 5, 10, 15],
        "metric": ["euclidean", "manhattan"],  # , 'cosine'], 'precomputed'],
        "alpha": [1.0, 0.5, 1.5],
        "algorithm": ["auto", "brute", "kdtree", "balltree"],
        "cluster_selection_method": ["eom", "leaf"],
    },
    "birch": {
        "threshold": [0.1, 0.3, 0.5, 0.7],
        "branching_factor": [10, 30, 50, 70],
        "n_clusters": [3, 4, 5, 6, 7, 8, 9],
    },
    "optics": {
        #         'max_eps': np.linspace(0.1, 0.99, 10),
        "metric": ["cityblock", "euclidean", "l1", "l2", "manhattan"],
        "p": [1, 2, 3],
        "cluster_method": ["xi", "dbscan"],
        #         'eps': [None, 0.1, 0.5, 1.0, 2.0],
        "xi": [0.01, 0.05, 0.1, 0.2],
        "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
        "leaf_size": [10, 30, 50, 100],
    },
    "gmm": {
        "n_components": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
        ],
        "covariance_type": ["full", "tied", "diag", "spherical"],
        "tol": [1e-4, 1e-3, 1e-2, 1e-1],
        "reg_covar": [1e-7, 1e-6, 1e-5],
        "n_init": [1, 5, 10],
        "init_params": ["kmeans", "k-means++", "random"],
    },
    "bgmm": {
        "n_components": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
        ],
        "covariance_type": ["full", "tied", "diag", "spherical"],
        "tol": [1e-4, 1e-3, 1e-2, 1e-1],
        "reg_covar": [1e-7, 1e-6, 1e-5],
        "n_init": [1, 5, 10],
        "init_params": ["kmeans", "k-means++", "random"],
    },
    "bkmeans": {
        "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "init": ["k-means++", "random"],
        "n_init": [1, 5, 10],
        "tol": [1e-4, 1e-3, 1e-2],
        "algorithm": ["elkan", "lloyd"],
        "bisecting_strategy": ["biggest_inertia", "largest_cluster"],
    },
    "mini_batch_kmeans": {
        "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "init": ["k-means++", "random"],
        "batch_size": [2, 4, 8, 16],
    },
}
