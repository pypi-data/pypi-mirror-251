# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================


class BaseSignal:

    def __init__(self):
        pass


class SignalError(BaseSignal):

    def __init__(self, exc: Exception = None):
        super().__init__()
        self.__exc = exc

    def get_exception(self):
        return self.__exc


class SignalKill(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalNoOp(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalOperationInit(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalOperationStart(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalOperationStop(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalResourcesCreation(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalResourcesDeletion(BaseSignal):

    def __init__(self):
        super().__init__()


class SignalServicesStart(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalServicesStop(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalShutdown(BaseSignal):
    def __init__(self):
        super().__init__()


class SignalTerminate(BaseSignal):
    def __init__(self):
        super().__init__()