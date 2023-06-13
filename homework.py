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

    def get_message(self) -> str:
        """Получить сообщение о тренировке."""
        info = (f'Тип тренировки: {self.training_type}; '
                f'Длительность:{self.duration: .3f} ч.; '
                f'Дистанция:{self.distance: .3f} км; '
                f'Ср. скорость:{self.speed: .3f} км/ч; '
                f'Потрачено ккал:{self.calories: .3f}.')
        return info


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar = 0.65
    M_IN_KM: ClassVar = 1000
    TIME_M: ClassVar = 60
    training_type: ClassVar = 'Training'
    action: int
    duration: float
    weight: float

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


@dataclass
class Running(Training):
    """Тренировка: бег."""
    training_type: ClassVar = 'Running'
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CAL_COF: int = 18
        COF_SHIFT: float = 1.79
        TIME_M: int = 60
        calories: float = (CAL_COF *
                           Training.get_mean_speed(self) +
                           COF_SHIFT) * self.weight \
                            / self.M_IN_KM \
                            * (self.duration * TIME_M)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type: ClassVar = 'SportsWalking'
    COF_COL_2: ClassVar = 0.035
    COF_2: ClassVar = 0.029
    KM_H_IN_M_C: ClassVar = 0.278
    HEIGHT_M: ClassVar = 100
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COF_COL_2: float = 0.035
        COF_2: float = 0.029
        KM_H_IN_M_C: float = 0.278
        HEIGHT_M: int = 100
        Time_m: int = 60
        speed: float = self.get_mean_speed() * KM_H_IN_M_C
        calories: float = ((COF_COL_2 * self.weight)
                           + (speed ** 2 / (self.height / HEIGHT_M))
                           * COF_2 * self.weight) * self.duration \
                           * Time_m
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar = 1.38
    SWIM_SPEED_COF: ClassVar = 1.1
    SWIM_WEIGHT_COF: ClassVar = 2
    training_type: ClassVar = 'Swimming'
    length_pool: float
    count_pool: int

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
