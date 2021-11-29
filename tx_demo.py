#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rx Demo
# GNU Radio version: 3.7.13.5
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import isdbt
import pmt
import sip
import sys
import time
from gnuradio import qtgui


class rx_demo(gr.top_block, Qt.QWidget):

    def __init__(self, tx_freq, default_tx_gain):
        gr.top_block.__init__(self, "Tx Demo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx Demo")
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

        self.settings = Qt.QSettings("GNU Radio", "Tx_demo")
        self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))


        ##################################################
        # Variables
        ##################################################
        self.mode = mode = 3
        self.tx_gain = tx_gain = default_tx_gain 
        self.total_carriers = total_carriers = 2**(10+mode)
        self.segments_c = segments_c = 0
        self.segments_b = segments_b = 12
        self.segments_a = segments_a = 1
        self.samp_rate_usrp = samp_rate_usrp = 8e6
        self.samp_rate = samp_rate = 8e6*64/63
        self.length_c = length_c = 0
        self.length_b = length_b = 2
        self.length_a = length_a = 4
        self.guard = guard = 1.0/16
        self.data_carriers = data_carriers = 13*96*2**(mode-1)
        self.const_size = const_size = 64
        self.center_freq = center_freq = tx_freq
        self.bb_gain = bb_gain = 0.0022097087
        self.active_carriers = active_carriers = 13*108*2**(mode-1)+1

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 89, 1, self.tx_gain, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, "tx_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win)
        self._bb_gain_tool_bar = Qt.QToolBar(self)
        self._bb_gain_tool_bar.addWidget(Qt.QLabel('BB gain'+": "))
        self._bb_gain_line_edit = Qt.QLineEdit(str(self.bb_gain))
        self._bb_gain_tool_bar.addWidget(self._bb_gain_line_edit)
        self._bb_gain_line_edit.returnPressed.connect(
        	lambda: self.set_bb_gain(eng_notation.str_to_num(str(self._bb_gain_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._bb_gain_tool_bar)
        self.uhd_usrp_sink_1_0 = uhd.usrp_sink(
        	",".join(("", 'type=b200')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_1_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_1_0.set_gain(tx_gain, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.isdbt_tmcc_encoder_0 = isdbt.tmcc_encoder(3, True, 4, 64, 4, 1, 2, 0, length_a, length_b, 0, segments_a, segments_b, 0)
        self.isdbt_time_interleaver_0 = isdbt.time_interleaver(3, segments_a, length_a, segments_b, length_b, segments_c, length_c)
        self.isdbt_pilot_signals_0 = isdbt.pilot_signals(3)
        self.isdbt_hierarchical_combinator_0 = isdbt.hierarchical_combinator(3, segments_a, segments_b, 0)
        self.isdbt_frequency_interleaver_0 = isdbt.frequency_interleaver(True, 3)
        self.isdbt_energy_dispersal_0_0 = isdbt.energy_dispersal(3, 64, 2, segments_b)
        self.isdbt_energy_dispersal_0 = isdbt.energy_dispersal(3, 4, 1, segments_a)
        self.isdbt_carrier_modulation_0_0 = isdbt.carrier_modulation(3, segments_b, 64)
        self.isdbt_carrier_modulation_0 = isdbt.carrier_modulation(3, segments_a, 4)
        self.isdbt_byte_interleaver_0_0 = isdbt.byte_interleaver(3, 64, 2, segments_b)
        self.isdbt_byte_interleaver_0 = isdbt.byte_interleaver(3, 4, 1, segments_a)
        self.fft_vxx_1 = fft.fft_vcc(total_carriers, False, (window.rectangular(total_carriers)), True, 1)
        self.dtv_dvbt_reed_solomon_enc_0_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 1)
        self.dtv_dvbt_reed_solomon_enc_0 = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, 1)
        self.dtv_dvbt_inner_coder_0_0_0 = dtv.dvbt_inner_coder(1, 1512*4, dtv.MOD_64QAM, dtv.ALPHA4, dtv.C3_4)
        self.dtv_dvbt_inner_coder_0_0 = dtv.dvbt_inner_coder(1, 1512*4, dtv.MOD_QPSK, dtv.ALPHA4, dtv.C2_3)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(total_carriers, total_carriers+int(total_carriers*guard), 0, '')
        self.blocks_vector_to_stream_0_1_0 = blocks.vector_to_stream(gr.sizeof_char*1, 1512*4)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_char*1, 1512*4)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_char*1, 188)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, 188)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*data_carriers, 2)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(bb_gain)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, '/home/gnuradio/c.ts', False)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/gnuradio/a.ts', True)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.uhd_usrp_sink_1_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.isdbt_pilot_signals_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.dtv_dvbt_reed_solomon_enc_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.dtv_dvbt_reed_solomon_enc_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.isdbt_carrier_modulation_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_0, 0), (self.isdbt_carrier_modulation_0_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.dtv_dvbt_inner_coder_0_0, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.dtv_dvbt_inner_coder_0_0_0, 0), (self.blocks_vector_to_stream_0_1_0, 0))
        self.connect((self.dtv_dvbt_reed_solomon_enc_0, 0), (self.isdbt_energy_dispersal_0, 0))
        self.connect((self.dtv_dvbt_reed_solomon_enc_0_0, 0), (self.isdbt_energy_dispersal_0_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.isdbt_byte_interleaver_0, 0), (self.dtv_dvbt_inner_coder_0_0, 0))
        self.connect((self.isdbt_byte_interleaver_0_0, 0), (self.dtv_dvbt_inner_coder_0_0_0, 0))
        self.connect((self.isdbt_carrier_modulation_0, 0), (self.isdbt_hierarchical_combinator_0, 0))
        self.connect((self.isdbt_carrier_modulation_0_0, 0), (self.isdbt_hierarchical_combinator_0, 1))
        self.connect((self.isdbt_energy_dispersal_0, 0), (self.isdbt_byte_interleaver_0, 0))
        self.connect((self.isdbt_energy_dispersal_0_0, 0), (self.isdbt_byte_interleaver_0_0, 0))
        self.connect((self.isdbt_frequency_interleaver_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.isdbt_hierarchical_combinator_0, 0), (self.isdbt_time_interleaver_0, 0))
        self.connect((self.isdbt_pilot_signals_0, 0), (self.isdbt_tmcc_encoder_0, 0))
        self.connect((self.isdbt_time_interleaver_0, 0), (self.isdbt_frequency_interleaver_0, 0))
        self.connect((self.isdbt_tmcc_encoder_0, 0), (self.fft_vxx_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Tx_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self.set_total_carriers(2**(10+self.mode))
        self.set_data_carriers(13*96*2**(self.mode-1))
        self.set_active_carriers(13*108*2**(self.mode-1)+1)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_1_0.set_gain(self.tx_gain, 0)


    def get_total_carriers(self):
        return self.total_carriers

    def set_total_carriers(self, total_carriers):
        self.total_carriers = total_carriers

    def get_segments_c(self):
        return self.segments_c

    def set_segments_c(self, segments_c):
        self.segments_c = segments_c

    def get_segments_b(self):
        return self.segments_b

    def set_segments_b(self, segments_b):
        self.segments_b = segments_b

    def get_segments_a(self):
        return self.segments_a

    def set_segments_a(self, segments_a):
        self.segments_a = segments_a

    def get_samp_rate_usrp(self):
        return self.samp_rate_usrp

    def set_samp_rate_usrp(self, samp_rate_usrp):
        self.samp_rate_usrp = samp_rate_usrp

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_length_c(self):
        return self.length_c

    def set_length_c(self, length_c):
        self.length_c = length_c

    def get_length_b(self):
        return self.length_b

    def set_length_b(self, length_b):
        self.length_b = length_b

    def get_length_a(self):
        return self.length_a

    def set_length_a(self, length_a):
        self.length_a = length_a

    def get_guard(self):
        return self.guard

    def set_guard(self, guard):
        self.guard = guard

    def get_data_carriers(self):
        return self.data_carriers

    def set_data_carriers(self, data_carriers):
        self.data_carriers = data_carriers

    def get_const_size(self):
        return self.const_size

    def set_const_size(self, const_size):
        self.const_size = const_size

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_1_0.set_center_freq(self.center_freq, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        Qt.QMetaObject.invokeMethod(self._bb_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.bb_gain)))
        self.blocks_multiply_const_xx_0.set_k(self.bb_gain)

    def get_active_carriers(self):
        return self.active_carriers

    def set_active_carriers(self, active_carriers):
        self.active_carriers = active_carriers


def main(top_block_cls=rx_demo, options=None, **kwargs):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."
    
    qapp = Qt.QApplication(sys.argv)
    tb = top_block_cls(kwargs['tx_freq'], kwargs['default_tx_gain'])
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    time.sleep(10)
    freq = sys.argv[1]
    try:
        d_tx_gain = sys.argv[2]
    except:
        d_tx_gain = 20

    if not freq:
        raise ValueError("Tx Freq Reuired")
    try:
        freq = int(freq)
        print freq
    except:
        raise ValueError("must be positive integer")
    if freq < 473143000:
        raise ValueError("Wrong freq: try 473143000")

    main(tx_freq=freq, default_tx_gain = float(d_tx_gain))
