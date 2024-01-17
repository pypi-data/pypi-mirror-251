"""This package provides support for CodeGrades Feedback messages in AutoTest
V2. It was developed mainly to be used with the ``Simple Python Test`` block
and provides an assertion-based API to provide feedback during the execution of
a piece of student code, as well as providing some useful helper functions to
more easily do input/output testing on said code.

To install locally, run ``python3 -mpip install cg-feedback-helpers``. To start,
take a look at :class:`cg_feedback_helpers.assertions.Asserter`.
"""

from . import helpers
from .types import NO_FEEDBACK, Feedback, FeedbackType
from .config import (
    Config, ExistFeedbackMaker, ExistFeedbackMakerF, ExpectFeedbackMaker,
    DefaultExistFeedback, ExpectFeedbackMakerF, PrimedFeedbackMakerF,
    DefaultExpectFeedback, ExistFeedbackMakerInput, ExpectFeedbackMakerInput
)
from .assertions import Asserter, FeedbackAssertionError, asserter
from .compatibility_layer import (
    emit_success, assert_equals, assert_is_set, assert_not_none,
    assert_has_length, assert_is_of_type, assert_not_equals,
    assert_file_exists, assert_is_imported
)

__all__ = [
    "Asserter",
    "asserter",
    "helpers",
    "NO_FEEDBACK",
    "FeedbackType",
    "Feedback",
    "FeedbackAssertionError",
    "Config",
    "ExpectFeedbackMaker",
    "ExistFeedbackMaker",
    "DefaultExistFeedback",
    "DefaultExpectFeedback",
    "ExpectFeedbackMakerInput",
    "ExistFeedbackMakerInput",
    "ExpectFeedbackMakerF",
    "ExistFeedbackMakerF",
    "PrimedFeedbackMakerF",
    "assert_is_set",
    "assert_equals",
    "assert_not_equals",
    "assert_is_of_type",
    "assert_has_length",
    "assert_not_none",
    "assert_file_exists",
    "assert_is_imported",
    "emit_success",
]
