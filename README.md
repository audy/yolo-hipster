# yolo-hipster

Naive Bayes taxonomy classifier using scikit-learn

![Hipster Bayes](http://i.imgur.com/lyUCFzB.png)

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
    --rank Species \
    --output results.csv
```

Results will look like this:

```
,autotrophica,lovleyi,mexicana
1111360,0.34330544871451424,0.3342029967950079,0.3224915544904801
1111372,0.336105138886059,0.3330440720766938,0.3308507890372489
1111409,0.3324123789067556,0.3353478772901851,0.33223974380307053
1111415,0.3341535755430514,0.3334952221444319,0.3323512023125195
1111416,0.33400844665482093,0.33724709216149507,0.3287444611836827
1111421,0.3367241747506031,0.3334891830574319,0.3297866421919595
```

- Row IDs are database OTU names (at rank specified with `--rank`).
- Column IDs are sequences IDs in query FASTA file (from head).

## Installation

Install numpy first because PIP:

`pip install numpy==1.8.2`

Install requirements:

`pip install -r requirements.txt`
