import ics
import csv
import tkinter
from tkinter.filedialog import askopenfile

months = {
    "January":1,
    "February":2,
    "March":3}

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
        #return "%s\t%s\t%s\t%s\t%s\t%s\t%s"%(self.guidename, self.tourname, self.date, self.begin, self.end, self.duration, self.description)
        return "%s\t%s\t%s\t%s\t%s\t%s"%(self.guidename, self.tourname, self.date, self.begin, self.end, self.duration)


class DetourCalendar:
    def __init__(self):
        self.begin_month = 1
        self.end_month = 1
        self.year = 2019
        self.window = tkinter.Toplevel()
        self.window.title("Detours")
        self.buttonframe = tkinter.LabelFrame(self.window, text="Date Range")
        self.months = tkinter.Menubutton(self.buttonframe, text="month")
        monthmenu = tkinter.Menu(self.months, tearoff=0)
        for month in months.keys():
            monthmenu.add_command(label=month)
        self.months["menu"] = monthmenu
        self.months.grid(row=0, column=0)
        self.submit = tkinter.Button(self.buttonframe, text="Submit", command=self.invoice)
        self.submit.grid(row=1, column=1)
        self.buttonframe.pack(pady=10)
        scrollbar = tkinter.Scrollbar(self.window)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.output = tkinter.Text(self.window, height=10, width=80, yscrollcommand=scrollbar.set)
        self.output.pack(expand=1, fill=tkinter.BOTH, padx=10)
        scrollbar.config(command=self.output.yview)
        with askopenfile(filetypes=[("Calendar files", "*.ics")]) as input_file:
            icaltext = input_file.read()
            self.calendar = ics.Calendar(icaltext)
        
    def invoice(self):
        self.output.delete("1.0", tkinter.END)
        for month in range(self.begin_month, self.end_month + 1):
            events = [DetourEvent(e) for e in self.calendar.events
                      if e.begin.month == month and e.begin.year == self.year]
            events.sort(key = lambda e:(e.guidename, e.date))
            for e in events:
                self.output.insert(tkinter.END, str(e)+"\n")

root = tkinter.Tk()
root.withdraw()
x = DetourCalendar()
#x.invoice()
tkinter.mainloop()
