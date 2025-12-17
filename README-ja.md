[English README is here](https://github.com/MiyamoriLab/SysPL-Dataset/blob/main/README.md)

# SysPL-Dataset (Systematic Propositional Logic Dataset)
このレポジトリには『GPT-2における体系性の分析』で使用したデータと，データ作成のためのプログラムが含まれています． 

SysPL-Datasetは言語モデルの記号推論における体系性を調査するためのデータセットです(『命題論理における言語の構成性に着目した言語モデルの汎化能力の調査』において提案)．具体的には，言語モデルが学習時に獲得した基本的な命題論理の推論能力を，より複雑な命題においても応用できるかを調査するために設計されたデータセットです．

## データセット `data/`
実験で使用したデータが含まれています．
`data/train/` は使用した学習データ，`data/test/` は使用したテストデータです．

## プログラム `src/`
データ作成のためのプログラムが含まれています．プログラムは指定された引数 (データ数，深さ，論理演算子) に基づいて命題論理の整式を作成します．出力形式はJSONファイルです．

### 基本コマンド
```
python src/dataset_creator.py --n <number of data> --depth <formula depth> --ops <operator list>
```

### 引数

| 引数 | 説明 | データ型 | 
| :--- | :--- | :--- | 
| `--n` | データ数． | `int` |
| `--depth` | 整式の深さ | `int` |
| `--ops` | 使用する論理演算子．`and`, `or`, `imply`, `not`の4つに対応．複数選択の場合は演算子の間にスペースが必要．| `str` | 

## コマンド例
以下に，連言(∧)と選言(∨)を使用した深さ4の命題論理の整式を200個作成するコマンド例を示します．
```
python src/dataset_creator.py --n 200 --depth 4 --ops and or
```
