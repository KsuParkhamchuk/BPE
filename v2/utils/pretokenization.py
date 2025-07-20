import os
import multiprocessing
from multiprocessing import freeze_support
import time
from typing import BinaryIO, List
import regex

PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""


def find_chunk_boundaries(
    file: BinaryIO, desired_num_chunks: int, split_special_token: bytes
) -> list[int]:
    """
    Chunk the file into parts that can be counted independently.
    May return fewer chunks if the boundaries end up overlapping.
    """
    assert isinstance(
        split_special_token, bytes
    ), "Must represent special token as a bytestring"

    # Get total file size in bytes
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    chunk_size = file_size // desired_num_chunks

    # Initial guesses for chunk boundary locations, uniformly spaced
    # Chunks start on previous index, don't include last index
    chunk_boundaries = [i * chunk_size for i in range(desired_num_chunks + 1)]
    chunk_boundaries[-1] = file_size

    mini_chunk_size = 4096  # Read ahead by 4k bytes at a time

    for bi in range(1, len(chunk_boundaries) - 1):
        initial_position = chunk_boundaries[bi]
        file.seek(initial_position)  # Start at boundary guess
        while True:
            mini_chunk = file.read(mini_chunk_size)  # Read a mini chunk

            # If EOF, this boundary should be at the end of the file
            if mini_chunk == b"":
                chunk_boundaries[bi] = file_size
                break

            # Find the special token in the mini chunk
            found_at = mini_chunk.find(split_special_token)
            if found_at != -1:
                chunk_boundaries[bi] = initial_position + found_at
                break
            initial_position += mini_chunk_size

    # Make sure all boundaries are unique, but might be fewer than desired_num_chunks
    return sorted(set(chunk_boundaries))


def remove_special_tokens(chunk: str, sp_token: str) -> List[str]:
    """Remove special tokens after chunking"""

    return chunk.split(sp_token)


def process_chunk_range(chunk_info):
    """
    Extracting a chunk of text based on start and end byte position

    Splitting the chunk by special token as a delimiter

    Pretokenizing list of strings
    """

    fpath, start, end = chunk_info

    with open(fpath, "rb") as f:
        f.seek(start)
        ch = f.read((end - start)).decode("utf-8", errors="ignore")
        ch = remove_special_tokens(ch, "<|endoftext|>")

    return pretokenize(ch)


def pretokenize(chunk: List[str]) -> List[str]:
    return [match.group(0) for story in chunk for match in regex.finditer(PAT, story)]


def process_file(fpath: str):

    with open(fpath, "rb") as f:
        num_processes = multiprocessing.cpu_count()

        boundaries = find_chunk_boundaries(
            f, num_processes, "<|endoftext|>".encode("utf-8")
        )

        chunk_ranges = [(fpath, boundaries[i - 1], boundaries[i]) for i in range(1, len(boundaries))]

        start_par_time = time.time()

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(process_chunk_range, chunk_ranges)

        print(f"parallel time: {time.time() - start_par_time}")

        return [item for chunk in results for item in chunk]


if __name__ == "__main__":
    FPATH = "data/TinyStoriesV2-GPT4-valid.txt"
    freeze_support()
    process_file(FPATH)
