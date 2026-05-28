import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
        n,e = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. Il grafo contiene {n} nodi e {e} archi")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        top3 = self._model.getTop3Archi()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Archi di peso maggiore: (tre migliori)")
        )
        for arco in top3:
            self._view.txt_result.controls.append(
                ft.Text(f"{arco[0]} --> {arco[1]} Peso: {arco[2]["weight"]}")
            )

        numero, largest, details = self._model.getConnessaInfo()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {numero} componenti connesse")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa maggiore ha dimensione {len(largest)}")
        )
        for l in largest:
            self._view.txt_result.controls.append(
                ft.Text(l)
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa in ordine decrescente di grado dei nodi")
        )
        for d in details:
            self._view.txt_result.controls.append(
                ft.Text(f"{d[0]} - grado: {d[1]}")
            )
        self._view.update_page()


    def handleCerca(self, e):
        k = self._view._txtInK.value
        #controlli validità
        kInt = int(k)

        listPilotiOttima, minDistEta = self._model.getListaPilotiOttima(k)
        if listPilotiOttima is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Non ho trovato una lista di {k} piloti ottima per il numero di componenti connesse che ho")
            )
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Lista di piloti con scarto di età minimo che non sono mai stati compagni di squadra nel range")
        )
        for p in listPilotiOttima:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.txt_result.controls.append(
            ft.Text(f"La differenza di età tra pilota più giovane e più anziano: {minDistEta}")
        )
        youngest = min(listPilotiOttima,key=lambda x:x.dob)
        oldest = max(listPilotiOttima, key=lambda x: x.dob)
        self._view.txt_result.controls.append(
            ft.Text(f"Pilota più giovane: {youngest} - Pilota più anziano: {oldest}")
        )

    def fillDDYear(self):
        years = self._model.getAllYears()
        for y in years:
             self._view._ddAnno1.options.append(ft.dropdown.Option(y))
             self._view._ddAnno2.options.append(ft.dropdown.Option(y))
        self._view.update_page()