from __future__ import with_statement
import os
from itertools import izip, repeat, chain
import java.lang.Float as JFloat
from ij import IJ, ImagePlus, WindowManager
from ij.plugin.frame import RoiManager, PlugInFrame
from ij.io import OpenDialog
from ij.measure import ResultsTable
from ij.gui import Overlay, GenericDialog, Line, PointRoi

from fiji.util.gui import GenericDialogPlus
from java.awt.event import ActionListener
from java.awt import GridLayout, Dimension, GridBagLayout, GridBagConstraints
from javax.swing import JButton, JPanel
from javax.swing import JList, DefaultListModel
from javax.swing import JTable, JScrollPane, BoxLayout
from javax.swing.table import DefaultTableModel
from javax.swing.event import TableModelListener
import java.lang.Boolean as JBool
import json
import os.path

class checkBoxTableModel(DefaultTableModel):
    def getColumnClass(self, col):
        if col == 0:
            return(str)
        elif col == 1:
            return(JBool)

class checkBoxTableListener(TableModelListener):
    def __init__(self, overlayManager):
        self.overlayManager = overlayManager
    def tableChanged(self, event):
        print(self.overlayManager.handle_tableChanged(event))

class OverlayManager():
    def __init__(self):
        self.roi = dict()
        self.overlay = Overlay()
        self.roicount = 0
        imp = WindowManager.getCurrentImage()
        if imp is not None:
            self.imp = imp
            self.imagePath = os.path.join(imp.getOriginalFileInfo().directory, imp.getOriginalFileInfo().fileName)

    def run(self):
        frame = PlugInFrame("Overlay Manager")
        frame.setSize(300, 600)

        # Parent
        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.X_AXIS))
        frame.add(p)

        # Left
        tblModel = checkBoxTableModel(["ROI name", "Overlay"], 0)
        tblModel.addTableModelListener(checkBoxTableListener(self))
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
        b_open = JButton('Open Image', actionPerformed = self.openImage)
        p2.add(b_open)
        b_add_roi = JButton('Add ROI', actionPerformed = self.add_roi)
        p2.add(b_add_roi)
        b_del_roi = JButton('Delete ROI', actionPerformed = self.del_roi)
        p2.add(b_del_roi)
        b_save = JButton('Save', actionPerformed = self.save_roi)
        p2.add(b_save)
        b_load = JButton('Load', actionPerformed = self.load_roi)
        p2.add(b_load)

        frame.visible = True

    def openImage(self, event):
        imagePath = IJ.getFilePath("Choose image")
        if imagePath is None:
            return 0
        self.imagePath = imagePath
        self.imp = IJ.openImage(imagePath)
        self.imp.show()

    def add_roi(self, event):
        selection = self.imp.getRoi()
        if selection is None:
            IJ.error("No selection")
            return 0
        tblModel = self.tbl.getModel()
        while True:
            gd = GenericDialog("ROI name")
            gd.addStringField("Name ?", "ROI%04d" % self.roicount, 10)
            gd.showDialog()
            s = gd.getNextString()
            if gd.wasCanceled():
                return
            elif s not in self.roi.keys():
                break
            else:
                IJ.error("ROI name already used. Please use different one")
        if s == "":
            s = "ROI%04d" % self.roicount
        self.roi[s] = selection
        tblModel.addRow([s, False])
        self.roicount += 1

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

    def save_roi(self, event):
        data = []
        for k in self.roi:
            v = self.roi[k]
            t_ = v.getType()
            if t_ == 5:
                data.append(self.lineRoiToDict(k, v)) 
            elif t_ == 10:
                data.append(self.pointRoiToDict(k, v))
        res = dict({"imagePath": self.imagePath, "data": data})
        fn = IJ.getFilePath("Save result to: ")
        if fn is None:
            return 0
        with open(fn, 'w') as f:
            json.dump(res, f)
    
    def lineRoiToDict(self, k, roi):
        p = roi.getFloatPoints()
        px = p.xpoints.tolist()
        py = p.ypoints.tolist()
        return(dict({"type": 5, "name": k, "ox1": px[0], "oy1": py[0], "ox2": px[1], "oy2": py[1]}))

    def pointRoiToDict(self, k, roi):
        p = roi.getContainedFloatPoints()
        return(dict({"type": 10, "name": k, "ox": p.xpoints.tolist(), "oy": p.ypoints.tolist()}))

    def load_roi(self, event):
        fn = IJ.getFilePath("Load result from: ")
        if fn is None:
            return
        with open(fn, 'r') as f:
            res = json.load(f)
        self.imagePath = res["imagePath"]
        self.imp = IJ.openImage(self.imagePath)
        self.imp.show()
        for e in res["data"]:
            if e["type"] == 5:
                self.roi[e["name"]] = Line(e["ox1"], e["oy1"], e["ox2"], e["oy2"])
            elif e["type"] == 10:
                self.roi[e["name"]] = PointRoi(e["ox"], e["oy"])
        tblModel = self.tbl.getModel()
        for k in self.roi:
            tblModel.addRow([k, False])

    def handle_tableChanged(self, event):
        if event.getType() == 0 and event.getColumn() == 1:
            i = event.getFirstRow()
            tblModel = event.source
            v = tblModel.getValueAt(i, 1) # value after event
            roiname = tblModel.getValueAt(i, 0)
            if v:
                # Add ROI to Overlay
                self.overlay.add(self.roi[roiname])
                # Draw
                self.imp.setOverlay(self.overlay)
            else:
                # Delete ROI from Overlay
                self.overlay.remove(self.roi[roiname])
                # Draw
                self.imp.setOverlay(self.overlay)

if __name__ == '__main__':
    OverlayManager().run()
