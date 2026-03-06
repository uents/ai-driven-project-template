"""CDK アプリケーション エントリポイント"""

import aws_cdk as cdk

from stacks.api_stack import ApiStack
from stacks.database_stack import DatabaseStack

app = cdk.App()

# 環境設定
env = cdk.Environment(
    account=app.node.try_get_context("account"),
    region=app.node.try_get_context("region") or "ap-northeast-1",
)

# スタックの作成
database_stack = DatabaseStack(app, "DatabaseStack", env=env)
api_stack = ApiStack(app, "ApiStack", env=env, table=database_stack.table)

# 依存関係の設定
api_stack.add_dependency(database_stack)

app.synth()
