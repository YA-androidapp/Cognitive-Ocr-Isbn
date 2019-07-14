# Cognitive-Ocr-Isbn
---

スマートフォンで撮影した書籍裏表紙画像から、ISBN13っぽい数値文字列を抽出


## Require

### pip

```sh
$ pip install requests matplotlib pillow
```

### Computer Visionのサブスクリプションキー

[Cognitive Services を試す](https://azure.microsoft.com/ja-jp/try/cognitive-services/my-apis/?api=computer-vision) にアクセスし、
エンドポイントとキーの値を取得しておく

## Images

![input](input.jpg 'input')

![result_input](result_input.jpg 'result_input')
