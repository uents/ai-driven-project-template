---
name: git-commit
description: Conventional Commits 規約に従ったコミットメッセージを作成するスキル。変更内容を適切なタイプ・スコープで表現する
---

# Git Commit スキル

## フォーマット

```
<type>(<scope>): <subject>

[body]

[footer]
```

## タイプ一覧

| タイプ | 用途 |
|---|---|
| `feat` | 新機能の追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `refactor` | リファクタリング（機能変更・バグ修正なし） |
| `test` | テストの追加・修正 |
| `chore` | ビルド・ツール・依存関係の変更 |
| `ci` | CI/CD 設定の変更 |
| `perf` | パフォーマンス改善 |

## スコープの例（本プロジェクト）

| スコープ | 対象 |
|---|---|
| `user-service` | ユーザーサービス全体 |
| `create-user` | ユーザー作成機能 |
| `get-user` | ユーザー取得機能 |
| `infra` | CDK インフラ定義 |
| `deps` | 依存関係の更新 |

## コミットメッセージの例

```
feat(create-user): ユーザー作成 Lambda 関数を実装

- handler.py に POST /users エンドポイントを追加
- model.py に User ドメインモデルを定義
- repository.py に DynamoDB への書き込み処理を実装

Closes #12
```

```
fix(create-user): メールアドレスの重複チェックが機能しない問題を修正

GSI1 を使用した既存ユーザー検索が条件式の誤りにより
常に空を返していたため修正。

Fixes #34
```

```
docs: README のセットアップ手順を CDK TypeScript 対応に更新
```

## ルール

- subject は命令形・現在形で書く（「追加した」ではなく「追加する」）
- subject は 72 文字以内に収める
- body には「なぜ」の説明を書く（「何を」はコードから読める）
- Breaking Change がある場合は footer に `BREAKING CHANGE:` を記載する
- Issue との紐付けは footer に `Closes #N` / `Fixes #N` で行う
