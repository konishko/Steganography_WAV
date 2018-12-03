# Стеганография WAV
Версия 1.00

Автор: Смольянов Данил Леонидович

## Описание
Данное приложение является утилитой, позволяющей шифровать и расшифровивать
файлы с расширением .wav стеганографией типа LSB(Least Significant Bit), а
также детектировать ее.


## Требования
* Python версии не ниже 3.4
* Cryptography версии не ниже 2.4.1


## Состав
* Основной модуль: `steg_wav.py`
* Паресер аргументов: `argument_parser.py` 
* Модули: 
    * `lsb_detector.py`
    * `operations_with_bytes_and_bits.py`
    * `operations_with_os.py`
    * `rle_modified.py`
    * `wav_parser.py`
* Тесты: 
    * `test_argparse.py`
    * `test_decoding.py`
    * `test_detector.py`
    * `test_encoding.py`
    * `test_operations_with_bytes.py`
    * `test_rle.py`


## Запуск

Пример запуска: `./python steg_wav.py -m encode_lsb -w input.wav -d data.png`

При запуске активны следующие флаги:
* `-h, --help` показывает помощь, подобную описанной здесь
  
 * `-m METHOD, --method METHOD` Метод, которым будет обработан данный wav файл
    * Список методов:
    
        * `encode_lsb` Шифрует данную информацию в заданном wav файле
        
        * `decode_lsb` Пытается расшифровать заданный wav файл
        
        * `detect_lsb`  Детектирует стеганографию типа LSB в заданном wav файле 
  
 * `-d DATA, --data DATA` Файл, который вы хотите зашифровать
 
 * `-w WAV, --wav WAV` wav файл, который вы хотите использовать
  
 * `-cc CIPHER_CODE, --cipher_code CIPHER_CODE` Файл с кодом шифра, который поможет расшифровать зашифрованный wav файл
  
 * `-z, --zip` Сжать файл
  
 * `-e, --encrypt` Зашифровать файл


## Подробности реализации
* В зависимости от от флага `--method` создается экземпляр одного из классов: 
`EncoderLSB`, `DecoderLSB`, `LSBDetector`, где и просиходит кодирование,
декодирование или детектирование стеганографии
* Сжатие происходит путем RLE кодирования
* Для шифрования используется модуль cryptography
* Используется стеганография типа LSB - Least Significant Bit, т.е. в младшие
биты байтов записываются биты шифруемой информации

## Тестирование
На данные модули написаны тесты, их можно найти в `./`.
Покрытие по строкам составляет около 92%:

    Name                        Stmts   Miss  Cover
    argument_parser.py                     36      7    81%
    lsb_detector.py                        66      2    97%
    operations_with_bytes_and_bits.py      25      0   100%
    operations_with_os.py                  16      2    88%
    rle_modified.py                        74      9    88%
    steg_wav.py                           146     21    86%
    test_argparse.py                       74      6    92%
    test_decoding.py                       26      0   100%
    test_detector.py                       17      0   100%
    test_encoding.py                       34      0   100%
    test_operations_with_bytes.py          34      0   100%
    test_rle.py                            15      0   100%
    wav_parser.py                          18      1    94%
    -------------------------------------------------------
    TOTAL                                 581     48    92%

