# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
from pypz.core.commons.loggers import DefaultContextLogger
from pypz.core.commons.parameters import OptionalParameter
from pypz.core.specs.plugin import LoggerPlugin


class DefaultLoggerPlugin(LoggerPlugin, DefaultContextLogger):

    _log_level = OptionalParameter(str,
                                   alt_name="logLevel",
                                   on_update=lambda instance, val: None
                                   if val is None else instance.set_log_level(val))

    def __init__(self, name: str = None, *args, **kwargs):
        LoggerPlugin.__init__(self, name, *args, **kwargs)
        DefaultContextLogger.__init__(self, self.get_full_name())

        self._log_level = "INFO"

    def _on_interrupt(self, system_signal: int = None) -> None:
        pass

    def _on_error(self) -> None:
        pass
