import logging

from .parent import Parent
from .initialization.gui_initialization import GuiInitialization
from .setup_ob.get import Get as Step1Get
from .utilities.table import TableHandler
from .session.new_session import NewSession
from .session import SessionKeys
from . import UI_TITLE


class EventHandler(Parent):

	def new_session(self):
		o_new = NewSession(parent=self.parent)
		o_new.show()

	def full_reset_clicked(self):
		o_init = GuiInitialization(parent=self.parent)
		o_init.full_reset()
		logging.info("Full reset of application!")

	def check_start_acquisition_button(self):
		button_ready_to_be_used = self._is_start_acquisition_ready_to_be_used()
		self.parent.ui.start_acquisition_pushButton.setEnabled(button_ready_to_be_used)
		self.parent.ui.help_pushButton.setVisible(not button_ready_to_be_used)

	def _is_start_acquisition_ready_to_be_used(self):

		# if selected OB tab and no OB selected -> return False
		if self.parent.ui.ob_tabWidget.currentIndex() == 1:
			o_get = Step1Get(parent=self.parent)
			list_of_selected = o_get.list_ob_folders_selected()
			if len(list_of_selected) == 0:
				logging.info(f"User selected `select obs` tab but no OBs have been selected!")
				logging.info(f"-> Possible correction: ")
				logging.info(f"     * select at least 1 OB folder")
				logging.info(f"     * select `Aquire new OBs` tab")
				return False

		return True
