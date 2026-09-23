"""
Atividade 5 - IDH
Abre a Tabela4.csv (IDHM por Unidade da Federação) e analisa a evolução do IDH.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "Tabela4.csv",
    sep=";",
    decimal=",",
    skiprows=1,
    encoding="latin1",
)

df = df.dropna(axis=1, how="all")
df.columns = df.columns.str.strip()

anos = [c for c in df.columns if str(c).isdigit()]
print("Formato final:", df.shape)
print(df.head())

ranking_2024 = df[["Sigla", "Estado", "2024"]].sort_values("2024", ascending=False)
print("\n=== Ranking por IDH em 2024 ===")
print(ranking_2024.to_string(index=False))

df["melhora_1991_2024"] = df["2024"] - df["1991"]
melhora_ordenada = df[["Sigla", "Estado", "1991", "2024", "melhora_1991_2024"]] \
    .sort_values("melhora_1991_2024", ascending=False)
print("\n=== Melhora do IDH entre 1991 e 2024 ===")
print(melhora_ordenada.to_string(index=False))

maior_melhora = melhora_ordenada.iloc[0]
print(
    f"\nEstado com maior melhora: {maior_melhora['Estado']} "
    f"({maior_melhora['1991']:.3f} -> {maior_melhora['2024']:.3f}, "
    f"+{maior_melhora['melhora_1991_2024']:.3f})"
)

pioraram = df[df["melhora_1991_2024"] < 0]
if pioraram.empty:
    print("\nNenhum estado teve queda no IDH entre 1991 e 2024.")
else:
    print("\nEstados em que o IDH piorou entre 1991 e 2024:")
    print(pioraram[["Sigla", "Estado", "1991", "2024", "melhora_1991_2024"]].to_string(index=False))

id_vars = [c for c in df.columns if c not in anos]
df_longo = df.melt(
    id_vars=id_vars,
    value_vars=anos,
    var_name="Ano",
    value_name="IDH",
)
df_longo["Ano"] = df_longo["Ano"].astype(int)
df_longo["IDH"] = pd.to_numeric(df_longo["IDH"], errors="coerce")
print("\n=== df_longo.head() ===")
print(df_longo.head())

mg = df_longo[df_longo["Sigla"] == "MG"].sort_values("Ano")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(mg["Ano"], mg["IDH"], marker="o", markersize=5, linewidth=2, color="#1f77b4")
ax.set_title("Evolução do IDH - Minas Gerais (1991-2024)")
ax.set_xlabel("Ano")
ax.set_ylabel("IDH")
ax.set_ylim(0.3, 0.9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("idh_minas_gerais.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(12, 7))

for sigla, grupo in df_longo.groupby("Sigla"):
    grupo = grupo.sort_values("Ano")
    ax.plot(grupo["Ano"], grupo["IDH"], marker="o", markersize=3, linewidth=1.5, label=sigla)

ax.set_title("Evolução do IDH por estado (1991-2024)")
ax.set_xlabel("Ano")
ax.set_ylabel("IDH")
ax.set_ylim(0.3, 0.9)
ax.legend(ncol=3, bbox_to_anchor=(1.02, 1), loc="upper left", title="UF")
fig.tight_layout()
fig.savefig("idh_todos_estados.png", dpi=150)
plt.close(fig)

print("\nGráficos salvos: idh_minas_gerais.png e idh_todos_estados.png")
