#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import List, Literal
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactChannel


class Evaluation(Component):
    yaml_define_path = "./component_define/fate/evaluation.yaml"

    def __init__(self,
                 name: str,
                 runtime_roles: List[str] = None,
                 eval_type: Literal['binary', 'multi', 'regression'] = PlaceHolder(),
                 input_data: ArtifactChannel = PlaceHolder(),
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(Evaluation, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.input_data = input_data
        self.eval_type = eval_type
