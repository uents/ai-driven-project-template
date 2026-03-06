#!/usr/bin/env node
/** CDK アプリケーション エントリポイント */

import * as cdk from "aws-cdk-lib";
import { DatabaseStack } from "../lib/stacks/database-stack";
import { ApiStack } from "../lib/stacks/api-stack";

const app = new cdk.App();

// 環境設定
const env: cdk.Environment = {
  account: app.node.tryGetContext("account"),
  region: app.node.tryGetContext("region") ?? "ap-northeast-1",
};

// スタックの作成
const databaseStack = new DatabaseStack(app, "DatabaseStack", { env });
const apiStack = new ApiStack(app, "ApiStack", {
  env,
  table: databaseStack.table,
});

// 依存関係の設定
apiStack.addDependency(databaseStack);
