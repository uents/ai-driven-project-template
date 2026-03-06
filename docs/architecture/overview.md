# アーキテクチャ概要

## システム構成

本システムは、AWSサーバーレスサービスを活用したイベント駆動型マイクロサービスアーキテクチャを採用する。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| API | Amazon API Gateway (REST) |
| コンピューティング | AWS Lambda (Python 3.13) |
| データベース | Amazon DynamoDB |
| イベントバス | Amazon EventBridge |
| IaC | AWS CDK (TypeScript) |
| CI/CD | GitHub Actions |
| 監視 | Amazon CloudWatch |

## サービス一覧

| サービス名 | 責務 |
|---|---|
| user-service | ユーザーの作成・取得・更新・削除 |

## 設計原則

1. **サーバーレスファースト**: マネージドサービスを最大限活用し、運用負荷を最小化する
2. **イベント駆動**: サービス間はEventBridgeを介したイベントで疎結合にする
3. **Single Table Design**: DynamoDBは単一テーブル設計を採用する
4. **Infrastructure as Code**: すべてのインフラをCDKでコード管理する

## 構成図

詳細な構成図は以下を参照:
- システムコンテキスト図: `diagrams/system-context.pu`
- コンポーネント図: `diagrams/component.pu`
