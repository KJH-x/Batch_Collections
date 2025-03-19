import numpy as np


def generate_linear_system(A_size, x):
    A = np.random.rand(*A_size)  # Generate random matrix A

    # Check if matrix A is full rank
    while np.linalg.matrix_rank(A) < A_size[0]:
        # If not full rank, regenerate a row that is linearly dependent
        A[np.random.randint(0, A_size[0])] = np.random.rand(*A_size)

    b = np.dot(A, x)  # Calculate b from Ax
    return A, b

# Example usage:
A_size = (10, 10)  # Size of the matrix A
x = np.array([40,2,5,7,100,25,86,97,33,62])  # Predefined array x
A, b = generate_linear_system(A_size, x)
print("Matrix A:")
print(A)
print("Array b:")
print(b)