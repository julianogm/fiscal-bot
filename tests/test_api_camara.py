import pytest

from camara import *


def test_lista_deputados():
    lista = lista_deputados()
    assert isinstance(lista, list)


def test_deputado_por_estado():
    lista = deputado_por_estado("SP")
    assert len(lista) != 0


def test_deputado_por_nome():
    dep = deputado_por_nome("jesse")
    assert len(dep) == 0

    dep = deputado_por_nome("alexandre")
    assert len(dep) != 0


def test_deputado_por_partido():
    lista = deputado_por_partido("PARTIDO_FALSO")
    assert len(lista) == 0

    lista = deputado_por_partido("PT")
    assert len(lista) != 0


def test_deputado_por_id():
    dep = deputado_por_id(5)
    assert dep["nome"] == "Não encontrado"

    dep = deputado_por_id(160600)
    assert "Arthur" in dep["nome"]


def test_nomes_deputados():
    lista = nomes_deputados()
    assert len(lista) != 0
    assert "Abou Anni" in lista
