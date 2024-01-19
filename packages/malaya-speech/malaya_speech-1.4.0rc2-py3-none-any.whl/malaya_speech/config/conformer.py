# https://arxiv.org/pdf/2005.08100.pdf, Table 1

tiny_encoder_config = {
    'name': 'conformer',
    'subsampling': {
        'type': 'conv2d',
        'filters': 144,
        'kernel_size': 3,
        'strides': 2,
    },
    'positional_encoding': 'sinusoid_concat',
    'dmodel': 144,
    'num_blocks': 8,
    'head_size': 36,
    'num_heads': 4,
    'mha_type': 'relmha',
    'kernel_size': 32,
    'fc_factor': 0.5,
    'dropout': 0.1,
}

small_encoder_config = {
    'name': 'conformer',
    'subsampling': {
        'type': 'conv2d',
        'filters': 144,
        'kernel_size': 3,
        'strides': 2,
    },
    'positional_encoding': 'sinusoid_concat',
    'dmodel': 144,
    'num_blocks': 16,
    'head_size': 36,
    'num_heads': 4,
    'mha_type': 'relmha',
    'kernel_size': 32,
    'fc_factor': 0.5,
    'dropout': 0.1,
}

base_encoder_config = {
    'name': 'conformer',
    'subsampling': {
        'type': 'conv2d',
        'filters': 144,
        'kernel_size': 3,
        'strides': 2,
    },
    'positional_encoding': 'sinusoid_concat',
    'dmodel': 256,
    'num_blocks': 16,
    'head_size': 36,
    'num_heads': 4,
    'mha_type': 'relmha',
    'kernel_size': 32,
    'fc_factor': 0.5,
    'dropout': 0.1,
}

large_encoder_config = {
    'name': 'conformer',
    'subsampling': {
        'type': 'conv2d',
        'filters': 144,
        'kernel_size': 3,
        'strides': 2,
    },
    'positional_encoding': 'sinusoid_concat',
    'dmodel': 512,
    'num_blocks': 16,
    'head_size': 36,
    'num_heads': 8,
    'mha_type': 'relmha',
    'kernel_size': 32,
    'fc_factor': 0.5,
    'dropout': 0.1,
}

xlarge_encoder_config = {
    'name': 'conformer',
    'subsampling': {
        'type': 'conv2d',
        'filters': 144,
        'kernel_size': 3,
        'strides': 2,
    },
    'positional_encoding': 'sinusoid_concat',
    'dmodel': 1024,
    'num_blocks': 16,
    'head_size': 36,
    'num_heads': 16,
    'mha_type': 'relmha',
    'kernel_size': 32,
    'fc_factor': 0.5,
    'dropout': 0.1,
}

xxlarge_encoder_config = {
    'name': 'conformer',
    'subsampling': {
        'type': 'conv2d',
        'filters': 144,
        'kernel_size': 3,
        'strides': 2,
    },
    'positional_encoding': 'sinusoid_concat',
    'dmodel': 2048,
    'num_blocks': 16,
    'head_size': 36,
    'num_heads': 32,
    'mha_type': 'relmha',
    'kernel_size': 32,
    'fc_factor': 0.5,
    'dropout': 0.1,
}

tiny_decoder_config = {
    'embed_dim': 128,
    'embed_dropout': 0.1,
    'num_rnns': 1,
    'rnn_units': 128,
    'rnn_type': 'lstm',
    'layer_norm': True,
    'projection_units': 0,
    'joint_dim': 128,
}

small_decoder_config = {
    'embed_dim': 320,
    'embed_dropout': 0.1,
    'num_rnns': 1,
    'rnn_units': 320,
    'rnn_type': 'lstm',
    'layer_norm': True,
    'projection_units': 0,
    'joint_dim': 320,
}

base_decoder_config = {
    'embed_dim': 640,
    'embed_dropout': 0.1,
    'num_rnns': 1,
    'rnn_units': 640,
    'rnn_type': 'lstm',
    'layer_norm': True,
    'projection_units': 0,
    'joint_dim': 640,
}

large_decoder_config = {
    'embed_dim': 640,
    'embed_dropout': 0.1,
    'num_rnns': 1,
    'rnn_units': 640,
    'rnn_type': 'lstm',
    'layer_norm': True,
    'projection_units': 0,
    'joint_dim': 640,
}

xlarge_decoder_config = {
    'embed_dim': 1024,
    'embed_dropout': 0.1,
    'num_rnns': 1,
    'rnn_units': 1024,
    'rnn_type': 'lstm',
    'layer_norm': True,
    'projection_units': 0,
    'joint_dim': 1024,
}
