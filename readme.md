# 音声感情分析アプリ

# 概要

このプロジェクトは、音声認識と自然言語処理を活用して、日本語の音声に含まれる感情を分析するアプリケーションです。
音声ファイルをアップロードする,もしくはその場で録音することで、その内容の文字起こしと、検出された感情の内訳を確認できます。
 OpenAIの強力な Whisper モデルを使用して、日本語の音声ファイルを文字起こしできるのが特徴です。

# 開発ツールインストール


- 管理者権限でコマンドプロンプトを起動します。

- 以下のコマンドを実行し、必要なソフトウェアを入手します。

```
winget install --id Git.Git -e --source winget
winget install --id Python.Python.3 -e --source winget
winget install --id Microsoft.VisualStudioCode -e --source winget
```

# 環境セットアップ

## Python ライブラリインストール

- 以下のコマンドでPythonの利用ライブラリをインストールします。

  ``` 
      pip install -r requrements.txt 
      pip install Flask
      pip install Flask-Cors
      pip install openai-whisper
      pip install transformers
      pip install "fugashi[unidic-lite]" protobuf
      pip install sentencepiece
  ```
## ffmpegのインストール&環境変数を編集

	Cドライブ直下に```ffmpeg```ファイルを新規作成します。
	ffmpegをダウンロードします。
	ファイルを解凍し、中身を作成したファイルに移動します。
	スタートメニューの検索から「環境変数を編集」と検索し、これを開きます。
	<font color="gray">*ユーザー名*</font>のユーザー環境変数の一覧から変数:Pathを選択し、編集をクリックします。
	新規をクリックして、以下のように入力します。
	```
			C:\ffmpeg\bin
	```
	OKをクリックして環境変数を閉じます。

## Node.jsのインストール

 Node.jsの公式サイトにアクセスしてLTS版をダウンロードして、インストーラをダウンロードしてください。
 Add to PATH という項目にチェックが入っていることを確認してください。

# 実行方法

- ２つのコマンドプロンプトを起動します。

- １つ目のコマンドプロンプトでは、以下のコマンドを実行します。

```
	cd .\backend
	venv\Scripts\activate
	python app.py
```

- ２つ目のコマンドプロンプトでは、以下のコマンドを実行します。

``` 
  cd .\frontend
  npm run dev
```

- ブラウザで以下のURLにアクセスしてみてください。

  ``` http://localhost:5173 ```


# 参考リンク

- [Flask](https://flask.palletsprojects.com/en/stable/)

  - Python で書かれた Webアプリケーションサーバ

- [Vue.js](https://vuejs.org/)

  - JavaScript製製のWebフロントエンド フレームワーク

- [Vue.js Tutorial](https://ja.vuejs.org/tutorial/)

  - Vue.jsの入門用チュートリアル
  
- [OpenAI API](https://github.com/openai/openai-python)

  - Pythonから、OpenAI APIを呼び出すライブラリ

- [ffmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)

  - 音声をAIが処理可能なフォーマットに変換するためのライブラリをダウンロードするサイト

- [Node.js](https://nodejs.org/ja)

 - npmを使えるようにするようインストールするNode.jsの公式サイト
