import unittest

from combo.data import LamboTokenizer


class LamboTokenizerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.lambo_tokenizer = LamboTokenizer()

    def test_tokenize_sentence(self):
        tokens = self.lambo_tokenizer.tokenize('Hello cats. I love you')
        self.assertListEqual([t.text for t in tokens],
                             ['Hello', 'cats', '.', 'I', 'love', 'you'])

    def test_segment_text(self):
        tokens = self.lambo_tokenizer.segment('Hello cats. I love you.\n\nHi.')
        self.assertListEqual(tokens,
                             [['Hello', 'cats', '.'], ['I', 'love', 'you', '.'], ['Hi', '.']])

    def test_segment_text_with_turns(self):
        tokens = self.lambo_tokenizer.segment('Hello cats. I love you.\n\nHi.', turns=True)
        self.assertListEqual(tokens,
                             [['Hello', 'cats', '.', 'I', 'love', 'you', '.'], ['Hi', '.']])

    def test_segment_text_with_multiwords(self):
        tokens = self.lambo_tokenizer.segment('I don\'t want a pizza.', split_subwords=True)
        self.assertListEqual(tokens,
                             [['I', 'do', 'n\'t', 'want', 'a', 'pizza', '.']])

    def test_segment_text_with_multiwords_without_splitting(self):
        tokens = self.lambo_tokenizer.segment('I don\'t want a pizza.', split_subwords=False)
        self.assertListEqual(tokens,
                             [['I', 'don\'t', 'want', 'a', 'pizza', '.']])

    def test_tokenize_sentence_with_multiword(self):
        tokens = self.lambo_tokenizer.tokenize('I don\'t like apples.')
        self.assertListEqual([t.text for t in tokens],
                             ['I', 'don\'t', 'like', 'apples', '.'])
        self.assertListEqual([t.subwords for t in tokens],
                             [[], ['do', 'n\'t'], [], [], []])
