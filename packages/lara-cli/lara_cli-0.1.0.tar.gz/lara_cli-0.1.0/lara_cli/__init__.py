import sentry_sdk

sentry_sdk.init(
    dsn="https://13eabfeaeb6390734b126106d1d391b6@o4506345010364416.ingest.sentry.io/4506553676267520",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
