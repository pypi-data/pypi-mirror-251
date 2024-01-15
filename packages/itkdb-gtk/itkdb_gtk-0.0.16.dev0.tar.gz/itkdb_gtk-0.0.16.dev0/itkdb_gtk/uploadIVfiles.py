#!/usr/bin/env python3
"""Read IV files and create plots."""
import os
import json
import math
from pathlib import Path

import gi
import tempfile

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

try:
    import dbGtkUtils
    import ITkDBlogin
    import ITkDButils
    import uploadTest

except ModuleNotFoundError:
    from itkdb_gtk import dbGtkUtils, ITkDBlogin, ITkDButils, uploadTest

# Check if Gtk can be open
gtk_runs, gtk_args = Gtk.init_check()


def remove_files(W, flist):
    for f in flist:
        os.unlink(f)

def scale_iv(I, T1, T2):
    """Normalize corrent  to given temperature (T2)

    Args:
        I (array): Current
        T1 (float): Original temperature
        T2 (float): New temperature.

    Return:
        Array with scaled currents.

    """
    factor = (T2 / T1) ** 2 * math.exp((-1.2 / 8.62) * (1 / T2 - 1 / T1))
    return factor * I


class IVwindow(dbGtkUtils.ITkDBWindow):
    """GUI for IV file handling."""

    def __init__(self, session, title="IV window", options=None):
        """Initialization."""
        super().__init__(
            session=session, title=title, show_search=None, gtk_runs=gtk_runs
        )
        self.mdata = {}
        self.mod_type = {}
        self.mod_SN = {}
        self.difference = None
        self.canvas = None

        self.init_window()

    def init_window(self):
        """Prepare the Gtk window."""
        self.hb.props.title = "IV data"

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.set_tooltip_text("Click to refresh canvas.")
        button.connect("clicked", self.on_refresh)
        self.hb.pack_end(button)

        # Button to upload
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-send-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.set_tooltip_text("Click to upload test")
        button.connect("clicked", self.upload_test)
        self.hb.pack_end(button)

        # File entry and search button
        self.single_file = Gtk.FileChooserButton()
        self.single_file.connect("file-set", self.on_single_file_set)

        self.double_file = Gtk.FileChooserButton()
        self.double_file.connect("file-set", self.on_double_file_set)

        self.single_SN = Gtk.Label(label="(None)")
        self.double_SN = Gtk.Label(label="(None)")

        grid = Gtk.Grid(column_spacing=5, row_spacing=1)

        grid.attach(Gtk.Label(label="Files"), 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="Serial No."), 2, 0, 1, 1)

        grid.attach(Gtk.Label(label="Single Data File"), 0, 1, 1, 1)
        grid.attach(self.single_file, 1, 1, 1, 1)
        grid.attach(self.single_SN, 2, 1, 1, 1)

        grid.attach(Gtk.Label(label="Double Data File"), 0, 2, 1, 1)
        grid.attach(self.double_file, 1, 2, 1, 1)
        grid.attach(self.double_SN, 2, 2, 1, 1)

        btn = Gtk.Button(label="Compute difference")
        btn.connect("clicked", self.on_difference)
        grid.attach(btn, 1, 3, 1, 1)

        self.mainBox.pack_start(grid, False, True, 0)

        self.fig = mpl.figure.Figure()
        self.fig.tight_layout()
        sw = Gtk.ScrolledWindow()  # Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width(10)
        sw.set_size_request(310, 310)

        self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
        self.canvas.set_size_request(400, 300)
        sw.add(self.canvas)
        self.mainBox.pack_start(sw, True, True, 0)

        # Create toolbar
        toolbar = NavigationToolbar(self.canvas)
        self.mainBox.pack_start(toolbar, False, False, 0)

        # The text view
        frame = self.create_text_view()
        self.mainBox.pack_start(frame, True, True, 5)

        self.show_all()

    def upload_test(self, *args):
        """Upload available tests."""
        test = ITkDButils.get_test_skeleton(
            self.session, "MODULE", self.mdata["double"]["TestType"]
        )
        mdata = self.mdata["double"]
        V = mdata["curve"]["V"]
        I = np.abs(mdata["curve"]["I"])

        indx = np.where(V == 500)[0]
        i_500 = I[indx][0]

        indx = np.where(V == 700)
        rms = np.std(I[indx])

        test["component"] = self.mod_SN["double"]
        test["institution"] = mdata["Institute"]
        test["runNumber"] = mdata["RunNumber"]
        test["date"] = ITkDButils.get_db_date(
            "{} {}".format(mdata["Date"], mdata["Time"])
        )
        test["passed"] = True
        test["problems"] = False
        test["properties"]["VBIAS_SMU"] = mdata["Vbias_SMU"]
        test["properties"]["RSERIES"] = mdata["Rseries"]
        test["properties"]["TEST_DMM"] = mdata["Test_DMM"]
        test["properties"]["RSHUNT"] = mdata["Rshunt"]
        test["properties"]["RUNNUMBER"] = mdata["RunNumber"]
        test["properties"]["COMMENTS"] = mdata["Comments"]
        test["properties"]["ALGORITHM_VERSION"] = "0.0.0"
        test["properties"]["SOFTWARE_TYPE_VERSION"] = "pyProbe"
        test["properties"]["MODULE_STAGE"] = mdata["Module_Stage"]
        test["results"]["TEMPERATURE"] = mdata["Temperature"]
        test["results"]["HUMIDITY"] = mdata["Humidity"]
        test["results"]["VBD"] = mdata["curve"]["V"][-1]
        test["results"]["I_500V"] = i_500
        test["results"]["VOLTAGE"] = V
        test["results"]["CURRENT"] = I
        test["results"]["RMS_STABILITY"] = 0.0
        test["results"]["SHUNT_VOLTAGE"] = np.zeros(V.shape)

        # write attachment.
        items = [
            "Type",
            "Wafer",
            "Module_SN",
            "Module_Stage",
            "Date",
            "Time",
            "Institute",
            "TestType",
            "Vbias_SMU",
            "Rseries",
            "Test_DMM",
            "Rshunt",
            "Software type and version, fw version",
            "RunNumber",
            "Temperature",
            "Humidity",
            "Comments",
        ]
        fnam = "{}_{}_IV_{}-".format(self.mod_SN["double"], mdata["Module_Stage"], mdata["RunNumber"])
        data_out = tempfile.NamedTemporaryFile('w', prefix=fnam, suffix=".dat", delete=False)
        data_out.write("{}\n".format(fnam))
        for key in items:
            if key == "Module_SN":
                data_out.write("{}: {}\n".format(key, self.mod_SN["double"]))
            else:
                data_out.write("{}: {}\n".format(key, mdata[key]))

        for il, label in enumerate(mdata["curve"]["labels"]):
            if il:
                data_out.write('\t')
            data_out.write(label)
        data_out.write("\n")

        ndata = len(mdata["curve"]["V"])
        for i in range(ndata):
            data_out.write("{:.2f}\t{:.2f}\t{:.2f}\n".format(V[i], self.difference[i], 0.0))

        print(data_out.name)
        data_out.close()

        js_out = tempfile.NamedTemporaryFile('w', prefix="payload-", suffix=".json", delete=False)
        js_out.write(json.dumps(test, indent=3, cls=dbGtkUtils.MyEncoder))
        js_out.close()

        attachment = ITkDButils.Attachment(data_out.name, "resultsFile", fnam)
        uploadW = uploadTest.UploadTest(self.session, js_out.name, attachment)
        uploadW.connect("destroy", remove_files, [data_out.name, js_out.name])

    def on_refresh(self, *args):
        """Refresh canvas."""
        if self.fig and self.canvas:
            self.fig.tight_layout()
            self.canvas.draw()

    def find_module(self, SN):
        """Find module (SN) on database

        Args:
        ----
            SN (str): Module Serial number
        """
        md = ITkDButils.get_DB_component(self.session, SN)
        if md is None:
            dbGtkUtils.complain(
                "Could not find {}".format(SN), str(ITkDButils.get_db_response())
            )

        return md

    def on_single_file_set(self, *args):
        """File chosen."""
        fnam = self.single_file.get_filename()
        if fnam is None or not Path(fnam).exists():
            dbGtkUtils.complain("Could not find data file", fnam, parent=self)

        mdata = self.read_file(fnam)

        SN = mdata["Module_SN"]
        self.write_message("Reading data for module {}\n".format(SN))
        md = self.find_module(SN)
        if md is None:
            self.write_message("...object does not exist.\n")
            self.single_file.unselect_all()
            return

        # All good
        self.mod_SN["single"] = SN
        self.mdata["single"] = mdata
        self.mod_type["single"] = md["type"]["code"]
        print(self.mod_type["single"])

        self.single_SN.set_text("{} - {}".format(SN, md["type"]["name"]))
        self.show_curve(
            131,
            mdata["curve"]["V"],
            mdata["curve"]["I"],
            self.mod_type["single"][0:4],
            mdata["curve"]["labels"][0],
            mdata["curve"]["labels"][1],
        )

    def on_double_file_set(self, *args):
        "File chosen for the 'double module'"
        fnam = self.double_file.get_filename()
        if fnam is None or not Path(fnam).exists():
            dbGtkUtils.complain("Could not find data file", fnam, parent=self)

        mdata = self.read_file(fnam)

        # Check SN in data file
        SN = mdata["Module_SN"]
        halfM_SN = SN
        if "single" in self.mod_SN:
            if self.mod_SN["single"] == SN:
                dbGtkUtils.complain("Wrong module SN", "{} already used.".format(SN))
                self.double_file.unselect_all()
                return

        # Check that it exists in the DB
        self.write_message("Reading data for module {}\n".format(SN))
        md = self.find_module(SN)
        if md is None:
            self.write_message("...object does not exist.\n")
            self.double_file.unselect_all()
            return

        found_child = False
        if md["type"]["name"].find("Ring"):
            self.write_message("...This is a Ring module. Searching children in DB\n")
            for child in md["children"]:
                if child["component"]:
                    ctype = child["type"]["code"]
                    if ctype.find("MODULE")<0:
                        continue

                    cSN = child["component"]["serialNumber"]
                    if cSN == self.mod_SN["single"]:
                        continue

                    halfM_SN = cSN
                    found_child = True
                    self.write_message("...found {}\n".format(halfM_SN))
                    break


            if not found_child:
                self.write_message("Requesting a Half Module SN\n")
                halfM_SN = dbGtkUtils.get_a_value("Give Half Module SN", "Serial Number")

            md = ITkDButils.get_DB_component(self.session, halfM_SN)
            if md is None:
                dbGtkUtils.complain(
                    "Could not find {}".format(halfM_SN),
                    str(ITkDButils.get_db_response()),
                )
                self.double_file.unselect_all()
                return

            self.write_message("... {}".format(halfM_SN))

        if "single" in self.mod_type:
            if self.mod_type["single"] == md["type"]["code"]:
                dbGtkUtils.complain(
                    "Wrong module type.",
                    "Module type cannot be {}".format(self.mod_type["single"]),
                )

                self.double_file.unselect_all()
                return

        self.mod_SN["double"] = halfM_SN
        self.mod_type["double"] = md["type"]["code"]
        self.mdata["double"] = mdata

        self.double_SN.set_text("{} - {}".format(SN, md["type"]["name"]))
        self.show_curve(
            133,
            mdata["curve"]["V"],
            mdata["curve"]["I"],
            "Double",
            mdata["curve"]["labels"][0],
            None,
        )

        # Compute difference if single already available
        if "single" in self.mdata:
            self.on_difference()

    def on_difference(self, *args):
        """Compute difference."""
        if "single" not in self.mdata or "double" not in self.mdata:
            dbGtkUtils.complain(
                "Data needed", "Check if single oand doubel module data are available"
            )
            return

        single_I = scale_iv(
            self.mdata["single"]["curve"]["I"],
            self.mdata["single"]["Temperature"] + 273.0,
            self.mdata["double"]["Temperature"] + 273.0,
        )

        self.difference = self.mdata["double"]["curve"]["I"] - single_I

        self.show_curve(
            132,
            self.mdata["double"]["curve"]["V"],
            self.difference,
            self.mod_type["double"][0:4],
            self.mdata["double"]["curve"]["labels"][0],
            None,
        )

    def show_curve(self, subplot, X, Y, title=None, xlabel="X", ylabel="Y"):
        """Shows data"""
        ax = self.fig.add_subplot(subplot)
        if xlabel:
            ax.set_xlabel(xlabel)

        if ylabel:
            ax.set_ylabel(ylabel)

        if title:
            ax.set_title(title)

        ax.plot(X, Y)
        ax.grid()
        self.on_refresh()

    @staticmethod
    def read_file(fnam):
        """Read a data file. Return dictionary with all teh data."""
        labels = []
        metadata = {}
        with open(fnam, "r", encoding="utf-8") as ifile:
            first = True
            for line in ifile:
                if first:
                    first = False
                    ipos = line.rfind('.')
                    metadata["fname"] = line[:ipos]
                    continue

                if line.find("Voltage [V]") >= 0:
                    labels = line.split("\t")
                    break

                rc = line.find(":")
                if rc >= 0:
                    key = line[:rc].strip()
                    val = line[rc + 1 :].strip()
                    if key in ["Temperature", "Humidity"]:
                        metadata[key] = float(val)
                    else:
                        metadata[key] = val

            V = []
            I = []
            for line in ifile:
                data = [float(s) for s in line.split()]
                V.append(data[0])
                I.append(data[1])

            metadata["curve"] = {
                "V": np.array(V),
                "I": np.array(I),
                "labels": labels[0:2],
            }
            return metadata


if __name__ == "__main__":
    import sys

    # DB login
    dlg = ITkDBlogin.ITkDBlogin()
    client = dlg.get_client()
    if client is None:
        print("Could not connect to DB with provided credentials.")
        dlg.die()
        sys.exit()

    client.user_gui = dlg

    # Start the Application
    win = IVwindow(client)
    win.show_all()
    win.set_accept_focus(True)
    win.present()
    win.connect("destroy", Gtk.main_quit)

    try:
        Gtk.main()
    except KeyboardInterrupt:
        print("Arrggggg !!!")

    dlg.die()
    print("Bye !!")
    sys.exit()
