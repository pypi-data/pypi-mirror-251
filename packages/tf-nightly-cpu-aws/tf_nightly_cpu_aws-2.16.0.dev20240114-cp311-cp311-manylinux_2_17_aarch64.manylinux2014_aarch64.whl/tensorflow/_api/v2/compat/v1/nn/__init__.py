# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.nn namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.nn import experimental
from tensorflow._api.v2.compat.v1.nn import rnn_cell
from tensorflow.python.ops.gen_math_ops import tanh # line: 12519
from tensorflow.python.ops.gen_nn_ops import conv3d_backprop_filter_v2 as conv3d_backprop_filter # line: 2408
from tensorflow.python.ops.gen_nn_ops import conv3d_backprop_filter_v2 # line: 2408
from tensorflow.python.ops.gen_nn_ops import elu # line: 3783
from tensorflow.python.ops.gen_nn_ops import l2_loss # line: 5717
from tensorflow.python.ops.gen_nn_ops import lrn as local_response_normalization # line: 5806
from tensorflow.python.ops.gen_nn_ops import lrn # line: 5806
from tensorflow.python.ops.gen_nn_ops import relu # line: 11562
from tensorflow.python.ops.gen_nn_ops import selu # line: 11829
from tensorflow.python.ops.gen_nn_ops import softsign # line: 12232
from tensorflow.python.ops.array_ops import depth_to_space # line: 3779
from tensorflow.python.ops.array_ops import space_to_batch # line: 3727
from tensorflow.python.ops.array_ops import space_to_depth # line: 3760
from tensorflow.python.ops.candidate_sampling_ops import all_candidate_sampler # line: 430
from tensorflow.python.ops.candidate_sampling_ops import compute_accidental_hits # line: 466
from tensorflow.python.ops.candidate_sampling_ops import fixed_unigram_candidate_sampler # line: 306
from tensorflow.python.ops.candidate_sampling_ops import learned_unigram_candidate_sampler # line: 212
from tensorflow.python.ops.candidate_sampling_ops import log_uniform_candidate_sampler # line: 116
from tensorflow.python.ops.candidate_sampling_ops import uniform_candidate_sampler # line: 27
from tensorflow.python.ops.ctc_ops import collapse_repeated # line: 1172
from tensorflow.python.ops.ctc_ops import ctc_beam_search_decoder # line: 380
from tensorflow.python.ops.ctc_ops import ctc_beam_search_decoder_v2 # line: 446
from tensorflow.python.ops.ctc_ops import ctc_greedy_decoder # line: 297
from tensorflow.python.ops.ctc_ops import ctc_loss # line: 71
from tensorflow.python.ops.ctc_ops import ctc_loss_v2 # line: 787
from tensorflow.python.ops.ctc_ops import ctc_unique_labels # line: 1270
from tensorflow.python.ops.embedding_ops import embedding_lookup # line: 265
from tensorflow.python.ops.embedding_ops import embedding_lookup_sparse # line: 437
from tensorflow.python.ops.embedding_ops import safe_embedding_lookup_sparse # line: 850
from tensorflow.python.ops.math_ops import sigmoid # line: 4069
from tensorflow.python.ops.math_ops import softplus # line: 628
from tensorflow.python.ops.nn_impl import batch_norm_with_global_normalization # line: 1594
from tensorflow.python.ops.nn_impl import batch_normalization # line: 1420
from tensorflow.python.ops.nn_impl import depthwise_conv2d # line: 663
from tensorflow.python.ops.nn_impl import fused_batch_norm # line: 1491
from tensorflow.python.ops.nn_impl import l2_normalize # line: 540
from tensorflow.python.ops.nn_impl import log_poisson_loss # line: 43
from tensorflow.python.ops.nn_impl import moments # line: 1215
from tensorflow.python.ops.nn_impl import nce_loss # line: 2005
from tensorflow.python.ops.nn_impl import normalize_moments # line: 1182
from tensorflow.python.ops.nn_impl import relu_layer # line: 406
from tensorflow.python.ops.nn_impl import sampled_softmax_loss # line: 2209
from tensorflow.python.ops.nn_impl import separable_conv2d # line: 893
from tensorflow.python.ops.nn_impl import sigmoid_cross_entropy_with_logits # line: 109
from tensorflow.python.ops.nn_impl import swish as silu # line: 430
from tensorflow.python.ops.nn_impl import sufficient_statistics # line: 1077
from tensorflow.python.ops.nn_impl import swish # line: 430
from tensorflow.python.ops.nn_impl import weighted_cross_entropy_with_logits # line: 341
from tensorflow.python.ops.nn_impl import weighted_moments # line: 1318
from tensorflow.python.ops.nn_impl import zero_fraction # line: 620
from tensorflow.python.ops.nn_impl_distribute import compute_average_loss # line: 70
from tensorflow.python.ops.nn_impl_distribute import scale_regularization_loss # line: 27
from tensorflow.python.ops.nn_ops import approx_max_k # line: 5882
from tensorflow.python.ops.nn_ops import approx_min_k # line: 5945
from tensorflow.python.ops.nn_ops import atrous_conv2d # line: 1790
from tensorflow.python.ops.nn_ops import atrous_conv2d_transpose # line: 2814
from tensorflow.python.ops.nn_ops import avg_pool # line: 4530
from tensorflow.python.ops.nn_ops import avg_pool1d # line: 4616
from tensorflow.python.ops.nn_ops import avg_pool as avg_pool2d # line: 4530
from tensorflow.python.ops.nn_ops import avg_pool3d # line: 4663
from tensorflow.python.ops.nn_ops import avg_pool_v2 # line: 4463
from tensorflow.python.ops.nn_ops import bias_add # line: 3516
from tensorflow.python.ops.nn_ops import conv1d # line: 1982
from tensorflow.python.ops.nn_ops import conv1d_transpose # line: 2169
from tensorflow.python.ops.nn_ops import conv2d # line: 2367
from tensorflow.python.ops.nn_ops import conv2d_backprop_filter # line: 2489
from tensorflow.python.ops.nn_ops import conv2d_backprop_input # line: 2550
from tensorflow.python.ops.nn_ops import conv2d_transpose # line: 2615
from tensorflow.python.ops.nn_ops import conv3d_v1 as conv3d # line: 3254
from tensorflow.python.ops.nn_ops import conv3d_transpose # line: 3275
from tensorflow.python.ops.nn_ops import conv_transpose # line: 3428
from tensorflow.python.ops.nn_ops import convolution # line: 1033
from tensorflow.python.ops.nn_ops import crelu # line: 3590
from tensorflow.python.ops.nn_ops import depthwise_conv2d_native_backprop_filter as depthwise_conv2d_backprop_filter # line: 3126
from tensorflow.python.ops.nn_ops import depthwise_conv2d_native_backprop_input as depthwise_conv2d_backprop_input # line: 3054
from tensorflow.python.ops.nn_ops import depthwise_conv2d_native # line: 2979
from tensorflow.python.ops.nn_ops import depthwise_conv2d_native_backprop_filter # line: 3126
from tensorflow.python.ops.nn_ops import depthwise_conv2d_native_backprop_input # line: 3054
from tensorflow.python.ops.nn_ops import dilation2d_v1 as dilation2d # line: 553
from tensorflow.python.ops.nn_ops import dropout # line: 5370
from tensorflow.python.ops.nn_ops import erosion2d # line: 6400
from tensorflow.python.ops.nn_ops import fractional_avg_pool # line: 6255
from tensorflow.python.ops.nn_ops import fractional_max_pool # line: 6042
from tensorflow.python.ops.nn_ops import in_top_k # line: 6532
from tensorflow.python.ops.nn_ops import leaky_relu # line: 3667
from tensorflow.python.ops.nn_ops import log_softmax # line: 3923
from tensorflow.python.ops.nn_ops import max_pool # line: 4849
from tensorflow.python.ops.nn_ops import max_pool1d # line: 4911
from tensorflow.python.ops.nn_ops import max_pool2d # line: 4971
from tensorflow.python.ops.nn_ops import max_pool3d # line: 5084
from tensorflow.python.ops.nn_ops import max_pool_v2 # line: 4705
from tensorflow.python.ops.nn_ops import max_pool_with_argmax_v1 as max_pool_with_argmax # line: 5201
from tensorflow.python.ops.nn_ops import pool # line: 1508
from tensorflow.python.ops.nn_ops import quantized_avg_pool # line: 6603
from tensorflow.python.ops.nn_ops import quantized_conv2d # line: 6606
from tensorflow.python.ops.nn_ops import quantized_max_pool # line: 6612
from tensorflow.python.ops.nn_ops import quantized_relu_x # line: 6609
from tensorflow.python.ops.nn_ops import relu6 # line: 3630
from tensorflow.python.ops.nn_ops import softmax # line: 3910
from tensorflow.python.ops.nn_ops import softmax_cross_entropy_with_logits # line: 4184
from tensorflow.python.ops.nn_ops import softmax_cross_entropy_with_logits_v2_helper as softmax_cross_entropy_with_logits_v2 # line: 4052
from tensorflow.python.ops.nn_ops import sparse_softmax_cross_entropy_with_logits # line: 4279
from tensorflow.python.ops.nn_ops import top_k # line: 5815
from tensorflow.python.ops.nn_ops import with_space_to_batch # line: 572
from tensorflow.python.ops.nn_ops import xw_plus_b # line: 5297
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn # line: 348
from tensorflow.python.ops.rnn import dynamic_rnn # line: 506
from tensorflow.python.ops.rnn import raw_rnn # line: 986
from tensorflow.python.ops.rnn import static_bidirectional_rnn # line: 1592
from tensorflow.python.ops.rnn import static_rnn # line: 1314
from tensorflow.python.ops.rnn import static_state_saving_rnn # line: 1494

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "nn", public_apis=None, deprecation=False,
      has_lite=False)
