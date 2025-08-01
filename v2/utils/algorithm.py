"""Core merging algorithm (optimized)"""
from typing import Dict, List, Tuple
from collections import Counter

from utils.vocab_ops import update_vocab

class BPEAlgorithm:
    def __init__(self):
        self.pair_counts = Counter()
        self.pair_positions: Dict[Tuple, List[Tuple[int, int]]] = {}
        self.vocab_size = 256
        self.merged_tokens: Dict[bytes, int] = {}

    def start(self, text: List[str], merges_num):
        encoded_text = [list(token.encode("utf-8")) for token in text]
        merges = []

        # initial pair count
        for idx, token in enumerate(encoded_text):
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

            best_count = self.pair_counts.most_common(1)[0]
            best_pair, _ = best_count

            self.merge_and_update_counts(encoded_text, best_pair, new_token_id)
            merges.append(best_pair)

        update_vocab(self.merged_tokens)

    def merge_and_update_counts(self, encoded_text, best_pair: Tuple[int, int], new_token_id: int):
        positions = list(self.pair_positions.pop(best_pair, []))
        del self.pair_counts[best_pair]
        print(best_pair)
        self.merged_tokens[bytes(best_pair)] = new_token_id

        # Group positions by token index to process each token separately
        positions_by_token = {}
        for idx, pos in positions:
            if idx not in positions_by_token:
                positions_by_token[idx] = []
            positions_by_token[idx].append(pos)

        # reversed is used to avoid index shifting mess up
        for idx, pos_list in positions_by_token.items():
            affected_str = encoded_text[idx]
            
            # Sort positions in descending order to avoid index shifting issues
            for pos in sorted(pos_list, reverse=True):
                # Check if position is still valid (list might have been shortened by previous merges)
                if pos + 1 >= len(affected_str):
                    continue
                
                # Check if the pair still exists at this position
                if (affected_str[pos], affected_str[pos + 1]) != best_pair:
                    continue

                # Capture neighboring pairs before merge
                left_pair = (affected_str[pos-1], affected_str[pos]) if pos > 0 else None
                right_pair = (affected_str[pos+1], affected_str[pos + 2]) if pos + 2 < len(affected_str) else None

                # Perform the merge
                affected_str[pos] = new_token_id
                del affected_str[pos + 1]

                # Update statistics
                self._update_affected_pos(affected_str, idx, pos, left_pair, right_pair, new_token_id)

    def _update_affected_pos(self, affected_str: List[int], idx: int, pos: int, left_pair: Tuple[int, int], right_pair: Tuple[int, int], new_token_id: int):
        # Decrement neighbour counts
        if left_pair:
            self.pair_counts[left_pair] -= 1
            if left_pair in self.pair_positions:
                self.pair_positions[left_pair].remove((idx, pos-1))

        if right_pair:
            self.pair_counts[right_pair] -= 1
            if right_pair in self.pair_positions:
                self.pair_positions[right_pair].remove((idx, pos+1))

        # Create new counts
        if pos > 0:
            new_left = (affected_str[pos - 1], new_token_id)
            self.pair_counts[new_left] += 1
            self.pair_positions.setdefault(new_left, []).append((idx, pos-1))

        if pos + 1 < len(affected_str):
            new_right = (new_token_id, affected_str[pos + 1])
            self.pair_counts[new_right] += 1
            self.pair_positions.setdefault(new_right, []).append((idx, pos))

        





    

