# yolo-hipster

Naive Bayes taxonomy classifier using scikit-learn

[Hipster Bayes](http://i.imgur.com/A23ztMl.png)

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

I modified the taxonomy table to look like a real CSV file. It looks like this:

```
"","Domain","Phylum","Class","Order","Family","Genus","Species","OTU"
"unclassified_reads","","","","","","","","unclassified_reads"
"367523","Bacteria","Bacteroidetes","Flavobacteriia","Flavobacteriales","Flavobacteriaceae","Flavobacterium","","367523"
"187144","Bacteria","Firmicutes","Clostridia","Clostridiales","","","","187144"
"836974","Bacteria","Cyanobacteria","Chloroplast","Cercozoa","","","","836974"
"310669","Bacteria","Firmicutes","Clostridia","Clostridiales","","","","310669"
"823916","Bacteria","Proteobacteria","Gammaproteobacteria","Pseudomonadales","Moraxellaceae","Enhydrobacter","","823916"
"878161","Bacteria","Acidobacteria","Acidobacteriia","Acidobacteriales","Acidobacteriaceae","Terriglobus","","878161"
"3064251","Bacteria","Verrucomicrobia","Opitutae","Puniceicoccales","Puniceicoccaceae","Puniceicoccus","","3064251"
"1138555","Bacteria","Firmicutes","Clostridia","Clostridiales","Caldicoprobacteraceae","Caldicoprobacter","","1138555"
```

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

`pip install -r requirements.txt`
