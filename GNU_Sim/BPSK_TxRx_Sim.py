#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BPSK Tx Rx Sim
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sys; sys.path.append('/home/anagh/Repos/RadioShift/GNU Radio/GNU'); import Header_Payload_Formatter



from gnuradio import qtgui

class BPSK_TxRx_Sim(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "BPSK Tx Rx Sim", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BPSK Tx Rx Sim")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "BPSK_TxRx_Sim")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.xpsk_const = xpsk_const = digital.constellation_bpsk().base()
        self.sync_bandwidth = sync_bandwidth = 0.05
        self.sps = sps = 8
        self.samp_rate = samp_rate = 1e6
        self.roll_off = roll_off = 0.35
        self.noise_pwr = noise_pwr = 0.5
        self.mod_order = mod_order = xpsk_const.arity()
        self.freq_off = freq_off = 5e-6
        self.epsilon = epsilon = 5e-3
        self.costas_bandwidth = costas_bandwidth = 0.0

        ##################################################
        # Blocks
        ##################################################
        self._sync_bandwidth_range = Range(0, 0.1, 0.005, 0.05, 200)
        self._sync_bandwidth_win = RangeWidget(self._sync_bandwidth_range, self.set_sync_bandwidth, "sym_sync_bw", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sync_bandwidth_win)
        self._samp_rate_range = Range(1e6, 20e6, 1e6, 1e6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "'samp_rate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._samp_rate_win)
        self._noise_pwr_range = Range(0, 1, 0.01, 0.5, 200)
        self._noise_pwr_win = RangeWidget(self._noise_pwr_range, self.set_noise_pwr, "'noise_pwr'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_pwr_win)
        self._freq_off_range = Range(0, 20e-6, 1e-6, 5e-6, 200)
        self._freq_off_win = RangeWidget(self._freq_off_range, self.set_freq_off, "'freq_off'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_off_win)
        self._epsilon_range = Range(0, 20e-3, 1e-3, 5e-3, 200)
        self._epsilon_win = RangeWidget(self._epsilon_range, self.set_epsilon, "'epsilon'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._epsilon_win)
        self._costas_bandwidth_range = Range(0.000, 0.2, 0.005, 0.0, 200)
        self._costas_bandwidth_win = RangeWidget(self._costas_bandwidth_range, self.set_costas_bandwidth, "costas_bw", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._costas_bandwidth_win)
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                samp_rate/sps,
                0.35,
                int(11*sps)))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                samp_rate/sps,
                0.35,
                int(11*sps)))
        self.qtgui_const_sink_x_0_0_1 = qtgui.const_sink_c(
            1024, #size
            'Post Costas Loop', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_1.enable_grid(True)
        self.qtgui_const_sink_x_0_0_1.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_1_win)
        self.qtgui_const_sink_x_0_0_0 = qtgui.const_sink_c(
            1024, #size
            'Post Symbol Sync', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_0_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            "Rx Signal IQ", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-3, 3)
        self.qtgui_const_sink_x_0_0.set_x_axis(-3, 3)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "TX Signal IQ", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_GARDNER,
            sps,
            sync_bandwidth,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(mod_order, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(costas_bandwidth, mod_order, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts('00001100110111100010001100101111',
          0, 'packet_len')
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=xpsk_const,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=roll_off,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(xpsk_const)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(32, True)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_pwr,
            frequency_offset=freq_off,
            epsilon=1.0 + epsilon,
            taps=[1.0 + 0],
            noise_seed=0,
            block_tags=False)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(int(mod_order**.5), gr.GR_MSB_FIRST)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, 'Debugger', "")
        self.blocks_tag_debug_0.set_display(False)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(int(mod_order**.5), 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_head_1_0 = blocks.head(gr.sizeof_gr_complex*1, 1024*4099)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/anagh/Post_SymbolSync.dat', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/anagh/Post_AGC_IQ.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 255, 0)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-2, 1, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_head_1_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_head_1_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "BPSK_TxRx_Sim")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_xpsk_const(self):
        return self.xpsk_const

    def set_xpsk_const(self, xpsk_const):
        self.xpsk_const = xpsk_const

    def get_sync_bandwidth(self):
        return self.sync_bandwidth

    def set_sync_bandwidth(self, sync_bandwidth):
        self.sync_bandwidth = sync_bandwidth
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.sync_bandwidth)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, 0.35, int(11*self.sps)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, 0.35, int(11*self.sps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, 0.35, int(11*self.sps)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, 0.35, int(11*self.sps)))

    def get_roll_off(self):
        return self.roll_off

    def set_roll_off(self, roll_off):
        self.roll_off = roll_off

    def get_noise_pwr(self):
        return self.noise_pwr

    def set_noise_pwr(self, noise_pwr):
        self.noise_pwr = noise_pwr
        self.channels_channel_model_0.set_noise_voltage(self.noise_pwr)

    def get_mod_order(self):
        return self.mod_order

    def set_mod_order(self, mod_order):
        self.mod_order = mod_order
        self.blocks_repack_bits_bb_0.set_k_and_l(int(self.mod_order**.5),1)

    def get_freq_off(self):
        return self.freq_off

    def set_freq_off(self, freq_off):
        self.freq_off = freq_off
        self.channels_channel_model_0.set_frequency_offset(self.freq_off)

    def get_epsilon(self):
        return self.epsilon

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.channels_channel_model_0.set_timing_offset(1.0 + self.epsilon)

    def get_costas_bandwidth(self):
        return self.costas_bandwidth

    def set_costas_bandwidth(self, costas_bandwidth):
        self.costas_bandwidth = costas_bandwidth
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.costas_bandwidth)




def main(top_block_cls=BPSK_TxRx_Sim, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
