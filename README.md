# TRF
TRFは、与えられた日本語テキストに対して、種々の読みやすさ指標を自動で計算し、出力するツールです。

## Requirements

+ Python 2.7+, 3.6+
+ KNP and pyknp
+ Juman
+ numpy
+ six
+ enum

## Installation

```
pip install trf
```

## Examples

### CLI mode 

```
trf -f <filename>
```

### Library

```
import trf
```

## TRFがサポートする指標一覧
TRFは大きく分けて、`基本指標`、`語彙に基づく指標`、`統語情報に基づく指標`、`言語モデルに基づく指標`の4種類をサポートしています。
現在サポートしている指標の一覧とその説明は、下記の通りです。

*語彙の難易度・語種の算出には、日本語教育語彙表(http://jhlee.sakura.ne.jp/JEV.html)を利用しています。語彙の難易度・語種指標を利用する場合は、日本語教育語彙表の利用規約に従ってください。*
*また、jReadabilityについても、こちら（http://jreadability.net/terms_of_use）に利用規約が記載されています。利用する場合は、jReadabilityの利用規約に従ってください。*

### 基本指標

| 指標名 | 指標の説明 | Center align |
|:-----------|:-----------|:------------:|
| 平均文長   | 各文に含まれる形態素数の平均 |     This     |
| 文数       | テキストに含まれる文の総数   |    column    |
| トークン数 | テキストに含まれる単語のトークン数 |     will     |
| タイプ数   | テキストに含まれる単語のタイプ数 |      be      |

### 語彙に基づく指標

| 指標名 | 指標の説明 | Center align |
|:-----------|:-----------|:------------:| 
| 語彙の難易度 | テキストに含まれる単語の難易度の割合 |    center    |
| 語種 | テキストに含まれる単語の語種の割合 |   aligned    |
| 品詞 | テキストに含まれる単語の品詞の割合 |   aligned    | 
| 語彙の具体度 | テキストに含まれる名詞の上位語数の割合 |   aligned    |  

### 統語情報に基づく指標

| 指標名 | 指標の説明 | Center align |
|:-----------|:-----------|:------------:| 
| 仮定節 | 仮定節が含まれる文の割合 |    center    |
| 係り受け木の深さ | 各文の係り受け木の深さの最大値の平均 |   aligned    |
| モダリティ | 各種モダリティが含まれる文の割合 |   aligned    | 

### 言語モデルに基づく指標

| 指標名 | 指標の説明 | Center align |
|:-----------|:-----------|:------------:| 
| 言語モデルの尤度 | 各文の言語モデルの対数尤度の平均 |    center    |
| 容認度 | 各文の容認度スコアの平均 |   aligned    |  

## Reference
本ツールについて、さらに詳細な情報が知りたい場合は、下記をご参照ください。
(言語処理学会原稿)
