# This program track's your APM action per minute and displays all actions
# divided by last two minutes.

# Imports
import win32api
import time
import PySimpleGUI as sg


class Tracker:
    def __init__(self):
        self.tracked_keys = [0x01, 0x02, 0x05, 0x09, 0x11,
                             0x31, 0x32, 0x33, 0x34, 0x35, 0x36,
                             0x37, 0x51, 0x52, 0x53, 0x50, 0x57, 0x45,
                             0x70, 0x71, 0x72, 0x73]

        self.multiplier = 0.565
        self.all_the_clicks = [time.time()]
        self.average_clicks = None
        self.length_of_time = 60

    def click_tracker(self):
        for i in range(1, 256):
            if win32api.GetAsyncKeyState(i):
                if i in self.tracked_keys:
                    self.all_the_clicks.append(time.time())

        self.average_clicks = round(len(self.all_the_clicks) * self.multiplier)
        self.check_distance()
        return self.average_clicks

    def check_distance(self):
        # if distance in time by first and last element is longer than allowed length of time,
        # first element will be deleted
        if self.all_the_clicks[-1] - self.all_the_clicks[0] > self.length_of_time:
            self.all_the_clicks.pop(0)


class MainGUI:
    def __init__(self):
        self.t = Tracker()
        self.layout = [[sg.Text("0000", key="-OUT-")]]
        self.window = sg.Window('w', self.layout, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

    def run_window(self):
        while True:
            event, values = self.window.read(timeout=1)
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            self.window['-OUT-'].update(self.t.click_tracker())
            self.window.refresh()
            time.sleep(0.05)

        self.window.Close()


m = MainGUI()
m.run_window()
