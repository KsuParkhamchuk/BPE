from typing import List
from multiprocessing import freeze_support
from utils.vocab_ops import init_vocab
from utils.pretokenization import process_file
from constants import VOCAB_PATH
from utils.algorithm import BPEAlgorithm

class BPETokenizer:
    def __init__(self, input_path: str, vocab_size: int, special_tokens: List[str]):
        self.input_path = input_path
        self.vocab_size = vocab_size
        self.special_tokens = special_tokens

    def train(self):
        init_vocab('vocab.json', self.special_tokens)
        pretokenized = process_file(self.input_path)
        algo = BPEAlgorithm()
        algo.start(pretokenized, 10)

    def encode(self):
        pass

    def decode(self):
        pass

if __name__ == "__main__":
    freeze_support()
    tokenizer = BPETokenizer(VOCAB_PATH, 5, ['<|endoftext|>'])
    tokenizer.train()