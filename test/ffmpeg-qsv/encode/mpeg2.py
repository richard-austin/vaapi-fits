###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ....lib.ffmpeg.qsv.util import *
from ....lib.ffmpeg.qsv.encoder import MPEG2EncoderTest

spec      = load_test_spec("mpeg2", "encode")
spec_r2r  = load_test_spec("mpeg2", "encode", "r2r")

class cqp(MPEG2EncoderTest):
  def init(self, tspec, case, gop, bframes, qp, quality):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bframes = bframes,
      case    = case,
      gop     = gop,
      qp      = qp,
      quality = quality,
      rcmode  = "cqp",
    )

  @slash.parametrize(*gen_mpeg2_cqp_parameters(spec))
  def test(self, case, gop, bframes, qp, quality):
    self.init(spec, case, gop, bframes, qp, quality)
    self.encode()

  @slash.parametrize(*gen_mpeg2_cqp_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, qp, quality):
    self.init(spec_r2r, case, gop, bframes, qp, quality)
    vars(self).setdefault("r2r", 5)
    self.encode()

class seek(MPEG2EncoderTest):
  def init(self, tspec, case, rcmode, bitrate, maxrate, fps, seek):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      case      = case,
      bitrate   = bitrate,
      maxrate   = maxrate,
      minrate   = bitrate,
      rcmode    = rcmode,
      fps       = fps,
      seek      = seek,
    )

  @slash.parametrize(*gen_mpeg2_seek_parameters(spec))
  def test(self, case, rcmode, bitrate, maxrate, fps, seek):
    self.init(spec, case, rcmode, bitrate, maxrate, fps, seek)
    self.encode()
