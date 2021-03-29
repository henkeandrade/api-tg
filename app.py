from flask import Flask, request
from flask_cors import CORS
import pickle
import json

app = Flask("Capro")
CORS(app)


# função para fazer busca no banco
def SearchCulture(yesterday, yesterday_1, yesterday_diff):
    
    loaded_model = pickle.load(open('./soy_quotation_lr.sav', 'rb'))
    result = loaded_model.predict([[yesterday, yesterday_diff, yesterday_1]])
    resultStr = str(result).replace('[', '').replace(']', '')

    return { 'result': float(resultStr) }


# seta a rota e chama a função de buscar a cultura
@app.route("/search", methods=["POST"])
def SearchCultureRequest():
    body = request.get_json()

    if("yesterday" not in body):
        return Responses(400, "O campo yesterday é obrigatório!")

    if("yesterday_1" not in body):
        return Responses(400, "O campo yesterday_1 é obrigatório!")

    if("yesterday_diff" not in body):
        return Responses(400, "O campo yesterday_diff é obrigatório!")

    dataSearch = SearchCulture(body["yesterday"], body["yesterday_1"], body["yesterday_diff"])

    return Responses(200, "Busca realizada com sucesso", "busca", dataSearch)


# função para gerar resposta geral
def Responses(status, message, name_content=False, content=False):
    response = {}
    response["status"] = status
    response["message"] = message

    if (name_content and content):
        response[name_content] = content

    return response


if __name__ == '__main__':
    app.run()
