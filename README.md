# workout_app


筋力トレーニングとランニングの記録を保存・管理するために作成した、
Python / Flet製のデスクトップアプリです。

PythonとGUIアプリ開発の学習を目的として制作しました。

## Features

- 筋トレ（外部重量）の記録
- 筋トレ（自重）の記録
- ランニングの記録
- RPEの記録
- 記録の編集
- 記録の削除
- 日付ごとのグループ表示
- 日付ごとの折り畳み
- JSONによるデータ保存
- アプリ再起動後もデータを保持

## Training Data

### 筋トレ・外部重量

- 日付
- RPE
- 種目
- 回数
- セット数
- 重量

### 筋トレ・自重

- 日付
- RPE
- 種目
- 回数
- セット数

### ランニング

- 日付
- RPE
- 距離
- 走行時間
- 休憩時間
- ラップ数

## Technologies

- Python
- Flet
- JSON
  
  
Windows用EXEはGitHub Releasesから配布予定です。

Pythonをインストールしていない環境でも実行できます。


## Current limitations
 v0.1では以下は未実装です。

- ウィンドウサイズの保存
- 小さいウィンドウへの最適化
- トレーニング履歴の分析
- グラフ表示
- 種目別の比較

今後、記録したデータを利用した分析機能を追加する予定です

## Run from source

Python環境にFletをインストールします。

```bash
pip install -r requirements.txt

その後、アプリを実行します。

python workout_app_v0.1.py



