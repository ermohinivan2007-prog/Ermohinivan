#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import Lexer, LexerError

def test_basic_tokens():
    """Тест базовых токенов"""
    lexer = Lexer('var x')
    tokens = lexer.tokens()
    assert tokens[0][0] == "VAR" and tokens[0][1] == "var"
    assert tokens[1][0] == "IDENT" and tokens[1][1] == "x"
    print("Базовые токены - проверка пройдена")

def test_strings():
    """Тест строк"""
    lexer = Lexer('"hello"')
    tokens = lexer.tokens()
    assert tokens[0][0] == "STRING" and tokens[0][1] == "hello"
    print("Строки - проверка пройдена")

def test_floats():
    """Тест дробных чисел"""
    lexer = Lexer('3.14 .5')
    tokens = lexer.tokens()
    assert tokens[0][0] == "NUMBER" and tokens[0][1] == "3.14"
    assert tokens[1][0] == "NUMBER" and tokens[1][1] == ".5"
    print("Дробные числа - проверка пройдена")

def test_dict():
    """Тест словарей"""
    lexer = Lexer('$[key "value"]')
    tokens = lexer.tokens()
    assert tokens[0][1] == "$["
    assert tokens[1][1] == "key"
    assert tokens[2][1] == "value"
    print("Словари - проверка пройдена ")

def test_comments():
    """Тест комментариев"""
    lexer = Lexer('=begin коммент =cut var x')
    tokens = lexer.tokens()
    assert tokens[0][1] == "var"
    assert tokens[1][1] == "x"
    print("Комментарии - проверка пройдена")

def test_constants():
    """Тест констант"""
    lexer = Lexer('var PI 3.14 @(PI)')
    tokens = lexer.tokens()
    assert tokens[0][1] == "var"
    assert tokens[1][1] == "PI"
    assert tokens[2][1] == "3.14"
    assert tokens[3][1] == "@("
    print("Константы - проверка пройдена")

def test_errors():
    """Тест ошибок"""
    try:
        lexer = Lexer('42') 
        lexer.tokens()
        print("Должна быть ошибка для целых чисел")
        return False
    except LexerError:
        print("Обработка ошибок - проверка пройдена ")
        return True

def run_tests():
    """Запуск всех тестов"""
    tests = [
        test_basic_tokens,
        test_strings,
        test_floats,
        test_dict,
        test_comments,
        test_constants,
        test_errors,
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"{test.__name__}: {e}")
        except Exception as e:
            print(f"{test.__name__}: {e}")

if __name__ == "__main__":
    print("Тесты лексера:")
    print("=" * 30)
    run_tests()
