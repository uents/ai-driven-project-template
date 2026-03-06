# ER図

```mermaid
erDiagram
    USER {
        string PK "USER#{user_id}"
        string SK "PROFILE"
        string user_id "UUID v4"
        string name "ユーザー名"
        string email "メールアドレス"
        string created_at "作成日時"
        string updated_at "更新日時"
        string GSI1PK "EMAIL#{email}"
        string GSI1SK "USER#{user_id}"
    }
```

## 説明

- 本システムは Single Table Design を採用している
- 現時点では User エンティティのみ
- サービス拡張に伴いエンティティを追加する場合は、同一テーブルに追加する
