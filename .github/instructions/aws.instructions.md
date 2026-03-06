---
applyTo: "**/*.py,infra/**,**/*.ts"
---

# AWS 指示

## Lambda

- Lambda関数は必ず AWS Lambda Powertools for Python を使用すること
- Logger, Tracer, Metrics の3つを標準で組み込むこと
- ハンドラー関数には `@logger.inject_lambda_context` デコレータを付与すること
- コールドスタートを意識し、グローバルスコープでの初期化を活用すること

## DynamoDB

- boto3のDynamoDB Resourceではなく、Tableリソースを使用すること
- テーブル定義は `contracts/database/table-definitions.yml` を参照すること
- アクセスパターンは `contracts/database/access-patterns.md` を参照すること
- Single Table Design を採用しているため、PK/SKの設計パターンに従うこと

## CDK

- CDK のスタック定義は `infra/cdk/stacks/` 配下に配置すること
- L2 Construct を優先的に使用すること
- リソースの命名規則: `{プロジェクト名}-{環境}-{リソース名}`

## EventBridge

- イベントスキーマは `contracts/events/schemas/` に定義されたJSON Schemaに準拠すること
- イベントソースは `custom.{サービス名}` の形式とすること
