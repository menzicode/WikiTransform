import dump_db
from sentence_transformers import SentenceTransformer
import numpy as np
import os


class WikiTransform:
    def __init__(self, db_path: str, model_path: str, chunk_size: int = 512):
        self.db = dump_db.DumpDB(db_path)
        self.model = SentenceTransformer(model_path)

    def chunk_article(self, title: str):
        paragraphs = self.db.get_paragraphs(title)
        total_len = 0
        for paragraph in paragraphs:
            p_len = len(paragraph.text.split(" "))
            total_len += p_len
        if total_len <= 512:
            full_text = ""
            for paragraph in paragraphs:
                full_text += paragraph.text
            return [full_text]
        else:
            n_chunks = total_len // 512
            if total_len % 512 != 0:
                n_chunks += 1
            chunk_size = total_len // n_chunks
            chunks = ["" for _ in range(n_chunks)]
            current_chunk = 0
            current_chunklen = 0
            for paragraph in paragraphs:
                sentences = paragraph.text.split(".")
                for sentence in sentences:
                    sentence_len = len(sentence.split(" "))
                    if current_chunklen + sentence_len > chunk_size:
                        if current_chunk == n_chunks - 1:
                            chunks[current_chunk] += " " + sentence + "."
                            current_chunklen += sentence_len
                        else:
                            current_chunk += 1
                            current_chunklen = 0
                            chunks[current_chunk] += " " + sentence + "."
                            current_chunklen += sentence_len
                    else:
                        chunks[current_chunk] += " " + sentence + "."
                        current_chunklen += sentence_len
            text_chunks = []
            for chunk in chunks:
                text_chunks.append(chunk)
            return text_chunks

    def encode_article(self, title: str):
        chunks = self.chunk_article(title)
        embeddings = self.model.encode(chunks)
        mean_pool = np.mean(embeddings, axis=0).reshape(1, -1)

        return mean_pool

    def encode_sentence(self, sentence: str, add_prompt: bool = True):
        if add_prompt:
            sentence = "Represent this sentence for searching relevant passages: " + sentence
        embedding = self.model.encode(sentence)
        embedding = embedding.reshape(1, -1)
        return embedding

    def train(self, batch_size: int = 100000, path: str = os.getcwd()):
        ctr = 0
        vecs = []
        titles = []
        for title in self.db.titles():
            ctr += 1
            if ctr % 10000 == 0:
                print(ctr)
            if ctr % batch_size == 0:
                vname = f'arrays_compressed_{ctr//batch_size}.npy'
                tname = f'titles_compressed_{ctr//batch_size}.npy'
                np.save(os.path.join(path, "NPY", "Vectors", vname), vecs)
                np.save(os.path.join(path, "NPY", "Titles", tname), titles)
                vecs = []
                titles = []
            if not self.db.is_disambiguation(title):
                mean_pool = self.encode_article(title)
                vecs.append(mean_pool)
                titles.append(title)
