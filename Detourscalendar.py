from icalevents import icalevents
from pytz import timezone
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

chi_time = timezone('US/Central')
months = tuple(datetime(2000, n, 1).strftime('%B') for n in range(1,13))
month_to_num = {months[n]:n + 1 for n in range(12)}
now = datetime.now()
bgcolor = '#ebebeb'
# class Calendar:
#     def __init__(self, ics_file):
#         self.ics_file = ics_file


class DetourEvent:
    def __init__(self, event):
        self.start = event.start.astimezone(chi_time)
        self.end = event.end.astimezone(chi_time)
        self.duration = (event.end - event.start).seconds / 3600
        parts = event.summary.split("-")
        if len(parts)<2:
            guidename = "???"
            self.tourname = event.summary
        else:
            guidename = parts[1].strip()
            self.tourname = parts[0].strip()
        self.guidename = guidename.replace('*', '')
        try:
            self.description = event.description.split('-::~:~:')
        except:
            self.description = ''

    def __repr__(self):
        #return "%s\t%s\t%s\t%s\t%s\t%s\t%s"%(self.guidename, self.tourname,
        #self.date, self.begin, self.end, self.duration, self.description)
        return "%s\t%s\t%s\t%s\t%s\t%s"%(
            self.guidename,
            self.tourname,
            self.start.strftime('%F'),
            self.start.strftime('%l:%M%p'),
            self.end.strftime('%l:%M%p'),
            self.duration)

class DetourCalendar:
    def __init__(self):
        self.begin_month = 1
        self.end_month = 1
        self.year = 2019
        self.ics_file = askopenfilename(filetypes=[("Calendar files", "*.ics")])
        self.window = tk.Toplevel(bg=bgcolor)
        self.window.title("Detours")
        self.buttonframe = tk.LabelFrame(self.window, text="Date Range", bg=bgcolor)
        tk.Label(self.buttonframe, text='Starting', bg=bgcolor).grid(row=0, column=0)
        self.month = tk.StringVar(value=months[(now.month - 2)%12])
        args = (self.buttonframe, self.month) + months
        self.months = tk.OptionMenu(*args)
        self.months.configure(width=7, bg=bgcolor)
        self.months.grid(row=0, column=1, padx=4, pady=4)
        self.year = tk.IntVar(value=now.year)
        args = (self.buttonframe, self.year) + tuple(range(now.year, 2012, -1))
        self.years = tk.OptionMenu(*args)
        self.years.configure(width=3, bg=bgcolor)
        self.years.grid(row=0, column=2, padx=4, pady=4)
        tk.Label(self.buttonframe, text="for", bg=bgcolor).grid(row=0, column=3)
        self.num_months = ttk.Spinbox(self.buttonframe, from_=1, to=120, width=2)
        self.num_months.set(1)
        self.num_months.grid(row=0, column=4, padx=4)
        tk.Label(self.buttonframe, text="months", bg=bgcolor).grid(row=0, column=5)
        self.submit = tk.Button(self.buttonframe, text="Submit",
                          highlightbackground=bgcolor,command=self.invoice)
        self.submit.grid(row=1, columnspan=6, pady=4)
        self.buttonframe.pack(pady=10)
        scrollbar = tk.Scrollbar(self.window)
        self.output = tk.Text(self.window, yscrollcommand=scrollbar.set,
                                       height=40, width=80)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=1)
        self.output.pack(expand=1, fill=tk.BOTH, padx=4, pady=4)
        scrollbar.config(command=self.output.yview)
        #self.window.update()
        #self.window.iconify()
        #self.window.deiconify()
       
    def event_list(self, start_year, start_month, num_months):
        start = datetime(start_year, start_month, 1, tzinfo=chi_time)
        end_year = start_year + (num_months // 12)
        end_month = start_month + (num_months % 12)
        if end_month > 12:
            end_month -= 12
            end_year += 1
        end = datetime(end_year, end_month, 1, tzinfo=chi_time)
        tour_dict = {}
        for event in icalevents.events(file=self.ics_file, start=start, end=end):
            if event.all_day:
                continue
            id = (event.uid.split('@')[0], event.start)
            if id not in tour_dict:
                tour_dict[id] = event
                continue
            if tour_dict[id].recurring == event.recurring:
                    raise RuntimeError("This should never happen!")
            if not event.recurring:
                tour_dict[id] = event
        result = [DetourEvent(event) for event in tour_dict.values()] 
        result.sort(key=lambda e :(e.guidename, e.start))
        return result

    def invoice(self):
        self.output.delete("1.0", tk.END)
        for e in self.event_list(
                self.year.get(),
                month_to_num[self.month.get()],
                int(self.num_months.get())):
            self.output.insert(tk.END, str(e)+"\n")


root = tk.Tk()
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar)
filemenu.add_command(label='Open ...', command=lambda : DetourCalendar())
menubar.add_cascade(label='File', menu=filemenu)
windowmenu = tk.Menu(menubar, name='window')
menubar.add_cascade(label='Window', menu=windowmenu)
root.configure(menu=menubar)
root.withdraw()
DetourCalendar()
tk.mainloop()    
