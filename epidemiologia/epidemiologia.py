import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Função para o modelo SIR
def sir_model(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N  # Taxa de variação dos suscetíveis
    dIdt = beta * S * I / N - gamma * I  # Taxa de variação dos infectados
    dRdt = gamma * I  # Taxa de variação dos recuperados
    return [dSdt, dIdt, dRdt]

# Parâmetros
N = 1000    # População total
I0 = 1      # Infectados iniciais
R0 = 0      # Recuperados iniciais
S0 = N - I0 # Suscetíveis iniciais

# Entrada de taxas pelo usuário
beta = float(input("Digite a taxa de transmissão (beta): "))   # Exemplo: 0.2
gamma = float(input("Digite a taxa de recuperação (gamma): ")) # Exemplo: 0.1

# Vetor de condições iniciais
y0 = [S0, I0, R0]

# Intervalo de tempo (dias)
t = np.linspace(0, 160, 200)

# Resolver EDOs
solution = odeint(sir_model, y0, t, args=(N, beta, gamma))
S, I, R = solution.T

# Plot dos resultados
plt.figure(figsize=(10, 6))
plt.plot(t, S, 'b', label='Suscetíveis')
plt.plot(t, I, 'r', label='Infectados')
plt.plot(t, R, 'g', label='Recuperados')
plt.xlabel('Tempo (dias)')
plt.ylabel('População')
plt.title('Modelo SIR')
plt.legend()
plt.grid(True)
plt.show()

# quanto a análise de redes sociais esse modelo poderia ser aplicado para
# o espalhamento de uma fake news por exemplo, se considerado que para se
# recuperar a pessoa precisa desacreditar da mensagem. 