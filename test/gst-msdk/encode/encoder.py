###
### Copyright (C) 2018-2019 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from ....lib import *
from ..util import *

@slash.requires(have_gst)
@slash.requires(have_gst_msdk)
@slash.requires(*have_gst_element("checksumsink2"))
@slash.requires(using_compatible_driver)
class EncoderTest(slash.Test):
  def gen_input_opts(self):
    opts = "filesrc location={source} num-buffers={frames}"
    opts += " ! rawvideoparse format={mformat} width={width} height={height}"

    if vars(self).get("fps", None) is not None:
      opts += " framerate={fps}"

    if self.codec not in ["hevc-8", "hevc-10"]:
      opts += " ! videoconvert ! video/x-raw,format={hwformat}"

    return opts

  def gen_output_opts(self):
    opts = "{gstencoder}"

    if self.codec not in ["jpeg",]:
      opts += " rate-control={rcmode}"
      opts += " hardware=true"

    if vars(self).get("gop", None) is not None:
      opts += " gop-size={gop}"
    if vars(self).get("qp", None) is not None:
      if self.codec in ["mpeg2"]:
        opts += " qpi={mqp} qpp={mqp} qpb={mqp}"
      else:
        opts += " qpp={qp}"
    if vars(self).get("quality", None) is not None:
      if self.codec in ["jpeg",]:
        opts += " quality={quality}"
      else:
        opts += " target-usage={quality}"
    if vars(self).get("slices", None) is not None:
      opts += " num-slices={slices}"
    if vars(self).get("bframes", None) is not None:
       opts += " b-frames={bframes}"
    if vars(self).get("rcmode") == "vbr":
       opts += " max-vbv-bitrate={maxrate}"
    if vars(self).get("minrate", None) is not None:
       opts += " bitrate={minrate}"
    if vars(self).get("refmode", None) is not None:
       opts += " ref-pic-mode={refmode}"
    if vars(self).get("refs", None) is not None:
      opts += " ref-frames={refs}"
    if vars(self).get("lowpower", False):
      opts += " low-power=true"
    if vars(self).get("ladepth", None) is not None:
      opts += " rc-lookahead={ladepth}"
#    if vars(self).get("loopshp", None) is not None:
#      opts += " sharpness-level={loopshp}"
#    if vars(self).get("looplvl", None) is not None:
#      opts += " loop-filter-level={looplvl}"

    if self.codec not in ["jpeg", "vp8", ]:
      opts += " ! {gstmediatype},profile={mprofile}"

    if vars(self).get("gstparser", None) is not None:
      opts += " ! {gstparser}"

    if vars(self).get("gstmuxer", None) is not None:
      opts += " ! {gstmuxer}"

    opts += " ! filesink location={encoded}"

    return opts

  def gen_name(self):
    name = "{case}-{rcmode}-{profile}"
    if vars(self).get("fps", None) is not None:
      name += "-{fps}"
    if vars(self).get("gop", None) is not None:
      name += "-{gop}"
    if vars(self).get("qp", None) is not None:
      name += "-{qp}"
    if vars(self).get("slices", None) is not None:
      name += "-{slices}"
    if vars(self).get("quality", None) is not None:
      name += "-{quality}"
    if vars(self).get("bframes", None) is not None:
      name += "-{bframes}"
    if vars(self).get("minrate", None) is not None:
      name += "-{minrate}k"
    if vars(self).get("maxrate", None) is not None:
      name += "-{maxrate}k"
    if vars(self).get("refmode", None) is not None:
      name += "-{refmode}"
    if vars(self).get("refs", None) is not None:
      name += "-{refs}"
    if vars(self).get("lowpower", False):
      name += "-low-power"
    if vars(self).get("loopshp", None) is not None:
      name += "-{loopshp}"
    if vars(self).get("looplvl", None) is not None:
      name += "-{looplvl}"
    if vars(self).get("ladepth", None) is not None:
      name += "-{ladepth}"
    return name

  def call_encode(self, iopts, oopts):
    self.output = call(
      "gst-launch-1.0 -vf"
      " {iopts} ! {oopts}".format(iopts = iopts, oopts = oopts)
    )

  def before(self):
    self.refctx = []

  def encode(self):
    self.mprofile = mapprofile(self.codec, self.profile)
    if self.mprofile is None:
      slash.skip_test("{profile} profile is not supported".format(**vars(self)))

    self.mformat = mapformat(self.format)
    self.mformatu = mapformatu(self.format)
    self.hwformat = mapformat_hwup(self.format)
    if self.mformat is None:
      slash.skip_test("{format} format not supported".format(**vars(self)))

    iopts = self.gen_input_opts()
    oopts = self.gen_output_opts()
    name  = self.gen_name()

    if vars(self).get("r2r", None) is not None:
      assert type(self.r2r) is int and self.r2r > 1, "invalid r2r value"
      for i in xrange(self.r2r):
        self.encoded = get_media()._test_artifact(
          "{}_{}.{}".format(name.format(**vars(self)), i, self.get_file_ext()))

        self.call_encode(iopts.format(**vars(self)), oopts.format(**vars(self)))

        result = md5(self.encoded)
        get_media()._set_test_details(**{"md5_{}".format(i): result})

        if i == 0:
          md5ref = result
          continue

        assert md5ref == result, "r2r md5 mismatch"
        # delete encoded file after each iteration
        get_media()._purge_test_artifact(self.encoded)

    else:
      self.encoded = get_media()._test_artifact(
          "{}.{}".format(name.format(**vars(self)), self.get_file_ext()))

      self.call_encode(iopts.format(**vars(self)), oopts.format(**vars(self)))
      self.check_bitrate()
      self.check_metrics()

  def check_metrics(self):
    name = self.gen_name().format(**vars(self))
    self.decoded = get_media()._test_artifact(
      "{}-{width}x{height}-{format}.yuv".format(name, **vars(self)))

    call(
      "gst-launch-1.0 -vf filesrc location={encoded}"
      " ! {gstdecoder}"
      " ! videoconvert ! video/x-raw,format={mformatu}"
      " ! checksumsink2 file-checksum=false frame-checksum=false"
      " plane-checksum=false dump-output=true qos=false"
      " dump-location={decoded}".format(**vars(self))
    )
    get_media().baseline.check_psnr(
      psnr = calculate_psnr(
        self.source, self.decoded,
        self.width, self.height,
        self.frames, self.format),
      context = self.refctx,
    )

  def check_bitrate(self):
    if "cbr" == self.rcmode:
      encsize = os.path.getsize(self.encoded)
      bitrate_actual = encsize * 8 * self.fps / 1024.0 / self.frames
      bitrate_gap = abs(bitrate_actual - self.bitrate) / self.bitrate

      get_media()._set_test_details(
        size_encoded = encsize,
        bitrate_actual = "{:-.2f}".format(bitrate_actual),
        bitrate_gap = "{:.2%}".format(bitrate_gap))

      # acceptable bitrate within 10% of bitrate
      assert(bitrate_gap <= 0.10)

    elif "vbr" == self.rcmode:
      encsize = os.path.getsize(self.encoded)
      bitrate_actual = encsize * 8 * self.fps / 1024.0 / self.frames

      get_media()._set_test_details(
        size_encoded = encsize,
        bitrate_actual = "{:-.2f}".format(bitrate_actual))

      # acceptable bitrate within 25% of minrate and 10% of maxrate
      assert(self.minrate * 0.75 <= bitrate_actual <= self.maxrate * 1.10)
