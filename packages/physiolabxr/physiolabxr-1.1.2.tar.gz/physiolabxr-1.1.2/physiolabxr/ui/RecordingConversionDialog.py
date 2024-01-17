import pickle

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import pyqtgraph as pg
from scipy.io import savemat
import numpy as np
import os
import csv

from physiolabxr.configs.configs import RecordingFileFormat, AppConfigs
from physiolabxr.presets.Presets import Presets
from physiolabxr.utils.data_utils import CsvStoreLoad
from physiolabxr.utils.RNStream import RNStream
from physiolabxr.utils.xdf_utils import create_xml_string, save_xdf


class RecordingPostProcessDialog(QtWidgets.QWidget):
    def __init__(self, file_path, file_format: RecordingFileFormat, open_directory_func):
        super().__init__()
        self.ui = uic.loadUi(AppConfigs()._ui_RecordingConversionDialog, self)
        self.copy_button.setIcon(AppConfigs()._icon_copy)
        self.copied_label.hide()
        self.setWindowTitle(f'Please wait for converting to {file_format.value}')

        self.finish_button.clicked.connect(self.on_finish_button_clicked)
        self.finish_postprocess_widget.hide()
        self.open_directory_button.clicked.connect(self.on_open_directory_button_clicked)
        self.copy_button.clicked.connect(self.on_copy_button_clicked)

        self.file_format = file_format
        self.file_path = file_path
        self.open_directory_func = open_directory_func

        self.thread = None


        # check if needs conversion
        if not file_format == RecordingFileFormat.dats:
            self.recording_convertion_worker = RecordingConversionWorker(RNStream(file_path), file_format, file_path)
            self.thread = QThread()
            self.thread.started.connect(self.recording_convertion_worker.run)
            self.recording_convertion_worker.moveToThread(self.thread)

            self.recording_convertion_worker.progress.connect(self.conversion_progress)
            self.recording_convertion_worker.finished_streamin.connect(self.streamin_finished)
            self.recording_convertion_worker.finished_conversion.connect(self.save_finished)
            self.finish_button.hide()
            self.thread.start()
            self.is_conversion_complete = False
        else:
            self.save_finished(file_path)

    def save_finished(self, newfile_path):
        print('Conversion finished, showing the finish button')
        self.setWindowTitle('Recording saved')
        self.progress_label.setText(f'To')
        self.save_path_line_edit.setText(newfile_path)

        self.finish_postprocess_widget.show()
        self.finish_button.show()
        self.is_conversion_complete = True
        self.activateWindow()

    def conversion_progress(self, progresses):
        read_bytes, total_bytes = progresses
        self.progress_label.setText('Loading file back in: {} % loaded'.format(str(round(100 * read_bytes/total_bytes, 2))))
        self.progress_label.repaint()
        # print('updated progress label')

    def streamin_finished(self):
        self.progress_label.setText('Converting to {}'.format(self.file_format))

    def on_finish_button_clicked(self):
        self.close()
        if self.thread is not None:
            self.thread.quit()

    def on_copy_button_clicked(self):
        QtWidgets.QApplication.clipboard().setText(self.save_path_line_edit.text())
        self.copied_label.show()

    def on_open_directory_button_clicked(self):
        self.open_directory_func()


class RecordingConversionWorker(QObject):
    finished_streamin = pyqtSignal()
    finished_conversion = pyqtSignal(str)
    progress = pyqtSignal(list)

    def __init__(self, stream, file_format: RecordingFileFormat, file_path):
        super().__init__()
        self.stream = stream
        self.file_format = file_format
        self.file_path = file_path

    def run(self):
        print("RecordingConversionWorker started running")
        file, buffer, read_bytes_count = None, None, None
        while True:
            file, buffer, read_bytes_count, total_bytes, finished = self.stream.stream_in_stepwise(file, buffer, read_bytes_count, jitter_removal=False)
            if finished:
                break
            self.progress.emit([read_bytes_count, total_bytes])
        self.finished_streamin.emit()

        newfile_path = self.file_path
        if self.file_format == RecordingFileFormat.matlab:
            newfile_path = self.file_path.replace(RecordingFileFormat.get_default_file_extension(),
                                                  self.file_format.get_file_extension())
            # buffer_copy = {}
            # for stream_label, data_ts_array in buffer.items():
            #     buffer_copy[stream_label + ' timestamp'] = data_ts_array[1]
            #     buffer_copy[stream_label] = data_ts_array[0]
            buffer = [{f'{s_name} timestamp': timestamps, s_name: data} for s_name, (data, timestamps) in buffer.items()]
            buffer = {k: v for d in buffer for k, v in d.items()}
            savemat(newfile_path, buffer, oned_as='row')
        elif self.file_format == RecordingFileFormat.pickle:
            newfile_path = self.file_path.replace(RecordingFileFormat.get_default_file_extension(), self.file_format.get_file_extension())
            pickle.dump(buffer, open(newfile_path, 'wb'))
        elif self.file_format == RecordingFileFormat.csv:
            csv_store = CsvStoreLoad()
            csv_store.save_csv(buffer, self.file_path)
        elif self.file_format == RecordingFileFormat.xdf:
            newfile_path = self.file_path.replace(RecordingFileFormat.get_default_file_extension(), self.file_format.get_file_extension())
            save_xdf(newfile_path, buffer)
        else:
            raise NotImplementedError
        self.finished_conversion.emit(newfile_path)
