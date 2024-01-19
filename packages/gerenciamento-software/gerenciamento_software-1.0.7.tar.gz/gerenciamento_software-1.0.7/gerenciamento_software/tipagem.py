from .geral import gerar_log,verificar_status_log,configurar_log
from colorama import init, Fore, Back
import linecache

init()


variaveisTipadas = []
tiposPossiveis = ['bool','int','str','float']
constantesCriadas = []


def verificarTipo(valor):
    tipo = type(valor)
    if tipo == str:
        return 'str'
    elif tipo == int:
        return 'int'
    elif tipo == bool:
        return 'bool'
    elif tipo == float:
        return 'float'


def declararVariavel(nomeVariavel:str,tipoVariavel:str,valorInicial=None):
    tipoVariavel = tipoVariavel.lower()

    if tipoVariavel in tiposPossiveis:
        if valorInicial == None:
            if tipoVariavel == 'bool':
                valorInicial = False
            elif tipoVariavel == 'str':
                valorInicial = ''
            elif tipoVariavel == 'float':
                valorInicial = 0.0
            elif tipoVariavel == 'int':
                valorInicial = 0

        tipo = verificarTipo(valorInicial)
        
        if tipo == tipoVariavel:
            newVariavel = {'nome':nomeVariavel,'tipo':tipoVariavel,'valor':valorInicial}    
            variaveisTipadas.append(newVariavel)

            return valorInicial
        else:
            erro = f'ERRO: O tipo inicial é "{tipoVariavel}", enquanto o valor inicial é do tipo "{tipo}"'
            print(Fore.YELLOW + erro)
            logAtivado = verificar_status_log()
            if logAtivado == True:
                configurar_log(criar_logs=True,exibir_logs_em_console=False)
                gerar_log('CRITICAL',erro)
            return None
    else:
        erro = f'ERRO: Não é possivel usar o tipo "{tipoVariavel}"'
        print(Fore.RED + erro)
        logAtivado == verificar_status_log()
        if logAtivado == True:
            configurar_log(criar_logs=True,exibir_logs_em_console=False)
            gerar_log('CRITICAL',erro)
        return None


def atribuirValor(nomeVariavel:str, valor):
    for i in range(len(variaveisTipadas)):
        if nomeVariavel == variaveisTipadas[i]['nome']:
            tipoDeclarado = variaveisTipadas[i]['tipo']
            tipoPassado = verificarTipo(valor)
            if tipoDeclarado == tipoPassado:
                variaveisTipadas[i]['valor'] = valor
                return valor
            else:
                erro = f"ERRO: Você está tentando atribuir um valor do tipo '{tipoPassado}' numa variável do tipo '{tipoDeclarado}'"
                print(Fore.YELLOW + erro)
                logAtivado = verificar_status_log()
                if logAtivado == True:
                    configurar_log(criar_logs=True,exibir_logs_em_console=False)
                    gerar_log('CRITICAL',erro)
                return None


def declararCostante(nome:str,valor):
    if (len(constantesCriadas)) <=0:
        novaConstante = {'nome':nome,'valor':valor,'qtd':0}
        constantesCriadas.append(novaConstante)
        return valor
    else:
        for i in range(len(constantesCriadas)):
            if nome == constantesCriadas[i]['nome']:
                erro = f"Constante {nome} já existe e seu valor não pode ser alterado"
                print(Fore.YELLOW + erro)
                logAtivado = verificar_status_log()
                if logAtivado == True:
                    configurar_log(criar_logs=True,exibir_logs_em_console=False)
                    gerar_log('CRITICAL',erro)
                return None
        else:
            novaConstante = {'nome':nome,'valor':valor,'qtd':0}
            constantesCriadas.append(novaConstante)
            return valor


def iniciarTipagem(caminho):

    with open(caminho, 'r') as arquivo:
        numeroDeLinhas = len(arquivo.readlines())
    
    for i in range(numeroDeLinhas):
        conteudoLinha = linecache.getline(caminho,i)
        quantidadeConst = len(constantesCriadas)
        for item in range(quantidadeConst):
            nomeConstante = constantesCriadas[item]['nome']
            vezesUsada = constantesCriadas[item]['qtd']

            possibilidade1 = f'{nomeConstante}='
            possibilidade2 = f'{nomeConstante} ='
            possibilidade3 = f'{nomeConstante}  ='

            if (possibilidade1 in conteudoLinha) or (possibilidade2 in conteudoLinha) or (possibilidade3 in conteudoLinha):
                constantesCriadas[item]['qtd'] = vezesUsada+1
            
            vezesUsada = constantesCriadas[item]['qtd']

            if (vezesUsada >=2):
                erro = f'ERRO: A Constante {nomeConstante} está sendo atribuida mais de uma vez --> linha {i} <--'
                print(Fore.RED + erro)
                logAtivado = verificar_status_log()
                if logAtivado == True:
                    configurar_log(criar_logs=True,exibir_logs_em_console=False)
                    gerar_log('CRITICAL',erro)
                exit()