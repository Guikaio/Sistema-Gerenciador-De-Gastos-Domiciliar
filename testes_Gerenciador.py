import io
import os
import unittest
from unittest import mock
from unittest.mock import patch
from unittest.mock import mock_open
from io import StringIO
from Gerenciador_main import Carteira
import json


class TestCarteira(unittest.TestCase):

    def setUp(self):
        self.carteira = Carteira.getInstance()
        self.carteira.carteira = {}
        self.carteira.id_transacao = 0

    # Este teste verifica se o método carregarCarteira_gastos está funcionando corretamente. Ele usa o patch para substituir a chamada à função open, que abre um arquivo no modo de leitura, por um objeto StringIO que contém dados em formato JSON.
    # O método carregarCarteira_gastos deve ler esses dados e preencher a carteira do usuário com as transações contidas neles.
    # O teste verifica se a carteira foi preenchida corretamente e se o número de transações carregadas é igual ao número esperado.
    def test_carregar_carteira_gastos(self):
        json_data = '{"idtransacao": 2, "id_1": {"valor": 50.0, "descricao": "luz", "data": "2022-03-17 13:00:00", "identificador": 1}, "id_2": {"valor": 100.0, "descricao": "Compras", "data": "2022-03-16 18:30:00", "identificador": 2}}'
        with patch('builtins.open', return_value=StringIO(json_data)):
            self.carteira.carregarCarteira_gastos()

        self.assertEqual(len(self.carteira.carteira), 2)
        self.assertEqual(self.carteira.id_transacao, 2)
        self.assertEqual(self.carteira.carteira['id_1']['valor'], 50.0)
        self.assertEqual(self.carteira.carteira['id_1']['descricao'], 'luz')
        self.assertEqual(
            self.carteira.carteira['id_1']['data'], '2022-03-17 13:00:00')
        self.assertEqual(self.carteira.carteira['id_1']['identificador'], 1)
        self.assertEqual(self.carteira.carteira['id_2']['valor'], 100.0)
        self.assertEqual(
            self.carteira.carteira['id_2']['descricao'], 'Compras')
        self.assertEqual(
            self.carteira.carteira['id_2']['data'], '2022-03-16 18:30:00')
        self.assertEqual(self.carteira.carteira['id_2']['identificador'], 2)

    # Este teste verifica se o método carregarCarteira_gastos lida corretamente com o caso em que o arquivo a ser lido não existe. Neste caso, ele deve deixar a carteira vazia e definir o número de transações como 1.

    def test_carregar_carteira_gastos_arquivo_nao_encontrado(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            self.carteira.carregarCarteira_gastos()

        self.assertEqual(len(self.carteira.carteira), 0)
        self.assertEqual(self.carteira.id_transacao, 1)

    # Este teste verifica se o método listarDespesas está funcionando corretamente. Ele configura a carteira do usuário com algumas transações.
    # Depois redireciona a saída padrão para um objeto StringIO e chama o método listarDespesas. O teste verifica se a saída gerada pelo método é a esperada.

    @patch('builtins.input', side_effect=['1'])
    def test_listar_despesas(self, mock_input):
        carteira = Carteira.getInstance()
        carteira.carteira = {
            1: {"identificador": 1, "data": "2022-01-01", "descricao": "Compra no supermercado", "valor": 100.0},
            2: {"identificador": 2, "data": "2022-01-02", "descricao": "Conta de luz", "valor": 50.0},
            3: {"identificador": 3, "data": "2022-01-03", "descricao": "Combustível", "valor": 70.0}
        }
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            carteira.listarDespesas()
            expected_output = "\nSuas Despesads: \n3 - 2022-01-03 - Combustível: R$70.00\n2 - 2022-01-02 - Conta de luz: R$50.00\n1 - 2022-01-01 - Compra no supermercado: R$100.00\n"
            self.assertEqual(fake_output.getvalue(), expected_output)

    # Este teste verifica se o método adcionarDespesas está funcionando corretamente.
    # Ele usa o patch para simular a entrada do usuário e adiciona uma transação à carteira do usuário com a descrição e o valor fornecidos. O teste verifica se a transação foi adicionada corretamente.

    def test_adcionar_despesas(self):
        descricao = "Despesa de teste"
        valor = -100.0
        with patch('builtins.input', side_effect=[descricao, valor]):
            self.carteira.adcionaDespesas()

        self.assertEqual(len(self.carteira.carteira), 1)
        transacao = list(self.carteira.carteira.values())[0]
        self.assertEqual(transacao["descricao"], descricao)
        self.assertEqual(transacao["valor"], valor)

    # Este teste verifica se o método editarDespesas está funcionando corretamente.
    # Ele usa o patch para simular a entrada do usuário e altera a descrição e o valor de uma transação existente na carteira do usuário. O teste verifica se a transação foi atualizada corretamente.

    @patch('builtins.input', side_effect=['Nova compra no mercado', 'Nova compra de mercado', '10.0', 's'])
    def test_editar_despesas(self, mock_input):
        carteira = Carteira.getInstance()
        carteira.carteira = {
            "1": {
                "valor": 15.7,
                "descricao": "Nova compra no mercado",
                "data": "2021-09-10 10:00:00",
                "identificador": 1
            }
        }

        carteira.editarDespesas()

        self.assertEqual(
            carteira.carteira['1']['descricao'], 'Nova compra de mercado')
        self.assertEqual(carteira.carteira['1']['valor'], 10.0)
        self.assertTrue('2023' in carteira.carteira['1']['data'])

    # Este teste verifica se o método somardespesas está funcionando corretamente.
    # Ele configura a carteira do usuário com algumas transações e verifica se o total de despesas retornadas pelo método é o esperado.

    @patch('builtins.input', side_effect=['S', '3'])
    def test_somardespesas(self, mock_input):
        carteira = Carteira.getInstance()
        carteira.carteira = {
            "1": {"valor": 10.5, "descricao": "Gasolina", "data": "2022-01-01 10:00:00", "identificador": 1},
            "2": {"valor": -30.0, "descricao": "Supermercado", "data": "2022-01-02 12:00:00", "identificador": 2},
            "3": {"valor": -15.5, "descricao": "Restaurante", "data": "2022-01-03 15:00:00", "identificador": 3},
            "4": {"valor": 20.0, "descricao": "Venda de livro", "data": "2022-01-04 17:00:00", "identificador": 4},
        }
        expected_output = 'Suas despesas totais são: R$-45.50\n'
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            carteira.somardespesas()
        self.assertEqual(mock_output.getvalue(), expected_output)

    # Este teste  simula a entrada de um valor de saldo de 100 através do uso da função patch que altera temporariamente a função input para retornar o valor esperado.
    # Em seguida, o teste calcula o saldo total esperado com base no valor inserido e nas despesas atuais da carteira. Depois, chama o método inserirSaldo da classe Carteira e verifica se o saldo total retornado corresponde ao saldo total esperado.
    # Por fim, o teste também verifica se as despesas da carteira permanecem iguais após a chamada do método inserirSaldo.

    @patch('builtins.input', side_effect=["100"])
    def test_inserirSaldo(self, mock_input):
        expected_despesas = self.carteira.exibirDespesas()
        expected_saldo_total = 100 + expected_despesas

        # chama o método inserirSaldo
        saldo_total = self.carteira.inserirSaldo()

        # verifica se o saldo total corresponde ao esperado
        self.assertEqual(saldo_total, expected_saldo_total)

        # verifica se as despesas correspondem ao esperado
        self.assertEqual(self.carteira.exibirDespesas(), expected_despesas)

    # Esse teste verifica se a função salvarcarteira_gastos() está salvando corretamente a carteira de gastos em um arquivo JSON.
    # Ele faz isso ao primeiro definir manualmente uma carteira de gastos com id de transação 1 e gastos de 10, 20 e 30.
    # Em seguida, define o id de transação como 2 e chama a função salvarcarteira_gastos() que deve salvar a carteira atualizada no arquivo 'carteira.json'.
    # Depois, o teste lê o arquivo 'carteira.json' e verifica se os dados salvos correspondem aos esperados, ou seja, uma carteira de gastos com id de transação 2 e os mesmos gastos de 10, 20 e 30. A asserção self.assertEqual() é usada para comparar se os dados obtidos do arquivo JSON são iguais à carteira de gastos esperada.

    def test_salvarcarteira_gastos(self):
        # Teste para verificar se a carteira foi salva corretamente
        self.carteira.carteira = {"idtransacao": 1, "gastos": [10, 20, 30]}
        self.carteira.id_transacao = 2
        self.carteira.salvarcarteira_gastos()
        with open('carteira.json', 'r') as c:
            dados_carteira = json.load(c)
        self.assertEqual(dados_carteira, {
                         "idtransacao": 2, "gastos": [10, 20, 30]})

    # Esse teste testa o método "encontrarDespesasPorNome" da classe "Carteira". Para isso, ele cria uma instância de "Carteira" e adiciona algumas despesas ao atributo "carteira".
    # Em seguida, o teste chama o método "encontrarDespesasPorNome" passando o nome de uma despesa existente ("descricao1") e espera que o método retorne o identificador correto (1).
    # Depois, o teste chama o método passando o nome de uma despesa inexistente ("descricao3") e espera que o método retorne "None".

    def test_encontrarDespesasPorNome(self):
        with mock.patch('builtins.input', return_value='descricao1'):
            self.carteira.carteira = {
                1: {'descricao': 'descricao1', 'valor': 10.0},
                2: {'descricao': 'descricao2', 'valor': 20.0}
            }
            identificador = self.carteira.encontrarDespesasPorNome(
                'descricao1')
            self.assertEqual(identificador, 1)

            identificador = self.carteira.encontrarDespesasPorNome(
                'descricao3')
            self.assertIsNone(identificador)

    # Este teste simula a entrada do usuário com a descrição "descricao1" e verifica se o método encontrarDespesasPorNome retorna o identificador correto da despesa correspondente. 
    # É esperado que o valor retornado seja 1, que é o identificador da primeira despesa adicionada à carteira.

    def test_encontrarDespesasPorNome_encontrada(self):
        with mock.patch('builtins.input', return_value='descricao1'):
            self.carteira.carteira = {
                1: {'descricao': 'descricao1', 'valor': 10.0},
                2: {'descricao': 'descricao2', 'valor': 20.0}
            }
            identificador = self.carteira.encontrarDespesasPorNome('descricao1')
            self.assertEqual(identificador, 1)


        

if __name__ == '__main__':
    unittest.main()
