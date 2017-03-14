from __future__ import with_statement, print_function
import os
import os.path
import json
from ij import IJ, ImagePlus, WindowManager
from ij.plugin.frame import PlugInFrame
from ij.gui import Overlay, GenericDialog, Line, PointRoi
from fiji.util.gui import GenericDialogPlus
import java.lang.Boolean as JBool
from java.awt import GridLayout
from javax.swing import JButton, JPanel, JTable, JScrollPane, BoxLayout
from javax.swing.table import DefaultTableModel
from javax.swing.event import TableModelListener, ListSelectionListener
from OverlayManagerPlus.OverlayManagerPlus import OverlayManagerPlus

class SegmentManager(OverlayManagerPlus):
    def __init__(self):
        # Window
        self.frame = PlugInFrame("Segment Manager")
        self.frame.setSize(300, 600)

        # Parent
        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.X_AXIS))
        self.frame.add(p)

        # Child, left
        tblModel = DefaultTableModel(["Index", "Length"], 0)
        self.tbl = JTable(tblModel)
        self.tbl.getColumn("Index").setMaxWidth(100)
        self.tbl.setRowHeight(20)
        self.tbl.getColumnModel().setColumnMargin(10)
        sp = JScrollPane(self.tbl)
        p.add(sp)

        # Child, right
        p2 = JPanel()
        p2.setLayout(GridLayout(15, 1))
        p.add(p2)

        ## Right component
        b_open = JButton('Open Image', actionPerformed = self.openImage)
        p2.add(b_open)
        b_add = JButton("Add", actionPerformed = self.add_row)
        p2.add(b_add)
        b_del = JButton("Delete", actionPerformed = self.delete_row)
        p2.add(b_del)
        b_ren_i = JButton("Rename index", actionPerformed = self.rename_index)
        p2.add(b_ren_i)
        b_ren_col = JButton("Rename column", actionPerformed = self.rename_column)
        p2.add(b_ren_col)
        b_save = JButton("Save", actionPerformed = self.save_segments)
        p2.add(b_save)

        self.frame.visible = True

    def add_row(self, event):
        pass

    def delete_row(self, event):
        pass

    def rename_index(self, event):
        pass

    def rename_column(self, event):
        pass

    def save_segments(self, event):
        pass

if __name__=='__main__':
    SegmentManager()