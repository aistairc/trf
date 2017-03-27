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
TRFは大きく分けて、基本指標、語彙に基づく指標、統語情報に基づく指標、言語モデルに基づく指標の4種類をサポートしています。
現在サポートしている指標の一覧とその説明は、下記の通りです。

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
| 語彙の難易度|       right |    center    |
| aligned    |     aligned |   aligned    |

### 統語情報に基づく指標

| 指標名 | 指標の説明 | Center align |
|:-----------|:-----------|:------------:| 
| 語彙の難易度|       right |    center    |
| aligned    |     aligned |   aligned    | 

### 言語モデルに基づく指標

| 指標名 | 指標の説明 | Center align |
|:-----------|:-----------|:------------:| 
| 語彙の難易度|       right |    center    |
| aligned    |     aligned |   aligned    |  

## Reference
本ツールについて、さらに詳細な情報が知りたい場合は、下記をご参照ください。
(言語処理学会原稿)
