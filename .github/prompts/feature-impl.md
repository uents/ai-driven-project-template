# 機能実装 プロンプトテンプレート

## 使い方

新機能の実装をCopilot Agentに依頼する際のテンプレート。

## プロンプト

```
以下の機能を実装してください。

## 機能仕様
{spec.md のパスまたは内容}

## 参照ドキュメント
- API契約: `contracts/api/openapi.yml`
- テーブル定義: `contracts/database/table-definitions.yml`
- 用語集: `docs/glossary.md`

## 実装要件
- `services/{サービス名}/{機能名}/` 配下に作成すること
- Handler / Model / Repository のレイヤー構造に従うこと
- ユニットテストを同時に作成すること
- `.github/instructions/` 配下の指示に従うこと

## 出力ファイル

- `src/__init__.py` - パッケージ初期化
- `src/handler.py` - Lambdaハンドラー
- `src/model.py` - ドメインモデル
- `src/repository.py` - データアクセス
- `src/tests/__init__.py` - テストパッケージ初期化
- `src/tests/test_handler.py` - ハンドラーテスト
- `src/tests/test_repository.py` - リポジトリテスト
```
