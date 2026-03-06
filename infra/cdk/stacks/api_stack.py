"""API スタック定義"""

import aws_cdk as cdk
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class ApiStack(cdk.Stack):
    """API Gateway + Lambda のスタック"""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        table: dynamodb.Table,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の作成
        create_user_fn = _lambda.Function(
            self,
            "CreateUserFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(
                "../../services/user-service/create-user/src"
            ),
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        # DynamoDBへのアクセス権限を付与
        table.grant_read_write_data(create_user_fn)

        # API Gatewayの作成
        api = apigw.RestApi(
            self,
            "UserApi",
            rest_api_name="User Service API",
            description="ユーザー管理API",
        )

        # リソースとメソッドの定義
        users = api.root.add_resource("users")
        users.add_method("POST", apigw.LambdaIntegration(create_user_fn))
