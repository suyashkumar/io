# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
# ==============================================================================
"""Tests for Genome."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np

import tensorflow as tf
tf.compat.v1.disable_eager_execution()
import tensorflow_io.genome as genome_io # pylint: disable=wrong-import-position

fastq_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "test_genome", "test.fastq")

def test_genome_fastq_reader():
  """test_genome_fastq_reader"""
  g1 = tf.compat.v1.Graph()

  with g1.as_default():
    data = genome_io.fastq_op(filename=fastq_path)

  sess = tf.compat.v1.Session(graph=g1)
  data_np = sess.run(data)
  print(data_np)

  data_expected = [
      'GATTACA',
      'CGTTAGCGCAGGGGGCATCTTCACACTGGTGACAGGTAACCGCCGTAGTAAAGGTTCCGCCTTTCACT',
      'CGGCTGGTCAGGCTGACATCGCCGCCGGCCTGCAGCGAGCCGCTGC',
      'CGG']
  assert np.all(data_np == data_expected)

if __name__ == "__main__":
  test.main()
