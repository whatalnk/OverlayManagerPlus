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

class checkBoxTableModel(DefaultTableModel):
    def getColumnClass(self, col):
        if col == 0:
            return(str)
        elif col == 1:
            return(JBool)

class checkBoxTableListener(TableModelListener):
    def __init__(self, overlayManagerPlus):
        self.overlayManagerPlus = overlayManagerPlus
    def tableChanged(self, event):
        self.overlayManagerPlus.handle_tableChanged(event)

class rowSelectionListener(ListSelectionListener):
    def __init__(self, overlayManagerPlus):
        self.overlayManagerPlus = overlayManagerPlus
    def valueChanged(self, event):
        self.overlayManagerPlus.show_selection(event)

class OverlayManagerPlus(object):
    def __init__(self):
        self.roi = dict()
        self.overlay = Overlay()
        self.roicount = 0
        imp = WindowManager.getCurrentImage()
        if imp is not None:
            self.imp = imp
            self.imagePath = os.path.join(imp.getOriginalFileInfo().directory, imp.getOriginalFileInfo().fileName)
        self.frame = PlugInFrame("Overlay Manager")
        self.frame.setSize(300, 600)

        # Parent
        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.X_AXIS))
        self.frame.add(p)

        # Left
        tblModel = checkBoxTableModel(["ROI name", "Overlay"], 0)
        tblModel.addTableModelListener(checkBoxTableListener(self))
        self.tbl = JTable(tblModel)
        self.tbl.getColumn("Overlay").setMaxWidth(100)
        self.tbl.setRowHeight(20)
        self.tbl.getColumnModel().setColumnMargin(10)
        self.tbl.getSelectionModel().addListSelectionListener(rowSelectionListener(self))
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
        b_update_roi = JButton('Update ROI', actionPerformed = self.update_roi)
        p2.add(b_update_roi)
        b_del_roi = JButton('Delete ROI', actionPerformed = self.del_roi)
        p2.add(b_del_roi)
        b_rename_roi = JButton('Rename ROI', actionPerformed = self.rename_roi)
        p2.add(b_rename_roi)
        b_save = JButton('Save', actionPerformed = self.save_roi)
        p2.add(b_save)
        b_load = JButton('Load', actionPerformed = self.load_roi)
        p2.add(b_load)

        self.frame.visible = True

    def openImage(self, event):
        imagePath = IJ.getFilePath("Choose image")
        if imagePath is None:
            return 0
        self.imagePath = imagePath
        self.imp = IJ.openImage(imagePath)
        self.imp.show()

    def add_roi(self, event):
        selection = self.imp.getRoi()
        if selection.getType() == 10:
            selection.setShowLabels(True)
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
    
    def update_roi(self, event):
        newRoi = self.imp.getRoi()
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
            gd.addMessage("Update %s ?" % v)
            gd.enableYesNoCancel()
            gd.showDialog()
            if gd.wasOKed():
                self.roi[v] = newRoi

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
                self.del_overlay(v)
                del self.roi[v]

    def rename_roi(self, event):
        tbl = self.tbl
        i = tbl.getSelectedRow()
        if i == -1:
            gd = GenericDialog("Confirm")
            gd.addMessage("Plese select an item")
            gd.hideCancelButton()
            gd.showDialog()
        else:
            tblModel = self.tbl.getModel()
            k_prev = tbl.getValueAt(i, 0)
            v_prev = self.roi[k_prev]
            del self.roi[k_prev]
            while True:
                gd = GenericDialog("Rename")
                gd.addStringField("Rename %s to: " % k_prev, k_prev, 10)
                gd.showDialog()
                s = gd.getNextString()
                if gd.wasCanceled():
                    return
                elif s == "":
                    IJ.error("Please enter a name")
                elif s in self.roi.keys():
                    IJ.error("ROI name already used. Please use different one")
                else:
                    break
        self.del_overlay(k_prev)
        self.tbl.getModel().removeRow(i)
        self.roi[s] = v_prev
        tblModel.addRow([s, False])

    def save_roi(self, event):
        data = dict()
        for k in self.roi:
            v = self.roi[k]
            t_ = v.getType()
            if t_ == 5:
                data[k] = self.lineRoiToDict(v) 
            elif t_ == 10:
                data[k] = self.pointRoiToDict(v)
        res = dict({"imagePath": self.imagePath, "data": data})
        fn = IJ.getFilePath("Save result to: ")
        if fn is None:
            return 0
        with open(fn, 'w') as f:
            json.dump(res, f, indent=True)

    def lineRoiToDict(self, roi):
        p = roi.getFloatPoints()
        px = p.xpoints.tolist()
        py = p.ypoints.tolist()
        return(dict({"type": 5, "ox1": px[0], "oy1": py[0], "ox2": px[1], "oy2": py[1]}))

    def pointRoiToDict(self, roi):
        p = roi.getContainedFloatPoints()
        ox, oy = zip(*sorted([(px, py) for (px, py) in zip(p.xpoints.tolist(), p.ypoints.tolist())], key=lambda k: k[0], reverse=True))
        return(dict({"type": 10, "ox": list(ox), "oy": list(oy)}))

    def load_roi(self, event):
        fn = IJ.getFilePath("Load result from: ")
        if fn is None:
            return
        with open(fn, 'r') as f:
            res = json.load(f)
        tblModel = self.tbl.getModel()
        for k, v in sorted(res["data"].items()):
            if v["type"] == 5:
                self.roi[k] = Line(v["ox1"], v["oy1"], v["ox2"], v["oy2"])
            elif v["type"] == 10:
                self.roi[k] = PointRoi(v["ox"], v["oy"])
                self.roi[k].setShowLabels(True)
            tblModel.addRow([k, False])
        if os.path.exists(res["imagePath"]):
            self.imagePath = res["imagePath"]
        else:
            IJ.error("%s was not found. Please locate." % res["imagePath"])
            imagePath = IJ.getFilePath("Locate image")
            if imagePath is None:
                return 0
            self.imagePath = imagePath
        self.imp = IJ.openImage(self.imagePath)
        self.imp.show()

    def handle_tableChanged(self, event):
        if event.getType() == 0 and event.getColumn() == 1:
            i = event.getFirstRow()
            tblModel = event.source
            v = tblModel.getValueAt(i, 1) # value after event
            roiname = tblModel.getValueAt(i, 0)
            if v:
                # Add ROI to Overlay
                self.overlay.add(self.roi[roiname], roiname)
                # Draw
                self.imp.setOverlay(self.overlay)
            else:
                self.del_overlay(roiname)

    def del_overlay(self, roiname):
        # Delete ROI from Overlay
        self.overlay.remove(roiname)
        # Draw
        self.imp.setOverlay(self.overlay)

    def show_selection(self, event):
        i = self.tbl.getSelectedRow()
        if i == -1:
            return
        else:
            tblModel = self.tbl.getModel()
            roiname = tblModel.getValueAt(i, 0)
            self.imp.setRoi(self.roi[roiname])

if __name__ == '__main__':
    OverlayManagerPlus()
