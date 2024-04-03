import os
try:
    from bs4 import BeautifulSoup
    import lxml
except:
    os.system("python -m pip install beautifulsoup4")
    os.system("python -m pip install lxml")
    from bs4 import BeautifulSoup
    import lxml


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

        def function_output():
            with open(f"output/{title}.md", "+w", encoding="utf-8") as output:
                output.write(text_output)

        if os.path.exists("output"):
            function_output()
        else:
            os.mkdir("output")
