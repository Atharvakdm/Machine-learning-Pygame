import matplotlib.pyplot as plt
import numpy as np

# Define the trigonometric function
def trig_function(x):
    return np.sin(x), np.cos(x)
    # TODO: complete the function definition
    # Hint: use np.sin() to calculate the sin of x, because np.sin(x) can handle calculating sin(x) for each item in an array.

# Generate x values
x = np.linspace((-2 * np.pi), (2 * np.pi), 400)
# Generate y values using the function
y = trig_function(x)


# Plot the function
plt.plot(x, y, label='f(x) = sin(x)','g(x) = cos(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Plot of the Function f(x) = sin(x)')
plt.legend()
plt.grid(True)
plt.show()
