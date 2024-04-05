# Importation des modules
# ------------
import os
import time
import datetime
from threading import Thread
# ------------

# Creation des variable
# ------------
suspect_exe=[]
suspect_dll=[]
threads=[]

injector_fingerprint=[]

folder_count=0
files_count=0

# ------------

# Stockage des Empreinte d'injection
# ------------
for i in os.scandir("./fingerprint"):
    if i.is_file():
        with open(i.path, encoding="ansi") as file:
            injector_fingerprint.append(file.readlines()[2])
            file.close()
# ------------



# Fonction d'analyse d'un fichier dll
# ------------
def if_is_dll(file_info):
    
    # Rendre global certaine variable
    # ------------
    global suspect_dll
    global injector_fingerprint
    # ------------
    
    
    file_info=file_info.split(";")                                                                  # Separer les differente information recuperer
    try:                                                                                            # Essayer d'ouvrir le fichier
        
        with open(file_info[0], encoding="ansi") as injector:                                       # Ouvrir le fichier
            if injector.readlines()[2] in injector_fingerprint:                                     # Comparer la ligne avec celle recupere
                suspect_dll.append([file_info[0], file_info[1]])                                    # Si suspect alors ajouter le fichier dll au fichier suspect
            injector.close()                                                                        # Fermer le fichier
            
    except:                                                                                         # Si echec alors avertir
        print(f"Impossible d'ouvrir le fichier {file_info[0]}")
# ------------




# Fonction des recherche
def if_is_dir(path="./"):

    # Rendre global certaine variable
    # ------------
    global threads
    global suspect_exe
    global suspect_dll
    global injector_fingerprint
    global folder_count
    global files_count
    # ------------

    try:                                                                                                # Essayer d'acceder au dossier
        for dir in os.scandir(path):                                                                    # Pour tout les element dans le dossier selectionner
            
            if dir.is_dir() and dir.name!="__os_finder":                                                # Si l'element est un dossier et si le dossier specifique n'est pas egale a celui du programme
                t=Thread(target=if_is_dir, args=[dir.path])#if_is_dir(path=dir.path)                    # Alors ça creer un nouveau Thread pour perdre moins de temps
                t.start()
                threads.append(t)                                                                       # Ajoute le Thread a la list 'threads'
                folder_count=+1
                
            elif dir.is_file():                                                                         # Sinon si c'est un fichier
                if dir.name in ["KrnlUI.exe", "JJS-UI.exe", "ScriptWare.exe", "krnlss.exe"]:            # Regarder si le nom du fichier corespond au nom suivant
                    suspect_exe.append([dir.name, dir.path])                                            # Si il en fait partie alors l'ajouter en temps que suspect
                    
                if dir.name.split(".")[-1]=="dll":                                                      # Et si c'est un fichier en '.dll' alors analyser son contenu
                    # with open(dir.path, encoding="ansi") as injector:
                    #     if injector.readlines()[2] in injector_fingerprint:
                    #         suspect_dll.append([dir.name, dir.path])
                    #     injector.close()
                    infos=f"{dir.path};{dir.name}"                                                      # Contenire les info du dossier dans une variable local
                    t_dll=Thread(target=if_is_dll, args=[infos], name=f"Thread for: {dir.name}")    # Lancer un Thread pour l'analyse du fichier car permet de gagner du temps et de par exemple continuer des analyse sur d'autre fichier
                    t_dll.start()
                    t_dll.join()
                    threads.append(t_dll)
                files_count=+1
    
    except:                                                                                             # Si l'acces au dossier est impossible alors avertir
        print(f"Impossible d'accéder au dossier {path}")
    

# print("Voulez-vous faire une verification d'injecteur?\n0. non\n1. oui\n\n")
# check=input("?")

# check=check.split(",")
# check_dll=False

# print(check)

# for i in check:
#     if i=="0":
#         check_dll=False
#     elif i=="1":
#         check_dll==True
#     else:
#         print("une erreur est survenu")


input("Appuyer sur entré pour commencer")

os.system("cls")
print("Les verification a commence, merci de bien vouloir patienter...")

thread1=Thread(target=if_is_dir, args=["C:\\"], name="Thread Disk C")                                   # Lancer l'analyse sur le disk C:
thread2=Thread(target=if_is_dir, args=["D:\\"], name="Thread Disk D")                                   # Lancer l'analyse sur le disk D:

thread1.start()
thread2.start()

time1=time.time()                                                                                       # Recuperer le temps du debut de l'analyse

thread1.join()                                                                                          # Attendre la fin de l'analyse du disk C:
thread2.join()                                                                                          # Attendre la fin de l'analyse du disk D:


for thread in threads:                                                                                  # Attendre la fin de tout les Thread si pas encore fini
    thread.join()

time2=time.time()                                                                                       # Recuperer le temps de la fin de l'analyse

os.system("cls")                                                                                        # Effacer ecran


# Afficher les fichier suspect
# ------------
print("\n < ----------------------------------------- > \n")

for exploit in suspect_exe:
    print(f"L'exploit {exploit[0]} a ete retrouve  |  {exploit[1]}")

print("\n < ----------------------------------------- > \n")

for injector in suspect_dll:
    print(f"L'injecteur {injector[0]} a ete retrouve | {injector[1]}")

print("\n < ----------------------------------------- > \n")
# -------------


print(f"Scan terminé en {datetime.timedelta(seconds=round(time2-time1, 3))}\n")


input("appuyer sur entré pour terminer")