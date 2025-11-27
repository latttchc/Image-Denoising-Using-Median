# PSNR-Based-Analysis プロジェクト紹介

## 概要

本プロジェクトは、画像にノイズを付与し各種フィルタで復元した後、PSNR・SSIM・MSEなどの指標で画質評価を行う解析ツールです。  
Kaggleデータセットの取得や、ノイズ画像の可視化もサポートしています。

---

## ディレクトリ構成
- `main.py`：解析のメインスクリプト
- `test_median.py`：メディアンフィルタの単体テスト
- `config.py`：設定ファイル（指標・画像名・出力設定など）
- `dataset/`：解析対象画像の保存先
- `results/`：解析結果（グラフ・画像）の保存先

---

## 使い方

### 1. 画像の準備

`dataset` フォルダに解析したい画像（例：`Lena-image.png`）を配置します。  
画像名は `config.FILE_NAME` で指定します（拡張子は不要）。

### 2. 設定の変更

`config.py` で解析指標や出力設定を変更できます。

```python
TASK_NAME = 'PSNR'      # 'PSNR', 'SSIM', 'MSE' から選択
FILE_NAME = 'sample-image' # 画像ファイル名（拡張子なし）
SAVE_RESULT = True      # グラフ・画像をresults/に保存
OUTPUT_IMAGE = True     # ノイズ画像も出力
```

### 3. 解析の実行
ノイズ（salt & pepper, gaussian）を付与し、各種フィルタ（median, gaussian, bilateral）で復元
PSNR/SSIM/MSEのグラフとテーブルを表示・保存

### 4. メディアンフィルタ単体テスト
ノイズレベルごとのメディアンフィルタ効果をグラフ化

## 出力内容
- ノイズ種類・フィルタごとの指標推移グラフ（`results`に保存）
- ノイズレベルと指標値のテーブル
- ノイズ画像の比較（`OUTPUT_IMAGE=True`の場合）
  
## 参考ファイル
- 解析メイン：`main.py`
- 設定：`config.py`
- メディアンフィルタテスト：`test_median.py`

## 注意事項
- 画像ファイルは必ず `dataset` に配置してください。
- 解析指標は `config.py` で切り替え可能です。
- 結果は `results` フォルダに保存されます。
