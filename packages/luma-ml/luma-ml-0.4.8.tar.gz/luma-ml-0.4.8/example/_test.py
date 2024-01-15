import __local__
from sklearn.datasets import make_blobs, make_moons
import numpy as np

from luma.clustering.density import OPTICS, DENCLUE
from luma.clustering.kmeans import KMedoidsClustering
from luma.visual.result import ClusterPlot, DecisionRegion

NUM = 100
RANDOM_STATE = 42


X0, y0 = make_moons(n_samples=NUM, noise=0.03, random_state=RANDOM_STATE)

X1, y1 = make_blobs(n_samples=NUM, 
                    centers=[(-0.75,2.25), (1.0, -2.0)], 
                    cluster_std=0.3, random_state=RANDOM_STATE)

X2, y2 = make_blobs(n_samples=NUM, 
                    centers=[(2,2.25), (-1, -2.0)], 
                    cluster_std=0.3, random_state=RANDOM_STATE)

X = np.vstack((X0, X1, X2))
y = np.vstack((y0, y1 + 2, y2 + 4))

model = KMedoidsClustering(n_clusters=6,
                           max_iter=300,
                           random_state=RANDOM_STATE,
                           verbose=True)

model.fit(X)

plot = DecisionRegion(estimator=model, X=X)
plot.plot()
