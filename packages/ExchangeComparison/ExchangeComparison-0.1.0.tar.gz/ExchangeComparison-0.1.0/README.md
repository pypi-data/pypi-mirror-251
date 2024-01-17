# similar_rates

This code searches for a range of historical exchange rates that is similar to the specified range. It will gather reference material for predicting future exchange rates. Currencies supported include.

| コード | 国名 | 通貨名 |
|------------|------------------|-------------------------|
| USDJPY=X   | アメリカ         | ドル                    |
| GBPJPY=X   | イギリス         | ポンド                  |
| INRJPY=X   | インド           | ルピー                  |
| IDRJPY=X   | インドネシア     | ルピア                  |
| EGPJPY=X   | エジプト         | ポンド                  |
| AUDJPY=X   | オーストラリア   | ドル                    |
| CADJPY=X   | カナダ           | ドル                    |
| KRWJPY=X   | 韓国             | ウォン                  |
| KWDJPY=X   | クウェート       | ディナール              |
| COPJPY=X   | コロンビア       | ペソ                    |
| SARJPY=X   | サウジアラビア   | リヤル                  |
| SGDJPY=X   | シンガポール     | ドル                    |
| CHFJPY=X   | スイス           | フラン                  |
| SEKJPY=X   | スウェーデン     | クローナ                |
| THBJPY=X   | タイ             | バーツ                  |
| TWDJPY=X   | 台湾             | ドル                    |
| CNYJPY=X   | 中国             | 元                      |
| CLPJPY=X   | チリ             | ペソ                    |
| DKKJPY=X   | デンマーク       | クローネ                |
| TRYJPY=X   | トルコ           | リラ                    |
| NZDJPY=X   | ニュージーランド   | ドル                    |
| NOKJPY=X   | ノルウェー       | クローネ                |
| PYGJPY=X   | パラグアイ       | グァラニ                |
| PHPJPY=X   | フィリピン       | ペソ                    |
| BRLJPY=X   | ブラジル         | レアル                  |
| VESJPY=X   | ベネズエラ       | ボリバル・ソベラノ      |
| PENJPY=X   | ペルー           | ソル                    |
| HKDJPY=X   | 香港             | ドル                    |
| MYRJPY=X   | マレーシア       | リンギット              |
| ZARJPY=X   | 南アフリカ       | ランド                  |
| MXNJPY=X   | メキシコ         | ペソ                    |
| AEDJPY=X   | UAE              | ディルハム              |
| EURJPY=X   | 欧州             | ユーロ                  |
| JODJPY=X   | ヨルダン         | ディナール              |
| RONJPY=X   | ルーマニア       | レウ                    |
| LBPJPY=X   | レバノン         | ポンド                  |
| RUBJPY=X   | ロシア           | ルーブル                |

# simple example

One request returns four candidates.

default:
money_kind = 'USDJPY'
date = 'Today'
days = 20

```python
import Exchange

e = Exchange(money_kind='USDJPY')
e.get_exchange(date='2010-01-04',days=20)
```

![output](./output.png "output")
