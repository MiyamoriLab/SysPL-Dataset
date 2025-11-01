# SysPL-Dataset (Systematic Propositional Logic Dataset)
This repository contains dataset which used in our research and program to generate the data.


## Dataset
`data/`.
`data/train/` is used for training models, and `data/test/` is used for test.

Here's the English version of the documentation:

## Program file
`src/`. Program file for building a propositional logic dataset.

### Basic Command

```
python src/dataset_creator.py --n <number of data> --depth <formula depth> --ops <operator list>
```

### Arguments

| Argument | Description | Type | Example |
| :--- | :--- | :--- | :--- |
| `--n` | Number of data samples to generate. | `int` | |
| `--depth` | Maximum depth of the logical formulas to generate. | `int` | |
| `--ops` | Logical operators to use. Select from `and`, `or`, `imply`, `not`, and specify separated by spaces. | `str` | `and or` |

## Usage Example
```
python src/dataset_creator.py --n 200 --depth 4 --ops and or
```
