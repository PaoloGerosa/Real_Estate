# Create the class
class Immobile:

    # Initialize the class
    def __init__(self, ID, Ora, Sito, Localita):

        # Research variables
        self.ID = ID
        self.Ora = Ora
        self.Sito = Sito
        self.Localita = Localita.title().replace('_', ' ')

        # Instance variables
        self.CodiceCasa        = None
        self.Headline          = None
        self.URL               = None
        self.Prezzo            = None
        self.Locali            = None
        self.Superficie        = None
        self.Bagni             = None
        self.Ratio             = None
        self.Tipologia         = None
        self.BoxPostoAuto      = None
        self.Piano             = None
        self.AnnodiCostruzione = None
        self.Stato             = None
        self.Riscaldamento     = None
        self.ClasseEnergetica  = None
        self.Via               = None
        self.Latitudine        = None
        self.Longitudine       = None

    # Setting functions
    def setCodiceCasa(self, valore):        self.CodiceCasa = valore
    def setHeadline(self, valore):          self.Headline = valore
    def setURL(self, valore):               self.URL = valore
    def setPrezzo(self, valore):            self.Prezzo = valore
    def setLocali(self, valore):            self.Locali = valore
    def setSuperficie(self, valore):        self.Superficie = valore
    def setBagni(self, valore):             self.Bagni = valore
    def setRatio(self, valore):             self.Ratio = valore
    def setTipologia(self, valore):         self.Tipologia = valore
    def setBoxPostoAuto(self, valore):      self.BoxPostoAuto = valore
    def setPiano(self, valore):             self.Piano = valore
    def setAnnodiCostruzione(self, valore): self.AnnodiCostruzione = valore
    def setStato(self, valore):             self.Stato = valore
    def setRiscaldamento(self, valore):     self.Riscaldamento = valore
    def setClasseEnergetica(self, valore):  self.ClasseEnergetica = valore
    def setVia(self, valore):               self.Via = valore
    def setLatitudine(self, valore):        self.Latitudine = valore
    def setLongitudine(self, valore):       self.Longitudine = valore

    # Research function
    def getCodiceCasa(self):   return self.CodiceCasa
    def getPrezzo(self):       return self.Prezzo
    def getSuperficie(self):   return self.Superficie
    def getLocali(self):       return self.Locali
    def getBoxPostoAuto(self): return self.BoxPostoAuto
    def getStato(self):        return self.Stato
    def getURL(self):          return self.URL
    def getBagni(self):        return self.Bagni

    # Recap best infos
    def scheda(self):
        return f"     Descrizione: {self.Headline}\n     URL: {self.URL}\n     Prezzo: {self.Prezzo}"