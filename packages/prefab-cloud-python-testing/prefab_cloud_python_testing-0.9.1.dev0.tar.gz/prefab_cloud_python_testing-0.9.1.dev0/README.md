# prefab-cloud-python

Python client for prefab.cloud, providing Config, FeatureFlags as a Service

**Note: This library is under active development**

[Sign up to be notified about updates](https://forms.gle/2qsjMFvjGnkTnA9T8)

## Example usage

```python
from prefab_cloud_python import Client, Options

options = Options(
    prefab_api_key="your-prefab-api-key"
)

context = {
  "user": {
    "team_id": 432,
    "id": 123,
    "subscription_level": 'pro',
    "email": "alice@example.com"
  }
}

client = Client(options)

result = client.enabled("my-first-feature-flag", context=context)

print("my-first-feature-flag is:", result)
```

See full documentation https://docs.prefab.cloud/docs/sdks/python

## StructLog Configuration

### Simple Usage

There's a convenience method to access an opinionated structlog setup. **No configuration of structlog is performed by default**

```python
from prefab_cloud_python import default_structlog_setup;
default_structlog_setup(colors=True) # true is the default, false to remove ANSI color codes
```

### Using With Existing Structlog

We have a structlog processor that can be mixed into your existing structlog configuration.

The code below is an example configuration. **_See the note below about CallSiteParameterAdder_**

```python
import structlog
from prefab_cloud_python import create_prefab_structlog_processor
from prefab_cloud_python import STRUCTLOG_CALLSITE_IGNORES

structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            ## ensure CallsiteparameterAdder is present before prefab_structlog_processor
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                ],
                additional_ignores=STRUCTLOG_CALLSITE_IGNORES,
            ),
            create_prefab_structlog_processor(), ## add this
            structlog.dev.ConsoleRenderer(),
        ]
    )
```

#### CallSiteParameterAdder

We do require that `CallSiteParameterAdder` is present and configured to handle `PATHNAME` and `FUNCNAME` in addition to any parameters you may be using
Please also merge our `STRUCTLOG_CALLSITE_IGNORES` list into the `additional_ignores` list as shown below

```python
import structlog
from prefab_cloud_python import STRUCTLOG_CALLSITE_IGNORES

your_ignores = ["some", "ignores"]

structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                ],
                additional_ignores=your_ignores + STRUCTLOG_CALLSITE_IGNORES,
            )
```
