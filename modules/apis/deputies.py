import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
grandparent = os.path.dirname(parent)
sys.path.append(parent)
sys.path.append(grandparent)
from datetime import date

import lxml.html
import requests

from constant import *

CSS_CEAP = "#percentualgastocotaparlamentar > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
CSS_VERBA_GAB = "#percentualgastoverbagabinete > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
CSS_EMAIL = ".email"


class Deputies:
    def __init__(self):
        pass

    def _get_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["dados"]
        else:
            raise Exception(
                f"Request failed with status {response.status_code}: {response.json()['title']}"
            )

    def list_deputies(self):
        url = f"{API_CAMARA}deputados"
        deputies = self._get_data(url)
        return deputies

    def _by_filter(self, filter_name, filter_value):
        url = f"{API_CAMARA}deputados?{filter_name}={filter_value}"
        deputies = self._get_data(url)
        return deputies

    def by_state(self, state_acronym):
        return self._by_filter("siglaUf", state_acronym)

    def by_political_party(self, party_acronym):
        return self._by_filter("siglaPartido", party_acronym)

    def by_name(self, name):
        legislature_data = self._get_data(LEGISLATURA)
        legislature = legislature_data[0]["id"]
        url = (
            API_CAMARA
            + f"deputados?nome={name}&idLegislatura={legislature}&ordem=ASC&ordenarPor=nome"
        )
        deputies = self._get_data(url)
        return deputies

    def list_political_parties(self):
        deputies = self.list_deputies()
        political_parties = list(set([deputy["siglaPartido"] for deputy in deputies]))
        return political_parties

    def get_names_ids(self, deputies=None):
        if deputies == None:
            deputies = self.list_deputies()
        name_ids = "\n".join(
            [f"{deputy['nome']} - /deputado_{deputy['id']}" for deputy in deputies]
        )
        return name_ids

    def get_deputy_data(self, deputy_id):
        deputy_data = self._message(deputy_id)
        return deputy_data

    # fetch data from chamber of deputies website via webscraping
    def _deputy_info(self, deputy_id):
        response = requests.get(f"{SITE_CAMARA}{deputy_id}")
        tree = lxml.html.fromstring(response.text)

        site_info = {}

        if tree.cssselect(CSS_EMAIL):
            email = tree.cssselect(CSS_EMAIL)[0].text_content()
            site_info["email"] = email
        else:
            site_info["email"] = "Email não encontrado"

        if tree.cssselect(CSS_CEAP):
            ceap_spending = tree.cssselect(CSS_CEAP)[0].text_content()
            site_info["ceap"] = f"R$ {ceap_spending}"
        else:
            site_info["ceap"] = "Ainda não há gasto registrado com CEAP nesse ano"

        if tree.cssselect(CSS_VERBA_GAB):
            verba_gabinete_spending = tree.cssselect(CSS_VERBA_GAB)[0].text_content()
            site_info["verba_gabinete"] = f"R$ {verba_gabinete_spending}"
        else:
            site_info[
                "verba_gabinete"
            ] = "Ainda não há gasto registrado com Verba de Gabinete nesse ano"

        return site_info

    # build the response message to the user
    def _message(self, deputy_id):
        current_year = date.today().year
        url = f"{API_CAMARA}deputados/{deputy_id}"
        deputy = self._get_data(url)

        deputy_api_data = deputy["ultimoStatus"]
        deputy_site_data = self._deputy_info(deputy_id)

        full_name = deputy["nomeCivil"].title()
        name_search_jusbrasil = (
            full_name.replace(" ", "+").translate(NORMALIZAR).lower()
        )

        message = (
            f"Nome civil: {full_name}\n"
            f"Partido: {deputy_api_data['siglaPartido']} | Estado: {deputy_api_data['siglaUf']}\n"
            f"Email: {deputy_site_data['email']}\n"
            f"Telefone: (61) {deputy_api_data['gabinete']['telefone']}\n\n"
            f"Gastos de {deputy_api_data['nome']} em {current_year}\n"
            f"CEAP: {deputy_site_data['ceap']}\n"
            f"Verba de Gabinete: {deputy_site_data['verba_gabinete']}\n\n"
            f"Mais sobre o deputado(a): https://www.camara.leg.br/deputados/{deputy_id}\n"
            f"https://www.jusbrasil.com.br/artigos-noticias/busca?q={name_search_jusbrasil})\n\n"
        )

        data_dict = {}
        data_dict["message"] = message
        data_dict["photo"] = deputy_api_data["urlFoto"]
        return data_dict


obj_deputy = Deputies()
