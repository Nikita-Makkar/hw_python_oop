from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info = ('Тип тренировки: {training_type}; '
            'Длительность:{duration: .3f} ч.; '
            'Дистанция:{distance: .3f} км; '
            'Ср. скорость:{speed: .3f} км/ч; '
            'Потрачено ккал:{calories: .3f}.')

    def get_message(self) -> str:
        """Получить сообщение о тренировке."""
        return self.info.format(training_type=self.training_type,
                                duration=self.duration,
                                distance=self.distance,
                                speed=self.speed,
                                calories=self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar = 0.65
    M_IN_KM: ClassVar = 1000
    TIME_M: ClassVar = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return None

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.TIME_M))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COF_COL_2: ClassVar = 0.035
    COF_2: ClassVar = 0.029
    KM_H_IN_M_C: ClassVar = 0.278
    HEIGHT_M: ClassVar = 100
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed() * self.KM_H_IN_M_C
        calories: float = ((self.COF_COL_2 * self.weight)
                           + (speed ** 2 / (self.height / self.HEIGHT_M))
                           * self.COF_2 * self.weight) * self.duration * self.TIME_M
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar = 1.38
    SWIM_SPEED_COF: ClassVar = 1.1
    SWIM_WEIGHT_COF: ClassVar = 2
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWIM_SPEED_COF)
                * self.SWIM_WEIGHT_COF * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type in type_training:
        return type_training[workout_type](*data)
    raise ValueError('Неизвестный тип тренировки.')


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
