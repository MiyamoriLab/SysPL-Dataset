[日本語版 README はこちら](https://github.com/MiyamoriLab/SysPL-Dataset/blob/main/README-ja.md)

# SysPL-Dataset (Systematic Propositional Logic Dataset)
This repository contains the data used in "Analyzing Systematicity in GPT-2" and the programs for data creation.

The SysPL-Dataset is a dataset for investigating the systematicity of language models in symbolic reasoning, proposed in the paper "命題論理における言語の構成性に着目した言語モデルの汎化能力の調査". Specifically, it is a dataset designed to investigate whether the basic propositional logic inference ability that a language model acquires during training can be applied to more complex propositions.



## Dataset `data/`
This directory contains data used for our experiment.
`data/train/` is used for training models, and `data/test/` is used for test.

## Program file `src/`
Program file for building a propositional logic dataset. The program outputs JSON file based on arguments (data size, depth, and logical operations).

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
The next command is an usage example. The command outputs 200 propositional expressions with depth 4 using "and (∧)", and "or (∨)" operations 
```
python src/dataset_creator.py --n 200 --depth 4 --ops and or
```
