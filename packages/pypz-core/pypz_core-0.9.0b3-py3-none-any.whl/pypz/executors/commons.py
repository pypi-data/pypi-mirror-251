# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
from enum import Enum


class ExecutionMode(Enum):

    Skip = "Skip"
    """
    If this mode is set, then the executor will not be invoked. This is necessary
    e.g., in deployment cases, where we want to ignore the execution of certain operators.
    """

    Standard = "Standard"
    """
    In this mode the ESM will perform its standard execution.
    VERY IMPORTANT NOTE, Standard means that resources will be created and deleted up automatically by ESM. If
    you want to have a standard mode, where resources are only created, but not deleted, then use the
    StandardModeWithoutResourceDeletion
    """

    WithoutResourceDeletion = "WithoutResourceDeletion"
    """
    In this mode the ESM will perform its standard execution. However the StateDeleteResources will be skipped. This
    is a relevant use-case, if you want to trigger centralized resource cleanup after the operations are done.
    """

    ResourceCreationOnly = "ResourceCreationOnly"
    """
    In this mode only resource creation will be considered. ESM is having the following plan:
    StateEntry->StateStartServices->StateCreateResources->StateShutdownServices->StateKilled
    """

    ResourceDeletionOnly = "ResourceDeletionOnly"
    """
    In this mode only resource deletion will be considered. ESM is having the following plan:
    StateEntry->StateStartServices->StateDeleteResources->StateShutdownServices->StateKilled
    """


class ExitCodes(Enum):

    # These are the common error codes
    # ================================

    NoError = 0
    GeneralError = 1
    CommandCannotBeExecutedError = 126
    CommandNotFoundError = 127
    InvalidExitArgumentError = 128
    FatalError = 129
    SigTerm = 130

    # These are the pypz specific error codes
    # =======================================

    StateServiceStartError = 110
    StateServiceShutdownError = 111
    StateResourceCreationError = 112
    StateResourcesDeletionError = 113
    StateOperationInitError = 114
    StateOperationError = 115
    StateOperationShutdownError = 116
