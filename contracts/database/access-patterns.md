# DynamoDB アクセスパターン

## メインテーブル

| # | アクセスパターン | 操作 | PK | SK | 備考 |
|---|---|---|---|---|---|
| AP-001 | ユーザーIDでユーザーを取得 | GetItem | `USER#{user_id}` | `PROFILE` | |
| AP-002 | ユーザーを作成 | PutItem | `USER#{user_id}` | `PROFILE` | 条件付き書き込み |
| AP-003 | ユーザー情報を更新 | UpdateItem | `USER#{user_id}` | `PROFILE` | |
| AP-004 | ユーザーを削除 | DeleteItem | `USER#{user_id}` | `PROFILE` | |

## GSI1

| # | アクセスパターン | 操作 | GSI1PK | GSI1SK | 備考 |
|---|---|---|---|---|---|
| AP-005 | メールアドレスでユーザーを検索 | Query | `EMAIL#{email}` | - | 一意性チェックに使用 |
