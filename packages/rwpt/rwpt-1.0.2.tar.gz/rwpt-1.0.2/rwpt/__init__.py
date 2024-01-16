"""
rwpt

A Romanian WordPiece tokenizer, that does Romanian clitic splitting,
recognizes some multi-word expressions and enforces the Romanian Academy
writing norms.
"""

__version__ = "1.0.2"
__author__ = 'Radu Ion'
__credits__ = 'Research Institute for AI, Romanian Academy'

from .ro_wordpiece import RoBertWordPieceTokenizer
from .ro_wordpiece import RoBertPreTrainedTokenizer


def get_bundled_vocab_file_path() -> str:
    """Returns the path to the Romanian CoRoLa trained vocab.txt file,
    included in this package."""
    return RoBertPreTrainedTokenizer.vocab_files_names['RoBertWordPieceTokenizer']


def load_ro_pretrained_tokenizer(max_sequence_len: int) -> RoBertPreTrainedTokenizer:
    """Takes the maximum length of an input sequence for a BERT forward call."""
    
    return RoBertPreTrainedTokenizer.from_pretrained(
        pretrained_model_name_or_path=get_bundled_vocab_file_path(),
        model_max_length=max_sequence_len)
