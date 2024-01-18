# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
import sys

import yaml

from pypz.core.specs.dtos import PipelineInstanceDTO
from pypz.core.specs.operator import Operator
from pypz.core.specs.pipeline import Pipeline
from pypz.executors.commons import ExecutionMode
from pypz.executors.operator.executor import OperatorExecutor


if __name__ == "__main__":
    print(sys.argv)
    if 3 > len(sys.argv):
        print("Missing arguments:\n"
              "$1 - path to config file\n"
              "$2 - operator simple name\n"
              f"$3 - [Optional] ExecutionMode (default: {ExecutionMode.Standard.name}). "
              f"Possible values: {[elem.name for elem in ExecutionMode]}",
              file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as json_file:
        pipeline_dto: PipelineInstanceDTO = PipelineInstanceDTO(**yaml.safe_load(json_file))

        pipeline: Pipeline = Pipeline.create_from_dto(pipeline_dto, mock_nonexistent=True)
        operator: Operator = pipeline.get_protected().get_nested_instance(sys.argv[2])
        exec_mode: ExecutionMode = ExecutionMode.Standard if 4 > len(sys.argv) else ExecutionMode(sys.argv[3])

        print(f"Operator to execute: {operator.get_full_name()}; Execution mode: {exec_mode.name}")

        executor: OperatorExecutor = OperatorExecutor(operator)

        exit_code = executor.execute(exec_mode)

        sys.exit(exit_code)
