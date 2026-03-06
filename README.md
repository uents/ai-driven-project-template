# ai-driven-project-template

GitHub Copilot Agentを活用したAI駆動開発に最適化されたプロジェクトテンプレートです。

## 技術スタック

- **言語**: Python 3.13
- **クラウド**: AWS（Lambda, API Gateway, DynamoDB, EventBridge）
- **IaC**: AWS CDK (Python)
- **CI/CD**: GitHub Actions

## セットアップ

```bash
# リポジトリのクローン
git clone <repository-url>
cd ai-driven-project-template
```

```bash
# 開発環境のセットアップ
task setup
```

## 主要コマンド

```bash
task lint          # Lintの実行
task format        # コードフォーマット
task test          # ユニットテストの実行
task test:integration  # 統合テストの実行
task test:e2e      # E2Eテストの実行
task cdk:deploy    # インフラのデプロイ
```

## ディレクトリ構成

| ディレクトリ | 内容 |
|---|---|
| `.github/` | Copilot指示、エージェント定義、CI/CD |
| `docs/` | 要件定義、アーキテクチャ、ADR、用語集 |
| `contracts/` | API定義、イベントスキーマ、DB定義 |
| `services/` | マイクロサービスの実装 |
| `tests/` | 統合テスト、E2Eテスト |
| `research/` | 技術検証・PoC |
| `tools/` | 運用支援ツール |
| `infra/` | AWS CDKインフラ定義 |

## ドキュメント

詳細は [docs/README.md](docs/README.md) を参照してください。
