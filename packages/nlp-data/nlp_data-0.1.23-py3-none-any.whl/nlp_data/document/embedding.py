from docarray import BaseDoc, DocList
from docarray.typing import NdArrayEmbedding
import numpy as np


class EmbeddingDoc(BaseDoc):
    """存放词(字)向量的文档
    """
    text: str
    embedding: NdArrayEmbedding
    
    
class EmbeddingDocList(DocList[EmbeddingDoc]):
    
    @classmethod
    def from_file(cls, file_path: str):
        """从文件中读取词向量
        """
        docs = EmbeddingDocList()
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                char = line.strip().split(' ')[0]
                if char not in docs.text:
                    embeddings = line.strip().split(' ')[1:]
                    embeddings = [float(i) for i in embeddings]
                    doc = EmbeddingDoc(text=char, embedding=embeddings)
                    docs.append(doc)
        return docs
    
    
    def get_vocab(self):
        """获取词表
        """
        return {doc.text: i for i, doc in enumerate(self)}
    
    def get_embeddings(self):
        """获取所有向量多用于构建embedding层
        """
        embeddings = [doc.embedding for doc in self]
        return np.array(embeddings)