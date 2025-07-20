## BPE Tokenize

**v2 stores the lates version and a more efficient implementation of BPE tokenizer**.

The previous version and naive implementation is in archive. The archive also includes scrapping scripts and experiments with a domain specific tokenizer.

### Data 

The new version of tokenizer is supposed to be trained on the following datasets:
- TinyStories train
- TinyStories validation
- OpenWebText train
- OpenWebText valid

Use this to download:

```
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-train.txt
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-valid.txt

wget https://huggingface.co/datasets/stanford-cs336/owt-sample/resolve/main/owt_train.txt.gz
gunzip owt_train.txt.gz
wget https://huggingface.co/datasets/stanford-cs336/owt-sample/resolve/main/owt_valid.txt.gz
gunzip owt_valid.txt.gz
```