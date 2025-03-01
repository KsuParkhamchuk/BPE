from bpe_tokenizer import BPETokenizer
from datasets import process_arrow, process_csv, process_scraped_text
from time import time


def train_general():
    general_tokenizer = BPETokenizer()
    preprocessed_data = process_arrow(12, "datasets/wikitext/train1.arrow")
    general_tokenizer.train(preprocessed_data)
    # encoded = general_tokenizer.encode(b"Hello world!")
    # decoded = general_tokenizer.decode(encoded)
    # print(encoded)
    # print(decoded)


def train_domain_specific():
    domain_specific_tokenizer = BPETokenizer()
    recipengl_data = process_csv()
    pubmed_data = process_scraped_text()
    combined_data = recipengl_data + pubmed_data
    domain_specific_tokenizer.train(combined_data)


def __main__():
    start = time()
    train_domain_specific()
    print(f"Training took: {time()-start:.2f} seconds")


__main__()
