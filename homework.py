class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def __str__(self):
        return self.get_message()


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    # Константа, содержащая длину одного шага в метрах.
    M_IN_KM: float = 1000
    # Константа, содержащая количество метров в километре.
    MIN_IN_H: float = 60
    # Константа, содержащая количество минут в часе.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return (distance)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return (speed)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Функция не реализована')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           distance,
                           speed,
                           calories
                           )
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    # Множитель скорости для расчета калорий в формуле бега.
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    # Слагаемое скорости для расчета калорий в формуле бега.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.training_type = 'Running'
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return (distance)

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                    + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                    / self.M_IN_KM * self.duration * self.MIN_IN_H)
        return (calories)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_WEIGHT_MULTIPLIER: float = 0.035
    # Первый множитель скорости для расчета калорий в формуле хотьбы.
    SECOND_WEIGHT_MULTIPLIER: float = 0.029
    # Второй множитель скорости для расчета калорий в формуле хотьбы.
    SPEED_KM_H_TO_M_S: float = 0.278
    # Множитель для перевода километров в час в метры в секунду.
    SM_IN_M: float = 100
    # Количество сантиметров в метре.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        self.training_type = 'SportsWalking'
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        calories = ((self.FIRST_WEIGHT_MULTIPLIER * self.weight
                    + (((speed * self.SPEED_KM_H_TO_M_S)**2)
                     / (self.height / self.SM_IN_M))
                     * self.SECOND_WEIGHT_MULTIPLIER * self.weight)
                    * (self.duration * self.MIN_IN_H))
        return (calories)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    # Константа, содержащая длину одного гребка в метрах.
    SPEED_SHIFT_SWIMMING: float = 1.1
    # Слагаемое для расчета калорий при плавании.
    SPEED_MULTIPLIER_SWIMMING: float = 2
    # Множитель для расчета калорий при плавании.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        self.training_type = 'Swimming'
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return (distance)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration)
        return (speed)

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        calories = ((speed + self.SPEED_SHIFT_SWIMMING)
                    * self.SPEED_MULTIPLIER_SWIMMING * self.weight
                    * self.duration)
        return (calories)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type in training_type:
        return training_type[workout_type](*data)
    else:
        raise ValueError('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
