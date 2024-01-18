import jax
import jax.numpy as jnp
from jax import random
from functools import partial
from typing import Optional, Mapping, Tuple, Sequence, Union, Any, Callable
import einops
import equinox as eqx
from abc import ABC, abstractmethod
from jaxtyping import Array, PRNGKeyArray
import generax.util.misc as misc
import numpy as np
from generax.flows.base import BijectiveTransform, TimeDependentBijectiveTransform

class FlowVF(eqx.Module):
  flow: BijectiveTransform
  w: Array

  def __init__(self,
               flow: BijectiveTransform):
    self.flow = flow
    self.w = jnp.ones(self.flow.input_shape)

  def __call__(self, x: Array) -> Array:
    assert x.shape == self.flow.input_shape
    z, _ = self.flow(x)
    z0, zrest = z[0], z[1:]
    def fwd(z0):
      z = jnp.concatenate([z0[None], zrest], axis=0)
      x, _ = self.flow(z, inverse=True)
      return x
    _, out = jax.jvp(fwd, (z0,), (self.w,))
    return out

  def divergence(self, x: Array) -> Array:
    assert x.shape == self.flow.input_shape
    z, log_det = self.flow(x)
    z0, zrest = z[0], z[1:]
    def fwd(z0):
      z = jnp.concatenate([z0[None], zrest], axis=0)
      x, log_det = self.flow(z, inverse=True)
      return log_det
    _, out = jax.jvp(fwd, (z0,), (self.w,))
    return out

  def vf_and_div(self, x: Array) -> Array:
    z, _ = self.flow(x)
    z0, zrest = z[0], z[1:]
    def fwd(z0):
      z = jnp.concatenate([z0[None], zrest], axis=0)
      x, log_det = self.flow(z, inverse=True)
      return x, log_det
    _, (v, div) = jax.jvp(fwd, (z0,), (self.w,))
    return v, div


class TimeDependentFlowVF(eqx.Module):
  flow: TimeDependentBijectiveTransform
  w: Array

  def __init__(self,
               flow: TimeDependentBijectiveTransform):
    self.flow = flow
    self.w = jnp.ones(self.flow.input_shape)

  def __call__(self, t: Array, x: Array) -> Array:
    return self.vf_and_div(t, x)[0]

  def divergence(self, t: Array, x: Array) -> Array:
    return self.vf_and_div(t, x)[1]

  def vf_and_div(self, t: Array, x: Array) -> Array:
    assert x.shape == self.flow.input_shape
    z, _ = self.flow(t, x)
    z0, zrest = z[0], z[1:]
    def fwd(z0):
      z = jnp.concatenate([z0[None], zrest], axis=0)
      x, log_det = self.flow(t, z, inverse=True)
      return x, log_det
    _, (v, div) = jax.jvp(fwd, (z0,), (self.w,))
    return v, div
