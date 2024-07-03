import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = ["2015","2016","2018","2019"]
        self._listCountry = []
        self._listCountry.extend(self._model.allCountry())
        self._year=None
        self._country=None


    def fillDD(self):
        myOptDDYear = list(map(lambda x: ft.dropdown.Option(x), self._listYear))
        self._view.ddyear.options=myOptDDYear
        myOptDDCountry = list(map(lambda x: ft.dropdown.Option(x), self._listCountry))
        self._view.ddcountry.options=myOptDDCountry



    def handle_graph(self, e):
        self._view.txtOut2.controls.clear()
        self._view.txt_result.controls.clear()
        self._view.txtOut3.controls.clear()
        nN,nA=self._model.creaGrafo(self._country,self._year)
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi; {nN} Numero di archi: {nA}"))
        self._view.update_page()





    def handle_volume(self, e):
        lista=self._model.calcolaVolumi()
        for l in lista[:6]:
            self._view.txt_result.controls.append(ft.Text(f"{l[0]} --> {l[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        try:
            n=int(self._view.txtN.value)
        except ValueError:
            print("inserisci un numero")
        path,peso = self._model.cercaPercorso(n)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {peso}"))
        for i in path:
            self._view.txtOut3.controls.append(ft.Text(f"{i[0]} --> {i[1]}: {i[2]}"))
        self._view.update_page()


    def readYear(self,e):
        self._year=self._view.ddyear.value
        print(self._year)

    def readCountry(self,e):
        self._country=self._view.ddcountry.value
        print(self._country)


