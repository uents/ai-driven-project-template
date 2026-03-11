# ユーザー作成機能 設計書

## 参照ドキュメント

- 機能仕様: なし（本ドキュメントが設計の起点）
- API契約: `contracts/api/openapi.yml` (`createUser`)
- テーブル定義: `contracts/database/table-definitions.yml`
- アクセスパターン: `contracts/database/access-patterns.md` (AP-002, AP-005)
- イベントスキーマ: `contracts/events/schemas/user-created.schema.json`

---

## レイヤー構成

```
handler.py        # Lambda エントリポイント・HTTPルーティング
model.py          # ドメインモデル・バリデーション
repository.py     # DynamoDB アクセス
```

各レイヤーの責務は単一責任原則に従い分離する。Handler は HTTP の変換のみを担い、  
ビジネスロジック（ユーザー生成・一意性チェック）は Model/Repository に委譲する。

---

## クラス設計

### `CreateUserRequest` (model.py)

Pydantic `BaseModel` を継承したリクエスト DTO。  
Lambda Powertools の `APIGatewayRestResolver.current_event.json_body` から直接アンパックして生成する。

| フィールド | 型         | バリデーション                            |
| ---------- | ---------- | ----------------------------------------- |
| `name`     | `str`      | 2〜50文字（`field_validator` で検証）     |
| `email`    | `EmailStr` | Pydantic 組み込みの RFC 5322 準拠チェック |

バリデーション失敗時は `ValueError` を raise し、handler がキャッチして 400 を返す。

### `User` (model.py)

ユーザードメインモデル。ファクトリメソッド `create()` で UUID v4 の採番と現在時刻の付与を行う。

| メソッド                   | 役割                                               |
| -------------------------- | -------------------------------------------------- |
| `create(name, email)`      | ID・タイムスタンプを付与して新規インスタンスを生成 |
| `to_dynamodb_item()`       | DynamoDB の Single Table キーパターンに変換        |
| `from_dynamodb_item(item)` | DynamoDB アイテムからモデルを復元                  |
| `to_json()`                | レスポンスボディ用 JSON 文字列に変換               |

DynamoDB のキーパターン:

| 属性     | 値               |
| -------- | ---------------- |
| `PK`     | `USER#{user_id}` |
| `SK`     | `PROFILE`        |
| `GSI1PK` | `EMAIL#{email}`  |
| `GSI1SK` | `USER#{user_id}` |

### `UserRepository` (repository.py)

DynamoDB アクセスをカプセル化するリポジトリ。テーブル名は環境変数 `TABLE_NAME` から取得する。  
コンストラクタで `table` を注入可能にしておくことで、ユニットテスト時のモック差し替えを容易にする。

| メソッド               | アクセスパターン     | 備考                                                            |
| ---------------------- | -------------------- | --------------------------------------------------------------- |
| `save(user)`           | AP-002: `PutItem`    | 条件付き書き込みは未実装（重複チェックは find_by_email で代替） |
| `find_by_email(email)` | AP-005: GSI1 `Query` | メール一意性チェックに使用                                      |
| `find_by_id(user_id)`  | AP-001: `GetItem`    | get_user 機能でも共用                                           |

---

## 処理フロー

```
POST /users
  │
  ├─ [1] CreateUserRequest(**body) でバリデーション
  │        └─ 失敗 → ValueError → 400 VALIDATION_ERROR
  │
  ├─ [2] User.create(name, email) でドメインオブジェクト生成
  │        └─ UUID v4 採番・タイムスタンプ付与
  │
  ├─ [3] repository.find_by_email(email) でメール重複チェック
  │        └─ 存在する → 409 DUPLICATE_EMAIL
  │
  ├─ [4] repository.save(user) で DynamoDB に保存
  │        └─ 障害 → 例外が伝播 → 500（Lambda がハンドル）
  │
  ├─ [5] EventBridge に UserCreated イベントを発行（※未実装、TODO）
  │
  └─ [6] 201 Created + user.to_json() を返却
```

> **TODO**: ステップ 5 の EventBridge 発行は現在未実装。  
> イベントスキーマは `contracts/events/schemas/user-created.schema.json` を参照。

---

## エラーハンドリング設計

| 例外                           | 発生箇所                           | HTTP ステータス | エラーコード       |
| ------------------------------ | ---------------------------------- | --------------- | ------------------ |
| `ValueError`                   | `CreateUserRequest` バリデーション | 400             | `VALIDATION_ERROR` |
| メール重複（明示的チェック）   | handler                            | 409             | `DUPLICATE_EMAIL`  |
| `Exception`（DynamoDB 障害等） | repository                         | 500             | Lambda デフォルト  |

500 系は handler で明示的にキャッチせず Lambda ランタイムに委ねる。  
ログは Lambda Powertools `Logger` で構造化ログとして出力する。

---

## 可観測性

Lambda Powertools を使用して以下を計装する。

| ツール    | 用途                                                             |
| --------- | ---------------------------------------------------------------- |
| `Logger`  | 構造化ログ（`inject_lambda_context` でリクエスト情報を自動付与） |
| `Tracer`  | X-Ray トレース（`capture_lambda_handler` / `capture_method`）    |
| `Metrics` | カスタムメトリクス `UserCreated`（Count）を CloudWatch に送信    |

---

## 依存ライブラリ

| ライブラリ              | 用途                                               |
| ----------------------- | -------------------------------------------------- |
| `aws-lambda-powertools` | Logger / Tracer / Metrics / APIGatewayRestResolver |
| `pydantic[email]`       | リクエスト DTO のバリデーション                    |
| `boto3`                 | DynamoDB アクセス                                  |
