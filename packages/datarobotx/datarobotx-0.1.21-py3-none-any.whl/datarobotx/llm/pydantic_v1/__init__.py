try:
    from pydantic.v1 import *  # noqa: F403, F401
except ImportError:
    from pydantic import *  # type: ignore[assignment, no-redef]  # noqa: F403, F401
