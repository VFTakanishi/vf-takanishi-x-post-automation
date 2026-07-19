# VF高西氏向け X（旧Twitter）自動投稿システム

VF高西様、この度はX（旧Twitter）自動投稿システムのご依頼、誠にありがとうございます。本システムは、OpenAIを活用してX（旧Twitter）の投稿案を生成し、LINE Messaging APIを通じて指定のLINEアカウントへ毎日自動で送信するものです。

## 1. システム概要

本システムは、以下の主要なコンポーネントで構成されています。

*   **OpenAI API**: X（旧Twitter）の投稿案を生成するために使用されます。
*   **LINE Messaging API**: 生成された投稿案を指定のLINEアカウントに送信するために使用されます。
*   **GitHub Actions**: 毎日決まった時間に投稿案の生成と送信を自動実行するためのワークフローを提供します。
*   **GitHub Repository**: システムのコード、設定、実行履歴が管理されます。

## 2. 動作フロー

1.  毎日午前7時（日本時間）にGitHub Actionsが自動的に起動します。
2.  PythonスクリプトがOpenAI APIを呼び出し、X（旧Twitter）の投稿案を生成します。
3.  生成された投稿案は、LINE Messaging APIを通じてVF高西様のLINEアカウントに送信されます。
4.  VF高西様は、LINEで受け取った投稿案を確認し、必要に応じて編集してX（旧Twitter）に投稿できます。

## 3. 設定済み情報

以下の情報がGitHub Secretsに安全に設定されています。

*   `OPENAI_API_KEY`: OpenAI APIへのアクセスキー
*   `LINE_CHANNEL_ACCESS_TOKEN`: LINE Messaging APIへのアクセスキー
*   `LINE_USER_ID`: 投稿案の送信先となるLINEユーザーID

## 4. GitHubリポジトリ

本システムのコードは以下のGitHubリポジトリで管理されています。

[https://github.com/VFTakanishi/vf-takanishi-x-post-automation](https://github.com/VFTakanishi/vf-takanishi-x-post-automation)

## 5. スクリプトの変更方法

投稿内容の調整や機能追加を行いたい場合は、GitHubリポジトリ内の `line_x_post_generator.py` ファイルを編集してください。

1.  上記GitHubリポジトリにアクセスします。
2.  `line_x_post_generator.py` ファイルを開きます。
3.  「Edit this file」ボタン（鉛筆アイコン）をクリックして、コードを編集します。
4.  変更内容をコミット（保存）すると、次回の自動実行から変更が反映されます。

## 6. ワークフローの変更方法

実行時間や依存関係を変更したい場合は、`.github/workflows/main.yml` ファイルを編集してください。

1.  上記GitHubリポジトリにアクセスします。
2.  `.github/workflows/main.yml` ファイルを開きます。
3.  「Edit this file」ボタン（鉛筆アイコン）をクリックして、コードを編集します。
4.  特に `cron: '0 22 * * *'` の部分が実行時間を指定しています（UTC時間で記述されており、日本時間の午前7時に相当します）。
5.  変更内容をコミット（保存）すると、次回の自動実行から変更が反映されます。

## 7. 手動での実行方法

自動実行を待たずにすぐに投稿案を生成・送信したい場合は、GitHub Actionsのワークフローを手動で実行できます。

1.  GitHubリポジトリの「Actions」タブにアクセスします。
2.  左側のワークフローリストから「Daily X Post Generator」を選択します。
3.  「Run workflow」ボタンをクリックし、「Run workflow」を再度クリックすると、すぐに実行が開始されます。

ご不明な点がございましたら、お気軽にお問い合わせください。
