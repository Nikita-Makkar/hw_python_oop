class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить сообщение о тренировке."""
        info = (f'Тип тренировки: {self.training_type}; '
                f'Длительность:{self.duration: .3f} ч.; '
                f'Дистанция:{self.distance: .3f} км; '
                f'Ср. скорость:{self.speed: .3f} км/ч; '
                f'Потрачено ккал:{self.calories: .3f}.')
        return info


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    TIME_M: int = 60
    training_type: str = 'Training'

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
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = Training.get_distance(self) / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = 0
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self.training_type,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    training_type: str = 'Running'
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
        CALORIES_MEAN_SPEED_SHIFT: float = 1.79
        TIME_M: int = 60
        calories: float = (CALORIES_MEAN_SPEED_MULTIPLIER *
                           Training.get_mean_speed(self) +
                           CALORIES_MEAN_SPEED_SHIFT) * self.weight / \
                          self.M_IN_KM * \
                          (self.duration * TIME_M)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type: str = 'SportsWalking'
    CALORIES_MEAN_SPEED_MULTIPLIER_2: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT_2: float = 0.029
    KM_H_IN_M_C: float = 0.278
    HEIGHT_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COF_COL_2: float = 0.035
        COF_SHIF_2: float = 0.029
        KM_H_IN_M_C: float = 0.278
        HEIGHT_M: int = 100
        Time_m: int = 60
        speed: float = self.get_mean_speed() * KM_H_IN_M_C
        calories: float = ((COF_COL_2 * self.weight)
                           + (speed ** 2 / (self.height / HEIGHT_M)) *
                           COF_SHIF_2 * self.weight) \
                          * (self.duration * Time_m)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_SPEED_COF = 1.1
    SWIM_WEIGHT_COF = 2
    training_type: str = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.get_mean_speed() + self.SWIM_SPEED_COF)
                    * self.SWIM_WEIGHT_COF * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    package: Training = type_training[workout_type](*data)
    return package


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())
    return None


if __name__ == '__main__':
    packages = [
        ('SWM', [420, 4, 20, 42, 4]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
