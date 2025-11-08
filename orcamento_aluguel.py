import csv

class Imovel:
    def __init__(self):
        self.tipo = ""
        self.quartos = 0
        self.vagas = 0
        self.tem_crianca = False
        self.parcelas = 1
        self.valor_aluguel = 0
        self.valor_contrato_total = 2000

    def coletar_dado(self):
        print("=== Sistema de Orçamento - R.M Imóveis ===")

        self.tipo = input("Tipo do imóvel (apartamento / casa / estudio): ").lower()
        while self.tipo not in ["apartamento", "casa", "estudio"]:
            self.tipo = input("Inválido. Digite novamente (apartamento / casa / estudio): ").lower()

        if self.tipo in ["apartamento", "casa"]:
            while True:
                try:
                    self.quartos = int(input("Quantidade de quartos (1 ou 2): "))
                    if self.quartos in [1, 2]:
                        break
                    else:
                        print("Digite 1 ou 2 quartos.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
        else:
            self.quartos = 0

        if self.tipo in ["apartamento", "casa"]:
            incluir_vaga = input("Deseja incluir vaga de garagem? (s/n): ").lower()
            self.vagas = 1 if incluir_vaga == "s" else 0
        elif self.tipo == "estudio":
            while True:
                try:
                    self.vagas = int(input("Quantas vagas deseja incluir no estúdio? "))
                    break
                except ValueError:
                    print("Entrada inválida. Digite um número.")

        if self.tipo == "apartamento":
            crianca = input("Possui criança? (s/n): ").lower()
            self.tem_crianca = (crianca == "s")
        else:
            self.tem_crianca = False

        while True:
            try:
                self.parcelas = int(input("Número de parcelas do contrato (1 a 5): "))
                if self.parcelas in [1, 2, 3, 4, 5]:
                    break
                else:
                    print("Digite um valor entre 1 e 5.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def calcular_aluguel(self):
        if self.tipo == "apartamento":
            self.valor_aluguel = 700
            if self.quartos == 2:
                self.valor_aluguel += 200
            if not self.tem_crianca:
                self.valor_aluguel *= 0.95
            if self.vagas == 1:
                self.valor_aluguel += 300

        elif self.tipo == "casa":
            self.valor_aluguel = 900
            if self.quartos == 2:
                self.valor_aluguel += 250
            if self.vagas == 1:
                self.valor_aluguel += 300

        elif self.tipo == "estudio":
            self.valor_aluguel = 1200
            if self.vagas >= 1:
                self.valor_aluguel += 250
            if self.vagas > 2:
                self.valor_aluguel += (self.vagas - 2) * 60

        return round(self.valor_aluguel, 2)

    def gerar_csv(self, valor_aluguel, valor_parcela):
        parcelas_aplicadas = 0
        with open("orcamento.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerow(["Mês", "Aluguel (R$)", "Parcela Contrato (R$)", "Total Mensal (R$)"])

            for mes in range(1, 13):
                if parcelas_aplicadas < self.parcelas:
                    parcela = valor_parcela
                    parcelas_aplicadas += 1
                else:
                    parcela = 0
                total_mes = valor_aluguel + parcela
                writer.writerow([
                    mes,
                    f"{valor_aluguel:.2f}".replace('.', ','),
                    f"{parcela:.2f}".replace('.', ','),
                    f"{total_mes:.2f}".replace('.', ',')
                ])

    def exibir_resultado(self):
        valor_aluguel = self.calcular_aluguel()
        valor_parcela = self.valor_contrato_total / self.parcelas

        print("\n--- Resultado do Orçamento ---")
        print(f"Tipo do imóvel: {self.tipo.capitalize()}")
        if self.tipo != "estudio":
            print(f"Quartos: {self.quartos}")
        if self.tipo in ["apartamento", "casa"]:
            print(f"Vaga de garagem incluída: {'Sim' if self.vagas == 1 else 'Não'}")
        if self.tipo == "estudio":
            print(f"Quantidade de vagas: {self.vagas}")
        if self.tipo == "apartamento":
            print(f"Possui criança: {'Sim' if self.tem_crianca else 'Não'}")
        print(f"Valor do aluguel: R$ {valor_aluguel:.2f}")
        print(f"Valor total do contrato: R$ {self.valor_contrato_total:.2f}")
        print(f"Parcelas: {self.parcelas} x R$ {valor_parcela:.2f}")

        print("\n--- Detalhamento mês a mês ---")
        parcelas_aplicadas = 0
        for mes in range(1, 13):
            if parcelas_aplicadas < self.parcelas:
                parcela = valor_parcela
                parcelas_aplicadas += 1
            else:
                parcela = 0
            total_mes = valor_aluguel + parcela
            print(f"Mês {mes:02d}: Aluguel R$ {valor_aluguel:.2f} + Parcela R$ {parcela:.2f} = Total R$ {total_mes:.2f}")

        self.gerar_csv(valor_aluguel, valor_parcela)
        print("\n✅ Arquivo 'orcamento.csv' gerado com sucesso!")
        print("   Contém aluguel, parcelas e total mês a mês.\n")



if __name__ == "__main__":
    imovel = Imovel()
    imovel.coletar_dado()
    imovel.exibir_resultado()
