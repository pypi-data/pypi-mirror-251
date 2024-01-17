from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Type, Union

import torch
from pydantic import BaseModel, Field, field_validator

from omnivault.transformer.utils.device import get_device

__all__ = ["TrainerConfig"]


class TrainerConfig(BaseModel):
    device: str = Field(default="auto", description="Device to use for training.")

    # general
    max_epochs: int = Field(default=2, description="Number of epochs to train for.")
    log_every_n_steps: int = Field(default=1, description="Log every n steps.")
    eval_every_n_steps: int = Field(default=1, description="Number of epochs between evaluations.")
    step_scheduler_on_batch_or_epoch: str = Field(
        default="epoch",
        description="Whether to step the scheduler on batch or epoch. "
        "If set to 'epoch', the scheduler will be stepped after each epoch. "
        "If set to 'batch', the scheduler will be stepped after each batch.",
    )

    # training stability
    # 1. gradient clipping
    clip_grad_norm: Union[Dict[str, Any], None] = Field(
        default={"max_norm": 1.0, "norm_type": 2.0, "error_if_nonfinite": False, "foreach": None},
        description="Gradient clipping, for details of the params, see `torch.nn.utils.clip_grad_norm_`.",
    )

    # 2. weight decay on targetted parameter groups
    apply_weight_decay_to_different_param_groups: bool = Field(
        default=False, description="Whether to apply weight decay to different parameter groups."
    )

    # saving shenanigans
    save_dir: Union[str, None] = Field(default="checkpoints", description="Directory to save checkpoints to.")
    save_every_epoch: bool = Field(default=False, description="Always save the model after each epoch.")
    save_best_only: bool = Field(default=True, description="Only save the best model.")
    monitor: str = Field(
        default="valid_this_epoch_average_loss",
        description="The metric to monitor for saving best model.",
        examples=[
            "valid_this_epoch_average_loss",
            "valid_this_batch_average_loss",
            "train_this_epoch_average_loss",
            "train_this_batch_average_loss",
            "train_this_epoch_average_accuracy",
            "train_this_batch_average_accuracy",
            "valid_this_epoch_average_accuracy",
            "valid_this_batch_average_accuracy",
        ],
    )
    mode: str = Field(default="min", description="The mode to monitor for saving best model.", examples=["min", "max"])

    @field_validator("device", mode="plain")
    @classmethod
    def set_device(cls: Type[TrainerConfig], v: str) -> torch.device:
        if v == "auto":
            return get_device()
        return torch.device(v)

    @field_validator("save_dir")
    @classmethod
    def set_and_create_timestamped_save_dir(cls: Type[TrainerConfig], v: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        v = f"{v}/{timestamp}"

        Path(v).mkdir(parents=True, exist_ok=True)
        return v
