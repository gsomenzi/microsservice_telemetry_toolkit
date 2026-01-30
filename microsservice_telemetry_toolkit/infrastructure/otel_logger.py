from typing import Optional
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, DEPLOYMENT_ENVIRONMENT
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    SimpleLogRecordProcessor,
    ConsoleLogRecordExporter,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
import logging


class OtelLogger:
    @staticmethod
    def configure_global_logging(
        service_name: str,
        service_environment: str = "development",
        log_level: int = logging.INFO,
        otlp_endpoint: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        resource = Resource.create(
            attributes={
                SERVICE_NAME: service_name,
                DEPLOYMENT_ENVIRONMENT: service_environment,
            }
        )

        provider = LoggerProvider(resource=resource)
        processor = (
            BatchLogRecordProcessor(
                OTLPLogExporter(endpoint=otlp_endpoint, headers=headers)
            )
            if otlp_endpoint
            else SimpleLogRecordProcessor(ConsoleLogRecordExporter())
        )
        provider.add_log_record_processor(processor)
        set_logger_provider(provider)

        handler = LoggingHandler(level=log_level, logger_provider=provider)
        logging.basicConfig(handlers=[handler], level=log_level, force=True)
