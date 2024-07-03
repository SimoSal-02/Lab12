import copy

import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._idMap={}
        self._bestPath=[]
        self.peso=0


    def allCountry(self):
        return DAO.getAllCountry()

    def creaGrafo(self,country,anno):
        self._grafo.clear()
        retailers=DAO.getAllRetailer(country)
        for r in retailers:
            self._idMap[r.Retailer_code]=r
        self._grafo.add_nodes_from(retailers)


        for r1 in self._grafo.nodes:
            for r2 in self._grafo.nodes:
                if r1.Retailer_code<r2.Retailer_code:
                    arco=DAO.getArchi(r1.Retailer_code,r2.Retailer_code,anno,self._idMap)
                    if arco != []:
                        self._grafo.add_edge(arco[0][0],arco[0][1],weight=arco[0][2])

        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def calcolaVolumi(self):
        lista = []
        for r in self._grafo.nodes:
            peso = 0
            for i in self._grafo.neighbors(r):
                peso += self._grafo[r][i]["weight"]
            lista.append((r.Retailer_name,peso))
        listaO = sorted(lista,key=lambda x: x[1],reverse=True)
        return listaO

    def cercaPercorso(self,n):
        self._bestPath=[]
        self.peso=0
        parziale=[]
        for r in self._grafo.nodes:
            parziale.append(r)
            self.ricorsione(parziale, n)
            parziale.pop()
        return self.getArchi(self._bestPath), self.calcolaPeso(self._bestPath)

    def ricorsione(self,parziale,n):
        if len(parziale) == n:
            vicini= self._grafo.neighbors(parziale[0])
            if parziale[-1] in vicini:
                parziale.append(parziale[0])
                if self.calcolaPeso(parziale)>self.peso:
                    self._bestPath = copy.deepcopy(parziale)
                    self.peso=self.calcolaPeso(parziale)
                parziale.pop()
        else:
            for i in self._grafo.neighbors(parziale[-1]):
                if i not in parziale:
                    parziale.append(i)
                    self.ricorsione(parziale,n)
                    parziale.pop()



    def calcolaPeso(self,path):
        peso=0
        for i in range(0,len(path)-1):
            peso += self._grafo[path[i]][path[i+1]]["weight"]
            print(peso)
        return peso

    def getArchi(self,path):
        lista=[]
        for i in range(0,len(path) - 1):
            lista.append((path[i],path[i+1],self._grafo[path[i]][path[i+1]]["weight"]))
        return lista



