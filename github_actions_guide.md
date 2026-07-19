# GitHub Actionsによる自動実行設定ガイド

このガイドでは、作成したPythonスクリプトをGitHub Actionsを使って毎朝自動実行する手順を説明します。これにより、Manusのクレジットを使わずに、OpenAIとLINEを連携したXポスト自動生成システムを運用できます。

## 1. GitHubリポジトリの作成

まず、Pythonスクリプトを保存するためのGitHubリポジトリを作成します。

1. GitHubにログインし、新しいリポジトリを作成します。
   - リポジトリ名（例: `x-post-line-bot`）は任意です。
   - プライベートリポジトリとして作成することをお勧めします。
2. 作成したリポジトリに、`line_x_post_generator.py` ファイルと、`.env` ファイル（中身は空でOK）をアップロードします。

## 2. GitHub Secretsの設定

APIキーなどの機密情報は、GitHub Actionsのシークレットとして安全に管理します。

1. 作成したGitHubリポジトリのページに移動します。
2. 「Settings」タブをクリックします。
3. 左側のメニューから「Secrets」→「Actions」を選択します。
4. 「New repository secret」ボタンをクリックし、以下のシークレットを追加します。
   - **Name**: `OPENAI_API_KEY`
   - **Value**: あなたのOpenAI APIキー
   - **Name**: `LINE_CHANNEL_ACCESS_TOKEN`
   - **Value**: あなたのLINEチャネルアクセストークン
   - **Name**: `LINE_USER_ID`
   - **Value**: あなたのLINEユーザーID

## 3. GitHub Actionsワークフローファイルの作成

次に、スクリプトを毎朝実行するためのワークフローファイルを作成します。

1. リポジトリのルートディレクトリに `.github/workflows` というディレクトリを作成します。
2. そのディレクトリ内に `main.yml` (ファイル名は任意) という名前のファイルを作成し、以下の内容を記述します。

```yaml
name: Generate X Posts and Send to LINE

on:
  schedule:
    # 毎日午前7時 (UTC) に実行
    # 日本時間だと午前7時 + 9時間 = 午後4時
    # 日本時間の午前7時に実行したい場合は '0 22 * * *' (UTCの午後10時) に設定
    - cron: '0 22 * * *'
  workflow_dispatch: # 手動実行を可能にする

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: pip install openai line-bot-sdk python-dotenv
    - name: Run script
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        LINE_CHANNEL_ACCESS_TOKEN: ${{ secrets.LINE_CHANNEL_ACCESS_TOKEN }}
        LINE_USER_ID: ${{ secrets.LINE_USER_ID }}
      run: python line_x_post_generator.py
```

**cronスケジュールの注意点:**
- `cron: '0 22 * * *'` は、UTC（協定世界時）の午後10時0分に実行されます。これは日本時間（JST）の午前7時0分に相当します。（JST = UTC + 9時間）
- もし実行時間を変更したい場合は、[crontab guru](https://crontab.guru/) などのツールを使ってUTCでの時間を計算してください。

## 4. 動作確認

1. `main.yml` ファイルをリポジトリにコミットしてプッシュします。
2. GitHubリポジトリの「Actions」タブに移動します。
3. 左側のワークフローリストから「Generate X Posts and Send to LINE」を選択します。
4. 「Run workflow」ボタンをクリックすると、手動でワークフローを実行できます。これにより、設定が正しく行われているかすぐに確認できます。
5. スケジュールされた時間になると、自動的にワークフローが実行され、LINEにポスト案が送信されます。

これで、毎朝自動でXポスト案がLINEに届くようになります。
