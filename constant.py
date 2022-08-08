UF = {'AC' : 'Acre', 'AL' : 'Alagoas', 'AP' : 'Amapá',
      'AM' : 'Amazonas', 'BA' : 'Bahia', 'CE' : 'Ceará',
      'DF' : 'Distrito Federal', 'ES' : 'Espirito Santo',
      'GO' : 'Goiás', 'MA' : 'Maranhão','MS' : 'Mato Grosso do Sul',
      'MT' : 'Mato Grosso', 'MG' : 'Minas Gerais', 'PA' : 'Pará',
      'PB' : 'Paraíba', 'PR' : 'Paraná', 'PE' : 'Pernambuco',
      'PI' : 'Piauí', 'RJ' : 'Rio de Janeiro',
      'RN' : 'Rio Grande do Norte', 'RS' : 'Rio Grande do Sul',
      'RO' : 'Rondônia', 'RR' : 'Roraima', 'SC' : 'Santa Catarina',
      'SP' : 'São Paulo', 'SE' : 'Sergipe', 'TO' : 'Tocantins' }

UF_SIGLAS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MS', 'MT', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
UF_NOME = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espirito Santo', 'Goiás', 'Maranhão', 'Mato Grosso do Sul', 'Mato Grosso', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins']

API_CAMARA = "https://dadosabertos.camara.leg.br/api/v2/"

LEGISLATURA = API_CAMARA + "legislaturas?itens=1&ordem=DESC&ordenarPor=id"

API_SENADO = "https://legis.senado.leg.br/dadosabertos/"


NORMALMAP = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
             'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
             'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
             'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
             'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
             'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
             'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
             'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
             'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
             'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
             'Ñ': 'N', 'ñ': 'n',
             'Ç': 'C', 'ç': 'c',
             '§': 'S',  '³': '3', '²': '2', '¹': '1'}

NORMALIZAR = str.maketrans(NORMALMAP)