# Route Search

Route Searchは、特定のルート検索アルゴリズムを実装したPythonパッケージです。このパッケージを使用することで、鉄道ネットワークやその他のネットワーク上での最短経路を簡単に見つけることができます。

## 特徴

- 簡単に使える最短経路探索機能。
- 複数のルートオプション。
- カスタマイズ可能な検索パラメータ。

## インストール

このパッケージはPython 3.6以上で動作します。以下のコマンドでインストールできます：

```bash
pip install route_search
```
## 使い方

基本的な使用方法は以下の通りです：

```python
from route_search import create_graph, calculate_shortest_path

# グラフを作成
G = create_graph()

# 最短経路を計算
start_station = '三鷹'
end_station = '大崎'
include_dash = False
path, total_time, compact_lines = calculate_shortest_path(G, start_station, end_station, include_dash)

print(f"最短経路: {path}")
print(f"合計時間: {total_time}")
```