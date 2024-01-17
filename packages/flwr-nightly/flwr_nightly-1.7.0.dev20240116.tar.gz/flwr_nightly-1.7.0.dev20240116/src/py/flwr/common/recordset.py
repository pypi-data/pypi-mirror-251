# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""RecordSet."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ParametersRecord:
    """Parameters record."""


@dataclass
class MetricsRecord:
    """Metrics record."""


@dataclass
class ConfigsRecord:
    """Configs record."""


@dataclass
class RecordSet:
    """Definition of RecordSet."""

    parameters: Dict[str, ParametersRecord] = {}
    metrics: Dict[str, MetricsRecord] = {}
    configs: Dict[str, ConfigsRecord] = {}

    def set_parameters(self, name: str, record: ParametersRecord) -> None:
        """Add a ParametersRecord."""
        self.parameters[name] = record

    def get_parameters(self, name: str) -> ParametersRecord:
        """Get a ParametesRecord."""
        return self.parameters[name]

    def del_parameters(self, name: str) -> None:
        """Delete a ParametersRecord."""
        del self.parameters[name]

    def set_metrics(self, name: str, record: MetricsRecord) -> None:
        """Add a MetricsRecord."""
        self.metrics[name] = record

    def get_metrics(self, name: str) -> MetricsRecord:
        """Get a MetricsRecord."""
        return self.metrics[name]

    def del_metrics(self, name: str) -> None:
        """Delete a MetricsRecord."""
        del self.metrics[name]

    def set_configs(self, name: str, record: ConfigsRecord) -> None:
        """Add a ConfigsRecord."""
        self.configs[name] = record

    def get_configs(self, name: str) -> ConfigsRecord:
        """Get a ConfigsRecord."""
        return self.configs[name]

    def del_configs(self, name: str) -> None:
        """Delete a ConfigsRecord."""
        del self.configs[name]
