# Dimension reduction
# Data source: TF-IDF of 2006-2012_posneg
import sys; sys.path.insert(0, '../')
from access.interim_storage import InterimStorage

print('Reading data')
results = InterimStorage('tfidf-object').read()
#print(len(results))
#print(next(iter(results.items())))



print('Transforming to lil_matrix')
from scipy.sparse import lil_matrix
lil_tfidf = results.tolil()
results = None

print('UMAP')
from umap.umap_ import UMAP
umap_results = UMAP(metric='cosine', low_memory=True, n_epochs=50).fit_transform(lil_tfidf)
print(InterimStorage('tfidf-umap').write(umap_results).get_filepath())

print(type(umap_results))
print(umap_results.shape)
print(type(umap_results))


if False:
    # Not used, sparse matrix reduction instead.
    from transformation.reduction import Reduction

    print('Dimension reduction: Fit')
    fifty_dim = {}
    reduction = Reduction()
    reduction.pca_fit(list(results.values()))
    #reduction.umap_fit(list(results.values()), parameters={'low_memory':True})
    #reduction.tsne_fit(list(results.values()))
    #reduction.pca_fit(list(results.values()), parameters={'n_components':50, 'iterated_power':2})
    print('Dimension reduction: Transform')
    for item in results.items():
        two_dim[item[0]] = reduction.pca_transform(item[1])
    #    two_dim[item[0]] = reduction.umap_transform(item[1], parameters={'low_memory':True})
    #    two_dim[item[0]] = reduction.tsne_transform(item[1])
    #    fifty_dim[item[0]] = reduction.pca_transform(item[1])
    print(len(fifty_dim))
    print(next(iter(fifty_dim.items())))
    print(InterimStorage('tfidf-50dim').write(fifty_dim).get_filepath())