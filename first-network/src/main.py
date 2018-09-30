import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import requests
from tkinter.scrolledtext import ScrolledText

rest_server = 'http://localhost:3000/api/' ##CONFIGURE THIS
resume_format = 'Organization Name: SAMPLE_COMPANY\nDate: DD/MM/YYYY\nEntry: PLEASE FOLLOW THIS FORMAT, RESUME ENTRY GOES HERE'


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        print('log - initializing GUI')
        root = tk.Tk.__init__(self, *args, **kwargs)
        self.frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        self.access_type = None
        self.person_id = None
        self.organization_id = None
        self.buttons = []
        self.entries = {}
        self.choose_access_type()

    def create_menu(self, person_id=None, org_id=None):
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.organization_id = org_id
        self.winfo_toplevel().title('Hyperledger')
        menu = tk.Menu(self.winfo_toplevel())
        self.geometry('500x500')

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label='Refresh', command=lambda: self.refresh())
        fileMenu.add_command(label='Query Resume', command = lambda:self.query_resume())
        fileMenu.add_command(label='Add to Resume (Organization)', command=lambda: self.organization_add())
        fileMenu.add_command(label='Approve Request (Organization)', command=lambda: self.organization_approve())
        fileMenu.add_command(label='Add to Resume (Person)', command=lambda: self.person_add())
        fileMenu.add_command(label='Update Resume (Person)', command=lambda: self.person_update())
        fileMenu.add_command(label='Add Employer (Person)', command=lambda: self.person_add_employer())
        fileMenu.add_command(label='Delete Employer (Person)', command=lambda: self.person_del_employer())
        if self.access_type == 'person':
            fileMenu.entryconfig('Add to Resume (Organization)', state='disabled')
            fileMenu.entryconfig('Approve Request (Organization)', state='disabled')
        elif self.access_type == 'org':
            fileMenu.entryconfig('Add to Resume (Person)', state='disabled')
            fileMenu.entryconfig('Update Resume (Person)', state='disabled')
            fileMenu.entryconfig('Add Employer (Person)', state='disabled')
            fileMenu.entryconfig('Delete Employer (Person)', state='disabled')

        menu.add_cascade(label='Operation', menu=fileMenu)

        if self.access_type == 'admin':
            adminMenu = tk.Menu(menu)
            adminMenu.add_command(label='Add New Organization (Admin)', command=lambda: self.create_new_org())
            adminMenu.add_command(label='Add New Person (Admin)', command=lambda: self.create_new_person())
            menu.add_cascade(label='Admin', menu=adminMenu)

        self.winfo_toplevel().config(menu=menu)
        self.refresh()

    def refresh(self):
        self.entries = {}
        if self.access_type == 'person':
            url = rest_server + 'approvedResume'
            response = requests.get(url)
            result = response.json()
            if 'error' not in result:
                self.frame.destroy()
                self.frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
                self.frame.pack(fill=tk.X, padx=5, pady=5)
                if len(result) == 0:
                    idLabel = ttk.Label(self.frame, text='No resume that needs to be updated')
                    idLabel.pack(side=tk.LEFT, padx=5, pady=5)
                else:
                    for item in result:
                        if item['owner'] == "resource:org.example.firstnetwork.Person#{}".format(self.person_id):
                            new = ResumeEntry()
                            new.id = item['org'][str(item['org']).find('#')+1:]
                            new.value = item['addValue']['Value']
                            approvedId = item['approvedId']
                            self.entries[approvedId] = new
                            button = tk.ttk.Button(self.frame, text=approvedId,
                                                   command=lambda approvedId=approvedId: self.resume_popup(approvedId))
                            button.pack(pady=5)

        elif self.access_type == 'org':
            url = rest_server + 'requestResume'
            response = requests.get(url)
            result = response.json()
            if 'error' not in result:
                self.frame.destroy()
                self.frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
                self.frame.pack(fill=tk.X, padx=5, pady=5)
                if len(result) == 0:
                    idLabel = ttk.Label(self.frame, text='No resume that needs to be approved')
                    idLabel.pack(side=tk.LEFT, padx=5, pady=5)
                else:
                    for item in result:
                        if item['org'] == "resource:org.example.firstnetwork.Organization#{}".format(
                                self.organization_id):
                            new = ResumeEntry()
                            new.id = item['owner'][str(item['owner']).find('#')+1:]
                            new.value = item['addValue']['Value']
                            approvedId = item['requestId']
                            self.entries[approvedId] = new
                            button = tk.ttk.Button(self.frame, text=approvedId,
                                                   command=lambda approvedId=approvedId: self.resume_popup(approvedId))
                            button.pack(pady=5)

        # print(self.entries)

    def resume_popup(self, id):
        win = tk.Toplevel()
        if self.access_type=='person':
            win.wm_title("Update Resume")
        elif self.access_type=='org':
            win.wm_title('Approve Resume Request')
        frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
        frame.pack(fill=tk.X, padx=5, pady=5)
        idFrame = ttk.Frame(frame)
        idFrame.pack(fill=tk.X, pady=5)
        if self.access_type == 'person':
            idLabel = ttk.Label(idFrame, text='{0:15}\t: {1}'.format('Organization ID', self.entries[id].id))
        elif self.access_type == 'org':
            idLabel = ttk.Label(idFrame, text='{0:15}\t: {1}'.format('Person ID', self.entries[id].id))
        idLabel.pack(side=tk.LEFT, padx=5)
        valueFrame = ttk.Frame(frame)
        valueFrame.pack(fill=tk.X, pady=5)
        valueLabel = ttk.Label(valueFrame, text='{0:15}\t: {1}'.format('Resume Entry', self.entries[id].value))
        valueLabel.pack(side=tk.LEFT, padx=5)
        if self.access_type == 'person':
            button = tk.ttk.Button(frame, text='Update',
                                   command=lambda: self.person_update(id,win) or self.refresh())
            button.pack(pady=5)
            button1 = tk.ttk.Button(frame, text='Delete',
                                    command=lambda : self.del_approved_resume(id, win))
            button1.pack(pady=5)

        elif self.access_type == 'org':
            button = tk.ttk.Button(frame, text='Approve',
                                   command=lambda: self.organization_approve(id,win) or self.refresh())
            button.pack(pady=5)
            button1 = tk.ttk.Button(frame, text='Delete',
                                    command=lambda: self.del_request_resume(id, win))
            button1.pack(pady=5)

    def del_approved_resume(self,id=None,win=None):
        if id is not None:
            msg = tk.messagebox.askokcancel('Confirmation','Are you sure?\nThe operation cannot be undone.',parent=win)
            if msg:
                response = requests.delete(rest_server + 'approvedResume/'+id)
                txt = response.text
                if txt != '':
                    response = response.json()
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()
                self.refresh()

    def del_request_resume(self,id=None,win=None):
        if id is not None:
            msg = tk.messagebox.askokcancel('Confirmation','Are you sure?\nThe operation cannot be undone.',parent=win)
            if msg:
                response = requests.delete(rest_server + 'requestResume/'+id)
                txt = response.text
                if txt != '':
                    response=response.json()
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()
                self.refresh()

    def query_resume(self):
        def operation():
            def proceed():
                person_id = idEntry.get()
                response = requests.get(rest_server + 'Resume/'+person_id)
                resume = response.json()
                if 'error' in resume:
                    tk.messagebox.showerror(resume['error']['name'], resume['error']['message'], parent=win)
                    win.destroy()
                else:
                    response = requests.get(rest_server + 'Person/' + person_id)
                    person = response.json()
                    if 'error' in person:
                        tk.messagebox.showerror(person['error']['name'], person['error']['message'], parent=win)
                        win.destroy()
                    else:
                        firstname = person['firstName']
                        lastname = person['lastName']
                        org_str = ''
                        for org in resume['org']:
                            if org == 'resource:org.example.firstnetwork.Organization#default':
                                continue
                            org_str = org_str+org+'\n'
                        value_str=''
                        for value in resume['value']:
                            value_str = value_str+value['Value']+'\n'
                        win.destroy()
                        new = tk.Toplevel()
                        new.resizable(width=False, height=False)
                        new.wm_title('Resume Result')
                        frame = ttk.Frame(new, border=2, relief=tk.GROOVE)
                        frame.pack(fill=tk.X, padx=5, pady=5)
                        nameFrame = ttk.Frame(frame)
                        nameFrame.pack(fill=tk.X, pady=5)
                        nameLabel = ttk.Label(nameFrame, text='{0:15}\t:'.format('Name'))
                        nameLabel.pack(side=tk.LEFT, padx=5)
                        nameLabel1 = ttk.Label(nameFrame, text='{} {}'.format(firstname,lastname))
                        nameLabel1.pack(side=tk.LEFT, padx=5)
                        idFrame1 = ttk.Frame(frame)
                        idFrame1.pack(fill=tk.X, pady=5)
                        idLabel1 = ttk.Label(idFrame1, text='{0:15}\t:'.format('Person ID (IC)'))
                        idLabel1.pack(side=tk.LEFT, padx=5)
                        idLabel2 = ttk.Label(idFrame1, text=person_id)
                        idLabel2.pack(side=tk.LEFT, padx=5)
                        orgFrame = ttk.Frame(frame)
                        orgFrame.pack(fill=tk.X, pady=5)
                        orgLabel = ttk.Label(orgFrame, text='{0:15}\t:'.format('Organization'))
                        orgLabel.pack(side=tk.LEFT, padx=5)
                        orgLabel1 = ttk.Label(orgFrame, text=org_str)
                        orgLabel1.pack(side=tk.LEFT, padx=5)
                        valFrame = ttk.Frame(frame)
                        valFrame.pack(fill=tk.X, pady=5)
                        valLabel = ttk.Label(valFrame, text='{0:15}\t:'.format('Resume Entry'))
                        valLabel.pack(side=tk.LEFT, padx=5)
                        valLabel1 = ScrolledText(master=valFrame, wrap=tk.WORD)
                        valLabel1.pack(side=tk.LEFT, padx=5,fill=tk.BOTH,expand=True)
                        valLabel1.insert(tk.INSERT,value_str)
                        valLabel1.config(state=tk.DISABLED)

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title('Query Resume by ID')
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            idFrame = ttk.Frame(frame)
            idFrame.pack(fill=tk.X, pady=5)
            idLabel = ttk.Label(idFrame, text='{0:15}\t:'.format('Person ID (IC)'))
            idLabel.pack(side=tk.LEFT, padx=5)
            idEntry = ttk.Entry(idFrame)
            idEntry.pack(side=tk.LEFT)
            idEntry.focus()

            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def create_new_person(self):
        def operation():
            def proceed():
                person_id = idEntry.get()
                first = firstEntry.get()
                last = lastEntry.get()
                json = {
                    "$class": "org.example.firstnetwork.Person",
                    "participantId": person_id,
                    "firstName": first,
                    "lastName": last
                }
                response = requests.post(rest_server + 'Person', json=json)
                json = {
                    "$class": "org.example.firstnetwork.Resume",
                    "resumeId": person_id,
                    "owner": 'resource:org.example.firstnetwork.Person#{}'.format(person_id),
                    "org": ["resource:org.example.firstnetwork.Organization#default"],
                    "value": []
                }
                response = requests.post(rest_server + 'Resume', json=json)
                response = response.json()
                if 'error' in response:
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Create New Person")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            idFrame = ttk.Frame(frame)
            idFrame.pack(fill=tk.X, pady=5)
            idLabel = ttk.Label(idFrame, text='{0:15}\t:'.format('Person ID (IC)'))
            idLabel.pack(side=tk.LEFT, padx=5)
            idEntry = ttk.Entry(idFrame)
            idEntry.pack(side=tk.LEFT)
            idEntry.focus()
            firstFrame = ttk.Frame(frame)
            firstFrame.pack(fill=tk.X, pady=5)
            firstLabel = ttk.Label(firstFrame, text='{0:15}\t:'.format('First Name'))
            firstLabel.pack(side=tk.LEFT, padx=5)
            firstEntry = ttk.Entry(firstFrame)
            firstEntry.pack(side=tk.LEFT)
            lastFrame = ttk.Frame(frame)
            lastFrame.pack(fill=tk.X, pady=5)
            lastLabel = ttk.Label(lastFrame, text='{0:15}\t:'.format('Last Name'))
            lastLabel.pack(side=tk.LEFT, padx=5)
            lastEntry = ttk.Entry(lastFrame)
            lastEntry.pack(side=tk.LEFT)

            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def create_new_org(self):
        def operation():
            def proceed():
                org_id = orgEntry.get()
                org_name = nameEntry.get()
                json = {
                    "$class": "org.example.firstnetwork.Organization",
                    "organizationId": org_id,
                    "Name": org_name
                }
                response = requests.post(rest_server + 'Organization', json=json)
                response = response.json()
                if 'error' in response:
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Create New Organization")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            orgFrame = ttk.Frame(frame)
            orgFrame.pack(fill=tk.X, pady=5)
            orgLabel = ttk.Label(orgFrame, text='{0:20}\t:'.format('Organization Unique ID'))
            orgLabel.pack(side=tk.LEFT, padx=5)
            orgEntry = ttk.Entry(orgFrame)
            orgEntry.pack(side=tk.LEFT)
            orgEntry.focus()
            nameFrame = ttk.Frame(frame)
            nameFrame.pack(fill=tk.X, pady=5)
            nameLabel = ttk.Label(nameFrame, text='{0:20}\t:'.format('Organization Name'))
            nameLabel.pack(side=tk.LEFT, padx=5)
            nameEntry = ttk.Entry(nameFrame)
            nameEntry.pack(side=tk.LEFT)

            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def person_del_employer(self):
        def operation():
            def proceed():
                org_id = orgEntry.get()
                json = {"$class": "org.example.firstnetwork.DeleteEmployer",
                        "resume": "resource:org.example.firstnetwork.Resume#{}".format(self.person_id),
                        "employer": "resource:org.example.firstnetwork.Organization#{}".format(org_id)}
                response = requests.post(rest_server + 'DeleteEmployer', json=json)
                response = response.json()
                if 'error' in response:
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Delete an Employer")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            orgFrame = ttk.Frame(frame)
            orgFrame.pack(fill=tk.X, pady=5)
            orgLabel = ttk.Label(orgFrame, text='{0:15}\t:'.format('Organization ID'))
            orgLabel.pack(side=tk.LEFT, padx=5)
            orgEntry = ttk.Entry(orgFrame)
            orgEntry.pack(side=tk.LEFT)
            orgEntry.focus()
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def person_add_employer(self):
        def operation():
            def proceed():
                org_id = orgEntry.get()
                json = {"$class": "org.example.firstnetwork.AddEmployer",
                        "resume": "resource:org.example.firstnetwork.Resume#{}".format(self.person_id),
                        "employer": "resource:org.example.firstnetwork.Organization#{}".format(org_id)}
                response = requests.post(rest_server + 'AddEmployer', json=json)
                response = response.json()
                if 'error' in response:
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Add a new Employer")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            orgFrame = ttk.Frame(frame)
            orgFrame.pack(fill=tk.X, pady=5)
            orgLabel = ttk.Label(orgFrame, text='{0:15}\t:'.format('Organization ID'))
            orgLabel.pack(side=tk.LEFT, padx=5)
            orgEntry = ttk.Entry(orgFrame)
            orgEntry.pack(side=tk.LEFT)
            orgEntry.focus()

            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def person_update(self, resume_id=None, win=None):
        def proceed(resume_inner_id, win):
            json = {"$class": "org.example.firstnetwork.UpdateResume",
                    "approved": "resource:org.example.firstnetwork.approvedResume#{}".format(resume_inner_id)}
            response = requests.post(rest_server + 'UpdateResume', json=json)
            response = response.json()
            if 'error' in response:
                tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
            else:
                tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
            win.destroy()

        if resume_id is None:
            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Update Resume as Person")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            resumeFrame = ttk.Frame(frame)
            resumeFrame.pack(fill=tk.X, pady=5)
            resumeLabel = ttk.Label(resumeFrame, text='{0:15}\t:'.format('Resume ID'))
            resumeLabel.pack(side=tk.LEFT, padx=5)
            resumeEntry = ttk.Entry(resumeFrame)
            resumeEntry.pack(side=tk.LEFT)
            resumeEntry.focus()
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed(resumeEntry.get(),win))
            submit.pack(pady=5)
        else:
            proceed(resume_id, win)


    def person_add(self):
        def operation():
            def proceed():
                org_id = resumeEntry.get()
                data = dataEntry.get("1.0", tk.END)
                json = {
                    "$class": "org.example.firstnetwork.PersonAdd",
                    "owner": "org.example.firstnetwork.Person#{}".format(self.person_id),
                    "org": "org.example.firstnetwork.Organization#{}".format(org_id),
                    "resume": "org.example.firstnetwork.Resume#{}".format(self.person_id),
                    "addValue": {
                        "$class": "org.example.firstnetwork.ResumeValue",
                        "Value": data,
                        "org": "org.example.firstnetwork.Organization#{}".format(org_id),
                        "Approved": False,
                    },
                }
                response = requests.post(rest_server + 'PersonAdd', json=json)
                response = response.json()
                if 'error' in response:
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Add Resume Entry as Person")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            resumeFrame = ttk.Frame(frame)
            resumeFrame.pack(fill=tk.X, pady=5)
            resumeLabel = ttk.Label(resumeFrame, text='{0:15}\t:'.format('Organization ID'))
            resumeLabel.pack(side=tk.LEFT, padx=5)
            resumeEntry = ttk.Entry(resumeFrame)
            resumeEntry.pack(side=tk.LEFT)
            resumeEntry.focus()
            dataFrame = ttk.Frame(frame)
            dataFrame.pack(fill=tk.X, pady=5)
            dataLabel = ttk.Label(dataFrame, text='{0:15}\t:'.format('Resume Entry'))
            dataLabel.pack(side=tk.LEFT, padx=5)
            dataEntry = tk.Text(dataFrame)
            dataEntry.pack(side=tk.LEFT)
            dataEntry.insert(tk.INSERT,resume_format)
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def organization_approve(self, resume_id=None, win=None):
        def proceed(resume_id, win):
            json = {"$class": "org.example.firstnetwork.OrganizationApproved",
                    "request": "resource:org.example.firstnetwork.requestResume#{}".format(resume_id)}
            response = requests.post(rest_server + 'OrganizationApproved', json=json)
            response = response.json()
            if 'error' in response:
                tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
            else:
                tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
            win.destroy()

        if resume_id is None:
            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Approve Resume Entry as Organization")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            resumeFrame = ttk.Frame(frame)
            resumeFrame.pack(fill=tk.X, pady=5)
            resumeLabel = ttk.Label(resumeFrame, text='{0:15}\t:'.format('Resume ID'))
            resumeLabel.pack(side=tk.LEFT, padx=5)
            resumeEntry = ttk.Entry(resumeFrame)
            resumeEntry.pack(side=tk.LEFT)
            resumeEntry.focus()
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed(resumeEntry.get(),win))
            submit.pack(pady=5)
        else:
            proceed(resume_id,win)

    def organization_add(self):
        def operation():
            def proceed():
                person_id = resumeEntry.get()
                data = dataEntry.get("1.0", tk.END)
                json = {
                    "$class": "org.example.firstnetwork.OrganizationAdd",
                    "resume": "resource:org.example.firstnetwork.Resume#{}".format(person_id),
                    "addValue": {
                        "$class": "org.example.firstnetwork.ResumeValue",
                        "Value": data,
                        "org": "resource:org.example.firstnetwork.Organization#{}".format(self.organization_id),
                        "Approved": False,
                    }
                }

                response = requests.post(rest_server + 'OrganizationAdd', json=json)
                response = response.json()
                if 'error' in response:
                    tk.messagebox.showerror(response['error']['name'], response['error']['message'], parent=win)
                else:
                    tk.messagebox.showinfo('Success', 'Transaction Successful', parent=win)
                win.destroy()

            win = tk.Toplevel()
            win.resizable(width=False, height=False)
            win.wm_title("Add Resume Entry as Organization")
            frame = ttk.Frame(win, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            resumeFrame = ttk.Frame(frame)
            resumeFrame.pack(fill=tk.X, pady=5)
            resumeLabel = ttk.Label(resumeFrame, text='{0:15}\t:'.format('Person ID (IC)'))
            resumeLabel.pack(side=tk.LEFT, padx=5)
            resumeEntry = ttk.Entry(resumeFrame)
            resumeEntry.pack(side=tk.LEFT)
            resumeEntry.focus()
            dataFrame = ttk.Frame(frame)
            dataFrame.pack(fill=tk.X, pady=5)
            dataLabel = ttk.Label(dataFrame, text='{0:15}\t:'.format('Resume Entry'))
            dataLabel.pack(side=tk.LEFT, padx=5)
            dataEntry = tk.Text(dataFrame)
            dataEntry.pack(side=tk.LEFT)
            dataEntry.insert(tk.INSERT,resume_format)
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: proceed())
            submit.pack(pady=5)

        t = threading.Thread(target=operation())
        t.start()

    def update_access(self, type):
        self.access_type = type

    def set_id(self):
        self.wm_title("Set ID")
        if self.access_type == 'admin':
            frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            nameFrame = ttk.Frame(frame)
            nameFrame.pack(fill=tk.X, pady=5)
            nameLabel = ttk.Label(nameFrame, text='{0:15}\t:'.format('IC (Person)'))
            nameLabel.pack(side=tk.LEFT, padx=5)
            nameEntry = ttk.Entry(nameFrame)
            nameEntry.pack(side=tk.LEFT)
            orgFrame = ttk.Frame(frame)
            orgFrame.pack(fill=tk.X, pady=5)
            orgLabel = ttk.Label(orgFrame, text='{0:15}\t:'.format('Organization ID'))
            orgLabel.pack(side=tk.LEFT, padx=5)
            orgEntry = ttk.Entry(orgFrame)
            orgEntry.pack(side=tk.LEFT)
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: self.create_menu(person_id=nameEntry.get(),
                                                                    org_id=orgEntry.get()) or frame.destroy())
            submit.pack(pady=5)
            nameEntry.focus()
        elif self.access_type == 'person':
            frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)
            nameFrame = ttk.Frame(frame)
            nameFrame.pack(fill=tk.X, pady=5)
            nameLabel = ttk.Label(nameFrame, text='{0:15}\t:'.format('IC (Person)'))
            nameLabel.pack(side=tk.LEFT, padx=5)
            nameEntry = ttk.Entry(nameFrame)
            nameEntry.pack(side=tk.LEFT)

            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: self.create_menu(person_id=nameEntry.get()) or frame.destroy())
            submit.pack(pady=5)
            nameEntry.focus()
        else:
            frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
            frame.pack(fill=tk.X, padx=5, pady=5)

            orgFrame = ttk.Frame(frame)
            orgFrame.pack(fill=tk.X, pady=5)
            orgLabel = ttk.Label(orgFrame, text='{0:15}\t:'.format('Organization ID'))
            orgLabel.pack(side=tk.LEFT, padx=5)
            orgEntry = ttk.Entry(orgFrame)
            orgEntry.pack(side=tk.LEFT)
            submit = tk.ttk.Button(frame, text='Submit', width=10,
                                   command=lambda: self.create_menu(org_id=orgEntry.get()) or frame.destroy())
            submit.pack(pady=5)
            orgEntry.focus()

    def choose_access_type(self):
        self.wm_title("Choose Access Type")
        frame = ttk.Frame(self, border=2, relief=tk.GROOVE)
        frame.pack(fill=tk.X, padx=5, pady=5)
        admin = tk.ttk.Button(frame, text='Admin', width=20,
                              command=lambda: self.update_access('admin') or frame.destroy() or self.set_id())
        admin.pack(pady=5)
        person = tk.ttk.Button(frame, text='Person', width=20,
                               command=lambda: self.update_access('person') or frame.destroy() or self.set_id())
        person.pack(pady=5)
        org = tk.ttk.Button(frame, text='Organization', width=20,
                            command=lambda: self.update_access('org') or frame.destroy() or self.set_id())
        org.pack(pady=5)


class ResumeEntry(object):
    def __init__(self):
        self.id = None
        self.value = None

    def __repr__(self):
        return self.id +' '+ self.value


if __name__ == '__main__':
    app = GUI()
    app.mainloop()
