# ユーザー作成機能 仕様書

## 概要

新規ユーザーをシステムに登録する機能。

## エンドポイント

- **メソッド**: POST
- **パス**: /users
- **API定義**: `contracts/api/openapi.yml` の `createUser` を参照

## 入力

| フィールド | 型 | 必須 | 制約 |
|---|---|---|---|
| name | string | ○ | 2〜50文字 |
| email | string | ○ | メールアドレス形式、システム内で一意 |

## 処理フロー

1. リクエストボディのバリデーション
2. メールアドレスの重複チェック（GSI1で検索）
3. UUID v4 でユーザーIDを生成
4. DynamoDBにユーザー情報を保存
5. EventBridge に `UserCreated` イベントを発行
6. 作成されたユーザー情報をレスポンスとして返却

## 出力

- **成功時**: 201 Created + ユーザー情報（JSON）
- **バリデーションエラー**: 400 Bad Request
- **メールアドレス重複**: 409 Conflict

## エラーケース

| ケース | HTTPステータス | エラーコード |
|---|---|---|
| 名前が空 | 400 | VALIDATION_ERROR |
| 名前が50文字超過 | 400 | VALIDATION_ERROR |
| メール形式不正 | 400 | VALIDATION_ERROR |
| メールアドレス重複 | 409 | DUPLICATE_EMAIL |
| DynamoDB障害 | 500 | INTERNAL_ERROR |

## 関連

- テーブル定義: `contracts/database/table-definitions.yml`
- イベントスキーマ: `contracts/events/schemas/user-created.schema.json`
- アクセスパターン: AP-002, AP-005
