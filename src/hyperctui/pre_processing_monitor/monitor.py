from qtpy.QtWidgets import QMainWindow
import os
import logging
from qtpy.QtGui import QIcon

from hyperctui import load_ui
from hyperctui import refresh_large_image

from .initialization import Initialization
from .event_handler import EventHandler as MonitorEventHandler
from ..preview_file.preview_file_launcher import PreviewFileLauncher, PreviewMetadataFileLauncher
from ..session import SessionKeys
from ..utilities.widgets import Widgets as UtilityWidgets
from hyperctui.utilities.table import TableHandler
from . import DataStatus
from . import ColorDataStatus


class Monitor(QMainWindow):

    # list of files in the reduction log folder to use as a reference
    # any new files will be used
    initial_list_of_reduction_log_files = []

    # dictionary that looks like
    # {0: { 'file_name': '<full path to ob>',
    #       'log_file': '<full path to log file>',
    #       'err_file': '<full path to err file>',
    #       'metadata_file': <full path to metadata file>',
    #     },
    #  1: { ... },
    #  ...
    # }
    dict_ob_log_err_metadata = None
    dict_projections_log_err_metadata = None

    all_obs_found = False
    all_projections_found = False

    def __init__(self, parent=None):
        super(Monitor, self).__init__(parent)
        self.parent = parent

        ui_full_path = os.path.join(os.path.dirname(__file__),
                                    os.path.join('../ui',
                                                 'pre_processing_monitor.ui'))

        self.ui = load_ui(ui_full_path, baseinstance=self)
        self.setWindowTitle("Monitor")

        refresh_icon = QIcon(refresh_large_image)
        self.ui.refresh_pushButton.setIcon(refresh_icon)

        o_init = Initialization(parent=self,
                                grand_parent=self.parent)
        o_init.data()
        o_init.ui()

        self.refresh_button_clicked()

    def preview_log(self, state=0, row=-1, data_type='ob'):
        log_file = self.dict_ob_log_err_metadata[row]['log_file']
        preview_file = PreviewFileLauncher(parent=self,
                                           file_name=log_file)
        preview_file.show()

    def preview_err(self, state=0, row=-1, data_type='ob'):
        err_file = self.dict_ob_log_err_metadata[row]['err_file']
        preview_file = PreviewFileLauncher(parent=self,
                                           file_name=err_file)
        preview_file.show()

    def preview_summary(self, state=0, row=-1, data_type='ob'):
        file_name = self.dict_ob_log_err_metadata[row]['metadata_file']
        preview_file = PreviewMetadataFileLauncher(parent=self,
                                                   file_name=file_name)
        preview_file.show()

    def refresh_button_clicked(self):
        logging.info("Updating monitor table!")
        o_event = MonitorEventHandler(parent=self,
                                      grand_parent=self.parent)
        o_event.checking_status_of_expected_obs()
        if self.all_obs_found:

            logging.info(f"-> all obs found!")
            # check if obs have already been moved

            if o_event.obs_have_been_moved_to_final_folder():  # all obs created and moved to their final folder

                # we can hide the move OBs widgets
                self.ui.monitor_moving_obs_label.setVisible(False)
                self.ui.final_ob_folder_label.setVisible(False)
                self.ui.final_ob_folder_status.setVisible(False)

                o_event.checking_status_of_expected_projections()
                if self.all_projections_found:

                    logging.info(f"-> all projections found!")
                    if not self.parent.session_dict[SessionKeys.all_tabs_visible]:
                        self.parent.session_dict[SessionKeys.all_tabs_visible] = True
                        o_widgets = UtilityWidgets(parent=self.parent)
                        o_widgets.make_tabs_visible(is_visible=True)
                        self.parent.initialize_crop()
                        self.parent.initialize_center_of_rotation()

            else:  # all OBs have been created but not been moved to their final location yet

                o_event.move_obs_to_final_folder()
                self.parent.session_dict[SessionKeys.obs_have_been_moved_already] = True
                o_event.first_projection_in_progress()
                o_event.checking_status_of_expected_projections()

                # FIXME
                # then we need to hide the Move_obs_to_folder widgets and we won't need to check for it
                # anymore as long as those guys are gone!

                if self.all_projections_found:

                    logging.info(f"-> all projections found!")
                    if not self.parent.session_dict.get(SessionKeys.all_tabs_visible, False):
                        self.parent.session_dict[SessionKeys.all_tabs_visible] = True
                        o_widgets = UtilityWidgets(parent=self.parent)
                        o_widgets.make_tabs_visible(is_visible=True)
                        self.parent.initialize_crop()
                        self.parent.initialize_center_of_rotation()

                    # saving the location of the 0 and 180 degrees folders
                    o_table = TableHandler(table_ui=self.ui.projections_tableWidget)
                    full_path_image_0_degree = o_table.get_item_str_from_cell(row=0, column=0)
                    full_path_image_180_degree = o_table.get_item_str_from_cell(row=1, column=0)
                    self.parent.session_dict[SessionKeys.full_path_to_projections][SessionKeys.image_0_degree] = \
                        full_path_image_0_degree
                    self.parent.session_dict[SessionKeys.full_path_to_projections][SessionKeys.image_180_degree] = \
                        full_path_image_180_degree

            # we moved the files so we can change the status of the move message
            self.ui.final_ob_folder_status.setText(DataStatus.done)
            self.ui.final_ob_folder_status.setStyleSheet(f"background-color: {ColorDataStatus.ready_button}")

        else:
            logging.info(f"-> not all obs found!")

    def closeEvent(self, c):
        self.parent.monitor_ui = None
        self.parent.ui.checking_status_acquisition_pushButton.setEnabled(True)
        self.close()
