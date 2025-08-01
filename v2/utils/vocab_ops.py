"""Vocabulary operations"""

import json
from typing import Dict, List
from constants import VOCAB_PATH


def insert_special_tokens(vocab: Dict[str, int], special_tokens: List[str]):
    """Initialize special tokens if exist"""

    for idx, token in enumerate(special_tokens):
        vocab[token] = idx

    return vocab


def save_vocab(vocab: Dict[str, int], fpath: str):
    """Save vocabulary to file"""
    # json.dump can not serialize bytes object
    serialized_vocab = {str(k) if isinstance(k, bytes) else k: v for k,v in vocab.items()}
    try:
        with open(fpath, "w", encoding="utf-8") as file:
            json.dump(serialized_vocab, file)
    except IOError as e:
        print(f"Error saving vocabulary to file {fpath}: {e}")


def init_vocab(fpath: str, special_tokens: List[str]):
    """Initialize vocabulary with raw bytes and special tokens"""

    vocab = {}
    idx = -1

    if special_tokens is not None:
        vocab = insert_special_tokens(vocab, special_tokens)
        idx = max(vocab.values())

    byte_vocab = {bytes([i]): i + idx + 1 for i in range(256)}
    vocab.update(byte_vocab)

    save_vocab(vocab, fpath)

def update_vocab(vocab_update: Dict[bytes, int]):
    """Writes the updated vocabulary to the vocabulary file"""
    current_vocab = load_vocab(VOCAB_PATH)
    current_vocab.update(vocab_update)
    save_vocab(current_vocab, VOCAB_PATH)


def load_vocab(fpath: str):
    """Returns existing vocabulary from the file in json object format"""
    with open(fpath, "r", encoding="utf-8") as file:
        return json.load(file)