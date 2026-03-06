# ユーザー取得機能 仕様書

## 概要

指定されたユーザーIDに基づいてユーザー情報を取得する機能。

## エンドポイント

- **メソッド**: GET
- **パス**: /users/{user_id}
- **API定義**: `contracts/api/openapi.yml` の `getUser` を参照

## 入力

| パラメータ | 型 | 場所 | 必須 | 説明 |
|---|---|---|---|---|
| user_id | string (UUID) | パスパラメータ | ○ | 取得するユーザーのID |

## 処理フロー

1. パスパラメータから user_id を取得
2. user_id の形式バリデーション（UUID形式）
3. DynamoDBからユーザー情報を取得（AP-001）
4. ユーザー情報をレスポンスとして返却

## 出力

- **成功時**: 200 OK + ユーザー情報（JSON）
- **ユーザー未存在**: 404 Not Found

## エラーケース

| ケース | HTTPステータス | エラーコード |
|---|---|---|
| user_id が不正な形式 | 400 | VALIDATION_ERROR |
| ユーザーが存在しない | 404 | NOT_FOUND |
| DynamoDB障害 | 500 | INTERNAL_ERROR |

## 関連

- テーブル定義: `contracts/database/table-definitions.yml`
- アクセスパターン: AP-001
