###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ....lib.ffmpeg.vaapi.util import *
from ....lib.ffmpeg.vaapi.encoder import HEVC8EncoderTest, HEVC8EncoderLPTest

spec      = load_test_spec("hevc", "encode", "8bit")
spec_r2r  = load_test_spec("hevc", "encode", "8bit", "r2r")

class cqp(HEVC8EncoderTest):
  def init(self, tspec, case, gop, slices, bframes, qp, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bframes = bframes,
      case    = case,
      gop     = gop,
      profile = profile,
      qp      = qp,
      quality = quality,
      rcmode  = "cqp",
      slices  = slices,
    )

  @slash.parametrize(*gen_hevc_cqp_parameters(spec, ['main']))
  def test(self, case, gop, slices, bframes, qp, quality, profile):
    self.init(spec, case, gop, slices, bframes, qp, quality, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_cqp_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, bframes, qp, quality, profile):
    self.init(spec_r2r, case, gop, slices, bframes, qp, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class cqp_lp(HEVC8EncoderLPTest):
  def init(self, tspec, case, gop, slices, qp, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      case     = case,
      gop      = gop,
      profile  = profile,
      qp       = qp,
      quality  = quality,
      rcmode   = "cqp",
      slices   = slices,
    )

  @slash.parametrize(*gen_hevc_cqp_lp_parameters(spec, ['main']))
  def test(self, case, gop, slices, qp, quality, profile):
    self.init(spec, case, gop, slices, qp, quality, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_cqp_lp_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, qp, quality, profile):
    self.init(spec_r2r, case, gop, slices, qp, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class cbr(HEVC8EncoderTest):
  def init(self, tspec, case, gop, slices, bframes, bitrate, fps, profile, level=None):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bframes = bframes,
      bitrate = bitrate,
      case    = case,
      fps     = fps,
      gop     = gop,
      maxrate = bitrate,
      minrate = bitrate,
      profile = profile,
      rcmode  = "cbr",
      slices  = slices,
      level   = level,
    )

  @slash.parametrize(*gen_hevc_cbr_parameters(spec, ['main']))
  def test(self, case, gop, slices, bframes, bitrate, fps, profile):
    self.init(spec, case, gop, slices, bframes, bitrate, fps, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_cbr_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, bframes, bitrate, fps, profile):
    self.init(spec_r2r, case, gop, slices, bframes, bitrate, fps, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

  @slash.parametrize(*gen_hevc_cbr_level_parameters(spec, ['main']))
  def test_level(self, case, gop, slices, bframes, bitrate, fps, profile, level):
    self.init(spec, case, gop, slices, bframes, bitrate, fps, profile, level)
    self.encode()

class cbr_lp(HEVC8EncoderLPTest):
  def init(self, tspec, case, gop, slices, bitrate, fps, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate = bitrate,
      case    = case,
      fps     = fps,
      gop     = gop,
      maxrate = bitrate,
      minrate = bitrate,
      profile = profile,
      rcmode  = "cbr",
      slices  = slices,
    )

  @slash.parametrize(*gen_hevc_cbr_lp_parameters(spec, ['main']))
  def test(self, case, gop, slices, bitrate, fps, profile):
    self.init(spec, case, gop, slices, bitrate, fps, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_cbr_lp_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, bitrate, fps, profile):
    self.init(spec_r2r, case, gop, slices, bitrate, fps, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class vbr(HEVC8EncoderTest):
  def init(self, tspec, case, gop, slices, bframes, bitrate, fps, quality, refs, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bframes = bframes,
      bitrate = bitrate,
      case    = case,
      fps     = fps,
      gop     = gop,
      maxrate = bitrate * 2, # target percentage 50%
      minrate = bitrate,
      profile = profile,
      quality = quality,
      rcmode  = "vbr",
      refs    = refs,
      slices  = slices,
    )

  @slash.parametrize(*gen_hevc_vbr_parameters(spec, ['main']))
  def test(self, case, gop, slices, bframes, bitrate, fps, quality, refs, profile):
    self.init(spec, case, gop, slices, bframes, bitrate, fps, quality, refs, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_vbr_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, bframes, bitrate, fps, quality, refs, profile):
    self.init(spec_r2r, case, gop, slices, bframes, bitrate, fps, quality, refs, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class vbr_lp(HEVC8EncoderLPTest):
  def init(self, tspec, case, gop, slices, bitrate, fps, quality, refs, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate = bitrate,
      case    = case,
      fps     = fps,
      gop     = gop,
      maxrate = bitrate * 2, # target percentage 50%
      minrate = bitrate,
      profile = profile,
      quality = quality,
      rcmode  = "vbr",
      refs    = refs,
      slices  = slices,
    )

  @slash.parametrize(*gen_hevc_vbr_lp_parameters(spec, ['main']))
  def test(self, case, gop, slices, bitrate, fps, quality, refs, profile):
    self.init(spec, case, gop, slices, bitrate, fps, quality, refs, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_vbr_lp_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, bitrate, fps, quality, refs, profile):
    self.init(spec_r2r, case, gop, slices, bitrate, fps, quality, refs, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class qvbr_lp(HEVC8EncoderLPTest):
  def init(self, tspec, case, gop, slices, bitrate, qp, fps, quality, refs, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate = bitrate,
      case    = case,
      fps     = fps,
      gop     = gop,
      maxrate = bitrate * 2, # target percentage 50%
      minrate = bitrate,
      qp      = qp,
      profile = profile,
      quality = quality,
      rcmode  = "qvbr",
      refs    = refs,
      slices  = slices,
    )

  @slash.parametrize(*gen_hevc_qvbr_lp_parameters(spec, ['main']))
  def test(self, case, gop, slices, bitrate, qp, fps, quality, refs, profile):
    self.init(spec, case, gop, slices, bitrate, qp, fps, quality, refs, profile)
    self.encode()

  @slash.parametrize(*gen_hevc_qvbr_lp_parameters(spec_r2r, ['main']))
  def test_r2r(self, case, gop, slices, bitrate, qp, fps, quality, refs, profile):
    self.init(spec_r2r, case, gop, slices, bitrate, qp, fps, quality, refs, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class roi(HEVC8EncoderTest):
  def init(self, tspec, case, gop, bframes, bitrate, maxrate, profile, rcmode):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      rcmode     = rcmode,
      bframes    = bframes,
      bitrate    = bitrate,
      case       = case,
      maxrate    = maxrate,
      minrate    = bitrate,
      profile    = profile,
      gop        = gop,
      roi        = 1,
    )

  @slash.parametrize(*gen_hevc_roi_parameters(spec, ['main']))
  def test(self, case, gop, bframes, bitrate, maxrate, profile, rcmode):
    self.init(spec, case, gop, bframes, bitrate, maxrate, profile, rcmode)
    self.encode()

class roi_lp(HEVC8EncoderLPTest):
  def init(self, tspec, case, gop, bframes, bitrate, maxrate, profile, rcmode):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      rcmode     = rcmode,
      bframes    = bframes,
      bitrate    = bitrate,
      case       = case,
      maxrate    = maxrate,
      minrate    = bitrate,
      profile    = profile,
      gop        = gop,
      roi        = 1,
    )

  @slash.parametrize(*gen_hevc_roi_lp_parameters(spec, ['main']))
  def test(self, case, gop, bframes, bitrate, maxrate, profile, rcmode):
    self.init(spec, case, gop, bframes, bitrate, maxrate, profile, rcmode)
    self.encode()
