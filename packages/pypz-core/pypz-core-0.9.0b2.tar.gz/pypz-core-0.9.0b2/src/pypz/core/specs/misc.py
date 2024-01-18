# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
from typing import Optional, Any

from pypz.core.specs.instance import Instance, NestedInstanceType
from pypz.core.specs.operator import Operator
from pypz.core.specs.plugin import Plugin, PortPlugin, InputPortPlugin, OutputPortPlugin, ResourceHandlerPlugin, \
    ServicePlugin


class BlankInstance(Instance[NestedInstanceType]):

    def _on_interrupt(self, system_signal: int = None) -> None:
        pass

    def _on_error(self) -> None:
        pass


class BlankPlugin(BlankInstance[None]):
    pass


class BlankResourceHandlerPlugin(ResourceHandlerPlugin, BlankPlugin):

    def _on_resource_creation(self) -> bool:
        return True

    def _on_resource_deletion(self) -> bool:
        return True


class BlankPortPlugin(PortPlugin, BlankPlugin):

    def _on_port_open(self) -> bool:
        return True

    def _on_port_close(self) -> bool:
        return True


class BlankInputPortPlugin(InputPortPlugin, BlankPortPlugin):

    def can_retrieve(self) -> bool:
        return False

    def retrieve(self) -> Any:
        pass

    def commit_current_read_offset(self) -> None:
        pass


class BlankOutputPortPlugin(OutputPortPlugin, BlankPortPlugin):

    def send(self, data: Any) -> Any:
        pass


class BlankServicePlugin(ServicePlugin, BlankPlugin):

    def _on_service_start(self) -> bool:
        return True

    def _on_service_shutdown(self) -> bool:
        return True


class BlankOperator(Operator, BlankInstance[Plugin]):

    def __init__(self, name: str = None, replication_factor: int = None, *args, **kwargs):
        super().__init__(name, replication_factor, *args, **kwargs)

    def _on_init(self) -> bool:
        return True

    def _on_running(self) -> Optional[bool]:
        return True

    def _on_shutdown(self) -> bool:
        return True
