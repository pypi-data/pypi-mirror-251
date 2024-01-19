import tensorflow as tf
import numpy as np
from ..utils import shape_list


def slice_segments(x, ids_str, segment_size=8192, pad_val=0.0):
    b, _, d = shape_list(x)
    t = segment_size
    ret = tf.TensorArray(dtype=tf.float32, size=b)

    def condition(j, ret):
        return j < b

    def body(j, ret):
        idx_str = ids_str[j]
        idx_end = idx_str + segment_size
        x_ = x[j, idx_str:idx_end]
        x_ = tf.pad(x_, [[0, t - tf.shape(x_)[0]], [0, 0]], constant_values=pad_val)
        ret = ret.write(j, x_)
        return j + 1, ret

    init_state = (0, ret)
    _, ret = tf.while_loop(condition, body, init_state)
    ret = ret.stack()
    ret.set_shape((None, None, d))
    return ret


def rand_slice_segments(x, x_lengths=None, segment_size=8192, pad_val=0.0):
    b, t, d = shape_list(x)
    if x_lengths is None:
        x_lengths = t
    ids_str_max = x_lengths - segment_size + 1
    ids_str = tf.cast(tf.random.uniform([b], minval=0, maxval=1) * tf.cast(ids_str_max, tf.float32), tf.int32)
    ret = slice_segments(x, ids_str, segment_size, pad_val=pad_val)
    return ret, ids_str
