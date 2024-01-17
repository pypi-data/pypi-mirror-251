from langtorch import TextTensor
import os
import unittest
from langtorch import Session
import logging

logging.basicConfig(level=logging.DEBUG)
# session = Session("embeddings_test_config.yaml")

class TestEmbeddingModules(unittest.TestCase):
    def test_openai_embedding(self):
        tensor = TextTensor([str(i) for i in range(100)])
        tensor.embed()
        del tensor
        tensor = TextTensor([str(i) for i in range(100)])
        tensor.embed()

        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.
        self.assertEqual(tuple(tensor.embedding.shape[:-1]), tensor.content.shape)


if __name__ == "__main__":
    unittest.main()
