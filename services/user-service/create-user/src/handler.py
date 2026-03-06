"""ユーザー作成 Lambda ハンドラー"""

import json

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    Response,
    content_types,
)
from aws_lambda_powertools.metrics import MetricUnit

from model import CreateUserRequest, User
from repository import UserRepository

logger = Logger(service="user-service")
tracer = Tracer(service="user-service")
metrics = Metrics(namespace="MyApp", service="user-service")
app = APIGatewayRestResolver()


@app.post("/users")
@tracer.capture_method
def create_user() -> Response:
    """ユーザーを作成する"""
    try:
        # リクエストボディのバリデーション
        body = app.current_event.json_body
        request = CreateUserRequest(**body)

        # ユーザー作成
        repository = UserRepository()
        user = User.create(name=request.name, email=request.email)

        # メールアドレスの重複チェック
        existing = repository.find_by_email(user.email)
        if existing:
            return Response(
                status_code=409,
                content_type=content_types.APPLICATION_JSON,
                body=json.dumps(
                    {"error_code": "DUPLICATE_EMAIL", "message": "メールアドレスが既に登録されています"}
                ),
            )

        # 保存
        repository.save(user)

        # メトリクス記録
        metrics.add_metric(name="UserCreated", unit=MetricUnit.Count, value=1)

        logger.info("ユーザーを作成しました", extra={"user_id": user.user_id})

        return Response(
            status_code=201,
            content_type=content_types.APPLICATION_JSON,
            body=user.to_json(),
        )

    except ValueError as e:
        logger.warning("バリデーションエラー", extra={"error": str(e)})
        return Response(
            status_code=400,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({"error_code": "VALIDATION_ERROR", "message": str(e)}),
        )


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context) -> dict:
    """Lambda エントリポイント"""
    return app.resolve(event, context)
