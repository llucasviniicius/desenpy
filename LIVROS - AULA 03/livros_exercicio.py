from pathlib import Path
import pandas as pd

def carregar_dataset(path: Path) -> pd.DataFrame:
    """Carrega o dataset livros.csv usando separador ponto-e-vírgula."""
    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}. Coloque 'livros.csv' na mesma pasta deste script."
        )
    return pd.read_csv(path, sep=';')

def analisar_estrutura(df: pd.DataFrame) -> None:
    """Imprime informações de estrutura do DataFrame."""
    print('=== 5 PRIMEIRAS LINHAS ===')
    print(df.head(), '\n')

    print('=== INFORMAÇÕES DO DATAFRAME ===')
    print(df.info(), '\n')

    print('=== ESTATÍSTICAS DESCRITIVAS ===')
    print(df.describe(include='all'), '\n')

    print('=== NULOS POR COLUNA ===')
    print(df.isnull().sum(), '\n')

def exercicio_nivel_1(df: pd.DataFrame) -> None:
    """Responde aos desafios do Nível 1."""
    print('=== NÍVEL 1: EXPLORAÇÃO ===')

    livros_zero = df[df['paginas'] == 0]
    print('Livros com 0 páginas:', len(livros_zero))
    if not livros_zero.empty:
        print(livros_zero, '\n')
    else:
        print('Nenhum livro com 0 páginas encontrado.\n')

    livros_por_ano = df['ano'].value_counts(dropna=False).sort_index()
    print('=== QUANTIDADE DE LIVROS POR ANO ===')
    print(livros_por_ano, '\n')

def criar_faixa_paginas(coluna: pd.Series) -> pd.Series:
    """Cria categoria de faixa de páginas para cada valor."""
    return coluna.apply(
        lambda x: 'Curto' if x < 150 else ('Médio' if x <= 350 else 'Longo')
    )

def exercicio_nivel_2(df: pd.DataFrame) -> pd.DataFrame:
    """Responde aos desafios do Nível 2 e retorna df_limpo."""
    print('=== NÍVEL 2: TRANSFORMAÇÃO E LIMPEZA ===')

    total_original = len(df)
    df_limpo = df[df['paginas'] > 0].copy()
    removidos = total_original - len(df_limpo)
    print(f'Registros removidos (paginas == 0): {removidos}')

    mediana_ano = df_limpo['ano'].median()
    print(f'Mediana de ano usada para preenchimento: {mediana_ano}')

    df_limpo['ano'] = df_limpo['ano'].fillna(mediana_ano).astype(int)

    df_limpo['faixa_paginas'] = criar_faixa_paginas(df_limpo['paginas'])

    df_limpo['decada'] = (df_limpo['ano'] // 10) * 10

    print('Colunas adicionais criadas: faixa_paginas, decada\n')
    return df_limpo

def exercicio_nivel_3(df_limpo: pd.DataFrame) -> None:
    """Responde aos desafios do Nível 3 e exporta o resultado."""
    print('=== NÍVEL 3: ANÁLISE AVANÇADA ===')

    media_paginas_decada = (
        df_limpo.groupby('decada')['paginas']
        .mean()
        .sort_index()
    )
    print('=== MÉDIA DE PÁGINAS POR DÉCADA ===')
    print(media_paginas_decada, '\n')

    top_autores = df_limpo['autor'].value_counts().head(10)
    print('=== TOP 10 AUTORES COM MAIS LIVROS ===')
    print(top_autores, '\n')

    distribuicao_pos_2010 = (
        df_limpo[df_limpo['ano'] > 2010]['faixa_paginas']
        .value_counts()
    )
    print('=== DISTRIBUIÇÃO DE faixa_paginas PARA LIVROS APÓS 2010 ===')
    print(distribuicao_pos_2010, '\n')
    arquivo_saida = Path('livros_analisados.xlsx')
    df_limpo.to_excel(arquivo_saida, index=False)
    print(f'Arquivo exportado: {arquivo_saida.resolve()}\n')

def main() -> None:
    arquivo = Path(__file__).parent / 'livros.csv'

    try:
        df = carregar_dataset(arquivo)
    except FileNotFoundError as exc:
        print(exc)
        return

    analisar_estrutura(df)
    exercicio_nivel_1(df)
    df_limpo = exercicio_nivel_2(df)
    exercicio_nivel_3(df_limpo)

if __name__ == '__main__':
    main()


#lucas : python3.13.exe livros_exercicio.py