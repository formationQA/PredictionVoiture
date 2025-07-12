from src.Model_entrainement import ModelDePrediction
from src.NettoyageRepertoireJson import JsonSauvegarde
from src.CreactionJSONObjects import JsonConvert
from src.NettoyageHTML import NettoyageHtml
from src.ScrapperWebSiteObjects import WebScraper
from src.ConnexionBDD import DatabaseConnection
from src.InsertionDonneesBDD import InsertionDonnees


def main():
    nettoyage = JsonSauvegarde()
    instance = WebScraper()
    instancenettoyage = NettoyageHtml()
    instancejson = JsonConvert( )
    db_connection = DatabaseConnection()
    db_connection.connect()

    instance.ScrapperSiteAnnonces()
    instancenettoyage.TraitementFichiersHTML()
    instancejson.SauvegardeJSON()
    data_inserter = InsertionDonnees(db_connection)
    data_inserter.InsererLesDonneesEnBase()
    db_connection.close()
    nettoyage.CompresserJSon()
    trainer = ModelDePrediction()
    trainer.train_and_save_model()


if __name__ == "__main__":
    main()