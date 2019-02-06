import ics
import csv
import tkinter
from tkinter.filedialog import askopenfile

class DetourEvent:
    def __init__(self, event):
        parts = event.name.split("-")
        if len(parts)<2:
            self.guidename = "???"
            self.tourname = event.name
        else:
            self.guidename = parts[1].strip()
            self.tourname = parts[0].strip()
        self.date = event.begin.date()
        self.begin = event.begin.strftime("%I:%M%p")
        self.end = event.end.strftime("%I:%M%p")
        self.duration = event.duration.seconds/3600
        self.description = event.description
    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s"%(self.guidename, self.tourname, self.date, self.begin, self.end, self.duration, self.description)

class DetourCalendar:
    def __init__(self):
        self.begin_month = 1
        self.end_month = 1
        self.year = 2019
        self.window = tkinter.Toplevel()
        self.window.title("detours")
        with askopenfile(filetypes=[("Calendar files", "*.ics")]) as input_file:
            icaltext = input_file.read()
            self.calendar = ics.Calendar(icaltext)
        
    def invoice(self):
        for month in range(self.begin_month, self.end_month + 1):
            events = [DetourEvent(e) for e in self.calendar.events
                      if e.begin.month == month and e.begin.year == self.year]
            events.sort(key = lambda e:(e.guidename, e.date))
            for e in events:
                print(e)
    
x = DetourCalendar()
x.invoice()
tkinter.mainloop()

