# yolo-hipster

Naive Bayes taxonomy classifier using scikit-learn

## Usage

```
Usage: yoloh classify [OPTIONS]

Options:
  --training-sequences TEXT  training sequences. hint: use greengenes.
  --query-sequences TEXT     query sequences in fasta format
  --taxonomies TEXT          training taxonomies. hint: use greengenes.
  --output TEXT              where to save trained model.
  --rank TEXT                taxonomic rank to train at
  --ngram-range INTEGER...
  --help                     Show this message and exit.
```

## Example

(using GreenGenes 13.5)

```sh
bin/yoloh classify \
    --training-sequences test.fasta \
    --query-sequences test.fasta \
    --taxonomies greengenes-taxonomies.csv \
    --rank Species
```

## Installation

Install numpy first because PIP:

`pip install numpy==1.8.2`

Install requirements:

`pip install requirements.txt`
