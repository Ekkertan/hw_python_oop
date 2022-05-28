from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE = ('Тип тренировки: {training_type}; '
                        'Длительность: {duration:.3f} ч.; '
                        'Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; '
                        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает информационное сообщение о тренировке."""
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           duration,
                           distance,
                           speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""

    coeff_cal_1: float = 18.0
    coeff_cal_2: float = 20.0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Рассчитывается по формуле
        (18 * mean_speed - 20) * weight / M_IN_KM * duration_in_minutes.
        """
        mean_speed = self.get_mean_speed()
        minutes = self.duration * self.MIN_IN_HOUR
        calories_per_kilo = (self.coeff_cal_1 * mean_speed - self.coeff_cal_2)
        return calories_per_kilo * self.weight / self.M_IN_KM * minutes


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_1: float = 0.035
    coeff_2: float = 0.029
    speed_pow: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Рассчитывается по формуле
        (0.035 * weight + (mean_speed**2 // height) * 0.029 * вес) * duration.
        """
        minutes = self.duration * self.MIN_IN_HOUR
        mean_speed = self.get_mean_speed()
        speed_to_height = mean_speed**self.speed_pow // self.height
        cal_by_kilo = (self.coeff_1 + speed_to_height * self.coeff_2)
        by_minutes = self.weight * cal_by_kilo
        result = by_minutes * minutes
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    ADD_COEFF: float = 1.1
    SPEED_COEFF: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        total_length = self.length_pool * self.count_pool
        return total_length / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Рассчитывается по формуле
        (mean_speed + 1.1) * 2 * weight.
        """
        mean_speed = self.get_mean_speed()
        return (mean_speed + self.ADD_COEFF) * self.SPEED_COEFF * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    traning_classes_map: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    traning_class = traning_classes_map[workout_type]
    return traning_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info_message = info.get_message()
    print(info_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
