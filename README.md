# TRF
TRFは、与えられた日本語テキストに対して、種々の読みやすさ指標を自動で計算し、出力するツールです。

## Requirements

+ Python 3.6+
+ [Juman](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN), [KNP](http://nlp.ist.i.kyoto-u.ac.jp/index.php?KNP) and [PyKNP](http://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP)

## インストール

```bash
git clone https://github.com/aistairc/trf.git
cd trf
./install-dependencies.sh
./download-resources.sh
pip install .
export PATH="${PATH}:$(pwd)/tools/bin"
```

## 使用例

テキストファイルを指定して実行する場合
```bash
trf -f FILENAME
```

テキストを直接与えて実行する場合
```bash
echo 'ごはんを食べました。' | trf
```


## TRFがサポートする指標一覧
TRFは大きく分けて、`基本指標`、`語彙に基づく指標`、`統語情報に基づく指標`、`言語モデルに基づく指標`の4種類をサポートしています。
現在サポートしている指標の一覧とその説明は、下記の通りです。

### 基本指標

| 指標名 | 指標の説明 |
|:-----------|:-----------|
| 文数       | テキストに含まれる文の総数   |
| 平均文長   | 各文に含まれる形態素数の平均 |
| トークン数 | テキストに含まれる単語のトークン数 |
| タイプ数   | テキストに含まれる単語のタイプ数 |

### 語彙に基づく指標

| 指標名 | 指標の説明 |
|:-----------|:-----------|
| 品詞 | テキストに含まれる単語の品詞の割合 |
| 語彙の具体度 | テキストに含まれる名詞の上位語数の割合 |

### 統語情報に基づく指標

| 指標名 | 指標の説明 |
|:-----------|:-----------|
| 仮定節 | 仮定節が含まれる文の割合 |
| 係り受け木の深さ | 各文の係り受け木の深さの最大値の平均 |
| モダリティ | 各種モダリティが含まれる文の割合 |

### 言語モデルに基づく指標

| 指標名 | 指標の説明 |
|:-----------|:-----------|
| 言語モデルの尤度 | 各文の言語モデルの対数尤度の平均 |
| 容認度 | 各文の容認度スコアの平均 |

## Reference
本ツールについて、さらに詳細な情報が知りたい場合は、
「TRF: テキストの読みやすさ解析ツール」[[PDF](http://www.anlp.jp/proceedings/annual_meeting/2017/pdf_dir/P6-6.pdf)] をご参照ください。

```tex
@inproceedings{watanabe2017,
  author={渡邉亮彦 and 村上聡一朗 and 宮澤彬 and 五島圭一 and 柳瀬利彦 and 高村大也 and 宮尾祐介},
  title={{TRF}: テキストの読みやすさ解析ツール},
  booktitle={言語処理学会第23回年次大会発表論文集},
  year={2017},
  pages={477--480}
}
```
