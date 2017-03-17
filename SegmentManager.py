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
from javax.swing import JFrame, JButton, JPanel, JTable, JScrollPane, BoxLayout, JMenu, JMenuBar, JMenuItem
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
        self.frame = JFrame("Segment Manager")
        self.frame.setSize(200, 600)

        # Parent
        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.X_AXIS))
        self.frame.add(p)

        # Child, left
        tblModel = DefaultTableModel(["Index", "Col1"], 0)
        self.tbl = JTable(tblModel)
        self.tbl.getColumn("Index").setMaxWidth(50)
        self.tbl.setRowHeight(20)
        self.tbl.getColumnModel().setColumnMargin(10)
        sp = JScrollPane(self.tbl)
        p.add(sp)

        # Menu
        menubar = JMenuBar()

        menu_file = JMenu("File")
        menubar.add(menu_file)
        
        menuitem_open = JMenuItem("Open Image")
        menuitem_load_pointroi = JMenuItem("Load PointRoi")
        menuitem_load_segments = JMenuItem("Load Segments")
        menu_file.add(menuitem_open)
        menu_file.add(menuitem_load_pointroi)
        menu_file.add(menuitem_load_segments)


        menu_row = JMenu("Row")
        menubar.add(menu_row)
        
        menuitem_rename_row = JMenuItem("Rename")
        menuitem_del_row = JMenuItem("Delete")
        menu_row.add(menuitem_rename_row)
        menu_row.add(menuitem_del_row)

        menu_col = JMenu("Column")
        menubar.add(menu_col)
        
        menuitem_add_col = JMenuItem("Add")
        menuitem_rename_col = JMenuItem("Rename")
        menuitem_del_col = JMenuItem("Delete")
        menu_col.add(menuitem_add_col)
        menu_col.add(menuitem_rename_col)
        menu_col.add(menuitem_del_col)

        menu_data = JMenu("Data")
        menubar.add(menu_data)

        menuitem_add_data = JMenuItem("Add")
        menuitem_edit_data = JMenuItem("Edit")
        menuitem_del_data = JMenuItem("Delete")
        menu_data.add(menuitem_add_data)
        menu_data.add(menuitem_edit_data)
        menu_data.add(menuitem_del_data)

        self.frame.setJMenuBar(menubar)

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