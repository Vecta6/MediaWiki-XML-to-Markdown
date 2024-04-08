import os
import time
import datetime
from bs4 import BeautifulSoup
import customtkinter as ctk
import json
import requests
from PIL import Image
from io import BytesIO

app_version="B-V0.4"

if not os.path.exists(f"{os.getenv('APPDATA')}\\MW-XML_to_MD"):
    os.mkdir(f"{os.getenv('APPDATA')}\\MW-XML_to_MD")

app_datas_dir=f"{os.getenv('APPDATA')}\\MW-XML_to_MD"



def configs_updates(config: dict):
    with open(f"{app_datas_dir}\\config.json", "w") as config_file:
        json.dump(config, config_file, indent=3)




if not os.path.exists(f"{app_datas_dir}\\config.json"):
    with open(f"{app_datas_dir}\\config.json", "w") as config_file:
        default_config={
            "version": app_version,
            "remind_update": True
        }
        configs_updates(default_config)
        config_file.close()

configs=json.load(open(f"{app_datas_dir}\\config.json", "r"))
current_version=configs["version"]

new_version_ask=False

try:
    response = requests.get("https://api.github.com/repos/Vecta6/MediaWiki-XML-to-Markdown/releases/latest")
    github_version=response.json()["tag_name"]
    if github_version!=current_version:
        # webbrowser.open("https://github.com/Vecta6/MediaWiki-XML-to-Markdown/releases/latest")
        new_version_ask=True
except:
    pass


if app_version!=current_version:
    with open(f"{app_datas_dir}\\config.json", "w") as config_file:
        default_config={
            "version": app_version,
            "remind_update": True
        }
        configs_updates(default_config)
        config_file.close()

app=ctk.CTk()

file=None
output_path=None
new_file=None

balises=[
    "u",
    "ins",
    "s",
    "del",
    "code",
    "blockquote",
    "q",
    "pre",
    "div",
    "center",
    "Ecrit"
]

can_convert=0

def enable_conert():
    if can_convert>=2:
        convert_btn.configure(state="normal")

def ask_for_file():
    global file
    global can_convert
    file=ctk.filedialog.askopenfile(title="Open file", filetypes=[("XML file", "*.xml")])
    if file:
        file_pos.configure(text=file.name)
        can_convert+=1
        enable_conert()

def ask_output_directory():
    global output_path
    global can_convert
    output_path=ctk.filedialog.askdirectory(title="Output direcory")
    if output_path:
        output_path_label.configure(text=output_path)
        can_convert+=1
        enable_conert()


def convert():

    time_start=time.time()

    global file
    global output_path
    remove_balises=option_remove_balises.get()

    soup=None
    with open(file.name, "+r", encoding="utf-8") as file:
        soup=BeautifulSoup(file.read(), "xml")
        file.close()

    pages=soup.find_all("page")

    output_path_eatch_files=None
    for i in pages:
        soup2=BeautifulSoup(str(i), "xml")
        title=soup2.find("title").string
        text=soup2.find("text").string

        if title!="Accueil":
            categorie=text.split("[[Catégorie:")[1::]
            categories=[]
            for j in categorie:
                categories.append(j.split("]]")[0])
            
            text_output=""

            for n in categories:
                text_output=f"{text_output}#{n}\n"
            

            text=text.split("[[Catégorie:")[0]
            text_output=f"{text_output}{text}"

            if remove_balises:
                for balise in balises:
                    text_output=text_output.replace(f"<{balise}>", "")
                    text_output=text_output.replace(f"</{balise}>", "")

            

            def function_output():
                with open(f"{output_path_eatch_files}/{title}.md", "+w", encoding="utf-8") as output:
                    output.write(text_output)
                    output.close()

            output_path_eatch_files=output_path

            if option_new_folder.get():
                output_path_eatch_files=f"{output_path}/{option_new_folder_name.get()}"


            if os.path.exists(f"{output_path_eatch_files}"):
                function_output()
            else:
                os.mkdir(f"{output_path_eatch_files}")
                function_output()

    time_stop=time.time()

    delta_time=datetime.timedelta(seconds=round(time_stop-time_start, 3))
    time_delta.configure(text=delta_time)

# Parametre de l'application
# app.geometry("500x500")

try:
    from ctypes import windll

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

app.minsize(width=300, height=100)
app.title("MW-XML to MD")
app.grid_columnconfigure(0, weight=1)

if new_version_ask:
    new_version_label=ctk.CTkLabel(app, text="New version available", text_color="#FFC400")
    new_version_label.grid(row=0, column=0, padx=1, pady=1)

ask_file=ctk.CTkButton(app, text="File", command=ask_for_file)
ask_file.grid(row=1, column=0, padx=20, pady=20)

file_pos=ctk.CTkLabel(app, text="")
file_pos.grid(row=2, column=0, padx=20, pady=20)

output_path_ask=ctk.CTkButton(app, text="Output Directory", command=ask_output_directory)
output_path_ask.grid(row=3, column=0, padx=20, pady=20)

output_path_label=ctk.CTkLabel(app, text="")
output_path_label.grid(row=4, column=0, padx=20, pady=20)

options=ctk.CTkFrame(app)
options.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

option_remove_balises=ctk.CTkCheckBox(options, text="Remove tags")
option_remove_balises.grid(row=0, column=0, padx=20, pady=20)

def if_newfolder_checked():
    if option_new_folder.get():
        option_new_folder_name.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="ew")
    else:
        option_new_folder_name.grid_remove()

option_new_folder=ctk.CTkCheckBox(options, text="Create a new folder", command=if_newfolder_checked)
option_new_folder.select()
option_new_folder.grid(row=0, column=1, padx=20, pady=20)

option_new_folder_name=ctk.CTkEntry(options, placeholder_text="MW-XML_to_MD_output")
option_new_folder_name.insert(0, "MW-XML_to_MD_output")
if_newfolder_checked()

convert_btn=ctk.CTkButton(app, text="Convert", command=convert)
convert_btn.configure(state="disabled")
convert_btn.grid(row=6, column=0, padx=20, pady=20)

time_delta=ctk.CTkLabel(app, text="")
time_delta.grid(row=7, column=0, padx=20, pady=2)

app.mainloop()