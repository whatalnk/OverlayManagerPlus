from __future__ import with_statement
import os
from itertools import izip, repeat, chain
import java.lang.Float as JFloat
from ij import IJ, ImagePlus
from ij.plugin.frame import RoiManager, PlugInFrame
from ij.io import OpenDialog
from ij.measure import ResultsTable
from ij.gui import Overlay, GenericDialog

from fiji.util.gui import GenericDialogPlus
from java.awt.event import ActionListener
from java.awt import GridLayout, Dimension, GridBagLayout, GridBagConstraints
from javax.swing import JButton, JPanel
from javax.swing import JList, DefaultListModel
from javax.swing import JTable, JScrollPane, BoxLayout
from javax.swing.table import DefaultTableModel
import java.lang.Boolean as JBool

class checkBoxTableModel(DefaultTableModel):
    def getColumnClass(self, col):
        if col == 0:
            return(str)
        elif col == 1:
            return(JBool)

class OverlayManager():
    def __init__(self):
        frame = PlugInFrame("Overlay Manager")
        frame.setSize(300, 600)

        # Parent
        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.X_AXIS))
        frame.add(p)

        # Left
        tblModel = checkBoxTableModel(["ROI name", "Overlay"], 0)
        self.tbl = JTable(tblModel)
        self.tbl.getColumn("Overlay").setMaxWidth(100)
        self.tbl.setRowHeight(20)
        self.tbl.getColumnModel().setColumnMargin(10)
        sp = JScrollPane(self.tbl)
        p.add(sp)

        # Right
        p2 = JPanel()
        p2.setLayout(GridLayout(15, 1))
        p.add(p2)

        # Right component
        b_add_roi = JButton('Add ROI', actionPerformed = self.add_roi)
        p2.add(b_add_roi)
        b_del_roi = JButton('Delete ROI', actionPerformed = self.del_roi)
        p2.add(b_del_roi)
        b_draw = JButton('Draw', actionPerformed = self.draw_overlay)
        p2.add(b_draw)
        b_save = JButton('Save', actionPerformed = self.save_roi)
        p2.add(b_save)
        b_load = JButton('Load', actionPerformed = self.load_roi)
        p2.add(b_load)

        frame.visible = True

    def add_roi(self, event):
        tblModel = self.tbl.getModel()
        tblModel.addRow(["name", False])

    def del_roi(self, event):
        tbl = self.tbl
        i = tbl.getSelectedRow()
        if i == -1:
            gd = GenericDialog("Confirm")
            gd.addMessage("Plese select an item")
            gd.hideCancelButton()
            gd.showDialog()
        else:
            v = tbl.getValueAt(i, 0)
            gd = GenericDialog("Confirm")
            gd.addMessage("Delete %s ?" % v)
            gd.enableYesNoCancel()
            gd.showDialog()
            if gd.wasOKed():
                tbl.getModel().removeRow(i)

    def draw_overlay(self, event):
        pass

    def save_roi(self, event):
        pass

    def load_roi(self, event):
        pass

if __name__ == '__main__':
    OverlayManager()
#imp = IJ.getImage()
#roi = imp.getRoi()
#roi.setName("PC0202l")
#ol = Overlay()
#
#gd = GenericDialogPlus("List of ROIs in the Overlay")
#def add_to_overlay(e):
#    ol.add(roi)
#
#gd.addButton("Add to Overlay", add_to_overlay)
#gd.showDialog()
#
#print(ol)
#  