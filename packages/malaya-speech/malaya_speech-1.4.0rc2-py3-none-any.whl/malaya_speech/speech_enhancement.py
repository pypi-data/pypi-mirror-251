from malaya_speech.supervised import unet
from herpetologist import check_type
from malaya_speech.utils import describe_availability
import logging

logger = logging.getLogger(__name__)

# https://github.com/sigsep/sigsep-mus-eval/blob/master/museval/__init__.py#L364
# Only calculate SDR, ISR, SAR on voice sample

_masking_availability = {
    'unet': {
        'Size (MB)': 78.9,
        'Quantized Size (MB)': 20,
        'SUM MAE': 0.85896,
        'MAE_SPEAKER': 0.46849,
        'MAE_NOISE': 0.39046,
        'SDR': 12.12805,
        'ISR': 14.67067,
        'SAR': 15.019682,
        'sample rate': 44100,
    },
    'resnet-unet': {
        'Size (MB)': 91.4,
        'Quantized Size (MB)': 23,
        'SUM MAE': 0.8153995,
        'MAE_SPEAKER': 0.447958,
        'MAE_NOISE': 0.367441,
        'SDR': 12.349259,
        'ISR': 14.85418,
        'SAR': 15.21751,
        'sample rate': 44100,
    },
}

_sampling_availability = {
    'unet': {
        'Size (MB)': 40.7,
        'Quantized Size (MB)': 10.3,
        'SDR': 9.877178,
        'ISR': 15.916217,
        'SAR': 13.709130,
        'sample rate': 22050,
    },
    'resnet-unet': {
        'Size (MB)': 36.4,
        'Quantized Size (MB)': 9.29,
        'SDR': 9.43617,
        'ISR': 16.86103,
        'SAR': 12.32157,
        'sample rate': 22050,
    },
    'resnext-unet': {
        'Size (MB)': 36.1,
        'Quantized Size (MB)': 9.26,
        'SDR': 9.685578,
        'ISR': 16.42137,
        'SAR': 12.45115,
        'sample rate': 22050,
    },
}


def available_deep_masking():
    """
    List available Speech Enhancement STFT masking deep learning model.
    """
    logger.info('Only calculate SDR, ISR, SAR on voice sample. Higher is better.')

    return describe_availability(_masking_availability)


def available_deep_enhance():
    """
    List available Speech Enhancement UNET Waveform sampling deep learning model.
    """
    logger.info('Only calculate SDR, ISR, SAR on voice sample. Higher is better.')

    return describe_availability(_sampling_availability)


@check_type
def deep_masking(model: str = 'resnet-unet', quantized: bool = False, **kwargs):
    """
    Load Speech Enhancement STFT UNET masking deep learning model.

    Parameters
    ----------
    model : str, optional (default='resnet-unet')
        Check available models at `malaya_speech.speech_enhancement.available_deep_masking()`.
    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.unet.UNETSTFT class
    """

    model = model.lower()
    if model not in _masking_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.speech_enhancement.available_deep_masking()`.'
        )

    return unet.load_stft(
        model=model,
        module='speech-enhancement-mask',
        instruments=['voice', 'noise'],
        quantized=quantized,
        **kwargs
    )


@check_type
def deep_enhance(model: str = 'unet', quantized: bool = False, **kwargs):
    """
    Load Speech Enhancement UNET Waveform sampling deep learning model.

    Parameters
    ----------
    model : str, optional (default='unet')
        Check available models at `malaya_speech.speech_enhancement.available_deep_enhance()`.
    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.unet.UNET1D class
    """

    model = model.lower()
    if model not in _sampling_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.speech_enhancement.available_deep_enhance()`.'
        )

    return unet.load_1d(
        model=model,
        module='speech-enhancement',
        quantized=quantized,
        **kwargs
    )
