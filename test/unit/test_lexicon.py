# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import os
from tempfile import TemporaryDirectory

import numpy as np

import sockeye.constants as C
import sockeye.lexicon


def test_topk_lexicon():
    vocab_list = ["a", "b", "c"]
    vocab = dict((y, x) for (x, y) in enumerate(C.VOCAB_SYMBOLS + vocab_list))
    k = 2
    lex = sockeye.lexicon.TopKLexicon(vocab, vocab, k)

    # Create from known lexicon
    with TemporaryDirectory(prefix="test_topk_lexicon.") as work_dir:
        input_lex_path = os.path.join(work_dir, "input.lex")
        with open(input_lex_path, "w") as out:
            print("a\ta\t-0.6931471805599453", file=out)
            print("a\tb\t-1.2039728043259361", file=out)
            print("a\tc\t-1.6094379124341003", file=out)
            print("b\tb\t0.0", file=out)
        lex.create(input_lex_path)

        # Test against known lexicon
        expected = np.zeros((len(C.VOCAB_SYMBOLS) + len(vocab_list), k), dtype=np.int)
        expected[len(C.VOCAB_SYMBOLS),:2] = [len(C.VOCAB_SYMBOLS), len(C.VOCAB_SYMBOLS) + 1]
        expected[len(C.VOCAB_SYMBOLS) + 1,:1] = [len(C.VOCAB_SYMBOLS) + 1]
        assert np.all(lex.lex == expected)

        # Test save/load
        json_lex_path = os.path.join(work_dir, "lex.json")
        lex.save(json_lex_path)
        lex.load(json_lex_path)
        assert np.all(lex.lex == expected)
