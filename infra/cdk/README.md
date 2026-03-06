# AWS CDK インフラ定義

## 概要

AWS CDK（Python）によるインフラストラクチャのコード管理です。

## スタック一覧

| スタック | 内容 |
|---|---|
| `ApiStack` | API Gateway + Lambda の定義 |
| `DatabaseStack` | DynamoDB テーブルの定義 |

## セットアップ

```bash
# CDK依存関係のインストール
cd infra/cdk
pip install -r requirements.txt

# スタックの確認
cdk list

# 差分確認
cdk diff

# デプロイ
cdk deploy --all
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|---|---|---|
| CDK_DEFAULT_ACCOUNT | AWSアカウントID | - |
| CDK_DEFAULT_REGION | AWSリージョン | ap-northeast-1 |
