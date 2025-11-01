# SysPL-Dataset (Systematic Propositional Logic Dataset)
This repository contains dataset which used in our research ("Analyzing Systematicity in GPT-2") and a program to generate the data. This dataset is based on the our previous paper「命題論理における言語の構成性に着目した言語モデルの汎化能力の調査」.


## Dataset `data/`
`data/train/` is used for training models, and `data/test/` is used for test.

## Program file `src/`
Program file for building a propositional logic dataset.

### Basic Command

```
python src/dataset_creator.py --n <number of data> --depth <formula depth> --ops <operator list>
```

### Arguments

| Argument | Description | Type | 
| :--- | :--- | :--- | 
| `--n` | Number of data samples to generate. | `int` |
| `--depth` | Maximum depth of the logical formulas to generate. | `int` |
| `--ops` | Logical operators to use. Select from `and`, `or`, `imply`, `not`, and specify separated by spaces. | `str` | 

## Usage Example
```
python src/dataset_creator.py --n 200 --depth 4 --ops and or
```
