import numpy as np

class GradientDescent:
    def __init__(self, learning_rate=0.01, max_iter=1000, tol=1e-4):
        self.lr = learning_rate      # η - скорость обучения
        self.max_iter = max_iter     # максимальное число итераций
        self.tol = tol               # точность сходимости
        self.history = []            # история значений loss
    
    def fit(self, X, y):
        """Обучение линейной регрессии"""
        m, n = X.shape
        self.theta = np.zeros(n)     # Шаг 1: инициализация
        self.bias = 0
        
        for i in range(self.max_iter):
            # Шаг 2: вычисление градиента
            predictions = X.dot(self.theta) + self.bias
            errors = predictions - y
            
            # Градиенты
            grad_theta = (1/m) * X.T.dot(errors)
            grad_bias = (1/m) * np.sum(errors)
            
            # Шаг 3: обновление параметров
            self.theta -= self.lr * grad_theta
            self.bias -= self.lr * grad_bias
            
            # Вычисление loss для проверки сходимости
            loss = np.mean(errors ** 2)
            self.history.append(loss)
            
            # Шаг 4: проверка сходимости
            if i > 0 and abs(self.history[-2] - loss) < self.tol:
                print(f"Сходимость достигнута на итерации {i}")
                break
    
    def predict(self, X):
        """Предсказание"""
        return X.dot(self.theta) + self.bias


# Пример использования
if __name__ == "__main__":
    # Генерация синтетических данных: y = 2x + 3 + шум
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    y = 2 * X.ravel() + 3 + np.random.randn(100) * 0.5
    
    # Добавляем единичный столбец для bias
    X_b = np.c_[np.ones((100, 1)), X]
    
    # Обучение
    gd = GradientDescent(learning_rate=0.1, max_iter=1000)
    gd.fit(X_b, y)
    
    print(f"Найденные параметры: θ₀={gd.bias:.3f}, θ₁={gd.theta[1]:.3f}")
    print(f"Истинные параметры: θ₀=3.0, θ₁=2.0")
    print(f"Loss на последней итерации: {gd.history[-1]:.4f}")
