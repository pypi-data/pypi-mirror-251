#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import json
from typing import Any, cast, Dict, List, Optional, Tuple, Union


class MappingObject:
    """MappingObject is a simple representation of a DataRobot class to Open Source class."""

    def __init__(
        self,
        dr_class: str,
        open_class: Optional[Union[str, Dict[str, Union[str, Dict[str, str]]]]] = None,
        dr_class_params_mapping: Optional[Dict[str, Any]] = None,
        versions: Optional[List[str]] = None,
    ):
        self.dr_class = dr_class
        self.dr_class_params_mapping = (
            dr_class_params_mapping if dr_class_params_mapping is not None else {}
        )
        self.open_class = open_class
        if isinstance(self.open_class, dict):
            self.is_complex = True
        else:
            self.is_complex = False
        self.versions = versions if versions is not None else []

    @staticmethod
    def param_is_number(param: Union[str, int, float, List[Any], Tuple[Any]]) -> bool:
        """Identify if the parameter is a numeric type (int or float)"""
        try:
            float(param)  # type: ignore[arg-type]
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def param_is_list(param: Union[str, int, float, List[Any], Tuple[Any]]) -> bool:
        """Identify if the parameter is a list or list encoded as a tuple"""
        if "(" in str(param) or "[" in str(param):
            return True
        return False

    def clean_param_value(self, param: Union[str, int, float, List[Any], Tuple[Any]]) -> str:
        """Return a cleaned value for open blueprint representation
        Parameters
        ----------
        param : Union[str, int, float, List[Any], Tuple[Any]]
            The parameter as provided by datarobot. This can be a string, numeric or list type format of values.

        Returns
        -------
        clean_param: str
            Returns a cleaned parameter that is compatible with a pipeline in string format. There are two special
            cases that may occur.
            1. If the original parameter is NUMERIC:
                The value returned will be a string representation of the numeric input.
            2. If the original parameter represents a LIST-TYPE:
                The value returned will be a string representation of the FIRST value in the list type.
        """
        if self.param_is_number(param):
            return str(param)
        if self.param_is_list(param):
            if isinstance(param, str):
                param = param.strip().replace("(", "[").replace(")", "]")
                param = json.loads(param)
            param = list(param)[0]  # type: ignore[arg-type]
            return str(param)

        return f"'{param}'"

    def get_class_mappings(self) -> Dict[str, str]:
        """Return a list of class and clone mappings from dr_class to open source open_class."""
        class_mapping = {self.dr_class: self.dr_class}
        # Add clone mappings
        for version in self.versions:
            class_mapping[version] = self.dr_class
        return class_mapping

    def get_open_representation(self, dr_class_params: Optional[Dict[str, Any]] = None) -> str:
        # If no class is defined or the class has no good mapping, return "passthrough" with quotes
        if self.is_complex:
            return self.get_complex_open_representation()
        return self.get_simple_open_representation(dr_class_params)

    def get_simple_open_representation(
        self, dr_class_params: Optional[Dict[str, Any]] = None
    ) -> str:
        # If no class is defined or the class has no good mapping, return "passthrough" with quotes
        if self.open_class is None or self.open_class == "passthrough":
            return '"passthrough"'

        # If the open class is a complex passthrough directly constructed
        if "(" in self.open_class:
            return str(self.open_class)

        # Convert the dr_class_params to open_class_params
        dr_class_params = dr_class_params if dr_class_params is not None else {}
        open_class_param_string = ""

        for key, val in dr_class_params.items():
            if key in self.dr_class_params_mapping:
                val = self.clean_param_value(val)
                open_class_param_string += f"{self.dr_class_params_mapping[key]}={val},"

        return f"{self.open_class}({open_class_param_string})"

    def get_complex_open_representation(self) -> str:
        # For mypy cast open_class (it is already a dict)
        open_class = cast(Dict[str, Any], self.open_class)

        # At this time dr_class_params are not used by stacking class representations
        if "stacking_class" not in open_class:
            raise ValueError("stacking_class must be defined for complex class representations")
        if "stacking_class_estimators" not in open_class:
            raise ValueError(
                "stacking_class_estimators must be defined for complex class representations"
            )

        estimators = ""
        for key, value in open_class["stacking_class_estimators"].items():
            if "(" not in value:
                value = f"{value}()"
            estimators += f"('{key}', {value}),"

        stacking_estimator = open_class["stacking_class"]

        params = ""
        if "stacking_class_params" in open_class:
            for key, value in open_class["stacking_class_params"].items():
                params += f"{key}={value}"

        return f"{stacking_estimator}([{estimators}], {params})"

    def get_required_imports(self) -> Optional[Union[str, List[str]]]:
        # If no class is defined or the class has no good mapping, return "passthrough" with quotes
        if self.open_class is None or self.open_class == "passthrough":
            return None

        if not self.is_complex:
            return self.parse_class_import(str(self.open_class))

        open_class = cast(Dict[str, Any], self.open_class)
        required_imports = [self.parse_class_import(str(open_class["stacking_class"]))]
        for _, value in open_class["stacking_class_estimators"].items():
            required_imports.append(self.parse_class_import(str(value)))

        return sorted(set(required_imports))

    @staticmethod
    def parse_class_import(open_class_str: str) -> str:
        open_class_parts = open_class_str.split(".")
        return (
            open_class_parts[0] if len(open_class_parts) == 1 else ".".join(open_class_parts[:-1])
        )
