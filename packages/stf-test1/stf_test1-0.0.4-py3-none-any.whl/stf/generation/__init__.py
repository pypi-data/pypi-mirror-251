# Copyright 2022 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..utils import OptionalDependencyNotAvailable, _LazyModule, is_flax_available, is_tf_available, is_torch_available

_import_structure = {
    "configuration_utils": ["GenerationConfig"],
    "streamers": ["TextIteratorStreamer", "TextStreamer"],
}

try:
    if not is_torch_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    pass
else:
    _import_structure["beam_constraints"] = [
        "Constraint",
        "ConstraintListState",
        "DisjunctiveConstraint",
        "PhrasalConstraint",
    ]
    _import_structure["beam_search"] = [
        "BeamHypotheses",
        "BeamScorer",
        "BeamSearchScorer",
        "ConstrainedBeamSearchScorer",
    ]
    _import_structure["logits_process"] = [
        "AlternatingCodebooksLogitsProcessor",
        "ClassifierFreeGuidanceLogitsProcessor",
        "EncoderNoRepeatNGramLogitsProcessor",
        "EncoderRepetitionPenaltyLogitsProcessor",
        "EpsilonLogitsWarper",
        "EtaLogitsWarper",
        "ExponentialDecayLengthPenalty",
        "ForcedBOSTokenLogitsProcessor",
        "ForcedEOSTokenLogitsProcessor",
        "ForceTokensLogitsProcessor",
        "HammingDiversityLogitsProcessor",
        "InfNanRemoveLogitsProcessor",
        "LogitNormalization",
        "LogitsProcessor",
        "LogitsProcessorList",
        "LogitsWarper",
        "MinLengthLogitsProcessor",
        "MinNewTokensLengthLogitsProcessor",
        "NoBadWordsLogitsProcessor",
        "NoRepeatNGramLogitsProcessor",
        "PrefixConstrainedLogitsProcessor",
        "RepetitionPenaltyLogitsProcessor",
        "SequenceBiasLogitsProcessor",
        "SuppressTokensLogitsProcessor",
        "SuppressTokensAtBeginLogitsProcessor",
        "TemperatureLogitsWarper",
        "TopKLogitsWarper",
        "TopPLogitsWarper",
        "TypicalLogitsWarper",
        "UnbatchedClassifierFreeGuidanceLogitsProcessor",
        "WhisperTimeStampLogitsProcessor",
    ]
    _import_structure["stopping_criteria"] = [
        "MaxNewTokensCriteria",
        "MaxLengthCriteria",
        "MaxTimeCriteria",
        "StoppingCriteria",
        "StoppingCriteriaList",
        "validate_stopping_criteria",
    ]
    _import_structure["utils"] = [
        "GenerationMixin",
        "top_k_top_p_filtering",
        "GreedySearchEncoderDecoderOutput",
        "GreedySearchDecoderOnlyOutput",
        "SampleEncoderDecoderOutput",
        "SampleDecoderOnlyOutput",
        "BeamSearchEncoderDecoderOutput",
        "BeamSearchDecoderOnlyOutput",
        "BeamSampleEncoderDecoderOutput",
        "BeamSampleDecoderOnlyOutput",
        "ContrastiveSearchEncoderDecoderOutput",
        "ContrastiveSearchDecoderOnlyOutput",
    ]

try:
    if not is_tf_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    pass
else:
    _import_structure["tf_logits_process"] = [
        "TFForcedBOSTokenLogitsProcessor",
        "TFForcedEOSTokenLogitsProcessor",
        "TFForceTokensLogitsProcessor",
        "TFLogitsProcessor",
        "TFLogitsProcessorList",
        "TFLogitsWarper",
        "TFMinLengthLogitsProcessor",
        "TFNoBadWordsLogitsProcessor",
        "TFNoRepeatNGramLogitsProcessor",
        "TFRepetitionPenaltyLogitsProcessor",
        "TFSuppressTokensAtBeginLogitsProcessor",
        "TFSuppressTokensLogitsProcessor",
        "TFTemperatureLogitsWarper",
        "TFTopKLogitsWarper",
        "TFTopPLogitsWarper",
    ]
    _import_structure["tf_utils"] = [
        "TFGenerationMixin",
        "tf_top_k_top_p_filtering",
        "TFGreedySearchDecoderOnlyOutput",
        "TFGreedySearchEncoderDecoderOutput",
        "TFSampleEncoderDecoderOutput",
        "TFSampleDecoderOnlyOutput",
        "TFBeamSearchEncoderDecoderOutput",
        "TFBeamSearchDecoderOnlyOutput",
        "TFBeamSampleEncoderDecoderOutput",
        "TFBeamSampleDecoderOnlyOutput",
        "TFContrastiveSearchEncoderDecoderOutput",
        "TFContrastiveSearchDecoderOnlyOutput",
    ]

try:
    if not is_flax_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    pass
else:
    _import_structure["flax_logits_process"] = [
        "FlaxForcedBOSTokenLogitsProcessor",
        "FlaxForcedEOSTokenLogitsProcessor",
        "FlaxForceTokensLogitsProcessor",
        "FlaxLogitsProcessor",
        "FlaxLogitsProcessorList",
        "FlaxLogitsWarper",
        "FlaxMinLengthLogitsProcessor",
        "FlaxSuppressTokensAtBeginLogitsProcessor",
        "FlaxSuppressTokensLogitsProcessor",
        "FlaxTemperatureLogitsWarper",
        "FlaxTopKLogitsWarper",
        "FlaxTopPLogitsWarper",
        "FlaxWhisperTimeStampLogitsProcessor",
    ]
    _import_structure["flax_utils"] = [
        "FlaxGenerationMixin",
        "FlaxGreedySearchOutput",
        "FlaxSampleOutput",
        "FlaxBeamSearchOutput",
    ]

from .streamers import TextIteratorStreamer, TextStreamer
import sys

sys.modules[__name__] = _LazyModule(__name__, globals()["__file__"], _import_structure, module_spec=__spec__)
