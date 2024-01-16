#
# For licensing see accompanying LICENSE.md file.
# Copyright (C) 2023 Argmax, Inc. All Rights Reserved.
#


import torch
import torch.nn as nn

from typing import Tuple

from argmaxtools.nn import Attention, AttentionType
from argmaxtools.utils import get_logger

logger = get_logger(__name__)


class QKFoldedAttention(Attention):
    """ Attention with folded weights for lossless compression

    blog.takeargmax.com/qk-fold
    """
    @classmethod
    def from_attention(cls, attention: Attention) -> "QKFoldedAttention":
        qk_fold = cls(
            attention.embed_dim,
            attention.n_heads,
            attention.attention_type,
            attention.n_kv_heads,
        )
        qk_fold.load_state_dict(attention.state_dict())
        qk_fold.fold_qk_weights()
        qk_fold = qk_fold.eval()

        return qk_fold

    def _fold_qk_weights(self,
                         q_proj: nn.Conv2d,
                         k_proj: nn.Conv2d,) -> Tuple[torch.Tensor]:
        """
        Fold query and key projection weights into a single weight matrix
        """
        assert q_proj.weight.shape == q_proj.weight.shape

        orig_dtype = q_proj.weight.dtype

        # Fold q and k weights assuming neither k nor q bias
        op1 = q_proj.weight[:, :, 0, 0].cpu().to(torch.float64)
        op2 = k_proj.weight[:, :, 0, 0].cpu().to(torch.float64)

        # Repeat key projection weight if AttentionHeadType != MultiHead
        repeats = op1.shape[0] // op2.shape[0]
        if repeats > 1:
            assert self.n_heads // self.n_kv_heads == repeats
            op2 = op2.repeat(repeats, 1)
        elif repeats != 1:
            raise ValueError(repeats)

        folded_weight = (op1 @ op2.T)[:, :, None, None].to(orig_dtype)

        q_proj_has_bias = q_proj.bias is not None and q_proj.bias.data.abs().gt(0.).any()
        if q_proj_has_bias:
            op1 = q_proj.bias.cpu().to(torch.float64)[None, :]
            op2 = k_proj.weight[:, :, 0, 0].cpu().to(torch.float64)
            if repeats > 1:
                op2 = op2.repeat(repeats, 1)

            folded_bias = (op1 @ op2).squeeze().to(orig_dtype)
        else:
            folded_bias = torch.zeros_like(q_proj.bias.data)

        return folded_weight, folded_bias

    def fold_qk_weights(self) -> None:
        """ Implements the weight folding optimization to fuse k_proj and q_proj weights
        """
        assert not hasattr(self, "qk_proj"), "fold_qk_weights() should be applied only once!"
        self = self.eval()
        device = self.q_proj.weight.device

        folded_w, folded_b = self._fold_qk_weights(
            self.q_proj,
            self.k_proj,
        )

        self.qk_proj = nn.Conv2d(folded_w.shape[1], folded_w.shape[0], 1, bias=True)
        delattr(self, "q_proj")
        delattr(self, "k_proj")

        self.qk_proj.weight.data = folded_w.to(device)
        self.qk_proj.bias.data = folded_b.to(device)

    def _qkv_proj(self,
                  input_embeds,
                  encoder_output_embeds,
                  kv_cache_update_mask):
        """ Compute qkv projections prescribed by attention type
        """
        if encoder_output_embeds is not None:
            if self.attention_type != AttentionType.EncoderDecoderCrossAttention:
                raise ValueError(
                    "`encoder_output_embeds` is only compatible with the "
                    "AttentionType.EncoderDecoderCrossAttention configuration")

            kv_proj_inputs = encoder_output_embeds
        else:
            kv_proj_inputs = input_embeds

        query = self.qk_proj(input_embeds)

        # TODO: Support KVCachedEncoderDecoderCrossAttention
        current_key = kv_proj_inputs
        current_value = self.v_proj(kv_proj_inputs)

        return query, current_key, current_value

    def _finalize_kv(self,
                     key_cache,
                     value_cache,
                     current_key,
                     current_value,
                     kv_cache_update_mask,
                     encoder_output_embeds):
        """
        Determine the key and value tensors based on attention type. If head type is GQA or MQA,
        repeat key and value tensors to match the query tensor embedding dimensionality.
        """
        # Repeat the key-value channels for MQA and GQA
        # Since QK Fold bypasses k_proj, current_key is already tiled
        # Hence, key_cache and value_cache are the only tensors that need to be tiled
        if self.attention_type == AttentionType.KVCachedSelfAttention:
            key_cache, value_cache = self._maybe_tile(key_cache, value_cache)

        return super()._finalize_kv(key_cache,
                                    value_cache,
                                    current_key,
                                    current_value,
                                    kv_cache_update_mask,
                                    encoder_output_embeds)


def fold_qk_weights(model: nn.Module) -> nn.Module:
    """ Applies QK weight folding to all `Attention` submodules of `model`
    """
    logger.info("fold_qk_weights: Searching submodules to fold")

    num_tensors_removed = 0
    numel_reduced = 0

    def apply_fn(module):
        nonlocal numel_reduced, num_tensors_removed
        for child_name, child_module in module.named_children():
            if isinstance(child_module, Attention):
                numel_reduced += child_module.k_proj.weight.data.numel()
                num_tensors_removed += 1

                setattr(
                    module,
                    child_name,
                    QKFoldedAttention.from_attention(child_module)
                )

    model.apply(apply_fn)
    logger.info(
        f"fold_qk_weights: Removed {num_tensors_removed} tensors "
        f"totalling {numel_reduced/1e6:.1f} M parameters"
    )

    model.qk_folded = True

    return model
