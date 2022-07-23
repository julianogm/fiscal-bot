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