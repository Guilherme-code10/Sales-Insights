from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "dados" / "vendas.csv"
PASTA_GRAFICOS = BASE_DIR / "graficos"


def carregar_dados():
    df = pd.read_csv(ARQUIVO_DADOS, parse_dates=["data"])
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return df


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_resumo(df):
    receita_total = df["receita"].sum()
    produto_receita = df.groupby("produto")["receita"].sum().sort_values(ascending=False)
    regiao_receita = df.groupby("regiao")["receita"].sum().sort_values(ascending=False)
    mes_receita = df.groupby("mes")["receita"].sum().sort_values(ascending=False)

    produto_lider = produto_receita.index[0]
    receita_produto_lider = produto_receita.iloc[0]
    participacao = receita_produto_lider / receita_total * 100

    print("=== SALES INSIGHTS ===")
    print(f"Receita total: {formatar_moeda(receita_total)}")
    print(
        f"Produto com maior receita: {produto_lider} "
        f"({formatar_moeda(receita_produto_lider)} | {participacao:.1f}% do total)"
    )
    print(
        f"Região com maior receita: {regiao_receita.index[0]} "
        f"({formatar_moeda(regiao_receita.iloc[0])})"
    )
    print(
        f"Mês com maior receita: {mes_receita.index[0]} "
        f"({formatar_moeda(mes_receita.iloc[0])})"
    )


def salvar_grafico(serie, titulo, xlabel, ylabel, nome_arquivo):
    plt.figure(figsize=(9, 5))
    serie.plot(kind="bar")
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(PASTA_GRAFICOS / nome_arquivo, dpi=160)
    plt.close()


def gerar_graficos(df):
    PASTA_GRAFICOS.mkdir(exist_ok=True)

    receita_produto = df.groupby("produto")["receita"].sum().sort_values(ascending=False)
    receita_mes = df.groupby("mes")["receita"].sum()
    receita_regiao = df.groupby("regiao")["receita"].sum().sort_values(ascending=False)
    quantidade_produto = df.groupby("produto")["quantidade"].sum().sort_values(ascending=False)

    salvar_grafico(receita_produto, "Receita por produto", "Produto", "Receita (R$)", "receita_por_produto.png")
    salvar_grafico(receita_mes, "Receita mensal", "Mês", "Receita (R$)", "receita_mensal.png")
    salvar_grafico(receita_regiao, "Receita por região", "Região", "Receita (R$)", "receita_por_regiao.png")
    salvar_grafico(quantidade_produto, "Quantidade vendida por produto", "Produto", "Unidades", "quantidade_por_produto.png")


def main():
    df = carregar_dados()
    gerar_resumo(df)
    gerar_graficos(df)
    print(f"\nGráficos salvos em: {PASTA_GRAFICOS}")


if __name__ == "__main__":
    main()
