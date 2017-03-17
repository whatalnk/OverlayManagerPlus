from __future__ import with_statement, print_function
import os
import os.path
import json
from ij import IJ, ImagePlus, WindowManager
from ij.plugin.frame import PlugInFrame
from ij.gui import Overlay, GenericDialog, Line, PointRoi, TextRoi
from fiji.util.gui import GenericDialogPlus
import java.lang.Boolean as JBool
from java.awt import GridLayout, Font
from javax.swing import JButton, JPanel, JTable, JScrollPane, BoxLayout
from javax.swing.table import DefaultTableModel
from javax.swing.event import TableModelListener, ListSelectionListener
from OverlayManagerPlus.OverlayManagerPlus import OverlayManagerPlus

class SegmentManager(OverlayManagerPlus):
    def __init__(self):
        imp = WindowManager.getCurrentImage()
        if imp is not None:
            self.imp = imp
        self.roi = dict()
        self.text = dict()
        self.overlay = Overlay()
        self.currentIndex = 0
    def run(self):
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
        b_add_col = JButton("Add column", actionPerformed = self.add_col)
        p2.add(b_add_col)
        b_del_col = JButton("Delete column", actionPerformed = self.del_col)
        p2.add(b_del_col)
        b_add = JButton("Add segment", actionPerformed = self.add_row)
        p2.add(b_add)
        b_edit = JButton("Edit segment", actionPerformed = self.edit_row)
        p2.add(b_edit)
        b_del = JButton("Delete segment", actionPerformed = self.delete_row)
        p2.add(b_del)
        b_ren_i = JButton("Rename index", actionPerformed = self.rename_index)
        p2.add(b_ren_i)
        b_ren_col = JButton("Rename column", actionPerformed = self.rename_column)
        p2.add(b_ren_col)
        b_load_pointroi = JButton("Load PointRoi", actionPerformed = self.load_pointroi)
        p2.add(b_load_pointroi)
        b_load_segments = JButton("Load Segments", actionPerformed = self.load_segments)
        p2.add(b_load_segments)
        b_save = JButton("Save", actionPerformed = self.save_segments)
        p2.add(b_save)

        self.frame.visible = True

    def add_col(self, event):
        pass

    def del_col(self, event):
        pass

    def add_row(self, event):
        selection = self.imp.getRoi()
        if selection is None or selection.getType() !=5:
            return
        self.roi[self.currentIndex+1] = selection
        label = TextRoi((selection.x1 + selection.x2)/2, (selection.y1 + selection.y2)/2, str(self.currentIndex+1), Font("Consolas", Font.PLAIN, 200))
        self.text[self.currentIndex+1] = label
        
        tblModel = self.tbl.getModel()
        tblModel.addRow([self.currentIndex+1, selection.getLength()])
        self.currentIndex += 1

        self.overlay.add(selection)
        self.overlay.add(label)
        self.imp.setOverlay(self.overlay)

    def edit_row(self, event):
        pass

    def delete_row(self, event):
        pass

    def rename_index(self, event):
        pass

    def rename_column(self, event):
        pass

    def save_segments(self, event):
        pass

    def load_pointroi(self, event):
        pass

    def point2segment(self):
        pass

    def load_segments(self, event):
        pass

if __name__=='__main__':
    SegmentManager().run()