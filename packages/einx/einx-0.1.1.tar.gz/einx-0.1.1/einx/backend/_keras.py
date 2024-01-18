from functools import partial
from .base import base_backend, associative_binary_to_nary
import einx

def make_keras_backend():
    import keras as keras_
    import numpy as np

    def einx_backend_for_keras():
        return einx.backend.get(keras_.config.backend())

    class keras(base_backend):
        @staticmethod
        def to_tensor(tensor):
            if isinstance(tensor, keras_.KerasTensor):
                return tensor
            else:
                return einx_backend_for_keras().to_tensor(tensor)

        tensor = keras_.KerasTensor
        name = "keras"

        def cast(tensor, dtype):
            return keras_.ops.cast(tensor, dtype=dtype)
        reshape = keras_.ops.reshape
        transpose = keras_.ops.transpose
        broadcast_to = keras_.ops.broadcast_to
        einsum = keras_.ops.einsum
        dot = keras_.ops.dot
        swapaxes = keras_.ops.swapaxes
        def arange(start, stop=None, step=1, dtype="float32"):
            return keras_.ops.arange(start, stop, step=step, dtype=dtype)

        stack = keras_.ops.stack
        concatenate = keras_.ops.concatenate

        def empty(shape, dtype="float32"):
            return keras_.KerasTensor(shape=shape, dtype=dtype)
        def zeros(shape, dtype="float32"):
            return keras_.ops.zeros(shape=shape, dtype=dtype)
        def ones(shape, dtype="float32"):
            return keras_.ops.ones(shape=shape, dtype=dtype)

        add = associative_binary_to_nary(keras_.ops.add)
        subtract = keras_.ops.subtract
        multiply = associative_binary_to_nary(keras_.ops.multiply)
        true_divide = keras_.ops.true_divide
        floor_divide = keras_.ops.floor_divide
        divide = keras_.ops.divide
        logical_and = associative_binary_to_nary(keras_.ops.logical_and)
        logical_or = associative_binary_to_nary(keras_.ops.logical_or)
        where = keras_.ops.where
        less = keras_.ops.less
        less_equal = keras_.ops.less_equal
        greater = keras_.ops.greater
        greater_equal = keras_.ops.greater_equal
        equal = keras_.ops.equal
        not_equal = keras_.ops.not_equal
        maximum = associative_binary_to_nary(keras_.ops.maximum)
        minimum = associative_binary_to_nary(keras_.ops.minimum)

        sum = keras_.ops.sum
        mean = keras_.ops.mean
        var = keras_.ops.var
        std = keras_.ops.std
        prod = keras_.ops.prod
        count_nonzero = keras_.ops.count_nonzero
        any = keras_.ops.any
        all = keras_.ops.all
        min = keras_.ops.amin
        max = keras_.ops.amax
        logsumexp = keras_.ops.logsumexp

        def get_at(tensor, coordinates):
            return tensor[coordinates]
        # def set_at(tensor, coordinates, updates):
        #     return tensor.at[coordinates].set(updates)
        # def add_at(tensor, coordinates, updates):
        #     return tensor.at[coordinates].add(updates)
        # def subtract_at(tensor, coordinates, updates):
        #     return tensor.at[coordinates].add(-updates)

        flip = keras_.ops.flip
        roll = keras_.ops.roll
        def softmax(x, axis=None):
            x = x - keras_.ops.max(x, axis=axis, keepdims=True)
            return keras_.ops.exp(x) / keras_.ops.sum(keras_.ops.exp(x), axis=axis, keepdims=True)
        def log_softmax(x, axis=None):
            x = x - keras_.ops.max(x, axis=axis, keepdims=True)
            return x - keras_.ops.log(keras_.ops.sum(keras_.ops.exp(x), axis=axis, keepdims=True))

        sqrt = keras_.ops.sqrt
        rsqrt = keras_.ops.rsqrt
        square = keras_.ops.square

        def allclose(*args, **kwargs):
            return keras_.ops.all(keras_.ops.isclose(*args, **kwargs))

        def vmap(op, in_axes, out_axes):
            raise NotImplementedError("vmap is not supported in keras backend")

        class random:
            def bernoulli(rng, p, shape):
                assert False, "TODO"
                return keras_.backend.random.uniform(0.0, 1.0, dtype="float32", shape=shape) <= p

    return keras