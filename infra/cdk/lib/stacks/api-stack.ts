/** API スタック定義 */

import * as cdk from "aws-cdk-lib";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import * as path from "path";

/** ApiStack のプロパティ */
interface ApiStackProps extends cdk.StackProps {
  table: dynamodb.Table;
}

/** API Gateway + Lambda のスタック */
export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    // Lambda関数の作成
    const createUserFn = new lambda.Function(this, "CreateUserFunction", {
      runtime: lambda.Runtime.PYTHON_3_13,
      handler: "handler.lambda_handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../../../services/user-service/create-user/src")
      ),
      environment: {
        TABLE_NAME: props.table.tableName,
      },
    });

    // DynamoDBへのアクセス権限を付与
    props.table.grantReadWriteData(createUserFn);

    // API Gatewayの作成
    const api = new apigateway.RestApi(this, "UserApi", {
      restApiName: "User Service API",
      description: "ユーザー管理API",
    });

    // リソースとメソッドの定義
    const users = api.root.addResource("users");
    users.addMethod("POST", new apigateway.LambdaIntegration(createUserFn));
  }
}
