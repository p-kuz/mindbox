import math
from abc import ABC, abstractmethod
from typing import Type, Dict
import unittest

# ===== Базовый абстрактный класс =====
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

# ===== Класс круга =====
class Circle(Shape):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Radius must be positive.")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

# ===== Класс треугольника =====
class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        sides = sorted([a, b, c])
        if any(side <= 0 for side in sides):
            raise ValueError("Sides must be positive.")
        if sides[0] + sides[1] <= sides[2]:
            raise ValueError("Invalid triangle sides.")
        self.a, self.b, self.c = sides

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right_triangle(self) -> bool:
        return math.isclose(self.a ** 2 + self.b ** 2, self.c ** 2, rel_tol=1e-9)

# ===== Фабрика фигур =====
class ShapeFactory:
    registry: Dict[str, Type[Shape]] = {
        'circle': Circle,
        'triangle': Triangle
    }

    @classmethod
    def create(cls, shape_type: str, *args) -> Shape:
        shape_class = cls.registry.get(shape_type.lower())
        if not shape_class:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return shape_class(*args)

# ===== Юнит-тесты =====
class TestGeometry(unittest.TestCase):
    def test_circle_area(self):
        c = Circle(1)
        self.assertAlmostEqual(c.area(), math.pi, places=5)

    def test_triangle_area(self):
        t = Triangle(3, 4, 5)
        self.assertAlmostEqual(t.area(), 6.0)

    def test_triangle_is_right(self):
        t = Triangle(3, 4, 5)
        self.assertTrue(t.is_right_triangle())

    def test_triangle_not_right(self):
        t = Triangle(4, 5, 6)
        self.assertFalse(t.is_right_triangle())

    def test_factory_circle(self):
        c = ShapeFactory.create("circle", 2)
        self.assertAlmostEqual(c.area(), math.pi * 4)

    def test_factory_triangle(self):
        t = ShapeFactory.create("triangle", 3, 4, 5)
        self.assertTrue(t.is_right_triangle())

# ===== Запуск тестов при запуске файла =====
if __name__ == "__main__":
    unittest.main()
