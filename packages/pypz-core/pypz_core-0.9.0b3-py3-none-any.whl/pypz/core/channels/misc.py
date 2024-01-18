# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
import concurrent.futures
from typing import Any, TYPE_CHECKING

from pypz.core.channels.io import ChannelReader, ChannelWriter

if TYPE_CHECKING:
    from pypz.core.specs.plugin import InputPortPlugin, OutputPortPlugin


class BlankChannelReader(ChannelReader):
    def __init__(self, channel_name: str,
                 context: 'InputPortPlugin',
                 executor: concurrent.futures.ThreadPoolExecutor = None,
                 **kwargs):
        super().__init__(channel_name, context, executor, **kwargs)

    def _load_input_record_offset(self) -> int:
        return 0

    def has_records(self) -> bool:
        return False

    def _read_records(self) -> list[Any]:
        return []

    def _commit_offset(self, offset: int) -> None:
        pass

    def _create_resources(self) -> bool:
        return True

    def _delete_resources(self) -> bool:
        return True

    def _open_channel(self) -> bool:
        return True

    def _close_channel(self) -> bool:
        return True

    def _configure_channel(self, channel_configuration: dict) -> None:
        pass

    def _send_status_message(self, message: str) -> None:
        pass

    def _retrieve_status_messages(self) -> list:
        return []


class BlankChannelWriter(ChannelWriter):

    def __init__(self, channel_name: str,
                 context: 'OutputPortPlugin',
                 executor: concurrent.futures.ThreadPoolExecutor = None,
                 **kwargs):
        super().__init__(channel_name, context, executor, **kwargs)

    def _write_records(self, records: list[Any]) -> None:
        pass

    def _create_resources(self) -> bool:
        return True

    def _delete_resources(self) -> bool:
        return True

    def _open_channel(self) -> bool:
        return True

    def _close_channel(self) -> bool:
        return True

    def _configure_channel(self, channel_configuration: dict) -> None:
        pass

    def _send_status_message(self, message: str) -> None:
        pass

    def _retrieve_status_messages(self) -> list:
        return []

