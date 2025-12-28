[日本語版 README はこちら](https://github.com/MiyamoriLab/SysPL-Dataset/blob/main/README-ja.md)

# SysPL-Dataset (Systematic Propositional Logic Dataset)
This repository contains the data used in "Analyzing Systematicity in GPT-2" and the programs for data creation.

The SysPL-Dataset is a dataset for investigating the systematicity of language models in symbolic reasoning, proposed in the paper "Analyzing Systematicity in GPT-2" (in Japanese). Specifically, it is a dataset designed to investigate whether the basic propositional logic inference ability that a language model acquires during training can be applied to more complex propositions.



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
The following command generates 200 propositional logic expressions with depth 4 using the logical operators "and (∧)" and "or (∨)".
```
python src/dataset_creator.py --n 200 --depth 4 --ops and or
```
## How to Cite
When using any datasets or code included in this repository, please cite the following paper.

```
@article{Inoue2026SystematicityGPT2,
  author  = {Ryosuke Inoue and Hisashi Miyamori},
  title   = {Analyzing Systematicity in GPT-2},
  journal = {IPSJ Transactions on Database},
  volume  = {19},
  number  = {1},
  pages   = {1--16},
  year    = {2026},
  language = {Japanese}
}
```
