#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import Lexer, Parser

def test_parse_floats():
    """Тест парсинга чисел"""
    lexer = Lexer('3.14 .5')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values == [3.14, 0.5]
    print("Парсинг чисел - пройден успешно")

def test_parse_strings():
    """Тест парсинга строк"""
    lexer = Lexer('"hello" "world"')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values == ["hello", "world"]
    print("Парсинг строк - пройден успешно")

def test_parse_dict():
    """Тест парсинга словарей - ПРАВИЛЬНЫЙ СИНТАКСИС"""
    # Синтаксис: $[key: value, key: value]
    lexer = Lexer('$[name: "John", age: 30.0]')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values[0] == {"name": "John", "age": 30.0}
    print("Парсинг словарей - пройден успешно ")

def test_parse_nested_dict():
    """Тест вложенных словарей - ПРАВИЛЬНЫЙ СИНТАКСИС"""
    lexer = Lexer('$[person: $[name: "John", age: 30.0]]')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values[0] == {"person": {"name": "John", "age": 30.0}}
    print("Вложенные словари - пройден успешно ")

def test_parse_constants():
    """Тест констант"""
    lexer = Lexer('var PI 3.14 @(PI)')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values == [3.14]
    print("Константы - пройден успешно")

def test_parse_complex():
    """Тест комплексного парсинга - ПРАВИЛЬНЫЙ СИНТАКСИС"""
    lexer = Lexer('''
        var URL "example.com"
        $[server: @(URL), port: 80.0]
    ''')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values[0]["server"] == "example.com"
    assert values[0]["port"] == 80.0
    print("Комплексный парсинг- пройден успешно ")

def test_parse_empty():
    """Тест пустого ввода"""
    lexer = Lexer('')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values == []
    print("Пустой ввод - пройден успешно")

def test_parse_simple_dict():
    """Тест простого словаря с одним элементом"""
    lexer = Lexer('$[key: "value"]')
    parser = Parser(lexer.tokens())
    values = parser.parse()
    assert values[0] == {"key": "value"}
    print("Простой словарь - пройден успешно ")

def run_tests():
    """Запуск всех тестов"""
    tests = [
        test_parse_floats,
        test_parse_strings,
        test_parse_dict,
        test_parse_nested_dict,
        test_parse_constants,
        test_parse_complex,
        test_parse_empty,
        test_parse_simple_dict,
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f" {test.__name__}: {e}")
        except Exception as e:
            print(f" {test.__name__}: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("Тесты парсера:")
    print("=" * 30)
    run_tests()
