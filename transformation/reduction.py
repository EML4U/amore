# This class provides basic methods to transform embedding dimensions.
# Every algorithm can be configured using the respective original parameters.
# The default target dimension is 2.
# Author: https://github.com/adibaba

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap_
import timeit

class Reduction:
    
    # https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
    def pca_fit(self, fit_data, parameters={}, print_time=False):
        time_begin = timeit.default_timer()
        if not 'n_components' in parameters:
            parameters['n_components'] = 2
        self.pca_instance = PCA(**parameters)
        self.pca_instance.fit(fit_data)
        if(print_time):
            print('PCA fit seconds:', timeit.default_timer() - time_begin)
    
    def pca_transform(self, transform_data, print_time=False):
        time_begin = timeit.default_timer()
        result = self.pca_instance.transform(transform_data)
        if(print_time):
            print('PCA seconds:', timeit.default_timer() - time_begin)
        return result

    
    # https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    def tsne_fit(self, fit_data, parameters={}, print_time=False):
        time_begin = timeit.default_timer()
        self.tsne_instance = TSNE(**parameters)
        self.tsne_instance.fit(fit_data)
        if(print_time):
            print('t-SNE fit seconds:', timeit.default_timer() - time_begin)
    
    def tsne_transform(self, transform_data, dimensions=2, print_time=False):
        time_begin = timeit.default_timer()
        result = self.tsne_instance.fit_transform(transform_data)
        if(print_time):
            print('t-SNE transform seconds:', timeit.default_timer() - time_begin)
        return result
    
    
    # https://umap-learn.readthedocs.io/en/latest/api.html
    def umap_fit(self, fit_data, parameters={}, print_time=False):
        time_begin = timeit.default_timer()
        self.umap_instance = umap_.UMAP(**parameters)
        self.umap_instance.fit(fit_data)
        if(print_time):
            print('UMAP fit seconds:', timeit.default_timer() - time_begin)
    
    def umap_transform(self, transform_data, print_time=False):
        time_begin = timeit.default_timer()
        result = self.umap_instance.transform(transform_data)
        if(print_time):
            print('UMAP seconds:', timeit.default_timer() - time_begin)
        return result