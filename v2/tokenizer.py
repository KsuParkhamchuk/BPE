from typing import List
from multiprocessing import freeze_support
from utils.vocab_ops import init_vocab
from utils.pretokenization import process_file

sample = 'Once upon a time, in a land full of trees, there was a little cherry tree. The cherry tree was very sad because it did not have any friends. All the other trees were big and strong, but the cherry tree was small and weak. The cherry tree was envious of the big trees. One day, the cherry tree felt a tickle in its branches. It was a little spring wind. The wind told the cherry tree not to be sad. The wind said, "You are special because you have sweet cherries that everyone loves. The cherry tree started to feel a little better.As time went on, the cherry tree grew more and more cherries. All the animals in the land came to eat the cherries and play under the cherry tree. The cherry tree was happy because it had many friends now. The cherry tree learned that being different can be a good thing. And they all lived happily ever after.'


class BPETokenizer:
    def __init__(self, input_path: str, vocab_size: int, special_tokens: List[str]):
        self.input_path = input_path
        self.vocab_size = vocab_size
        self.special_tokens = special_tokens

    def train(self):
        vocab = init_vocab('vocab.json', self.special_tokens)
        pretokenized = process_file(self.input_path)

    def encode(self):
        pass

    def decode(self):
        pass

if __name__ == "__main__":
    freeze_support()
    tokenizer = BPETokenizer('data/TinyStoriesV2-GPT4-valid.txt', 10, ['<|endoftext|>'])
    tokenizer.train()