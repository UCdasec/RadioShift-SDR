#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: XPSK_Rx
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import math



from gnuradio import qtgui

class XPSK_Rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "XPSK_Rx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("XPSK_Rx")
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

        self.settings = Qt.QSettings("GNU Radio", "XPSK_Rx")

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
        self.mod_order = mod_order = xpsk_const.arity()
        self.sync_bw = sync_bw = 0.01*(mod_order/2)
        self.sps = sps = 8
        self.samp_rate = samp_rate = 1*10**6
        self.rx_gain = rx_gain = 22
        self.rx_chooser = rx_chooser = 0
        self.roll_off = roll_off = .35
        self.costas_loop_bw = costas_loop_bw = 0.03*(mod_order/2)
        self.center_freq = center_freq = 915e6

        ##################################################
        # Blocks
        ##################################################
        self._sync_bw_range = Range(0, 0.07*(mod_order/2), 0.005, 0.01*(mod_order/2), 200)
        self._sync_bw_win = RangeWidget(self._sync_bw_range, self.set_sync_bw, "sync_bw_val", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sync_bw_win)
        self._samp_rate_range = Range(1*10**6, 20*10**6, 1e6, 1*10**6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "'samp_rate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._samp_rate_win)
        self._rx_gain_range = Range(0, 80, 1, 22, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "Rx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        # Create the options list
        self._rx_chooser_options = [0, 1]
        # Create the labels list
        self._rx_chooser_labels = ['Monitor', 'Capture']
        # Create the combo box
        self._rx_chooser_tool_bar = Qt.QToolBar(self)
        self._rx_chooser_tool_bar.addWidget(Qt.QLabel("'rx_chooser'" + ": "))
        self._rx_chooser_combo_box = Qt.QComboBox()
        self._rx_chooser_tool_bar.addWidget(self._rx_chooser_combo_box)
        for _label in self._rx_chooser_labels: self._rx_chooser_combo_box.addItem(_label)
        self._rx_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rx_chooser_options.index(i)))
        self._rx_chooser_callback(self.rx_chooser)
        self._rx_chooser_combo_box.currentIndexChanged.connect(
            lambda i: self.set_rx_chooser(self._rx_chooser_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._rx_chooser_tool_bar)
        self._costas_loop_bw_range = Range(0.001, 0.2*(mod_order/2), 0.005, 0.03*(mod_order/2), 200)
        self._costas_loop_bw_win = RangeWidget(self._costas_loop_bw_range, self.set_costas_loop_bw, "cl_bw", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._costas_loop_bw_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('type=b200', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(center_freq, 1e6), 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                samp_rate/sps,
                roll_off,
                11*sps))
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Demodulated Signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-.5, 1.5)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, .5, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Decoder', 'Bit Slicer', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_const_sink_x_0_2 = qtgui.const_sink_c(
            1024, #size
            "Post Symbol Sync", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_2.set_update_time(.2)
        self.qtgui_const_sink_x_0_2.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_2.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_2.enable_autoscale(False)
        self.qtgui_const_sink_x_0_2.enable_grid(True)
        self.qtgui_const_sink_x_0_2.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_2.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_2.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_2.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_2.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_2.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_2_win = sip.wrapinstance(self.qtgui_const_sink_x_0_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_2_win)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            1024, #size
            "Post Costas", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(.2)
        self.qtgui_const_sink_x_0_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1.enable_grid(True)
        self.qtgui_const_sink_x_0_1.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_1_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            'Post DC Blocker + AGC"', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(.2)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
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
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_GARDNER,
            sps,
            sync_bw,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(mod_order, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(costas_loop_bw, mod_order, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts('00001100110111100010001100101111',
          4, 'packet_len')
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(xpsk_const)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(256, True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, 'Debugger', "")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,0,rx_chooser)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,rx_chooser)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(int(math.log2(mod_order)), 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(5.12e6))
        self.blocks_file_sink_1_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/anagh/Documents/8PSK_Post_Processing.dat', False)
        self.blocks_file_sink_1_0.set_unbuffered(False)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/anagh/Documents/8PSK_Pre_Processing.dat', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-2, 1e-4, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0_0, 1), (self.blocks_head_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0_2, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.dc_blocker_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "XPSK_Rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_xpsk_const(self):
        return self.xpsk_const

    def set_xpsk_const(self, xpsk_const):
        self.xpsk_const = xpsk_const

    def get_mod_order(self):
        return self.mod_order

    def set_mod_order(self, mod_order):
        self.mod_order = mod_order
        self.set_costas_loop_bw(0.03*(self.mod_order/2))
        self.set_sync_bw(0.01*(self.mod_order/2))
        self.blocks_repack_bits_bb_0.set_k_and_l(int(math.log2(self.mod_order)),1)

    def get_sync_bw(self):
        return self.sync_bw

    def set_sync_bw(self, sync_bw):
        self.sync_bw = sync_bw
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.sync_bw)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, self.roll_off, 11*self.sps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, self.roll_off, 11*self.sps))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_rx_chooser(self):
        return self.rx_chooser

    def set_rx_chooser(self, rx_chooser):
        self.rx_chooser = rx_chooser
        self._rx_chooser_callback(self.rx_chooser)
        self.blocks_selector_0.set_output_index(self.rx_chooser)
        self.blocks_selector_0_0.set_output_index(self.rx_chooser)

    def get_roll_off(self):
        return self.roll_off

    def set_roll_off(self, roll_off):
        self.roll_off = roll_off
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.samp_rate/self.sps, self.roll_off, 11*self.sps))

    def get_costas_loop_bw(self):
        return self.costas_loop_bw

    def set_costas_loop_bw(self, costas_loop_bw):
        self.costas_loop_bw = costas_loop_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.costas_loop_bw)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.center_freq, 1e6), 0)




def main(top_block_cls=XPSK_Rx, options=None):

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
