import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Read datam
df = pd.read_excel("Experiment.xlsx").drop('Location', axis=1)

# Filter on bottom substrate
bs = df[df['Position/ role'] == 'Bottom substate']

# Drop columns to exclude
bs.drop(['Volume (ul)', 'Transfer %'], axis=1, inplace=True)

# Plot correlation matrix
sns.heatmap(bs.corr(numeric_only=True), annot=True)
plt.tight_layout()
plt.show()

# Boxplots
sns.swarmplot(bs, y='Log10 LR DNAxs', x='Weight (g)')
plt.gca().spines[['right', 'top']].set_visible(False)
plt.grid(axis='y')
plt.show()

sns.swarmplot(bs, y='Log10 LR DNAxs', x='Movement (rpm) ')
plt.gca().spines[['right', 'top']].set_visible(False)
plt.grid(axis='y')
plt.show()

sns.swarmplot(bs, y='Log10 LR DNAxs', x='Duraction of contact (min)')
plt.gca().spines[['right', 'top']].set_visible(False)
plt.grid(axis='y')
plt.show()