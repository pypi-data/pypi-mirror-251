import logging

import sentry_sdk
from configurations import values
from duke.common import (
    PluginConfiguration,
    build_plugin,
    build_plugin_manifest_from_package,
)
from sentry_sdk.integrations.django import DjangoIntegration

ENVIRON_PREFIX = "SENTRY"
logger = logging.getLogger(__name__)


class SentryConfiguration(PluginConfiguration):
    DSN = values.Value(environ_prefix=ENVIRON_PREFIX, default=None)
    TRACING = values.BooleanValue(environ_prefix=ENVIRON_PREFIX, default=False)

    @classmethod
    def post_setup(cls):
        super().post_setup()
        if cls.DSN is None:
            logger.warning(
                f"Sentry DSN is not set. Sentry will not be enabled. Tip: set {ENVIRON_PREFIX}_DSN environment variable"
            )
            return
        dsn = cls.DSN
        if dsn is not None:
            sentry_sdk.init(
                dsn=dsn,
                enable_tracing=cls.TRACING,
                integrations=[
                    DjangoIntegration(),
                ],
            )  # type: ignore


def plugin():
    name = "django-duke-sentry"
    description = "Sentry integration for Duke"

    manifest = build_plugin_manifest_from_package(
        name=name,
        description=description,
    )

    return build_plugin(configuration=SentryConfiguration, manifest=manifest)
