from tkinter import *
import random
from functools import partial
from string import ascii_uppercase
from pathlib import Path
import mysql.connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
ASSETS_PATH1 = OUTPUT_PATH / Path("./assets2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def relative_to_assets1(path: str) -> Path:
    return ASSETS_PATH1 / Path(path)


cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Diti Dalal",
  database="hangman_db"
)

cursor = cnx.cursor()



# fruits = ''' Apple Watermelon Orange Pear Cherry Strawberry  Nectarine Grape Mango Blueberry Pomegranate Plum Banana Raspberry Mandarin Jackfruit Papaya Kiwi Pineapple Lime Lemon Apricot Grapefruit Melon Coconut Avocado Peach tomato'''
# vegetables = ''' Corn Mushroom Cucumber Broccoli Carrot Pumpkin Cabbage Potato Eggplant Turnip zucchini chilli Onion Lettuce Radish Pea Asparagus Celery pepper Spinach '''
# sports = ''' Archery Badminton Cricket Bowling Boxing Curling Tennis Skateboarding Surfing Hockey Figure skating Yoga Fencing Gymnastics Karate Volleyball Weightlifting Basketball Baseball Rugby Wrestling Cycling Running Fishing Judo Climbing Billiards Shooting Golf Football Soccer '''

def new():
    window2.destroy()
    start()

def check(letter, index):
    global blank, char, label3, var2, word, window2, wrong_count, sketch, buttons, highscore,score,curr_user_name
    #print(letter,index)
    if wrong_count < 7 and "_" in blank:
        n = 0
        temp = blank.copy()
        for i in word:
            n = n + 1
            string = ""
            if letter == i:
                blank[n - 1] = letter
                for j in blank:
                    string = string + j + " "
                char = string
        if temp == blank:
            wrong_count = wrong_count + 1

        label3.grid_forget()
        var2 = StringVar()
        var2.set(char)
        #label3 = Label(window2, text=var2.get(), font=22,fg='white',bg="#000000")
        label3 = Label(window2, text=var2.get(), font=22,fg='white',bg="#000000", width=50)
        label3.place(x=360, y=329)

        # Disable the button by index
        buttons[index-1].config(state="disabled")

    #Creating hanging man with each wrong input
    print(wrong_count)
    if wrong_count == 1:
        # hangman()
        # image_head = PhotoImage(
        # file=relative_to_assets("oval.png"))
        # image_h = sketch.create_image(
        # 494.0,
        # 120.0,
        # image=image_head)
        sketch.create_oval(80, 10, 140, 65, width=2, outline='#ffffff')
    if wrong_count == 2:
        #hangman()
        sketch.create_line(110, 61, 110, 124, width=2, fill='white')
    if wrong_count == 3:
        sketch.create_line(110, 64, 84, 98, width=2, fill='white')
    if wrong_count == 4:
        sketch.create_line(110, 64, 134, 98, width=2, fill='white')
    if wrong_count == 5:
        sketch.create_line(110, 124, 92, 164, width=2, fill='white')
    if wrong_count == 6:
        sketch.create_line(110, 124, 129, 164, width=2, fill='white')
    if wrong_count == 7:
        sketch.create_line(107, -2, 107, 14, width=2, fill='white')
        sketch.create_line(102, 33, 107, 38, width=2,fill='white')
        sketch.create_line(102, 38, 107, 33, width=2, fill='white')
        sketch.create_line(119, 33, 124, 38, width=2, fill='white')
        sketch.create_line(119, 38, 124, 33, width=2, fill='white')
        sketch.create_line(109, 48, 118, 48, width=2, fill='white')

    if "_" in blank and wrong_count == 7:
        sketch.create_text(180, 150, text="Sorry, you're out of chances :(", font=20, fill="#FFAF36")
        score -= 5

    if "_" in blank:
        pass
    else:
        sketch.create_text(180, 150, text="Congratulations! YOU WON! :)", font=20, fill="#FFAF36")
        score += 10
        if highscore < score:
            highscore = score

            query = ("Update user_data set highscore=%s where username=%s")

            cursor.execute(query, (highscore, curr_user_name))
            cnx.commit()

    scr = str(score)
    if score < 10:
        scr = "0" + str(score)

    label_score = Label(window2, text=scr, font=("bold",20), bg="Black", fg="White")
    label_score.place(x=900,y=15)

    label_hscore = Label(window2, text=str(highscore), font=("bold",20), bg="Black", fg="White")
    label_hscore.place(x=900,y=47)
    
    #label5=Label(window2, text=f"Score={score}", font=18).place(x=50, y=70)
    #label6=Label(window2, text=f"HighScore: {highscores[n]}")


def generate_word(n):
    global wrong_count, blank, word, char, score

    category = ['fruits', 'vegetables', 'sports']
    diff_lvl = ['easy', 'medium', 'hard']

    query = ("SELECT word FROM words "
            "WHERE category=%s and Difficulty_Level=%s order by rand() limit 1")

    print("generate word", score)
    if(score < 30):
        m = 0
    elif(score < 60):
        m = 1
    else:
        m = 2

    cursor.execute(query, (category[n-1], diff_lvl[m]))

    for x in cursor: 
        word = x[0]
    
    # category = {1: fruits.split(), 2: vegetables.split(), 3: sports.split()}
    # word = random.choice(category[n])
    word = word.upper()
    print(word)
    char = list(word)

    wrong_count = 0
    char = ""
    blank = []
    for i in word:
        char = char + " _"
        blank = blank + ["_"]
    var2 = StringVar()
    var2.set(char)
    print(blank)
    return blank


def new_word(n):
    global label3, sketch, wrong_count, buttons

    #Generate new word
    label3=label3.destroy()
    #label3 = Label(window2, text=generate_word(n), font=22, fg='white',bg="#000000")
    label3 = Label(window2, text=generate_word(n), font=22, fg='white',bg="#000000", width=50)
    label3.place(x=360, y=329)

    #Reset hangman canvas
    sketch.delete('all')
    hangman()

    #Reset Wrong Counter
    wrong_count=0

    #Enabling all disabled alphabet buttons
    for button in buttons:
        button.config(state="normal")

def hangman():
    global sketch
    # sketch = Canvas(window2, width=201, height=188,bg="#000000", highlightbackground='#000000')
    sketch = Canvas(window2, width=601, height=188,bg="#000000", highlightbackground='#000000')
    sketch.place(x=420, y=110)
    # sketch.place(x=120, y=110)
    # sketch = Canvas(window2, width=400, height=400)
    # sketch.place(x=100, y=50)
    # sketch.create_line(30, 350, 200, 350, width=4)
    # sketch.create_line(50, 50, 50, 350, width=4)
    # sketch.create_line(30, 50, 350, 50, width=4)
    # sketch.create_line(50, 100, 125, 50, width=4)

def submit(n, name):
    global fruits, vegetables, sports, label3, char, word, blank, window2, wrong_count, sketch, label3, letters, buttons, highscore, score, curr_user_name
    #retrieving scores
    # highscores={1:0, 2:0, 3:0}

    curr_user_name = name

    cursor.execute("Select * from user_data")
    temp=[]
    temp_hs=[]
    for x in cursor:
        temp.append(x[0])
        temp_hs.append(x[1])

    print(temp)
    print(temp_hs)

    for i in range(len(temp)):
        if name == temp[i]:
            highscore = temp_hs[i]
            print("FDGBD")

    if name not in temp:
        add_user_data_query = (
            "INSERT INTO user_data "
            "VALUES (%s, %s)")

        cursor.execute(add_user_data_query, (name, 0))

        cnx.commit()



    window.destroy()
    window2 = Tk()
                                                                
                             
    window2.title("Hangman Game")
    window2.geometry("1000x600")
    window2.configure(bg = "#000000")
    canvas = Canvas(
    window2,
    bg = "#000000",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    #label3 = Label(window2, text=generate_word(n), font=22, fg='white',bg="#000000")
    label3 = Label(window2, text=generate_word(n), font=22, fg='white',bg="#000000",width=50)
    label3.place(x=360, y=329)
    
    hangman()
    #Defining alphabet buttons and placing them
    letter = StringVar()
    buttons=[]

    label_score = Label(window2, text=str(score), font=("bold",20), bg="Black", fg="White")
    label_score.place(x=900,y=15)

    label_hscore = Label(window2, text=str(highscore), font=("bold",20), bg="Black", fg="White")
    label_hscore.place(x=900,y=47)

    
    button_image_1 = PhotoImage(
    file=relative_to_assets1("button_1.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("Q", 1),
    relief="flat"
    )
    button_1.place(
    x=201.0,
    y=365.0,
    width=49.759674072265625,
    height=41.801727294921875
    )
    buttons.append(button_1)

    button_image_2 = PhotoImage(
    file=relative_to_assets1("button_2.png"))
    button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("W", 2),
    relief="flat"
    )
    button_2.place(
    x=225.2838134765625,
    y=420.09918212890625,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_2)

    button_image_3 = PhotoImage(
    file=relative_to_assets1("button_3.png"))
    button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("E", 3),
    relief="flat"
    )
    button_3.place(
    x=249.56756591796875,
    y=475.1982727050781,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_3)

    button_image_4 = PhotoImage(
    file=relative_to_assets1("button_4.png"))
    button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("R", 4),
    relief="flat"
    )
    button_4.place(
    x=264.1378173828125,
    y=365.0,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_4)

    button_image_5 = PhotoImage(
    file=relative_to_assets1("button_5.png"))
    button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("T", 5),
    relief="flat"
    )
    button_5.place(
    x=288.4216003417969,
    y=420.09918212890625,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_5)

    button_image_6 = PhotoImage(
    file=relative_to_assets1("button_6.png"))
    button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("Y", 6),
    relief="flat"
    )
    button_6.place(
    x=312.70538330078125,
    y=475.1982727050781,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_6)

    button_image_7 = PhotoImage(
    file=relative_to_assets1("button_7.png"))
    button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("U", 7),
    relief="flat"
    )
    button_7.place(
    x=327.2756042480469,
    y=365.0,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_7)

    button_image_8 = PhotoImage(
    file=relative_to_assets1("button_8.png"))
    button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("I", 8),
    relief="flat"
    )
    button_8.place(
    x=351.5594482421875,
    y=420.09918212890625,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_8)

    button_image_9 = PhotoImage(
    file=relative_to_assets1("button_9.png"))
    button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("O", 9),
    relief="flat"
    )
    button_9.place(
    x=375.8432312011719,
    y=475.1982727050781,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_9)

    button_image_10 = PhotoImage(
    file=relative_to_assets1("button_10.png"))
    button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("P", 10),
    relief="flat"
    )
    button_10.place(
    x=390.4134216308594,
    y=365.0,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_10)

    button_image_11 = PhotoImage(
    file=relative_to_assets1("button_11.png"))
    button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("A", 11),
    relief="flat"
    )
    button_11.place(
    x=414.6972351074219,
    y=420.09918212890625,
    width=49.75966262817383,
    height=41.801727294921875
    )
    buttons.append(button_11)

    button_image_12 = PhotoImage(
    file=relative_to_assets1("button_12.png"))
    button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("S", 12),
    relief="flat"
    )
    button_12.place(
    x=438.9809875488281,
    y=475.1982727050781,
    width=49.75966262817383,
    height=41.801727294921875
    )
    buttons.append(button_12)

    button_image_13 = PhotoImage(
    file=relative_to_assets1("button_13.png"))
    button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("D", 13),
    relief="flat"
    )
    button_13.place(
    x=453.55126953125,
    y=365.0,
    width=49.75966262817383,
    height=41.801727294921875
    )
    buttons.append(button_13)

    button_image_14 = PhotoImage(
    file=relative_to_assets1("button_14.png"))
    button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("F", 14),
    relief="flat"
    )
    button_14.place(
    x=477.8350830078125,
    y=420.09918212890625,
    width=49.75966262817383,
    height=41.801727294921875
    )
    buttons.append(button_14)

    button_image_15 = PhotoImage(
    file=relative_to_assets1("button_15.png"))
    button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("G", 15),
    relief="flat"
    )
    button_15.place(
    x=502.11883544921875,
    y=475.1982727050781,
    width=49.75966262817383,
    height=41.801727294921875
    )
    buttons.append(button_15)

    button_image_16 = PhotoImage(
    file=relative_to_assets1("button_16.png"))
    button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("H", 16),
    relief="flat"
    )
    button_16.place(
    x=516.6890869140625,
    y=365.0,
    width=49.75966262817383,
    height=41.801727294921875
    )
    buttons.append(button_16)

    button_image_17 = PhotoImage(
    file=relative_to_assets1("button_17.png"))
    button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("J", 17),
    relief="flat"
    )
    button_17.place(
    x=540.972900390625,
    y=420.09918212890625,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_17)

    button_image_18 = PhotoImage(
    file=relative_to_assets1("button_18.png"))
    button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("K", 18),
    relief="flat"
    )
    button_18.place(
    x=565.2566528320312,
    y=475.1982727050781,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_18)

    button_image_19 = PhotoImage(
    file=relative_to_assets1("button_19.png"))
    button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("L", 19),
    relief="flat"
    )
    button_19.place(
    x=579.8268432617188,
    y=365.0,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_19)

    button_image_20 = PhotoImage(
    file=relative_to_assets1("button_20.png"))
    button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("Z", 20),
    relief="flat"
    )
    button_20.place(
    x=604.1106567382812,
    y=420.09918212890625,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_20)

    button_image_21 = PhotoImage(
    file=relative_to_assets1("button_21.png"))
    button_21 = Button(
    image=button_image_21,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("X", 21),
    relief="flat"
    )
    button_21.place(
    x=628.3944702148438,
    y=475.1982727050781,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_21)

    button_image_22 = PhotoImage(
    file=relative_to_assets1("button_22.png"))
    button_22 = Button(
    image=button_image_22,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("C", 22),
    relief="flat"
    )
    button_22.place(
    x=642.9647827148438,
    y=365.0,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_22)

    button_image_23 = PhotoImage(
    file=relative_to_assets1("button_23.png"))
    button_23 = Button(
    image=button_image_23,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("V", 23),
    relief="flat"
    )
    button_23.place(
    x=667.24853515625,
    y=420.09918212890625,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_23)

    button_image_24 = PhotoImage(
    file=relative_to_assets1("button_24.png"))
    button_24 = Button(
    image=button_image_24,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("B", 24),
    relief="flat"
    )
    button_24.place(
    x=706.1025390625,
    y=365.0,
    width=49.75965881347656,
    height=41.801727294921875
    )
    buttons.append(button_24)

    button_image_25 = PhotoImage(
    file=relative_to_assets1("button_25.png"))
    button_25 = Button(
    image=button_image_25,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("N", 25),
    relief="flat"
    )
    button_25.place(
    x=730.3863525390625,
    y=420.09918212890625,
    width=49.759674072265625,
    height=41.801727294921875
    )
    buttons.append(button_25)

    button_image_26 = PhotoImage(
    file=relative_to_assets1("button_26.png"))
    button_26 = Button(
    image=button_image_26,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check("M", 26),
    relief="flat"
    )
    button_26.place(
    x=769.2403564453125,
    y=365.0,
    width=49.759674072265625,
    height=41.801727294921875
    )
    buttons.append(button_26)

    image_image_1 = PhotoImage(
    file=relative_to_assets1("image_1.png"))
    image_1 = canvas.create_image(
    498.0,
    74.0,
    image=image_image_1
    )
    
    
    categories={1:'Fruits', 2:'Vegetables', 3:'Sports'}

    canvas.create_text(
    498.0,
    74.0,
    #anchor="nw",
    text=f"{categories[n]}",
    fill="#000000",
    font=("Belleza Regular", 24 * -1)
    )

    button_image_27 = PhotoImage(
    file=relative_to_assets1("button_27.png"))
    button_27 = Button(
    image=button_image_27,
    borderwidth=0,
    highlightthickness=0,
    command=partial(new_word, n),
    relief="flat"
    )
    button_27.place(
    x=389.0,
    y=536.0,
    width=115.04081726074219,
    height=41.0
    )

    button_image_28 = PhotoImage(
    file=relative_to_assets1("button_28.png"))
    button_28 = Button(
    image=button_image_28,
    borderwidth=0,
    highlightthickness=0,
    command=new,
    relief="flat"
    )
    button_28.place(
    x=519.0748291015625,
    y=536.0,
    width=114.96598815917969,
    height=41.0
    )

    image_image_2 = PhotoImage(
    file=relative_to_assets1("image_2.png"))
    image_2 = canvas.create_image(
    442.0,
    30.0,
    image=image_image_2
    )

    canvas.create_text(
    503.0,
    13.0,
    anchor="nw",
    text=name+"!",
    fill="#FFFFFF",
    font=("Belleza Regular", 28 * -1)
    )

    image_image_3 = PhotoImage(
    file=relative_to_assets1("image_3.png"))
    image_3 = canvas.create_image(
    824.0,
    35.0,
    image=image_image_3
    )

    image_image_4 = PhotoImage(
    file=relative_to_assets1("image_4.png"))
    image_4 = canvas.create_image(
    824.0,
    67.0,
    image=image_image_4
    )

    image_image_5 = PhotoImage(
    file=relative_to_assets1("image_5.png"))
    image_5 = canvas.create_image(
    484.0,
    204.0,
    image=image_image_5
    )
    #window.resizable(False, False)
    window.mainloop()

def start():
    global window
    window = Tk()
    window.title("Hangman Game")
    window.geometry("1000x600")
    window.configure(bg = "#000000")


    global score,highscore
    score = 0
    highscore = 0



    canvas = Canvas(
    window,
    bg = "#000000",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
    0.0,
    0.0,
    450.0,
    600.0,
    fill="#6C3706",
    outline="")

    image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
    721.0,
    77.0,
    image=image_image_1
    )

    entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
    716.0,
    218.5,
    image=entry_image_1
    )
    name_entry = Entry(
    bd=0,
    bg="#C4C4C4",
    highlightthickness=0
    )
    name_entry.place(
    x=600.0,
    y=196.0,
    width=232.0,
    height=43.0
    )
    n = IntVar()
    n.set(1)
    button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: submit(1, name_entry.get()),
    relief="flat"
    )
    button_1.place(
    x=589.0,
    y=311.0,
    width=272.0,
    height=45.0
    )

    button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
    button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: submit(2, name_entry.get()),
    relief="flat"
    )
    button_2.place(
    x=589.0,
    y=373.0,
    width=272.0,
    height=45.0
    )

    button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
    button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: submit(3, name_entry.get()),
    relief="flat"
    )
    button_3.place(
    x=589.0,
    y=435.0,
    width=272.0,
    height=45.0
    )

    image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
    716.0,
    170.0,
    image=image_image_2
    )

    image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
    722.0,
    283.0,
    image=image_image_3
    )

    image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
    225.0,
    300.0,
    image=image_image_4
    )

    # button_image_4 = PhotoImage(
    # file=relative_to_assets("button_4.png"))
    # button_4 = Button(
    # image=button_image_4,
    # borderwidth=0,
    # highlightthickness=0,
    # command=lambda: print("button_4 clicked"),
    # relief="flat"
    # )
    # button_4.place(
    # x=587.0,
    # y=496.0,
    # width=282.0,
    # height=45.0
    # )
    #window.resizable(False, False)
    window.mainloop()

    
    cursor.close()
    cnx.close()
    

start()
