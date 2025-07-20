"""Core merging algorithm (optimized)"""
from typing import Dict, List, Tuple
from collections import Counter

class BPEAlgorithm:
    def __init__(self):
        self.pair_counts = Counter()
        self.pair_positions: Dict[Tuple, List[Tuple[int, int]]] = {}
        self.vocab_size = 256

    def start(self, text: List[str], merges_num):
        encoded_text = [bytearray(token.encode("utf-8")) for token in text]
        merges = []

        # initial pair count
        for token, idx in enumerate(encoded_text):
            for pos in range(len(token)-1):
                pair = (token[pos], token[pos + 1])
                self.pair_counts[pair] += 1

                if pair not in self.pair_positions:
                    self.pair_positions[pair] = []
                self.pair_positions[pair].append((idx, pos))

        for n in range(merges_num):
            if not self.pair_counts:
                break
            
            new_token_id = self.vocab_size + n

            best_pair = self.pair_counts.most_common(1)[0]
            self.merge_and_update_counts(encoded_text, best_pair, new_token_id)
            merges.append(best_pair)

    def merge_and_update_counts(self, encoded_text, best_pair: Tuple[Tuple, int], new_token_id: int):
        positions = self.pair_positions[best_pair]

        # reversed is used to avoid index shifting mess up
        for idx, pos in reversed(positions):
            affected_str = encoded_text[idx]

            self.decrement_affected_pos(affected_str, idx, pos)

            updated_str = self.merge_pair(affected_str, pos, new_token_id)
            encoded_text[idx] = updated_str

            self.create_new_pairs(updated_str, idx, pos)

    def decrement_affected_pos(self, affected_str: bytearray, idx: int, pos: int):
        affected_pairs = []

        # if pos is not last in the given word - form a pair (the best pair to merge)
        if pos < len(affected_str) - 1:
            pair = (affected_str[pos], affected_str[pos + 1])
            affected_pairs.append((pair, (idx, pos)))

        # Process left neighbour
        if pos > 0:
            left_pair = (affected_str[pos-1], affected_str[pos])
            affected_pairs.append((left_pair, (idx, pos - 1)))

        # Process right neighbour
        if pos + 1 < len(affected_str) - 1:
            right_pair = (affected_str[pos + 1], affected_str[pos + 2])
            affected_pairs.append((right_pair, (idx, pos + 1)))

        # Decrement pair count because the pairs will be destroyed
        for pair, position in affected_pairs:
            self.pair_counts[pair] -= 1
            self.pair_positions[pair].remove(position)


    def merge_pair(self, affected_str: bytearray, pos: int, new_token_id: int):
        """Merges a pair of bytes at a given position into a new single token ID."""
        affected_str[pos] = new_token_id
        del affected_str[pos + 1]

        return affected_str

    def create_new_pairs(self, affected_str: bytearray, idx: int, pos: int):
        new_pairs = []

        # pair with a left neighbour
        if pos > 0:
            left_pair = (affected_str[pos - 1], affected_str[pos])
            new_pairs.append((left_pair, (idx, pos-1)))

        # pair with a right neighbour
        if pos + 1 < len(affected_str) - 1:
            right_pair = (affected_str[pos], affected_str[pos + 1])
            new_pairs.append((right_pair, (idx, pos+1)))

        for pair, position in new_pairs:
            self.pair_counts[pair] += 1
            self.pair_positions[pair].append(position)





    

