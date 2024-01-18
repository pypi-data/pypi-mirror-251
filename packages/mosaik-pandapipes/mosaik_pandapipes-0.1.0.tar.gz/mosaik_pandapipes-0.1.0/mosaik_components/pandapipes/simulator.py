from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple

import mosaik_api_v3
import pandas as pd
from mosaik_api_v3.types import (
    CreateResult,
    CreateResultChild,
    Meta,
    ModelDescription,
    OutputData,
    OutputRequest,
)

import pandapipes as pp
import pandapipes.networks

# For META, see below. (Non-conventional order do appease the type
# checker.)

class Simulator(mosaik_api_v3.Simulator):
    _sid: str
    """This simulator's ID."""
    _step_size: Optional[int]
    """The step size for this simulator. If ``None``, the simulator
    is running in event-based mode, instead.
    """
    _net: pp.pandapipesNet
    """The pandapipesNet for this simulator."""

    def __init__(self):
        super().__init__(META)
        self._net = None  # type: ignore  # set in init()

    def init(self, sid: str, time_resolution: float, step_size: Optional[int] = None):
        self._sid = sid
        if not step_size:
            self.meta["type"] = "event-based"
        self._step_size = step_size

        return self.meta

    def create(self, num: int, model: str, **model_params: Any) -> List[CreateResult]:
        if model == "Grid":
            if num != 1:
                raise ValueError("must create exactly one Grid entity")
            return [self.create_grid(**model_params)]

        if not self._net:
            raise ValueError(f"cannot create {model} entities before creating Grid")

        else:
           raise ValueError(f"no entities for the model {model} can be created")
         
    def create_grid(self, **params: Any) -> CreateResult:
        if self._net:
            raise ValueError("Grid was already created") 
        self._net, self._profiles = load_grid(params)
        child_entities: List[CreateResultChild] = []

        for child_model, info in MODEL_TO_ELEMENT_INFO.items():
            if  child_model in self._net:
                for elem_tuple in self._net[info.elem].itertuples():
                    child_entities.append(
                        {
                            "type": child_model,
                            "eid": f"{child_model}-{elem_tuple.Index}",
                            "rel": [
                                f"Junction-{getattr(elem_tuple, junction)}"
                                for junction in info.connected_junctions
                            ],
                        }
                    )
        return {
            "eid": "Grid",
            "type": "Grid",
            "children": child_entities,
            "rel": [],
        }

    def setup_done(self):
       pass

    def get_model_and_idx(self, eid: str) -> Tuple[str, int]:
        model, idx_str = eid.split("-")
        return (model, int(idx_str))

    def step(self, time, inputs, max_advance):
        for eid, data in inputs.items():
            model, idx = self.get_model_and_idx(eid)
            info = MODEL_TO_ELEMENT_INFO[model]

            for attr, values in data.items():
                attr_info = info.in_attrs[attr]
                self._net[attr_info.target_elem or info.elem].at[
                    attr_info.idx_fn(idx, self), attr_info.column
                ] = attr_info.aggregator(values.values())

        pp.pipeflow(self._net)
        print(f"Results at each junction:{self._net.res_junction}")
        print(f"Results at each pipe:{self._net.res_pipe}")
        if self._step_size:
            return time + self._step_size

    def get_data(self, outputs: OutputRequest) -> OutputData:
        return {eid: self.get_entity_data(eid, attrs) for eid, attrs in outputs.items()}

    def get_entity_data(self, eid: str, attrs: List[str]) -> Dict[str, Any]:
        model, idx = self.get_model_and_idx(eid)
        info = MODEL_TO_ELEMENT_INFO[model]
        elem_table = self._net[f"res_{info.elem}"]
        return {
            attr: elem_table.at[idx, info.out_attr_to_column[attr]] for attr in attrs
        }

@dataclass
class InAttrInfo:
    """Specificaction of an input attribute of a model."""

    column: str
    """The name of the column in the target element's dataframe
    corresponding to this attribute.
    """
    target_elem: Optional[str] = None
    """The name of the pandaipes element to which this attribute's
    inputs are written. (This might not be the element type
    corresponding to the model to support connecting Components
    directly to the buses.)
    If ``None``, use the element corresponding to the model.
    """
    idx_fn: Callable[[int, Simulator], int] = lambda idx, sim: idx
    """A function to transform the entity ID's index part into the
    index for the target_df.
    """
    aggregator: Callable[[Iterable[Any]], Any] = sum
    """The function that is used for aggregation if several values are
    given for this attribute.
    """

@dataclass
class ModelElementInfo:
    """Specification of the pandapipes element that is represented by
    a (mosaik) model of this simulator.
    """
    elem: str
    """The name of the pandapipes element corresponding to this model.
    """
    connected_junctions: List[str]
    """The names of the columns specifying the buses to which this
    element is connected.
    """
    in_attrs: Dict[str, InAttrInfo]
    """Mapping each input attr to the corresponding column in the
    element's dataframe and an aggregation function.
    """
    out_attr_to_column: Dict[str, str]
    """Mapping each output attr to the corresponding column in the
    element's result dataframe.
    """
    #TODO: Add Option to create grid elements by the User
    #createable: bool = False
    #"""Whether this element can be created by the user.""" 
    params: List[str] = field(default_factory=list)
    """The mosaik params that may be given when creating this element.
    (Only sensible if ``createable=True``.)
    """

MODEL_TO_ELEMENT_INFO = {
    "junction": ModelElementInfo(
        elem="junction",
        connected_junctions=[],
        in_attrs={},# TODO: Add Option to add source/sink by user to it
        out_attr_to_column={
            "p[bar]": "p_bar",
            "t[k]": "t_k",
        },
    ),
    "source": ModelElementInfo(    
        elem="source",
        connected_junctions=["junction"],
        in_attrs={
                "mdot_source[kg/s]": InAttrInfo(
                column="mdot_kg_per_s",
                ),
        },
        out_attr_to_column={
            "mdot[kg/s]": "mdot_kg_per_s",
        },
    ),
    "sink": ModelElementInfo(       
        elem="sink",
        connected_junctions=["junction"],
        in_attrs={
                "mdot_sink[kg/s]": InAttrInfo(
                column="mdot_kg_per_s"
                ),
        },
        out_attr_to_column={
            "mdot[kg/s]": "mdot_kg_per_s",
        },
    ),
    "pt": ModelElementInfo(     #ExternalGrid
        elem="ext_grid",
        connected_junctions=["junction"],
        in_attrs={},
        out_attr_to_column={
            "mdot[kg/s]": "mdot_kg_per_s",
        },
    ),
    "pipe": ModelElementInfo(
        elem="pipe",
        connected_junctions=["from_junction", "to_junction"],
        in_attrs={},
        out_attr_to_column={
            "Re": "reynolds",
            "lamda": "lamda",
            "v_mean[m/s]": "v_mean_m_per_s",
        },
    ),
    "valve": ModelElementInfo( 
        elem="valve",
        connected_junctions=["from_junction", "to_junction"],
        in_attrs={},
        out_attr_to_column={
            "Re": "reynolds",
            "lamda": "lamda",
            "v_mean[m/s]": "v_mean_m_per_s",
        },
    ),
    "mass_storage": ModelElementInfo( 
        elem="mass_storage",
        connected_junctions=["junction"],
        in_attrs={
                "mdot_storage[kg/s]": InAttrInfo(
                column="mdot_kg_per_s"
                ),
        },
        out_attr_to_column={
            "mdot[kg/s]": "mdot_kg_per_s",
        },
    ),
}

# Generate mosaik model descriptions out of the MODEL_TO_ELEMENT_INFO
ELEM_META_MODELS: Dict[str, ModelDescription] = {
    model: {
        "public": False,#info.createable,
        "params": info.params,
        "attrs": list(info.in_attrs.keys()) + list(info.out_attr_to_column.keys()),
        "any_inputs": False,
        "persistent": [],
        "trigger": [],
    }
    for model, info in MODEL_TO_ELEMENT_INFO.items()
}

META: Meta = {
    "api_version": "3.0",
    "type": "time-based",
    "models": {
        "Grid": {
            "public": True,
            "params": ["json", "xlsx", "net", "params"],
            "attrs": [],
            "any_inputs": False,
            "persistent": [],
            "trigger": [],
        },
        **ELEM_META_MODELS,
    },
    "extra_methods": [],
}

def load_grid(params: Dict[str, Any]) -> Tuple[pp.pandapipesNet, Any]:
    """Load a grid and the associated element profiles (if any).

    :param params: A dictionary describing which grid to load. It should
        contain one of the following keys (or key combinations).

        - `"net"` where the corresponding value is a pandapowerNet
        - `"json"` where the value is the name of a JSON file in
          pandapower JSON format
        - `"xlsx"` where the value is the name of an Excel file
        - `"params"` may be given to specify the kwargs 

    :return: a tuple consisting of a :class:`pandapowerNet`.

    :raises ValueError: if multiple keys are given in `params`
    """
    found_sources: Set[str] = set()
    result: Optional[Tuple[pp.pandapipesNet, Any]] = None

    # Accept a pandapipes grid
    if net := params.get("net", None):
        if isinstance(net, pp.pandapipesNet):
            result = (net, None)
            found_sources.add("net")
        else:
            raise ValueError("net is not a pandapipesNet instance")

    if json_path := params.get("json", None):
        result = (pp.from_json(json_path), None)
        found_sources.add("json")

    if xlsx_path := params.get("xlsx", None):
        result = (pp.from_excel(xlsx_path), None)
        found_sources.add("xlsx")

    if len(found_sources) != 1 or not result:
        raise ValueError(
            f"too many or too few sources specified for grid, namely: {found_sources}"
        )

    return result



