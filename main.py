import os
try:
    from bs4 import BeautifulSoup
except:
    os.system("python -m pip install beautifulsoup4")
    from bs4 import BeautifulSoup


remove_balises=True

balises=[
    "u"
]

soup=None
with open("wiki_ac.xml", "+r", encoding="utf-8") as file:
    soup=BeautifulSoup(file.read(), "xml")

pages=soup.find_all("page")

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
            new_text=""
            new_text_wb=""
            for balise in balises:
                whithout_b=text_output.split(f"<{balise}>")
                for m in whithout_b:
                    new_text=f"{new_text}{m}"

                whithout_b=new_text.split(f"</{balise}>")
                for m in whithout_b:
                    new_text_wb=f"{new_text_wb}{m}"
                
                
            text_output=new_text_wb

        def function_output():
            with open(f"output/{title}.md", "+w", encoding="utf-8") as output:
                output.write(text_output)

        if os.path.exists("output"):
            function_output()
        else:
            os.mkdir("output")
