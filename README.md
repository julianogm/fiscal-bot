# Bot Fiscal


Bem vindo ao Bot Fiscal.
Esse é um bot do telegram de consultas as apis da [câmara do deputados](https://dadosabertos.camara.leg.br/swagger/api.html) e do [senado federal](https://legis.senado.leg.br/dadosabertos/docs/ui/index.html) do Brasil.

Você pode testar o bot pesquisando @fiscal_politico_bot no telegram, ou clicando [aqui](http://t.me/fiscal_politico_bot). Caso o bot não esteja online, sinta-se a vontade para executa-lo na sua máquina.
_______________
### Ferramentas utilizadas:

python 3.10.12

cssselect 1.2.0 \
lxml 4.9.3 \
python-dotenv 1.0.0 \
python_telegram_bot 13.14 \
requests 2.31.0 \
telegram 0.0.1  \
pytest 7.4.3 \
coverage 7.3.2

\
Para instalar os pacotes necessários, rode o comando no terminal:
```
pip install -r requirements.txt
```

Para executar o bot localmente, crie um arquivo .env seguindo o padrão do arquivo .env.example e adicione o TOKEN para seu bot do telegram. Se quiser executar o bot no modo webhook, adicione o WEBHOOK_URL e a PORT, e altere MODE de polling para webhook.

Em seguida, rode o comando no terminal
```
python3 main.py
```
