import torch
import faiss
import os
import numpy as np
import WikiTransform.WikiTransform as model


class VectorDB:

    def __init__(self, dimensions, path):
        self.dimensions = dimensions
        self.path = path
        self.index = faiss.IndexFlatL2(dimensions)
        self.title_to_index = {}
        self.index_to_title = {}
        self.vectors = []
        self.titles = []
        self.index_len = 0

        for file in os.listdir(os.path.join(path, 'NPY', 'Titles')):
            path = os.path.join(os.path.join(path, 'NPY', 'Titles'), file)
            self.titles.extend(np.load(path))

        self.titles = np.array(self.titles)
        self.titles = self.titles.flatten()

        for i in range(len(self.titles)):
            self.title_to_index[self.titles[i]] = i
            self.index_to_title[i] = self.titles[i]

        for file in os.listdir(os.path.join(path, 'NPY', 'Vectors')):
            path = os.path.join(os.path.join(path, 'NPY', 'Titles'), file)
            v = np.load(path)
            v = v.reshape(v.shape[0], dimensions)
            self.vectors.extend(v)

        self.vectors = np.array(self.vectors)
        self.vectors = self.vectors.reshape(self.vectors.shape[0], dimensions)

        self.index.add(self.vectors)

    def __len__(self):
        return self.index_len

    def has_title(self, title: str) -> bool:
        return title in self.title_to_index

    def get_article_vector(self, title: str) -> np.ndarray:
        return self.vectors[self.title_to_index[title]].reshape(1, -1)

    def top_n(self, title: str, n: int = 10):
        if title not in self.title_to_index:
            return []
        else:
            vec = self.get_article_vector(title)
            D, I = self.index.search(vec, n)
            ret = [self.index_to_title[i] for i in I[0]]
            return ret

    def get_top_n_by_sentence(self, sentence: str, n: int = 10, model: model.WikiTransform = None, add_prompt: bool = True):
        vec = model.encode_sentence(sentence)
        D, I = self.index.search(vec, n)
        ret = [self.index_to_title[i] for i in I[0]]
        return ret
