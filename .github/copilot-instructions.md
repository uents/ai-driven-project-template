# Copilot グローバル指示

## プロジェクト概要

本プロジェクトは、AWS上にサーバーレスアーキテクチャで構築されるマイクロサービスシステムです。

## 技術スタック

- **言語**: Python 3.13
- **クラウド**: AWS（Lambda, API Gateway, DynamoDB, EventBridge）
- **IaC**: AWS CDK (Python)
- **CI/CD**: GitHub Actions

## 共通ルール

- ディレクトリ名・ファイル名は原則として英数字（ハイフン、アンダースコア含む）のみを使用すること
- ファイルの文字コードは UTF-8、改行コードは LF を使用すること
- 関数・変数の命名は英語で行うこと
- コメント文は日本語で記述すること
- すべてのパブリック関数にはdocstringを記述すること
- エラーハンドリングは必ず行い、適切なログを出力すること
- 機密情報はハードコードせず、環境変数またはAWS Secrets Managerを使用すること

## ドキュメント参照

- ビジネス要件: `docs/requirements/business.md`
- システム要件: `docs/requirements/system.md`
- アーキテクチャ概要: `docs/architecture/overview.md`
- 用語集: `docs/glossary.md`
- API契約: `contracts/api/openapi.yml`
- DynamoDBテーブル定義: `contracts/database/table-definitions.yml`
