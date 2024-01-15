import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expit


def S_x(k, t, t_0, a, min_share=5, max_share=70):
    """S_x gives the shares of adopter using a logistic growth model (S-curve)"""
    return min_share + (max_share - min_share) * np.power(expit(-k * (t - t_0)), a)


if __name__ == "__main__":
    # Time points (e.g., days, months, years)
    t_vals = np.linspace(0, 500, 500)
    t_0 = len(t_vals) / 2

    # Solving the differential equation for our logistic growth model
    # Q = odeint(logistic_growth, Q0, t, args=(K, b))
    # Q = np.array(Q).flatten()
    N_vals = list(map(lambda t: S_x(k=0.1, t=t, t_0=t_0, a=5), t_vals))

    # Plotting
    plt.plot(t_vals, N_vals, 'r-', label='Logistic Growth Model')
    plt.xlabel('Time')
    plt.ylabel('Number of Adopters')
    plt.title('Diffusion of Innovations: Logistic Growth Model')
    plt.grid(True)
    plt.show()
