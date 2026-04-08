import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

print('✅ Bibliotecas importadas com sucesso!')

np.random.seed(42)

produtos = {
    'Dom Casmurro': ('Literatura', 35.90),
    'O Pequeno Príncipe': ('Infantil', 29.90),
    'Sapiens': ('Ciências', 54.90),
    'Python para Dados': ('Tecnologia', 89.90),
    'Clean Code': ('Tecnologia', 95.00),
    'Harry Potter Vol.1': ('Fantasia', 49.90),
    'Atomic Habits': ('Autoajuda', 44.90),
    'A Arte da Guerra': ('Filosofia', 32.00),
    'Cosmos': ('Ciências', 62.50),
    'Cem Anos de Solidão': ('Literatura', 39.90),
}

vendedores = ['Ana Lima', 'Carlos Mendes', 'Bruno Costa', 'Fernanda Rocha']
regioes = ['Sudeste', 'Sul', 'Nordeste', 'Norte', 'Centro-Oeste']
datas = pd.date_range('2024-01-01', '2024-06-30', periods=50)
nomes_prod = np.random.choice(list(produtos.keys()), 50)

dados = {
    'id_venda': range(1, 51),
    'data': datas.strftime('%Y-%m-%d'),
    'produto': nomes_prod,
    'categoria': [produtos[p][0] for p in nomes_prod],
    'quantidade': np.random.randint(1, 6, 50),
    'preco_unit': [produtos[p][1] for p in nomes_prod],
    'vendedor': np.random.choice(vendedores, 50),
    'regiao': np.random.choice(regioes, 50),
}

df = pd.DataFrame(dados)
df['total_venda'] = df['quantidade'] * df['preco_unit']
df.to_csv('vendas_livraria.csv', index=False)

print(f'✅ Dataset criado! Shape: {df.shape}')
print('Colunas:', list(df.columns))
print(df.head())

print('\n' + '='*45)
print('📋 INFORMAÇÕES DO DATASET')
print('='*45)
print(f'Linhas:   {df.shape[0]}')
print(f'Colunas:  {df.shape[1]}')

print('\n📊 TIPOS DE DADOS:')
print(df.dtypes)

print('\n🔍 VALORES NULOS:')
print(df.isnull().sum())

print('\n📈 ESTATÍSTICAS DESCRITIVAS:')
print(df[['quantidade', 'preco_unit', 'total_venda']].describe().round(2))

total = df['total_venda'].sum()
print(f'\n💰 Faturamento Total: R$ {total:,.2f}')

cat_fat = df.groupby('categoria')['total_venda'].sum().sort_values(ascending=False)
print('\n📦 Faturamento por Categoria:')
print(cat_fat.apply(lambda x: f'R$ {x:,.2f}'))

vend_rank = df.groupby('vendedor')['total_venda'].sum().sort_values(ascending=False)
print('\n🏆 Ranking de Vendedores:')
print(vend_rank.apply(lambda x: f'R$ {x:,.2f}'))

top_prod = df.groupby('produto')['quantidade'].sum().sort_values(ascending=False).head(3)
print('\n📚 Top 3 Produtos (qtd vendida):')
print(top_prod)

reg_media = df.groupby('regiao')['total_venda'].mean().round(2).sort_values(ascending=False)
print('\n🗺️ Ticket Médio por Região:')
print(reg_media.apply(lambda x: f'R$ {x:,.2f}'))

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Dashboard: Livraria 2024', fontsize=14, fontweight='bold', y=1.02)

ax1 = axes[0]
cores = ['#e84b1a' if i == 0 else '#c8bfaa' for i in range(len(cat_fat))]
ax1.barh(cat_fat.index, cat_fat.values, color=cores)
ax1.set_title('Faturamento por Categoria', fontweight='bold')
ax1.set_xlabel('Receita (R$)')
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x/1000:.0f}k'))

ax2 = axes[1]
ax2.bar(vend_rank.index, vend_rank.values, color=['#1a6ee8', '#4a90e8', '#8ab8f0', '#c8d8f0'])
ax2.set_title('Ranking de Vendedores', fontweight='bold')
ax2.set_ylabel('Total Vendido (R$)')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'R${y/1000:.0f}k'))
ax2.tick_params(axis='x', rotation=15)

ax3 = axes[2]
reg_total = df.groupby('regiao')['total_venda'].sum()
ax3.pie(reg_total, labels=reg_total.index, autopct='%1.1f%%',
        colors=['#e84b1a', '#1a6ee8', '#c9a84c', '#28a745', '#6f42c1'],
        startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax3.set_title('Participação por Região', fontweight='bold')

plt.tight_layout()
plt.savefig('dashboard_livraria.png', dpi=150, bbox_inches='tight')
plt.show()
print('✅ Gráficos salvos em dashboard_livraria.png')
