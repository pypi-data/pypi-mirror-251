import os
import unittest

from combo.data import SingleIdTokenIndexer, Token
from combo.data.vocabulary import Vocabulary


class VocabularyTest(unittest.TestCase):

    def setUp(self):
        self.vocabulary = Vocabulary.from_files(
            os.path.join(os.getcwd(), '../../fixtures/train_vocabulary'),
            oov_token='_',
            padding_token='__PAD__'
        )
        self.single_id_indexer = SingleIdTokenIndexer(namespace='token_characters')

    def test_get_index_to_token(self):
        token = Token(idx=0, text='w')
        counter = {'token_characters': {'w': 0}}
        self.single_id_indexer.count_vocab_items(token, counter)
        self.assertEqual(counter['token_characters']['w'], 1)

    def test_tokens_to_indices(self):
        self.assertEqual(
            self.single_id_indexer.tokens_to_indices(
                [Token('w'), Token('nawet')], self.vocabulary),
            {'tokens': [11, 127]})
