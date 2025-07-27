from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import time
from tkinter import messagebox

single_article = ("The Importance of Good Typing Skills Typing is an essential skill in today's digital world. "
                  "Whether for work, school, or personal communication, the ability to type quickly and accurately "
                  "can boost productivity. A proficient typist can complete tasks efficiently, reducing errors and "
                  "saving time. With remote work and online learning on the rise, strong typing skills are more important "
                  "than ever. By practicing regularly and using proper techniques, individuals can enhance their typing "
                  "speed and accuracy, leading to improved workflow and better opportunities in the job market.")

root = Tk()
root.title('Typing Master')
root.config(height=500, width=1000)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
Label(root, text="Welcome To Typing Master:)",
      font=('calibre', 20, 'bold')).place(relx=0.475, anchor='center', rely=0.05)

data = pd.read_csv('typing_master_articles.csv').to_dict()

articles = {}
for n in range(10):
    articles[data['Title'][n]] = data['Content'][n]


class TypingMaster:
    def __init__(self):
        self.speed_label = None
        self.article = None
        self.entry_var = StringVar()
        # self.entry_var.trace_add("write", self.check_text)
        self.start_time = None
        self.text_var = StringVar()
        self.entry_text = None
        self.accuracy_label = None
        self.sample_text = None
        self.seconds = 5
        self.minutes = 1
        self.temp = int(self.minutes) * 60 + int(self.seconds)

    def label(self, option):
        # Create the label widget with all options
        self.article = articles[option]
        self.text_var.set(self.article)
        self.sample_text = f"{option}\n\n{self.article}"
        label = Label(root,
                      text=self.sample_text,
                      anchor='center',
                      bg="lightblue",
                      height=10,
                      width=60,
                      bd=3,
                      font=("Arial", 16, "bold"),
                      cursor="hand2",
                      fg="black",
                      padx=15,
                      pady=15,
                      justify='center',
                      relief='raised',
                      underline=0,
                      wraplength=800
                      )
        label.place(relx=0.5, rely=0.3, anchor='center')

        # Text entry
        self.entry_text = Text(root, height=8, width=65,
                               font=('Arial', 16, 'normal'),
                               padx=12, pady=12,
                               relief='raised',
                               wrap="word")
        self.entry_text.place(relx=0.5, rely=0.6, anchor='center')

        # Apply text highlighting for correct/incorrect text
        self.entry_text.tag_configure("correct", foreground="green")
        self.entry_text.tag_configure("incorrect", foreground="red")

        # Live tracking of accuracy
        self.entry_text.bind("<KeyRelease>", self.check_accuracy)

        # Accuracy label
        self.accuracy_label = Label(root, text="Accuracy: 100%", font=("Arial", 14))
        self.accuracy_label.place(relx=0.5, rely=0.8, anchor='center')

        # Speed label
        self.speed_label = Label(root, text="WPM: 00", font=("Arial", 14))
        self.speed_label.place(relx=0.5, rely=0.85, anchor='center')

        self.start_time = time.time()

    def check_accuracy(self, event):
        user_text = self.entry_text.get("1.0", "end-1c")  # Get user input
        correct_chars = 0

        for i in range(len(user_text)):
            if i < len(self.article) and user_text[i] == self.article[i]:
                self.entry_text.tag_add("correct", f"1.{i}")
                correct_chars += 1
            else:
                self.entry_text.tag_add("incorrect", f"1.{i}")

        # Calculate accuracy
        if len(user_text) > 0:
            accuracy = (correct_chars / len(user_text)) * 100
        else:
            accuracy = 100

        # Speed check
        self.check_speed()

        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")

    def check_speed(self):
        words_typed = len(self.entry_text.get("1.0", "end-1c").split())
        elapsed_time = time.time() - self.start_time
        wpm = int((words_typed / elapsed_time) * 60)  # Words per minute formula
        self.speed_label.config(text=f"WPM: {wpm}")

    def timer(self):
        minute_label = Label(root,
                             text=f"{self.minutes}",
                             anchor='center',
                             bg="seashell2",
                             height=1,
                             width=1,
                             bd=3,
                             font=("Arial", 16, "bold"),
                             cursor="hand2",
                             fg="black",
                             padx=15,
                             pady=10,
                             justify='center',
                             relief='raised')
        minute_label.place(relx=0.49, rely=0.1)

        second_label = Label(root,
                             text=f"{self.seconds}",
                             anchor='center',
                             bg="seashell2",
                             height=1,
                             width=1,
                             bd=3,
                             font=("Arial", 16, "bold"),
                             cursor="hand2",
                             fg="black",
                             padx=15,
                             pady=10,
                             justify='center',
                             relief='raised')
        second_label.place(relx=0.515, rely=0.1)

        if self.temp > -1:

            # div-mod (first value = temp//60, second value = temp%60)
            mins, secs = divmod(self.temp, 60)

            # using format () method to store the value up to
            # two decimal places
            minute_label.config(text="{0:2d}".format(mins))
            second_label.config(text="{0:2d}".format(secs))

            # updating the GUI window after decrementing the
            # temp value every time
            root.after(1000, self.timer)

            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            if self.temp == 0:
                messagebox.showinfo("Time Countdown", "Time's up ")

            # after every one sec the value of temp will be decremented by one
            self.temp -= 1


master = TypingMaster()


def drop_down(option):
    logo_label.destroy()
    dropdown.place_forget()
    print(option)
    master.label(option)
    master.timer()


actions = [title for title in data['Title'].values()]
# Create dropdown menu
selected_option = StringVar()
selected_option.set('Choose an action!')  # Default selection

dropdown = OptionMenu(root, selected_option, *actions, command=drop_down)
dropdown.config(font=("Arial", 12, "bold"), bg="lightblue", fg="black", width=15)
dropdown.place(relx=0.5, rely=0.52, anchor='center')

# Quit root button
Button(text="Quit", command=root.destroy,
       font=('calibre', 16, 'normal')).place(relx=0.6, rely=0.05, anchor='center')

# Logo label
img = Image.open("keyboard.jpg")
max_size = (500, 500)
img.thumbnail(max_size)
logo_image = ImageTk.PhotoImage(img)
logo_label = Label(root, image=logo_image)
logo_label.place(relx=0.5, rely=0.3, anchor='center')

root.mainloop()
