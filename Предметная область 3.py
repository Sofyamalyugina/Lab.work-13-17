import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=3, metric='euclidean'):
        self.k = k
        self.metric = metric
        self.X_train = None
        self.y_train = None
    
    def fit(self, X, y):
        """Обучение - просто запоминаем данные"""
        self.X_train = np.array(X)
        self.y_train = np.array(y)
    
    def _calculate_distance(self, x1, x2):
        """Вычисление расстояния между двумя точками"""
        if self.metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        else:
            return np.sqrt(np.sum((x1 - x2) ** 2))  # по умолчанию евклидово
    
    def predict(self, X, task='classification'):
        """Предсказание для новых данных"""
        predictions = []
        
        for x in np.array(X):
            # Шаг 4: Вычисляем расстояния
            distances = []
            for x_train in self.X_train:
                dist = self._calculate_distance(x, x_train)
                distances.append(dist)
            
            # Шаг 5: Выбираем k ближайших соседей
            k_indices = np.argsort(distances)[:self.k]
            k_nearest_labels = self.y_train[k_indices]
            
            # Шаг 6: Принимаем решение
            if task == 'classification':
                # Классификация - самый частый класс
                most_common = Counter(k_nearest_labels).most_common(1)[0][0]
                predictions.append(most_common)
            else:
                # Регрессия - среднее значение
                predictions.append(np.mean(k_nearest_labels))
        
        return np.array(predictions)


# Пример использования
if __name__ == "__main__":
    # Тестовые данные: [рост, вес] -> пол (0 - жен, 1 - муж)
    X_train = np.array([[160, 55], [170, 65], [180, 80], 
                        [155, 50], [165, 60], [175, 75]])
    y_train = np.array([0, 1, 1, 0, 1, 1])  # пол
    
    # Создаем и обучаем модель
    knn = KNN(k=3)
    knn.fit(X_train, y_train)
    
    # Предсказываем для нового человека
    new_person = [[168, 62]]
    prediction = knn.predict(new_person)
    
    print(f"Новый человек: рост 168, вес 62")
    print(f"Предсказанный пол: {'Мужской' if prediction[0] == 1 else 'Женский'}")