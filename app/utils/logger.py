from typing import TYPE_CHECKING

from structlog import get_logger

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger
logger_system: "BoundLogger" = get_logger()