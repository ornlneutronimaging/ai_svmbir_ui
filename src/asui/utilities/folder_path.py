import os

from ..parent import Parent
from ..session import SessionKeys


class FolderPath(Parent):
    """
    This class will retrieve the path to the various folders of the
    project
    """
    ipts_full_path = None

    shared = None
    autoreduce = None
    reduction_log = None
    nexus = None

    def update(self):
        homepath = self.parent.homepath
        ipts = self.parent.session_dict[SessionKeys.ipts_selected]
        instrument = self.parent.session_dict[SessionKeys.instrument]
        self.ipts_full_path = os.path.abspath(os.sep.join([homepath,
                                           instrument,
                                           ipts]))

        self.shared()
        self.autoreduce()
        self.reduction_log()
        self.nexus()

    def shared(self):
        self.shared = os.sep.join([self.ipts_full_path, "shared"])

    def autoreduce(self):
        self.autoreduce = os.sep.join([self.shared,
                                       "autoreduce"])

    def reduction_log(self):
        self.reduction_log = os.sep.join([self.autoreduce,
                                          "reduction_log"])

    def nexus(self):
        self.nexus = os.sep.join([self.ipts_full_path,
                                  "nexus"])
