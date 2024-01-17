import unittest

from combo.data import SpacyTokenizer


class SpacyTokenizerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.spacy_tokenizer = SpacyTokenizer()

    def test_tokenize_sentence(self):
        tokens = self.spacy_tokenizer.tokenize('Hello cats. I love you')
        self.assertListEqual([t.text for t in tokens],
                             ['Hello', 'cats', '.', 'I', 'love', 'you'])

    def test_tokenize_empty_sentence(self):
        tokens = self.spacy_tokenizer.tokenize('')
        self.assertEqual(len(tokens), 0)

