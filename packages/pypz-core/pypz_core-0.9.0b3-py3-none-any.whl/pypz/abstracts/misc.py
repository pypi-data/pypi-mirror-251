# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
from typing import Any, Optional

from pypz.abstracts.channel_ports import ChannelInputPort, ChannelOutputPort
from pypz.core.channels.misc import BlankChannelReader, BlankChannelWriter


class BlankChannelInputPort(ChannelInputPort):

    def __init__(self, name: str = None, schema: Any = None, group_mode: bool = False, *args, **kwargs):
        super().__init__(name, schema, group_mode, BlankChannelReader, *args, **kwargs)


class BlankChannelOutputPort(ChannelOutputPort):
    def __init__(self, name: str = None, schema: Optional[Any] = None, *args, **kwargs):
        super().__init__(name, schema, BlankChannelWriter, *args, **kwargs)
