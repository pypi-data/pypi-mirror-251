from json import loads
from requests import get
from os.path import isfile
from re  import compile, sub
from datetime import datetime, timedelta

def validar_cpf(cpf):
    # Expressão regular para verificar o formato do CPF
    padrao_cpf = compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')

    if not padrao_cpf.match(cpf):
        return False

    # Remove os caracteres não numéricos do CPF
    cpf_numerico = sub(r'\D', '', cpf)

    # Verifica se todos os dígitos são iguais (situação inválida)
    if len(set(cpf_numerico)) == 1:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf_numerico[i]) * peso
        peso -= 1

    resto = soma % 11
    digito_verificador_1 = 11 - resto if resto > 1 else 0
 
    if digito_verificador_1 != int(cpf_numerico[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf_numerico[i]) * peso
        peso -= 1

    resto = soma % 11
    digito_verificador_2 = 11 - resto if resto > 1 else 0

    return digito_verificador_2 == int(cpf_numerico[10])

def armazenar_cpf():
    while True:
        # Solicita o CPF ao usuário
        cpf = input("Digite o CPF (formato: 123.456.789-01): ")

        # Verifica se o CPF está no formato correto e é válido
        if validar_cpf(cpf):

            with open('cpf.txt', 'w') as arquivo_cpf:
                arquivo_cpf.write(cpf)

            print(f"CPF {cpf} armazenado com sucesso.")
            break  
        else:
            print("CPF no formato ou lógica incorretos. Por favor, tente novamente.")

def limpar_cpf(cpf_formatado):
    # Remove todos os caracteres não numéricos do CPF
    cpf_numerico = ''.join(filter(str.isdigit, cpf_formatado))
    return cpf_numerico

def json_to_hash(response):
    
    data = loads(response)
    pessoas = data.get("pessoas", [])
    
    hashes = [pessoa.get("hash", "") for pessoa in pessoas]
    return hashes[0]

def get_hash():

    if not isfile('cpf.txt'):
        armazenar_cpf()
        
    with open('cpf.txt','r') as file:
            cpf = file.readline()
            file.close() 
    
    cpf = limpar_cpf(cpf)
    
    url = f"http://www.fnde.gov.br/digef/rs/spba/publica/pessoa/1/10/{cpf}"
    
    resposta = get(url)
    
    hash = json_to_hash(resposta.text)
    
    return hash

def formatar_dados(dados):
    # Imprime apenas o nome
    print("Nome:", dados["nome"])
    # Imprime os pagamentos
    for programa in dados["programas"]:
        for cnpj, entidade in programa["entidades"].items():
            for funcao_id, funcao in entidade["funcoes"].items():
                for pagamento in funcao["pagamentos"]:
                    print(f"Ordem Bancária: {pagamento['ordermBancaria']}, Data: {pagamento['data']}, Subtotal: {pagamento['valor']}")
                    
    # Imprime o total
    print("Total:", dados["total"])

    print("\n" + "=" * 40)

def consulta():

    url=f"https://www.fnde.gov.br/digef/rs/spba/publica/pagamento/{get_hash()}"
    
    response = get(url)
    
    data = loads(response.text)
    formatar_dados(data)
    
    return data

def caiu(): 
    mes_anterior = datetime.now().month -1
    if mes_anterior == 0:
        mes_anterior = 12
        
    mes_anterior = str(mes_anterior)
    
    data = consulta()
    total_atual = data.get("total")
    
    if not isfile('total.txt'):
        with open('total.txt', "w") as file:  
            file.write(f"{total_atual}p{mes_anterior}")
            file.close()
   
    with open('total.txt','r') as file:
        test = file.readline().split('p') 
        file.close()
 
    total_anterior, mes_anterior_armazenado = test[0], test[1]
    
    
    ######## encontrando o ultimo pagemento
    
    mes_anterior_armazenado = data["programas"][0]["entidades"][list(data["programas"][0]["entidades"].keys())[0]]["funcoes"][list(data["programas"][0]["entidades"][list(data["programas"][0]["entidades"].keys())[0]]["funcoes"].keys())[0]]["pagamentos"][-1]["data"][3:5]
    
    if mes_anterior_armazenado == mes_anterior:
        
        print("Se não tiver atraso, a sua bolsa está te esperando no banco.\n")
        
    else:
        print("Nenhum novo pagamento recebido.\n")

    troca = input("Trocar o cpf (Y/N): ").lower()
    
    if troca =='y':
        armazenar_cpf()
        caiu()
    
if __name__=='__main__':
    caiu()         
