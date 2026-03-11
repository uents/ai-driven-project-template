# ユーザー取得機能 設計書

## 参照ドキュメント

- API契約: `contracts/api/openapi.yml` (`getUser`)
- テーブル定義: `contracts/database/table-definitions.yml`
- アクセスパターン: `contracts/database/access-patterns.md` (AP-001)

---

## レイヤー構成

```
handler.py        # Lambda エントリポイント・HTTPルーティング
model.py          # ドメインモデル
repository.py     # DynamoDB アクセス
```

各レイヤーの責務は単一責任原則に従い分離する。Handler は HTTP の変換（パラメータ取得・レスポンス整形）のみを担い、  
DynamoDB アクセスは Repository に委譲する。

---

## クラス設計

### `User` (model.py)

ユーザードメインモデル。create_user 機能と共通定義。

| メソッド                   | 役割                                      |
| -------------------------- | ----------------------------------------- |
| `from_dynamodb_item(item)` | DynamoDB アイテムからドメインモデルを復元 |
| `to_json()`                | レスポンスボディ用 JSON 文字列に変換      |

`User` が保持するフィールド:

| フィールド   | 型    | 説明                  |
| ------------ | ----- | --------------------- |
| `user_id`    | `str` | ユーザーID（UUID v4） |
| `name`       | `str` | ユーザー名            |
| `email`      | `str` | メールアドレス        |
| `created_at` | `str` | 作成日時（ISO 8601）  |

### `UserRepository` (repository.py)

DynamoDB アクセスをカプセル化するリポジトリ。テーブル名は環境変数 `TABLE_NAME` から取得する。  
コンストラクタで `table` を注入可能にしておくことで、ユニットテスト時のモック差し替えを容易にする。

| メソッド              | アクセスパターン  | 備考                                                         |
| --------------------- | ----------------- | ------------------------------------------------------------ |
| `find_by_id(user_id)` | AP-001: `GetItem` | PK=`USER#{user_id}` / SK=`PROFILE`。未存在時は `None` を返す |

---

## 処理フロー

```
GET /users/{user_id}
  │
  ├─ [1] パスパラメータから user_id を取得
  │
  ├─ [2] user_id の UUID 形式バリデーション（uuid.UUID() でパース）
  │        └─ ValueError → 400 VALIDATION_ERROR
  │
  ├─ [3] repository.find_by_id(user_id) で DynamoDB からユーザーを取得
  │        ├─ None → 404 NOT_FOUND
  │        └─ 障害 → 例外が伝播 → 500 INTERNAL_ERROR
  │
  └─ [4] 200 OK + user.to_json() を返却
```

---

## バリデーション設計

UUID 形式チェックは Python 標準ライブラリの `uuid.UUID()` を使用する。  
パースに失敗した場合は `ValueError` を raise し、handler でキャッチして 400 を返す。

```python
import uuid

def validate_user_id(user_id: str) -> None:
    """user_id が UUID v4 形式かどうかを検証する。"""
    try:
        uuid.UUID(user_id, version=4)
    except ValueError:
        raise ValueError(f"無効な user_id 形式: {user_id}")
```

---

## エラーハンドリング設計

| 例外 / 条件                    | 発生箇所   | HTTP ステータス | エラーコード       |
| ------------------------------ | ---------- | --------------- | ------------------ |
| `ValueError`（UUID 形式不正）  | handler    | 400             | `VALIDATION_ERROR` |
| `None`（ユーザー未存在）       | handler    | 404             | `NOT_FOUND`        |
| `Exception`（DynamoDB 障害等） | repository | 500             | `INTERNAL_ERROR`   |

500 系は handler で明示的にキャッチせず Lambda ランタイムに委ねる。  
ログは Lambda Powertools `Logger` で構造化ログとして出力する。

レスポンスのエラーボディは `contracts/api/openapi.yml` の `ErrorResponse` スキーマに準拠する。

```json
{
  "error_code": "NOT_FOUND",
  "message": "ユーザーが見つかりません"
}
```

---

## 可観測性

Lambda Powertools を使用して以下を計装する。

| ツール    | 用途                                                             |
| --------- | ---------------------------------------------------------------- |
| `Logger`  | 構造化ログ（`inject_lambda_context` でリクエスト情報を自動付与） |
| `Tracer`  | X-Ray トレース（`capture_lambda_handler` / `capture_method`）    |
| `Metrics` | カスタムメトリクス `UserFetched`（Count）を CloudWatch に送信    |

---

## 依存ライブラリ

| ライブラリ              | 用途                                               |
| ----------------------- | -------------------------------------------------- |
| `aws-lambda-powertools` | Logger / Tracer / Metrics / APIGatewayRestResolver |
| `pydantic`              | ドメインモデルの定義                               |
| `boto3`                 | DynamoDB アクセス                                  |
