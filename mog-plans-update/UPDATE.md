# mogフォトワーク 更新方法

既存の静的HTMLサイトを拡張したものです。外部ライブラリやJavaScriptの実行は不要です。

## GitHubへ反映

1. mog-plans-update.zipを展開します。
2. https://github.com/mog-photo/mog-photo.github.io を通常のブラウザで開きます。
3. mainブランチのルートで「Add file」→「Upload files」を開きます。
4. 展開したフォルダの**中身をすべて**アップロードします。フォルダ自体を一段追加しないでください。
5. 「Commit changes」で保存します。
6. ActionsでPagesの公開処理が完了した後、https://mog-photo.github.io/ を確認します。

最低限必要な更新ファイルはindex.html、styles.css、business.html、facilities.htmlです。既存のmog-logo.pngと20251213秋山様4254.jpgは同一ファイルを再利用しています。README.mdの上書きや既存画像の削除は不要です。

## 料金や内容の変更

plans.jsonを編集し、このフォルダで次を実行します。

```sh
python3 build.py
```

料金・枚数・プラン内容・予約URLはplans.jsonで管理します。生成したHTMLも一緒にGitHubへアップロードしてください。JSONだけ更新しても公開ページは変わりません。

文章・ページ構成はtemplates/、見た目はstyles.cssで調整します。生成済みHTMLへの直接編集は、次のビルドで消えるため避けてください。

## 撮影シーンの写真

scene-images.jsonのshichigosanとdogは現在nullです。適切な作例がないため、代替画像は表示していません。

作例を追加する場合は、画像ファイルを配置し、対象のnullを次の形式に置き換えてビルドします。

```json
{"src":"images/shichigosan.jpg","alt":"写真の内容を具体的に説明","width":1600,"height":1067}
```

widthとheightは実際の画像寸法に合わせてください。掲載許可を確認した写真を使用します。

## 予約と決済

この更新はSquare・公式LINEへのリンクを整えます。Square側のサービス登録、価格、予約枠、事前決済設定を自動変更するものではありません。サイト掲載プランとSquare側の内容をそろえて運用してください。
