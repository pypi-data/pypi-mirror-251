# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
import concurrent.futures
import signal
from typing import Optional

from pypz.executors.commons import ExecutionMode
from pypz.executors.operator.executor import OperatorExecutor
from pypz.core.specs.pipeline import Pipeline


class PipelineExecutor:

    _max_operator_count: int = 32

    def __init__(self, pipeline: Pipeline):
        signal.signal(signal.SIGTERM, self.interrupt)
        signal.signal(signal.SIGINT, self.interrupt)

        self.__pipeline: Pipeline = pipeline

        self.__executor: Optional[concurrent.futures.ThreadPoolExecutor] = None

        self.__operator_executors: set[OperatorExecutor] = set()

        self.__futures: set[concurrent.futures.Future] = set()

        for operator in self.__pipeline.get_protected().get_nested_instances().values():
            self.__operator_executors.add(OperatorExecutor(operator, handle_interrupts=False))

        if PipelineExecutor._max_operator_count < len(self.__operator_executors):
            raise AttributeError(f"Max number of operators exceeded "
                                 f"({PipelineExecutor._max_operator_count}): "
                                 f"{len(self.__operator_executors)}")

    def start(self, exec_mode: ExecutionMode = ExecutionMode.Standard):
        if self.__executor is None:
            self.__executor = concurrent.futures.ThreadPoolExecutor(max_workers=PipelineExecutor._max_operator_count,
                                                                    thread_name_prefix=self.__class__.__name__)
            self.__futures.clear()
            for operator_executor in self.__operator_executors:
                self.__futures.add(self.__executor.submit(operator_executor.execute, exec_mode))

            while any(not future.done() for future in self.__futures):
                pass

    def shutdown(self):
        if self.__executor is not None:
            self.__executor.shutdown(wait=True, cancel_futures=False)
            self.__executor = None

    def interrupt(self, signal_number, current_stack):
        for operator_executor in self.__operator_executors:
            if operator_executor.is_running():
                operator_executor.interrupt(signal_number, current_stack)
        for future in self.__futures:
            future.cancel()
