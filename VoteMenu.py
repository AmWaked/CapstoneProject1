import tkinter
import csv
from typing import Dict, List


class VoteMenu(tkinter.Tk):
    """

    Main window, where user starts

    """

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('Vote Menu')
        self.geometry('250x250')
        self.resizable(False, False)

        container = tkinter.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # type: Dict[str, tkinter.Frame]
        self.john_count = 0  # type: int
        self.jane_count = 0  # type: int
        self.votes = []  # type: List[tuple]
        self.current_voter = None  # type: int
        self.used_ids = self.check_voter_ids()  # type: List[int]
        for F in (YNMenu, IDPage, CandidateMenu, ResultsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('YNMenu')
        banner_frame2 = tkinter.Frame(self, bg='red', height=20)
        banner_frame2.pack(side='bottom', fill='x')
        banner_frame2 = tkinter.Frame(self, bg='white', height=20)
        banner_frame2.pack(side='bottom', fill='x')
        banner_frame2 = tkinter.Frame(self, bg='red', height=20)
        banner_frame2.pack(side='bottom', fill='x')
        banner_frame2 = tkinter.Frame(self, bg='white', height=20)
        banner_frame2.pack(side='bottom', fill='x')
        banner_frame2 = tkinter.Frame(self, bg='red', height=20)
        banner_frame2.pack(side='bottom', fill='x')
        banner_frame = tkinter.Frame(self, bg='blue', height=20)
        banner_frame.pack(side='bottom', fill='x')

        stars_label = tkinter.Label(banner_frame, text='★' * 12, fg='white', bg='blue', font=('Arial', 14))
        stars_label.pack(side='left')

    def show_frame(self, page_name) -> None:
        """
        shows frame specified in page_name

        """
        frame = self.frames[page_name]
        frame.tkraise()

    def check_voter_ids(self) -> list:
        """

        loads voter record csv, or creates if one doesn't exist

        """
        filename = 'vote_records.csv'
        ids = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ids.append(int(row['Voter ID']))
        except FileNotFoundError:
            with open(filename, mode='w', newline='') as csvfile:
                fieldnames = ['Voter ID', 'Candidate']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        return ids


class YNMenu(tkinter.Frame):
    """

    Frame to prompt user if they want to vote or end/see results


    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.yn_question = tkinter.Label(self, text='Would you like to vote?')
        self.yn_question.pack(side='top', fill='x', pady=10)

        self.yes_button = tkinter.Button(self, text='Yes',
                                         command=self.chose_yes)
        self.no_button = tkinter.Button(self, text='No, show results',
                                        command=self.chose_no)
        self.yes_button.pack()
        self.no_button.pack()

    def chose_yes(self) -> None:
        """

        logic for yes button, goes to IDPage

        """
        self.controller.show_frame('IDPage')

    def chose_no(self):
        """

        logic for no button, goes to ResultsPage

        """
        self.controller.show_frame('ResultsPage')


class IDPage(tkinter.Frame):
    """

    Frame for verifying and setting up to record voter ID

    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.used_ids = []
        self.voter_id_label = tkinter.Label(self, text='Input your Voter ID')
        self.voter_id_label.pack(side='top', fill='x', pady=10)
        self.input_name = tkinter.Entry(self, width=20)
        self.input_name.pack()
        self.submit_button = tkinter.Button(self, text='Submit', command=self.id_check)
        self.submit_button.pack()
        self.restart_button = tkinter.Button(self, text='Return', command=self.restart)
        self.restart_button.pack()

    def id_check(self) -> None:
        """

        checks validity of voter id and checks for duplicates

        """
        try:
            voter_id = int(self.input_name.get())
            if not 1 <= voter_id <= 9999:
                raise ValueError
            if voter_id in self.controller.used_ids:
                self.id_exceptions('YOU ALREADY VOTED')
            else:
                self.controller.current_voter = voter_id
                self.controller.used_ids.append(voter_id)
                self.controller.show_frame('CandidateMenu')
        except ValueError:
            self.id_exceptions('INVALID ID')

    def id_exceptions(self, message) -> None:
        """

        shows problem text for user

        """
        self.voter_id_label.config(text=message, fg='red', font=('16'))
        self.voter_id_label.pack(side='top', fill='x', pady=10)

    def restart(self) -> None:
        """

        returns user to start and resets IDPage

        """
        self.input_name.delete(0, 'end')
        self.controller.show_frame('YNMenu')


class CandidateMenu(tkinter.Frame):
    """

    Frame for candidate input

    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.candidate_name = tkinter.Label(self, text='Input the name of your candidate:')
        self.candidate_name.pack(side='top', fill='x', pady=10)
        self.input_name = tkinter.Entry(self, width=20)
        self.input_name.pack()
        self.submit_button = tkinter.Button(self, text='Submit',
                                            command=self.vote)
        self.submit_button.pack()
        self.return_button = tkinter.Button(self, text='Vote again or view results',
                                            command=self.reset)

        self.return_button.pack()

    def vote(self) -> None:
        """

        checks validity of candidate input and records vote

        """
        try:
            candidate = self.input_name.get().strip().lower()
            if candidate == 'john':
                self.controller.john_count += 1
                self.candidate_name.config(text='Voted John', fg='green')
                self.controller.votes.append((self.controller.current_voter, candidate))
            elif candidate == 'jane':
                self.controller.jane_count += 1
                self.candidate_name.config(text='Voted Jane', fg='green')
                self.controller.votes.append((self.controller.current_voter, candidate))
            else:
                raise ValueError
        except ValueError:
            self.candidate_name.config(text='Must be John or Jane', fg='red', font=(16))

    def reset(self) -> None:
        """

        resets CandidateMenu and returns user to YNMenu

        """
        self.return_button.pack_forget()
        self.input_name.delete(0, 'end')
        self.candidate_name.config(text='Input the name of your candidate:')
        self.submit_button.pack()
        self.return_button.pack()
        self.controller.show_frame('YNMenu')


class ResultsPage(tkinter.Frame):
    """

    Frame for displaying results and appending them to voter records csv

    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.results_text = f'This session: John - {self.controller.john_count}, Jane - {self.controller.jane_count}, Total - {self.controller.john_count + self.controller.jane_count}'
        self.results = tkinter.Label(self, text=self.results_text)
        self.results.pack(side='top', fill='x', pady=5)

        self.winner_label = tkinter.Label(self, text='')
        self.winner_label.pack(pady=2)

        self.record_button = tkinter.Button(self, text='Record', command=self.record)
        self.record_button.pack()

        self.close_button = tkinter.Button(self, text='Close', command=quit)
        self.close_button.pack()

    def record(self) -> None:
        """

        shows current session's score and records votes to voter records csv

        """
        self.results.config(
            text=f'This session: John - {self.controller.john_count}, Jane - {self.controller.jane_count}, Total - {self.controller.john_count + self.controller.jane_count}')

        if self.controller.john_count > self.controller.jane_count:
            self.winner_label.config(text='Winner is John!', fg='green')
        elif self.controller.jane_count > self.controller.john_count:
            self.winner_label.config(text='Winner is Jane!', fg='green')
        else:
            self.winner_label.config(text='Tie! Maybe try rock-paper-scissors?', fg='green')
        self.winner_label.pack()

        with open('vote_records.csv', 'a', newline='') as csvfile:
            fieldnames = ['Voter ID', 'Candidate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for vote in self.controller.votes:
                writer.writerow({'Voter ID': vote[0], 'Candidate': vote[1]})
