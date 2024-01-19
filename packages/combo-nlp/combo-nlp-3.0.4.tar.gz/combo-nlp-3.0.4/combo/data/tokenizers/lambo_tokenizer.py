from typing import List, Optional

from lambo.segmenter.lambo import Lambo

from combo.config import Registry
from combo.config.from_parameters import register_arguments
from combo.data.tokenizers.token import Token
from combo.data.tokenizers.tokenizer import Tokenizer


@Registry.register('lambo_tokenizer')
class LamboTokenizer(Tokenizer):
    @register_arguments
    def __init__(
            self,
            language: str = "English",
            default_turns: bool = False,
            default_split_subwords: bool = False
    ):
        self._language = language
        self.__tokenizer = Lambo.get(language)
        self.__default_turns = default_turns
        self.__default_split_subwords = default_split_subwords

    def tokenize(self, text: str) -> List[Token]:
        """
        Simple tokenization - ignoring the sentence splits
        :param text:
        :return:
        """
        document = self.__tokenizer.segment(text)
        tokens = []

        for turn in document.turns:
            for sentence in turn.sentences:
                for token in sentence.tokens:
                    tokens.append(Token(token.text, subwords=token.subwords))

        return tokens

    def segment(self, text: str, turns: Optional[bool] = None, split_subwords: Optional[bool] = None) -> List[List[str]]:
        """
        Full segmentation - segment into sentences.
        :param text:
        :param turns: segment into sentences by splitting on sentences or on turns. Default: sentences.
        :return:
        """

        turns = turns or self.__default_turns
        split_subwords = split_subwords or self.__default_split_subwords

        document = self.__tokenizer.segment(text)
        sentences = []
        sentence_tokens = []

        for turn in document.turns:
            if turns:
                sentence_tokens = []
            for sentence in turn.sentences:
                if not turns:
                    sentence_tokens = []
                for token in sentence.tokens:
                    if len(token.subwords) > 0 and split_subwords:
                        sentence_tokens.extend([s for s in token.subwords])
                    else:
                        sentence_tokens.append(token.text)
                if not turns:
                    sentences.append(sentence_tokens)
            if turns:
                sentences.append(sentence_tokens)

        return sentences
