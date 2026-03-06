# AWS CDK インフラ定義

## 概要

AWS CDK（TypeScript）によるインフラストラクチャのコード管理です。

## スタック一覧

| スタック | 内容 |
|---|---|
| `ApiStack` | API Gateway + Lambda の定義 |
| `DatabaseStack` | DynamoDB テーブルの定義 |

## ディレクトリ構成

```
infra/cdk/
├── bin/
│   └── app.ts          # CDK アプリケーション エントリポイント
├── lib/
│   └── stacks/
│       ├── api-stack.ts       # API Gateway + Lambda
│       └── database-stack.ts  # DynamoDB
├── cdk.json
├── package.json
└── tsconfig.json
```

## セットアップ

```bash
# CDK依存関係のインストール
cd infra/cdk
npm install

# ビルド
npm run build

# スタックの確認
npx cdk list

# 差分確認
npx cdk diff

# デプロイ
npx cdk deploy --all
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|---|---|---|
| CDK_DEFAULT_ACCOUNT | AWSアカウントID | - |
| CDK_DEFAULT_REGION | AWSリージョン | ap-northeast-1 |
