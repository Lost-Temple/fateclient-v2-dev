from transformers import TrainingArguments as _hf_TrainingArguments
from dataclasses import dataclass, field, fields
from typing import Union, Literal
from enum import Enum


class AggregateStrategy(Enum):
    EPOCH = "epochs"
    STEP = "steps"


class AggregatorType(Enum):
    PLAINTEXT = "plaintext"
    SECURE_AGGREGATE = "secure_aggregate"


@dataclass
class FedArguments(object):
    """
    The argument for Fed algorithm
    """

    aggregate_strategy: str = field(default=AggregateStrategy.EPOCH.value)
    aggregate_freq: int = field(default=1)
    aggregator: str = field(default=AggregatorType.SECURE_AGGREGATE.value)

    def to_dict(self):
        """
        Serializes this instance while replace `Enum` by their values (for JSON serialization support). It obfuscates
        the token values by removing their value.
        """
        # filter out fields that are defined as field(init=False)
        d = dict(
            (field.name, getattr(self, field.name))
            for field in fields(self)
            if field.init
        )

        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], Enum):
                d[k] = [x.value for x in v]
            if k.endswith("_token"):
                d[k] = f"<{k.upper()}>"
        return d


@dataclass
class _TrainingArguments(_hf_TrainingArguments):
    # in fate-2.0, we will control the output dir when using pipeline
    output_dir: str = field(default="./")
    disable_tqdm: bool = field(default=True)
    save_strategy: str = field(default="no")
    logging_strategy: str = field(default="epoch")
    evaluation_strategy: str = field(default="no")
    logging_dir: str = field(default=None)
    checkpoint_idx: int = field(default=None)
    # by default, we use constant learning rate, the same as FATE-1.X
    lr_scheduler_type: str = field(default="constant")
    log_level: str = field(default="info")

    def __post_init__(self):
        self.push_to_hub = False
        self.hub_model_id = None
        self.hub_strategy = "every_save"
        self.hub_token = None
        self.hub_private_repo = False
        self.push_to_hub_model_id = None
        self.push_to_hub_organization = None
        self.push_to_hub_token = None

        super().__post_init__()


@dataclass
class TrainingArguments(_TrainingArguments):

    # To simplify the to dict result(to_dict only return non-default args)

    def to_dict(self):
        # Call the superclass's to_dict method
        all_args = super().to_dict()
        # Get a dict with default values for all fields
        default_args = _TrainingArguments().to_dict()
        # Filter out args that are equal to their default values
        set_args = {name: value for name, value in all_args.items() if value != default_args.get(name)}
        return set_args

@dataclass
class FedAVGArguments(FedArguments):
    pass


@dataclass
class Args(object):
    def to_dict(self):
        d = dict((field.name, getattr(self, field.name)) for field in fields(self) if field.init)
        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], Enum):
                d[k] = [x.value for x in v]
            if k.endswith("_token"):
                d[k] = f"<{k.upper()}>"
        return d


@dataclass
class StdAggLayerArgument(Args):

    merge_type: Literal['sum', 'concat'] = 'sum'
    concat_dim = 1

    def to_dict(self):
        d = super().to_dict()
        d['agg_type'] = 'std'
        return d


@dataclass
class FedPassArgument(StdAggLayerArgument):

    layer_type: Literal['conv', 'linear'] = 'conv'
    in_channels_or_features: int = 8
    out_channels_or_features: int = 8
    kernel_size: Union[int, tuple] = 3
    stride: Union[int, tuple] = 1
    padding: int = 0
    bias: bool = True
    hidden_features: int = 128
    activation: Literal['relu', 'tanh', 'sigmoid'] = "relu"
    passport_distribute: Literal['gaussian', 'uniform'] = 'gaussian'
    passport_mode: Literal['single', 'multi'] = 'single'
    loc: int = -1.0
    scale: int = 1.0
    low: int = -1.0
    high: int = 1.0
    num_passport: int = 1
    ae_in: int = None
    ae_out: int = None

    def to_dict(self):
        d = super().to_dict()
        d['agg_type'] = 'fed_pass'
        return d


@dataclass
class HESSArgument(object):
    pass


def parse_agglayer_conf(agglayer_arg_conf):

    if 'agg_type' not in agglayer_arg_conf:
        raise ValueError('can not load agg layer conf, keyword agg_type not found')
    agg_type = agglayer_arg_conf['agg_type']
    agglayer_arg_conf.pop('agg_type')
    if agg_type == 'fed_pass':
        agglayer_arg = FedPassArgument(**agglayer_arg_conf['fed_pass_arg'])
    elif agg_type == 'std':
        agglayer_arg = StdAggLayerArgument(**agglayer_arg_conf['std_arg'])
    else:
        raise ValueError(f'agg type {agg_type} not supported')

    return agglayer_arg

"""
Top & Bottom Model Strategy
"""

@dataclass
class TopModelStrategyArguments(Args):

    protect_strategy: Literal['fedpass'] = None
    fed_pass_arg: Union[FedPassArgument, dict] = None
    add_output_layer: Literal[None, 'sigmoid', 'softmax'] = None

    def __post_init__(self):

        if self.protect_strategy == 'fedpass':
            if isinstance(self.fed_pass_arg, dict):
                self.fed_pass_arg = FedPassArgument(**self.fed_pass_arg)
            if not isinstance(self.fed_pass_arg, FedPassArgument):
                raise TypeError("fed_pass_arg must be an instance of FedPassArgument for protect_strategy 'fedpass'")

        assert self.add_output_layer in [None, 'sigmoid', 'softmax'], \
            "add_output_layer must be None, 'sigmoid' or 'softmax'"

    def to_dict(self):
        d = super().to_dict()
        if 'fed_pass_arg' in d:
            d['fed_pass_arg'] = d['fed_pass_arg'].to_dict()
            d['fed_pass_arg'].pop('agg_type')
        return d

