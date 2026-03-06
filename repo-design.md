# GitHub Copilot Agent 最適化リポジトリ構成

## 構成図

```
repo/
 │
 ├── .github/
 │    ├── copilot-instructions.md              # グローバル指示（プロジェクト概要・共通ルール）
 │    ├── instructions/                        # 技術領域別の指示
 │    │    ├── aws.instructions.md             # AWS固有の指示
 │    │    ├── python.instructions.md          # Python固有の指示
 │    │    └── testing.instructions.md         # テスト固有の指示
 │    ├── agents/                              # エージェント定義（役割別）
 │    │    ├── architect.md                    # 設計エージェント
 │    │    ├── developer.md                    # 実装エージェント
 │    │    ├── reviewer.md                     # レビューエージェント
 │    │    └── tester.md                       # テストエージェント
 │    ├── skills/                              # 知識ベース・リファレンス
 │    │    ├── aws-skills.md                   # AWSスキル定義
 │    │    ├── coding-skills.md                # コーディングスキル定義
 │    │    └── testing-skills.md               # テストスキル定義
 │    ├── prompts/                             # 定型プロンプトテンプレート
 │    │    ├── code-review.md                  # コードレビュー用
 │    │    ├── bug-fix.md                      # バグ修正用
 │    │    └── feature-impl.md                 # 機能実装用
 │    ├── ISSUE_TEMPLATE/                       # イシューテンプレート
 │    │    ├── bug_report.md                    # バグ報告テンプレート
 │    │    └── feature_request.md               # 機能要望テンプレート
 │    ├── pull_request_template.md              # PRテンプレート（Copilotレビュー指示付き）
 │    └── workflows/                           # CI/CD
 │         └── ci.yml                          # CIパイプライン定義
 │
 ├── docs/
 │    ├── README.md                            # ドキュメント全体の案内
 │    ├── requirements/
 │    │    ├── business.md                     # ビジネス要件
 │    │    └── system.md                       # システム要件（非機能含む）
 │    ├── architecture/
 │    │    ├── overview.md                     # アーキテクチャ概要
 │    │    ├── diagrams/                       # 構成図（PlantUML）
 │    │    │    ├── system-context.pu           # システムコンテキスト図
 │    │    │    └── component.pu               # コンポーネント図
 │    │    └── patterns.md                     # 採用パターン・規約
 │    ├── adr/
 │    │    ├── README.md                       # ADRテンプレート
 │    │    ├── 0001-serverless.md              # ADR: サーバーレス採用
 │    │    └── 0002-event-driven.md            # ADR: イベント駆動採用
 │    └── glossary.md                          # 用語集
 │
 ├── contracts/
 │    ├── README.md                            # 契約定義の目的と利用ルール
 │    ├── api/
 │    │    ├── openapi.yml                     # OpenAPI定義
 │    │    └── examples/                       # リクエスト/レスポンス例
 │    │         └── create-user.json           # ユーザー作成の例
 │    ├── events/
 │    │    ├── schemas/                        # イベントスキーマ（JSON Schema）
 │    │    │    └── user-created.schema.json   # ユーザー作成イベント定義
 │    │    └── examples/                       # イベントペイロード例
 │    │         └── user-created.json          # ユーザー作成イベントの例
 │    └── database/
 │         ├── table-definitions.yml           # DynamoDBテーブル定義
 │         ├── access-patterns.md              # アクセスパターン一覧
 │         └── er.md                           # ER図（Mermaid）
 │
 ├── services/
 │    └── user-service/
 │         ├── create-user/                    # ユーザー作成機能
 │         │    ├── spec.md                    # 機能仕様
 │         │    └── src/
 │         │         ├── __init__.py           # パッケージ初期化
 │         │         ├── handler.py            # Lambdaハンドラー
 │         │         ├── model.py              # ドメインモデル
 │         │         ├── repository.py         # データアクセス
 │         │         └── tests/
 │         │              ├── __init__.py      # テストパッケージ初期化
 │         │              ├── test_handler.py  # ハンドラーのテスト
 │         │              └── test_repository.py # リポジトリのテスト
 │         └── get-user/                       # ユーザー取得機能
 │              ├── spec.md                    # 機能仕様
 │              └── src/
 │                   ├── __init__.py           # パッケージ初期化
 │                   └── ...
 │
 ├── tests/
 │    ├── integration/                         # 統合テスト
 │    │    ├── README.md                       # 統合テスト戦略・実行方法
 │    │    ├── test-plan.md                    # 統合テスト計画書
 │    │    ├── test-spec.md                    # 統合テスト仕様書
 │    │    ├── test-report.md                  # 統合テスト成績書
 │    │    └── test_user_flow.py               # 統合テストコード
 │    ├── e2e/                                 # E2Eテスト
 │    │    ├── README.md                       # E2Eテスト戦略・実行方法
 │    │    ├── test-plan.md                    # E2Eテスト計画書
 │    │    ├── test-spec.md                    # E2Eテスト仕様書
 │    │    ├── test-report.md                  # E2Eテスト成績書
 │    │    └── test_api_e2e.py                 # E2Eテストコード
 │    └── fixtures/                            # 共通テストデータ
 │         └── users.json                      # ユーザーテストデータ
 │
 ├── research/                                 # 技術検証・PoC
 │    └── performance/
 │         └── load-test-results.md            # 負荷テスト結果
 │
 ├── tools/                                    # システム運用支援ツール
 │    ├── README.md                            # ツール一覧・利用方法
 │    ├── migration/                           # データ移行ツール
 │    └── monitoring/                          # 監視・アラート関連
 │
 ├── infra/
 │    └── cdk/                                 # AWS CDKインフラ定義
 │         ├── README.md                       # CDKセットアップ・デプロイ手順
 │         ├── app.py                          # CDKアプリエントリポイント
 │         └── stacks/
 │              ├── api_stack.py               # APIスタック
 │              └── database_stack.py          # データベーススタック
 │
 ├── .vscode/
 │    ├── settings.json                        # ワークスペース設定
 │    ├── extensions.json                      # 推奨拡張機能
 │    └── launch.json                          # デバッグ構成
 │
 ├── .gitignore
 ├── pyproject.toml                            # 依存関係・ruff・mypy設定
 ├── Taskfile.yml                              # タスクランナー定義
 └── README.md                                 # プロジェクト概要・セットアップ手順
```

## ディレクトリ内容・役割一覧

### `.github/`

| パス | 内容・役割 |
|---|---|
| `copilot-instructions.md` | プロジェクト全体のコンテキスト・共通ルール。Copilot Agentが全セッションで自動読込する最上位の指示ファイル |
| `instructions/` | 技術領域別の指示ファイル群。フロントマターの `applyTo` で対象ファイルを指定し、Copilotが自動適用する |
| `instructions/aws.instructions.md` | AWS関連の実装ルール（Lambda, DynamoDB, CDK等の使い方の指示） |
| `instructions/python.instructions.md` | Pythonコーディング規約・スタイルの指示 |
| `instructions/testing.instructions.md` | テスト実装時のルール・方針の指示 |
| `agents/` | Copilot Agentの役割別ペルソナ定義。タスクに応じてAgentに「誰として振る舞うか」を指示する |
| `agents/architect.md` | 設計エージェント：アーキテクチャ判断・設計レビュー用 |
| `agents/developer.md` | 実装エージェント：コード実装用 |
| `agents/reviewer.md` | レビューエージェント：コードレビュー用 |
| `agents/tester.md` | テストエージェント：テスト設計・実装用 |
| `skills/` | Agentが参照する知識ベース・リファレンス。instructionsが「何をすべきか」なら、skillsは「どうやるか」の詳細知識 |
| `skills/aws-skills.md` | AWSサービスの使い方・パターン・ベストプラクティス集 |
| `skills/coding-skills.md` | コーディングパターン・設計パターンの知識集 |
| `skills/testing-skills.md` | テスト手法・パターンの知識集 |
| `prompts/` | 繰り返し使う定型プロンプトのテンプレート。作業品質の標準化に使用 |
| `prompts/code-review.md` | コードレビュー依頼時のプロンプトテンプレート |
| `prompts/bug-fix.md` | バグ修正依頼時のプロンプトテンプレート |
| `prompts/feature-impl.md` | 機能実装依頼時のプロンプトテンプレート |
| `ISSUE_TEMPLATE/` | イシューテンプレート。新規イシュー作成時にフォームとして表示される |
| `ISSUE_TEMPLATE/bug_report.md` | バグ報告テンプレート（再現手順、環境情報等を構造化して記入） |
| `ISSUE_TEMPLATE/feature_request.md` | 機能要望テンプレート（背景・動機、受け入れ条件等を構造化して記入） |
| `pull_request_template.md` | PRテンプレート。HTMLコメントでCopilotへの日本語レビュー指示を埋め込み、PR作成時に自動適用 |
| `workflows/` | GitHub Actions CI/CDパイプライン定義 |
| `workflows/ci.yml` | CIパイプライン（lint, test, build等） |

### `docs/`

| パス | 内容・役割 |
|---|---|
| `README.md` | ドキュメント全体のナビゲーション・案内 |
| `requirements/business.md` | ビジネス要件定義（ユースケース、ビジネスルール等） |
| `requirements/system.md` | システム要件定義（非機能要件含む：性能、可用性、セキュリティ等） |
| `architecture/overview.md` | アーキテクチャ概要（技術スタック、全体方針） |
| `architecture/diagrams/` | PlantUML形式の構成図。Agentがシステム構造を理解するために参照 |
| `architecture/diagrams/system-context.pu` | システムコンテキスト図（C4モデル Level 1） |
| `architecture/diagrams/component.pu` | コンポーネント図（C4モデル Level 3） |
| `architecture/patterns.md` | プロジェクトで採用する実装パターン・規約。Agentのコード生成の一貫性を担保 |
| `adr/` | Architecture Decision Records。技術的意思決定の記録 |
| `adr/README.md` | ADRのテンプレート・書き方ガイド |
| `glossary.md` | ドメイン用語集。Agentが生成するコードの命名を統一するために参照 |

### `contracts/`

| パス | 内容・役割 |
|---|---|
| `README.md` | 契約定義の目的・利用ルール・更新フロー |
| `api/openapi.yml` | OpenAPI仕様。APIの入出力契約。Agentがハンドラー実装時に参照 |
| `api/examples/` | リクエスト/レスポンスの具体例。Agentのテストデータ生成に利用 |
| `events/schemas/` | イベントのJSON Schema定義。サービス間契約の厳密な型定義 |
| `events/examples/` | イベントペイロードの具体例 |
| `database/table-definitions.yml` | DynamoDBテーブル定義（PK/SK、GSI、LSI、キャパシティモード等） |
| `database/access-patterns.md` | DynamoDBアクセスパターン一覧。クエリ設計の根拠 |
| `database/er.md` | エンティティ関連図（Mermaid形式） |

### `services/`

| パス | 内容・役割 |
|---|---|
| `user-service/` | ユーザーサービスのルート。マイクロサービス単位のディレクトリ |
| `user-service/create-user/` | 「ユーザー作成」機能のディレクトリ。機能単位で分離 |
| `user-service/create-user/spec.md` | 機能仕様書。Agentがコード・テストを生成する際の元ネタ |
| `user-service/create-user/src/` | 機能の実装コード。`__init__.py` によりパッケージとして認識 |
| `user-service/create-user/src/tests/` | 機能の単体テスト。`src/` 配下に配置しインポートパスを簡潔にする |

### `tests/`

| パス | 内容・役割 |
|---|---|
| `integration/` | 統合テスト。サービス間連携の検証 |
| `integration/README.md` | 統合テストの戦略・実行方法・前提条件 |
| `integration/test-plan.md` | 統合テスト計画書（テスト範囲、スケジュール、環境、リスク等） |
| `integration/test-spec.md` | 統合テスト仕様書（テストケース一覧、入出力、期待結果） |
| `integration/test-report.md` | 統合テスト成績書（実行結果、合否判定、不具合一覧） |
| `e2e/` | E2Eテスト。エンドツーエンドのシナリオ検証 |
| `e2e/README.md` | E2Eテストの戦略・実行方法・前提条件 |
| `e2e/test-plan.md` | E2Eテスト計画書（テスト範囲、スケジュール、環境、リスク等） |
| `e2e/test-spec.md` | E2Eテスト仕様書（テストケース一覧、入出力、期待結果） |
| `e2e/test-report.md` | E2Eテスト成績書（実行結果、合否判定、不具合一覧） |
| `fixtures/` | 共通テストデータ（JSON等）。複数テストから参照 |

### その他ルートディレクトリ

| パス | 内容・役割 |
|---|---|
| `research/` | 技術検証・PoC。本番コードとは分離した実験領域 |
| `research/performance/` | 負荷テスト結果等のパフォーマンス検証 |
| `tools/` | システム運用支援ツール |
| `tools/migration/` | データ移行ツール・スクリプト |
| `tools/monitoring/` | 監視・アラート関連ツール |
| `infra/cdk/` | AWS CDKによるインフラ定義 |
| `infra/cdk/stacks/` | CDKスタック定義（APIスタック、DBスタック等） |
| `.vscode/settings.json` | VS Codeワークスペース設定（フォーマッタ、リンター等） |
| `.vscode/extensions.json` | 推奨拡張機能リスト |
| `.vscode/launch.json` | デバッグ構成 |
| `pyproject.toml` | 依存関係・ruff・mypy の設定を一元管理 |
| `Taskfile.yml` | タスクランナー定義（lint, test, typecheck, deploy等の共通コマンド） |
| `README.md` | プロジェクト概要・セットアップ手順・開発フロー |
