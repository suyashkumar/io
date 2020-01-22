# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""Genomics related ops for Tensorflow.

This package provides ops for reading common genomics file formats and
performing common genomics IO-related operations. 
"""

from tensorflow_io.core.python.ops.genome_ops import read_fastq # pylint: disable=unused-import
from tensorflow_io.core.python.ops.genome_ops import sequences_to_onehot # pylint: disable=unused-import
from tensorflow_io.core.python.ops.genome_ops import phred_sequences_to_probability # pylint: disable=unused-import
