from datetime import datetime
from colorama import init, Fore, Back
import os
from hashlib import sha256

init()

parametros_bloqueados = []
gerar_logs = False
estado_console_log = False
caracteres_separadores = [' ']
palavras_bloqueadas = []
comandos_sql_bloquados = ['WHERE','FROM','SELECT','CREATE',';','=',"'",'"','`','AND','OR','ALTER','TABLE','GROUP BY','NOT','!','--']


def retornar_hora_atual():
    hora_atual = datetime.now()
    hora_atual = hora_atual.time()
    hora_atual = str(hora_atual)

    return hora_atual[0:8]


def retornar_data_atual(formato):
    data_atual = datetime.now()
    data_atual = data_atual.date()
    data_atual = data_atual.strftime(formato)

    return data_atual


def verificar_strings_vazias(*strings):
    for item in strings:
        if (len(item)) <=0:
            return False
        else:
            contador = 0
            for letra in range(len(item)):
                if item[letra] == ' ':
                    contador += 1
            
            if contador >= len(item):
                return True
            else:
                return False


def bloquear_parametros_url(*valores_parametros):
    for item in valores_parametros:
        item = item.upper()
        parametros_bloqueados.append(item)


def verificar_parametro_bloqueado(*valores_parametros):
    for item in valores_parametros:
        item = item.upper()
        if item in parametros_bloqueados:
            return True
    else:
        return False
    
    
def configurar_log(criar_logs:bool=False,exibir_logs_em_console:bool=False):
    global gerar_logs
    global estado_console_log
    gerar_logs = criar_logs
    estado_console_log = exibir_logs_em_console


def verificar_status_log():
    global gerar_logs
    return gerar_logs

    
def gerar_log(tipo:str,conteudo:str):
    if gerar_logs == True:
        data_atual = retornar_data_atual("%d-%m-%Y")
        hora_atual = retornar_hora_atual()

        tipo = tipo.upper()

        conteudo = f'{tipo}: {conteudo} || DATA: {data_atual} || HORA: {hora_atual}\n'
        with open('log.txt', 'a') as arquivo:
            arquivo.write(conteudo)

        if estado_console_log == True:
            os.system("cls")
            print(Fore.RED + conteudo)

        return True
    else:
        print(Fore.RED + "ERRO: Gerar Log está desativado! Para ativar use a função 'configLog()'")


def quebrar_frase(frase):
    palavras = []
    controle = 0
    tamanho_frase = len(frase)

    for i in range(tamanho_frase):
        item = frase[i]
        if ((item in caracteres_separadores) or (i == (tamanho_frase-1))):
            if (i == (tamanho_frase-1)):
                i +=1
            palavra = frase[controle:i]
            palavras.append(palavra)
            controle = i+1
    return palavras


def verificar_validade_parametros_anti_injecao_sql(*parametros):
    for parametro in parametros:
        parametro = parametro.upper()
        isolados = quebrar_frase(parametro)
        for i in range(len(isolados)):
            if (isolados[i] in comandos_sql_bloquados) or (isolados[i] in palavras_bloqueadas):
                return [False, 'Parametro potencialmente perigoso']
        else:
            for letra in parametro:
                if (letra in comandos_sql_bloquados) or (letra in palavras_bloqueadas):
                    return [False, 'Parametro potencialmente perigoso']
    else:
        return [True, 'Parametro válido']


def bloquear_outras_injecoes_sql(*palavra):
    for item in palavra:
        item = item.upper()
        palavras_bloqueadas.append(item)
    return True


def criptografar_SHA256(arg:str):
    hash = sha256(arg.encode())
    resultado = hash.hexdigest()
    return resultado