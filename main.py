from microsservice_telemetry_toolkit.infrastructure.otel_app_tracer import (
    OtelAppTracer,
)

app_tracer = OtelAppTracer(service_name="example-service")


def main():
    with app_tracer.start_root_span("service.operation.task") as root_span:
        try:
            with app_tracer.start_span_action("subtask") as action_span:
                print(f"Started action span: {action_span.name}")
        except Exception as e:
            root_span.record_and_raise_exception(e)


if __name__ == "__main__":
    main()
