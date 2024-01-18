# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Laszlo Anka. All rights reserved.
# Licensed under the Apache 2.0 license.
# =============================================================================
from typing import cast

import yaml

from pypz.core.specs.dtos import PipelineInstanceDTO, PipelineSpecDTO
from pypz.core.specs.instance import Instance, RegisteredInterface
from pypz.core.specs.operator import Operator


class Pipeline(Instance[Operator], RegisteredInterface):

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, Operator, *args, **kwargs)

    def get_dto(self) -> PipelineInstanceDTO:
        instance_dto = super().get_dto()

        # Replicas must be excluded from the dto
        instance_dto.spec.nestedInstances = {
            operator.get_dto() for operator in self.get_protected().get_nested_instances().values()
            if operator.is_principal()
        }

        return PipelineInstanceDTO(name=instance_dto.name,
                                   parameters=instance_dto.parameters,
                                   dependsOn=instance_dto.dependsOn,
                                   spec=PipelineSpecDTO(**instance_dto.spec.__dict__))

    @staticmethod
    def create_from_string(source, *args, **kwargs) -> 'Pipeline':
        return Pipeline.create_from_dto(PipelineInstanceDTO(**yaml.safe_load(source)), *args, **kwargs)

    @staticmethod
    def create_from_dto(instance_dto: 'PipelineInstanceDTO', *args, **kwargs) -> 'Pipeline':
        return cast(Pipeline, Instance.create_from_dto(instance_dto, *args, **kwargs))

    def _on_interrupt(self, system_signal: int = None) -> None:
        pass

    def _on_error(self) -> None:
        pass

