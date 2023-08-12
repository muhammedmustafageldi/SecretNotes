import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import base64
from tkinter import filedialog

root = Tk()


def windowSettings():
    root.title(string='Secrets Note')
    root.iconbitmap('app_icon.ico')
    root.config(pady=20, padx=10)


def save_and_encrypt(title_entry, note_text, key_entry):
    title = title_entry.get()
    note = note_text.get('1.0', END)
    password = key_entry.get()

    if len(title) == 0 or len(note) == 0 or len(password) == 0:
        messagebox.showwarning(title='Warning', message='Please enter all info.')
    else:
        encrypted_message = encode(key=password, message=note)
        file_name = 'secret.txt'

        selected_file_path = get_selected_folder_path()

        if selected_file_path is not None:
            file_path = selected_file_path + '/' + file_name
            save_file(file_path=file_path, title=title, encrypted_message=encrypted_message)
        else:
            if os.name == "nt":  # Windows
                desktop_location = os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(desktop_location, file_name)
                save_file(file_path=file_path, title=title, encrypted_message=encrypted_message)

            elif os.name == "posix":  # other (Linux, Unix etc.)
                desktop_location = os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(desktop_location, file_name)
                save_file(file_path=file_path, title=title, encrypted_message=encrypted_message)

            else:
                messagebox.showerror(title='Error',
                                     message='Sorry, your operating system does not support the operation of this program.')

        # Clear the widgets
        title_entry.delete(0, END)
        note_text.delete('1.0', END)
        key_entry.delete(0, END)


def decrypt_and_read(read_code_entry, read_password_entry, read_result_label):
    code = read_code_entry.get()
    password = read_password_entry.get()

    if len(code) == 0 or len(password) == 0:
        messagebox.showwarning(title='Warning', message='Please enter all info.')
    else:
        decrypted_message = decode(password, code)
        read_result_label.config(text=f'Your note: {decrypted_message}')
        read_result_label.pack(padx=10, pady=10)
        # Clear widgets
        read_code_entry.delete(0, END)
        read_password_entry.delete(0, END)
        read_code_entry.focus()


def save_file(file_path, title, encrypted_message):
    try:
        with open(file_path, 'a') as file:
            file.write(f'{title}\n{encrypted_message}\n')
    except FileNotFoundError:
        with open(file_path, 'w') as file:
            file.write(f'{title}\n{encrypted_message}\n')


def encode(key, message):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(message[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def select_folder_path(path_label):
    selected_file_path = filedialog.askdirectory()
    if selected_file_path:
        path_label.config(text=f' Selected Path:\n {selected_file_path}')
        with open('file_path.txt', 'w') as file_path:
            file_path.write(selected_file_path)
    else:
        print('File path could not be retrieved.')


def get_selected_folder_path():
    try:
        with open('file_path.txt', 'r') as file_path:
            return file_path.read()
    except FileNotFoundError:
        return None


def initWidgets():
    # Create the application logo
    image = Image.open('app_icon.png')
    resized_image = image.resize((150, 150), Image.LANCZOS)
    appIcon = ImageTk.PhotoImage(resized_image)

    icon_label = Label(root, image=appIcon)
    icon_label.image = appIcon
    icon_label.pack(padx=20, pady=5)

    # Define font of application
    APPLICATION_FONT = ('Courier New', 15, 'bold')

    # Define other widgets
    image_folder = Image.open('folder.png')
    image_folder = image_folder.resize((24, 24), Image.LANCZOS)
    folder_icon = ImageTk.PhotoImage(image_folder)

    selected_save_path = get_selected_folder_path()

    if selected_save_path is None:
        save_path = ' Default Path:\n Desktop'
    else:
        save_path = f' Selected Path:\n {selected_save_path}'

    path_label = Label(text=save_path, font=('Courier New', 10, 'bold'), image=folder_icon,
                       compound=TOP)
    path_label.image = folder_icon
    path_label.pack(padx=10)

    change_path_button = Button(text='Change', relief=SOLID, borderwidth=1, font=('Courier New', 10, 'bold'),
                                command=lambda: select_folder_path(path_label))
    change_path_button.pack(pady=10)

    divider = Canvas(root, height=1, bg="black")
    divider.pack(fill="x")

    radio_frame = Frame(root)
    radio_frame.pack(padx=10, pady=10)

    # Define widgets of the save frame ->

    save_frame = Frame(root)
    save_frame.pack()

    title_label = Label(master=save_frame, text='Enter your title', font=APPLICATION_FONT)
    title_label.pack(padx=10, pady=10)

    title_entry = Entry(master=save_frame, width=40, relief=SOLID, borderwidth=2)
    title_entry.pack()

    note_label = Label(master=save_frame, text='Enter your note', font=APPLICATION_FONT)
    note_label.pack(padx=10, pady=10)

    note_text = Text(master=save_frame, width=40, height=10, relief=SOLID, borderwidth=2)
    note_text.pack()

    key_label = Label(master=save_frame, text='PASSWORD', font=APPLICATION_FONT)
    key_label.pack(padx=10, pady=10)

    key_entry = Entry(master=save_frame, width=40, show='*', relief=SOLID, borderwidth=2)
    key_entry.pack()

    img_encrypted = Image.open('encrypted.png')
    img_encrypted = img_encrypted.resize((32, 32), Image.LANCZOS)
    icon_encrypted = ImageTk.PhotoImage(img_encrypted)

    save_button = Button(master=save_frame, text=' Save & Encrypt ', font=APPLICATION_FONT,
                         compound=RIGHT, image=icon_encrypted,
                         relief=SOLID, command=lambda: save_and_encrypt(title_entry, note_text, key_entry))
    save_button.image = icon_encrypted
    save_button.pack(padx=15, pady=25)

    # Define widgets of the read frame ->

    read_frame = Frame(root)

    read_label = Label(master=read_frame, text='Enter your text code', font=APPLICATION_FONT)
    read_label.pack(padx=10)

    read_code_entry = Entry(master=read_frame, borderwidth=2, width=45, relief=SOLID)
    read_code_entry.pack(padx=10, pady=10)

    read_password_label = Label(master=read_frame, text='PASSWORD', font=APPLICATION_FONT)
    read_password_label.pack()

    read_password_entry = Entry(master=read_frame, borderwidth=2, width=35, relief=SOLID, show='*')
    read_password_entry.pack(padx=10, pady=10)

    read_result_label = Label(master=read_frame, font=APPLICATION_FONT)

    img_decrypt = Image.open('decrypt.png')
    img_decrypt = img_decrypt.resize((32, 32), Image.LANCZOS)
    icon_decrypt = ImageTk.PhotoImage(img_decrypt)

    decrypt_button = Button(master=read_frame, text=' Decrypt ', font=APPLICATION_FONT,
                            compound=RIGHT, image=icon_decrypt,
                            relief=SOLID, command=lambda: decrypt_and_read(read_code_entry, read_password_entry, read_result_label))
    decrypt_button.image = icon_decrypt
    decrypt_button.pack(padx=10, pady=10)

    # Save or Read mode radio buttons ->
    def radio_selected():
        if check_state_radio.get() == 10:
            read_frame.pack_forget()
            save_frame.pack()
        else:
            save_frame.pack_forget()
            read_frame.pack()

    check_state_radio = IntVar(value=10)

    save_radio_button = Radiobutton(master=radio_frame, text='Save note', value=10, variable=check_state_radio,
                                    font=('Courier New', 10, 'bold'), command=radio_selected)
    save_radio_button.pack(side='left', padx=10, pady=10)

    read_radio_button = Radiobutton(master=radio_frame, text='Read note', value=20, variable=check_state_radio,
                                    font=('Courier New', 10, 'bold'), command=radio_selected)
    read_radio_button.pack(side='left', padx=10, pady=10)


initWidgets()
windowSettings()

root.mainloop()
