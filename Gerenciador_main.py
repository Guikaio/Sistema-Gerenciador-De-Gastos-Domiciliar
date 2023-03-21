# importando o módulo json e o datetime da biblioteca padrão do Python.
import json
from datetime import datetime


class Carteira:  # importa o módulo json e o datetime da biblioteca padrão do Python.
    # O padrão de projeto utilizado neste código é o Singleton.
    # O método getInstance() é estático e é responsável por garantir que apenas uma única instância da classe Carteira seja criada.
    # Além disso, o construtor da classe é privado e só pode ser chamado internamente pela classe, o que impede que novas instâncias da classe sejam criadas a partir do código fora da classe.
    _instance = None

    @staticmethod
    def getInstance():
        if Carteira._instance == None:
            Carteira._instance = Carteira()
        return Carteira._instance

    def __init__(self):
        if Carteira._instance != None:
            raise Exception(
                "Você não pode criar mais de uma instância da Carteira!")
        else:
            Carteira._instance = self
            self.id_transacao = None
            self.carteira = None
            self.carregarCarteira_gastos()


# A função carregarCarteira_gastos() tenta carregar os dados da carteira de um arquivo JSON.
# Se a operação falhar, um dicionário vazio é criado e a despesa é definida para um.
# Caso contrário, a despesa atual é definida como o valor armazenado em "idtransacao" e removida do dicionário.
    def carregarCarteira_gastos(self):
        try:
            with open('carteira.json', 'r') as c:
                self.carteira = json.loads(c.read())
            self.id_transacao = self.carteira["idtransacao"]
            self.carteira.pop("idtransacao")
        except:
            self.carteira = {}
            self.id_transacao = 1


# A função adcionaDespesas(self) é responsável por adicionar uma nova despesa à carteira.
# Ela solicita ao usuário que informe a descrição e o valor da despesa, e em seguida cria um dicionário transacao com as informações informadas.
# O dicionário é então adicionado à carteira, com uma chave gerada a partir do atributo id_transacao.
# Por fim, o atributo id_transacao é incrementado em 1 e a função exibe uma mensagem informando que a despesa foi adicionada com sucesso.
    def adcionaDespesas(self):
        descricao = input('\nDigite a descrição da Despesa: ')
        valor = float(
            input('Digite o valor da Despesa (com sinal de - se for gasto): '))
        data = str(datetime.now())

        transacao = {
            "valor": valor,
            "descricao": descricao,
            "data": data,
            "identificador": str(self.id_transacao),
        }

        self.carteira["id_" + str(self.id_transacao)] = transacao
        self.id_transacao += 1
        print('Despesa adicionada com sucesso!')

# A função listarDespesas() exibe as transações armazenadas na carteira.
# Ela verifica se a carteira está vazia e as ordena por ordem decrescente de identificador.
    def listarDespesas(self):
        if len(self.carteira) == 0:
            print('\nSem transações!')
            return
        print('\nSuas transações: ')

        for transacao in sorted(
                self.carteira.values(),
                key=lambda transacao: str(transacao["identificador"]),
                reverse=True):
            print(
                f'{transacao["identificador"]} - {transacao["data"]} - {transacao["descricao"]}: R${transacao["valor"]:.2f}')


# A função deletar_despesas() solicita que o usuário forneça a descrição da despesa que deseja excluir.
# Ele chama o método encontrarDespesasPorNome() para localizar a despesa e, se encontrada, a exclui do dicionário da carteira.
    def deletar_despesas(self):
        nome = input('\nDigite a descrição da despesa que quer deletar: ')
        identificador = self.encontrarDespesasPorNome(nome)
        if identificador:
            transacao = self.carteira.pop(identificador)
            print(
                f'Despesa {transacao["identificador"]} - "{transacao["descricao"]}", no valor de R${transacao["valor"]:.2f} foi excluída!')
        else:
            print('Despesa não encontrada!')

# A função encontrarDespesasPorNome possibilita com que se possa busca a despesa pelo nome inserido e depois possa editar o mesmo ou deletar
    def encontrarDespesasPorNome(self, nome):
        for identificador, transacao in self.carteira.items():
            if transacao['descricao'] == nome:
                return identificador
        print('Despesa não encontrada!')
        return None

# A função editarDespesas() solicita ao usuário que forneça a descrição da despesa que deseja editar.
# Ele chama a função encontrarDespesasPorNome() para localizar a despesa e, se encontrada, permite que o usuário edite a descrição, valor e data da despesa.
    def editarDespesas(self):
        nome = input('\nDigite a descrição da Despesa que quer editar: ')
        identificador = self.encontrarDespesasPorNome(nome)
        if identificador:
            id_transacao = int(self.carteira[identificador]["identificador"])
            descricao = input('Digite a nova descrição da Despesa: ')
            valor = float(input('Digite o novo valor da Despesa: '))
            mudar_data = input(
                'Digite S para mudar a data da despesa para a data atual ou N para manter a data antiga: ').upper()
            if mudar_data == 'S':
                data = str(datetime.now())
            else:
                data = self.carteira[identificador]["data"]

            transacao = {
                "valor": valor,
                "descricao": descricao,
                "data": data,
                "identificador": id_transacao,
            }

            self.carteira[identificador] = transacao

            print(f'Despesa {id_transacao} editada com sucesso!')
        else:
            print('Despesa não encontrada!')

# A função somarespesas soma todas as despesas salvas na carteira e exibe a soma das mesmas no menu
    def somardespesas(self):
        despesas = 0
        for transacao in self.carteira.values():
            if transacao["valor"] < 0:
                despesas += transacao["valor"]
        print(f'Suas despesas totais são: R${despesas:.2f}')


# A função exibirDespesas serve para capturar a soma das despesas na carteira e retornar essa soma para a função inserir saldo que a exibira atualizada com base no saldo
    def exibirDespesas(self):
        despesas = 0
        for transacao in self.carteira.values():
            if transacao["valor"] < 0:
                despesas += transacao["valor"]
        return despesas

# A função inserirSaldo solicita que o usuário insira o saldo atual da carteira, armazena esse valor como atributo da classe Carteira
# depoos ela exibe a soma das despesas presentes na carteira
# e soma o saldo e as despesas e exibe o saldo atualizado. Por fim, retorna o saldo total.
    def inserirSaldo(self):
        saldo = float(input('\nInsira o seu saldo atual: '))
        self.saldo = saldo
        despesas = self.exibirDespesas()
        saldo_total = saldo + despesas
        print(f'Suas despesas totais são: R${despesas:.2f}')
        print('Saldo atualizado com base nas despesas: R$ {:.2f}'.format(
            saldo_total))
        return saldo_total


# A função salvarcarteira_gastos() salva a carteira atual no arquivo "carteira.json"
    def salvarcarteira_gastos(self):
        self.carteira["idtransacao"] = self.id_transacao
        with open('carteira.json', 'w') as c:
            c.write(json.dumps(self.carteira))
            print('Carteira salva com sucesso!')


# O método menu() exibe um menu de opções para o usuário e chama os métodos apropriados com base na entrada do usuário.
# Ele executa em loop até que o usuário escolha a opção "0" para sair.
    def menu(self):
        while True:
            print('\n##########MENU##########')
            print(' Selecione uma opção: ')
            print('1 - Listar Despesas')
            print('2 - Adicionar Despesas')
            print('3 - Deletar Despesas')
            print('4 - Editar Despesas')
            print('5 - Soma das despesas')
            print('6 - Calcule o seu saldo atual')
            print('0 - Sair')

            opcao = input('Digite sua escolha: ')
            if opcao == '1':
                self.listarDespesas()
            elif opcao == '2':
                self.adcionaDespesas()
            elif opcao == '3':
                self.deletar_despesas()
            elif opcao == '4':
                self.editarDespesas()
            elif opcao == '5':
                self.somardespesas()
            elif opcao == '6':
                self.inserirSaldo()
            elif opcao == '0':
                self.salvarcarteira_gastos()
                break
            else:
                print('Opção inválida!')


if __name__ == '__main__':
    carteira = Carteira.getInstance()
    carteira.menu()
######################################################################################################################################
