# Image Denoising Using Median, Gaussian and Bilateral Filters

このリポジトリは、画像に人工ノイズを付与し、**メディアンフィルタ・ガウシアンフィルタ・バイラテラルフィルタ**で復元した結果を  
**PSNR / SSIM / MSE / LPIPS** などの指標で体系的に評価・可視化するための解析ツールです。

研究論文に基づく実験コードとして、**ノイズモデルごとのフィルタ特性の比較**や、  
ノイズレベルに対する指標値のトレンドを簡単に再現できるよう設計されています。

---

## 1. 概要

デジタル画像は、撮像デバイスや通信経路の制約により、  
代表的には以下のようなノイズにさらされます。

- **Salt-and-pepper noise**（インパルスノイズ）
  - 画素がランダムに 0 または 255 の極端な値に置き換わるノイズ
- **Gaussian noise**
  - 平均 0、分散 `var` の正規分布に従う値が画素に加算されるノイズ

本プロジェクトでは、これら 2 種類のノイズを **指数スケールで強度を変化させながら付与**し、  
3 種類のクラシカルな空間フィルタによる復元性能を比較します。

適用するフィルタは以下の 3 つです。

- **Median Filter**
- **Gaussian Filter**
- **Bilateral Filter**

評価には **MSE / PSNR / SSIM / LPIPS** を使用します。

---

## 2. 各種機能

- **2 種類のノイズモデル**
  - Salt-and-pepper noise（インパルスノイズ）
  - Gaussian noise（連続値ノイズ）

- **3 種類の空間フィルタ**
  - Median / Gaussian / Bilateral フィルタによる復元

- **複数指標での画質評価**
  - **MSE / PSNR / SSIM / LPIPS** をまとめて算出し、テーブル・グラフで保存

- **ノイズレベルの一括スイープ**
  - ノイズレベルを指数スケールで増加させ、低ノイズ〜高ノイズまでの挙動を一括で解析

- **ノイズ画像の可視化**
  - ノイズ付与前後・フィルタ適用後の画像を `results/` に保存し、視覚的比較が可能

---

## ディレクトリ構成
- `main.py`：解析のメインスクリプト
- `test_median.py`：メディアンフィルタの単体テスト
- `config.py`：設定ファイル（指標・画像名・出力設定など）
- `dataset/`：解析対象画像の保存先
- `results/`：解析結果（グラフ・画像）の保存先

---

## 3. セットアップ
### 1. リポジトリのクローン

```bash
git clone https://github.com/latttchc/Image-Denoising-Using-Median.git
cd Image-Denoising-Using-Median
```

### 2. 必要ライブラリ
- numpy
- opencv-python
- scikit-image
- matplotlib
- lpips


---

## 4. 使用方法

### 1. 画像の準備

`dataset` フォルダに解析したい画像（例：`sample-image.png`）を配置します。  

### 2. 設定の変更

`config.py` で解析指標や出力設定を変更できます。

```python
TASK_NAME = 'PSNR'      # 'PSNR', 'SSIM', 'MSE' 'LPIPS' から選択
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
