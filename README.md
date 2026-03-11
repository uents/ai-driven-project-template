# ai-driven-project-template

GitHub Copilot Agentを活用したAI駆動開発に最適化されたプロジェクトテンプレートです。

## 技術スタック

- **言語**: Python 3.13
- **クラウド**: AWS（Lambda, API Gateway, DynamoDB, EventBridge）
- **IaC**: AWS CDK (TypeScript)
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

```
├── .github/
│    ├── copilot-instructions.md       # グローバル指示（プロジェクト概要・共通ルール）
│    ├── instructions/                 # 技術領域別の指示（AWS, Python, テスト）
│    ├── agents/                       # エージェント定義（{name}.agent.md）
│    ├── prompts/                      # プロンプトテンプレート
│    ├── skills/                       # エージェントスキル（{skill-name}/SKILL.md）
│    ├── ISSUE_TEMPLATE/               # イシューテンプレート
│    ├── pull_request_template.md      # PRテンプレート
│    └── workflows/                    # ワークフロー定義
│
├── .vscode/
│    ├── settings.json                 # VS Code設定
│    ├── extensions.json               # 推奨VS Code拡張機能
│    └── launch.json                   # デバッグ構成
│
├── docs/
│    ├── requirements/                 # ビジネス要件・システム要件
│    ├── architecture/                 # アーキテクチャ概要・構成図・パターン
│    ├── adr/                          # Architecture Decision Records
│    └── glossary.md                   # 用語集
│
├── contracts/
│    ├── api/                          # OpenAPI定義・リクエスト例
│    ├── events/                       # イベントスキーマ・ペイロード例
│    └── database/                     # テーブル定義・アクセスパターン・ER図
│
├── services/
│    └── user_service/                 # マイクロサービス（機能単位で分離）
│         ├── create_user/             # ユーザー作成
│         │    ├── docs/
│         │    │    └── spec.md        # 機能仕様書
│         │    ├── src/                # 実装コード
│         │    │    ├── handler.py     # Lambdaハンドラー
│         │    │    └── *.py
│         │    └── tests/              # ユニットテスト
│         │         ├── test_*.py
│         │         ├── conftest.py
│         │         └── test.env
│         └── get_user/                # ユーザー取得
│
├── tests/
│    ├── integration/                  # 統合テスト
│    └── e2e/                          # E2Eテスト
│
├── infra/cdk/                         # AWS CDK インフラ定義（TypeScript）
├── research/                          # 技術検証・PoC
├── tools/                             # 運用支援ツール
├── pyproject.toml                     # Python依存関係・ruff・mypy設定
└── Taskfile.yml                       # タスクランナー定義
```

### 各ディレクトリの詳細

<details>
<summary>.github/</summary>

#### グローバル指示

| パス                      | 内容・役割                                                                                                |
| ------------------------- | --------------------------------------------------------------------------------------------------------- |
| `copilot-instructions.md` | プロジェクト全体のコンテキスト・共通ルール。Copilot Agentが全セッションで自動読込する最上位の指示ファイル |

#### instructions/（技術領域別の指示）

技術領域別の指示ファイル群。フロントマターの `applyTo` で対象ファイルを指定し、Copilotが自動適用する。

| パス                                   | 内容・役割                                                   |
| -------------------------------------- | ------------------------------------------------------------ |
| `instructions/aws.instructions.md`     | AWS関連の実装ルール（Lambda, DynamoDB, CDK等の使い方の指示） |
| `instructions/python.instructions.md`  | Pythonコーディング規約・スタイルの指示                       |
| `instructions/testing.instructions.md` | テスト実装時のルール・方針の指示                             |

#### agents/（役割別エージェント定義）

Copilot Agentの役割別ペルソナ定義。タスクに応じてAgentに「誰として振る舞うか」を指示する。`{name}.agent.md` 形式で配置する。

| パス                        | 内容・役割                                           |
| --------------------------- | ---------------------------------------------------- |
| `agents/architect.agent.md` | 設計エージェント：アーキテクチャ判断・設計レビュー用 |
| `agents/developer.agent.md` | 実装エージェント：コード実装用                       |
| `agents/reviewer.agent.md`  | レビューエージェント：コードレビュー用               |
| `agents/tester.agent.md`    | テストエージェント：テスト設計・実装用               |

#### prompts/（プロンプトテンプレート）

繰り返し使うプロンプトのテンプレート。作業品質の標準化に使用。

| パス                      | 内容・役割                                   |
| ------------------------- | -------------------------------------------- |
| `prompts/code-review.md`  | コードレビュー依頼時のプロンプトテンプレート |
| `prompts/bug-fix.md`      | バグ修正依頼時のプロンプトテンプレート       |
| `prompts/feature-impl.md` | 機能実装依頼時のプロンプトテンプレート       |

#### skills/（エージェントスキル）

Agentが参照する知識ベース・リファレンス。各スキルは `{skill-name}/SKILL.md` として配置する。instructionsが「何をすべきか」なら、skillsは「どうやるか」の詳細知識。

| パス                           | 内容・役割                                    |
| ------------------------------ | --------------------------------------------- |
| `skills/git-commit/SKILL.md`   | Conventional Commits 形式のコミットメッセージ |
| `skills/write-adr/SKILL.md`    | Architecture Decision Record の作成方法       |
| `skills/write-readme/SKILL.md` | README.md の構成・記述ルール                  |


#### テンプレート（Issue / PR）

| パス                                | 内容・役割                                                                                |
| ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `ISSUE_TEMPLATE/bug_report.md`      | バグ報告テンプレート（再現手順、環境情報等を構造化して記入）                              |
| `ISSUE_TEMPLATE/feature_request.md` | 機能要望テンプレート（背景・動機、受け入れ条件等を構造化して記入）                        |
| `pull_request_template.md`          | PRテンプレート。HTMLコメントでCopilotへの日本語レビュー指示を埋め込み、PR作成時に自動適用 |

#### workflows/（CI/CD）

| パス               | 内容・役割                            |
| ------------------ | ------------------------------------- |
| `workflows/ci.yml` | CIパイプライン（lint, test, build等） |

</details>

<details>
<summary>docs/</summary>

| パス                       | 内容・役割                                                       |
| -------------------------- | ---------------------------------------------------------------- |
| `README.md`                | ドキュメント全体のナビゲーション・案内                           |
| `requirements/business.md` | ビジネス要件定義（ユースケース、ビジネスルール等）               |
| `requirements/system.md`   | システム要件定義（非機能要件含む：性能、可用性、セキュリティ等） |
| `architecture/overview.md` | アーキテクチャ概要（技術スタック、設計原則）                     |
| `architecture/diagrams/`   | PlantUML形式の構成図（C4モデル）                                 |
| `architecture/patterns.md` | プロジェクトで採用する実装パターン・規約                         |
| `adr/`                     | Architecture Decision Records（技術的意思決定の記録）            |
| `glossary.md`              | ドメイン用語集                                                   |

</details>

<details>
<summary>contracts/</summary>

| パス                             | 内容・役割                                               |
| -------------------------------- | -------------------------------------------------------- |
| `README.md`                      | 契約定義の目的・利用ルール・更新フロー                   |
| `api/openapi.yml`                | OpenAPI仕様。APIの入出力契約                             |
| `api/examples/`                  | リクエスト/レスポンスの具体例                            |
| `events/schemas/`                | イベントのJSON Schema定義。サービス間契約の厳密な型定義  |
| `events/examples/`               | イベントペイロードの具体例                               |
| `database/table-definitions.yml` | DynamoDBテーブル定義（PK/SK、GSI、キャパシティモード等） |
| `database/access-patterns.md`    | DynamoDBアクセスパターン一覧                             |
| `database/er.md`                 | エンティティ関連図（Mermaid形式）                        |

</details>

<details>
<summary>services/</summary>

| パス                                 | 内容・役割                                           |
| ------------------------------------ | ---------------------------------------------------- |
| `{サービス名}/`                      | サービスのルート。マイクロサービス単位のディレクトリ |
| `{サービス名}/{機能名}/docs/spec.md` | 機能の設計書                                         |
| `{サービス名}/{機能名}/src/`         | 機能の実装コード                                     |
| `{サービス名}/{機能名}/tests/`       | 機能のユニットテストコード                           |

</details>

<details>
<summary>tests/</summary>

| パス           | 内容・役割                                         |
| -------------- | -------------------------------------------------- |
| `integration/` | 統合テスト（計画書・仕様書・成績書・テストコード） |
| `e2e/`         | E2Eテスト（計画書・仕様書・成績書・テストコード）  |

</details>

<details>
<summary>その他</summary>

| パス             | 内容・役割                                            |
| ---------------- | ----------------------------------------------------- |
| `infra/cdk/`     | AWS CDKによるインフラ定義（TypeScript）               |
| `research/`      | 技術検証・PoC                                         |
| `tools/`         | システム運用支援ツール（migration, monitoring）       |
| `.vscode/`       | VS Code設定（settings, extensions, launch）           |
| `pyproject.toml` | Python依存関係・ruff・mypy の設定を一元管理           |
| `Taskfile.yml`   | タスクランナー定義（lint, test, typecheck, deploy等） |

</details>

## ドキュメント

詳細は [docs/README.md](docs/README.md) を参照してください。
