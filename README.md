# Отчёт по лабораторной работе №3 (обычной)
## Задание

1. Написать “плохой” CI/CD файл, который работает, но в нем есть не менее трех “bad practices” по написанию CI/CD
2. Написать “хороший” CI/CD, в котором эти плохие практики исправлены
3. В Readme описать каждую из плохих практик в плохом файле, почему она плохая и как в хорошем она была исправлена, как исправление повлияло на результат
4. Прочитать историю про Васю (она быстрая, забавная и того стоит): https://habr.com/ru/articles/689234/
5. Написать обычный отчет себе на гитхаб


## Введение

На первом курсе, в первом семестре, мы впервые столкнулись с CI/CD, когда клонировали репозиторий с шаблонами для лабораторных работ. Там уже был настроен GitHub Actions workflow, который автоматически проверял наш код. Это был наш первый опыт с автоматизацией процессов разработки. Вот этот файл:

```yaml
name: CS102 Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.11.9
      uses: actions/setup-python@v2
      with:
        python-version: '3.11.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black mypy pandas boddle pytest nltk pymorphy3 deep-translator scikit-learn
    - name: Download NLTK data
      run: |
        python -c "import nltk; nltk.download('stopwords')"
    - name: Install project dependencies
      run: |
        if [ -f ${{ github.head_ref }}/requirements.txt ];
        then
          pip install -r ${{ github.head_ref }}/requirements.txt
        fi
    - name: Run unittests
      run: |
        python -m pytest
```


Во втором семестре, работая над проектом "Классификатор спама", я  создал свой CI/CD пайплайн на основе исходного шаблона. В этой работе мы проанализируем его, найдем плохие практики, исправим их и сравним результаты.

CI/CD для этого проекта можно посмотреть [здесь](https://github.com/Mitya01/Spam_classifier/blob/development/.github/workflows/ci_cd.yml) или ниже

## 1. Исходный ("плохой") CI/CD файл


```yaml
name: CS102 Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.11.9
      uses: actions/setup-python@v2
      with:
        python-version: '3.11.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black mypy pandas boddle pytest nltk pymorphy3 deep-translator scikit-learn
    - name: Download NLTK data
      run: |
        python -c "import nltk; nltk.download('stopwords')"
    - name: Install project dependencies
      run: |
        if [ -f ${{ github.head_ref }}/requirements.txt ];
        then
          pip install -r ${{ github.head_ref }}/requirements.txt
        fi
    - name: Run unittests
      run: |
        python -m pytest
```

## 2. Улучшенный ("хороший") CI/CD файл

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python with cache
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    
    - name: Cache NLTK data
      id: cache-nltk
      uses: actions/cache@v3
      with:
        path: ~/nltk_data
        key: ${{ runner.os }}-nltk-data
        restore-keys: |
          ${{ runner.os }}-nltk-data
    
    - name: Download NLTK data if not cached
      if: steps.cache-nltk.outputs.cache-hit != 'true'
      run: |
        python -c "import nltk; nltk.download('stopwords', quiet=True)"
    
    - name: Run tests
      run: |
        python -m pytest -v
```

## 3. Анализ плохих практик и их исправление

### Плохая практика 1: Слишком широкие триггеры запуска
**Проблема:**
```yaml
on: [push, pull_request]
```
Запускается на каждый push в любую ветку, даже при изменении README.md или документации.

**Исправление:**
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```
Запускается только для ветки `main` и pull request в `main`. Экономит ресурсы CI/CD.

---

### Плохая практика 2: Устаревшие версии Actions
**Проблема:**
```yaml
uses: actions/checkout@v2
uses: actions/setup-python@v2
```
В старых версиях нет новых оптимизаций и функций безопасности.

**Исправление:**
```yaml
uses: actions/checkout@v4
uses: actions/setup-python@v4
```
Актуальные версии с лучшей производительностью и встроенным кэшированием.

---

### Плохая практика 3: Отсутствие кэширования зависимостей
**Проблема:** Каждый запуск заново скачивает все pip-пакеты (.

**Исправление:**
```yaml
cache: 'pip'
```
Автоматическое кэширование pip-пакетов между запусками.

---

### Плохая практика 4: Загрузка NLTK данных без кэширования
**Проблема:**
```yaml
- name: Download NLTK data
  run: |
    python -c "import nltk; nltk.download('stopwords')"
```
NLTK данные загружаются каждый раз, а загрузка занимает время.

**Исправление:**
```yaml
- name: Cache NLTK data
  id: cache-nltk
  uses: actions/cache@v3
  with:
    path: ~/nltk_data
    key: ${{ runner.os }}-nltk-data

- name: Download NLTK data if not cached
  if: steps.cache-nltk.outputs.cache-hit != 'true'
  run: |
    python -c "import nltk; nltk.download('stopwords', quiet=True)"
```

**Что изменилось:**
1. Добавлено кэширование NLTK данных
2. Данные загружаются только при первом запуске
3. Флаг `quiet=True` убирает лишний вывод
4. Используется `cache-hit` для условного выполнения

---

### Плохая практика 5: Ручное перечисление зависимостей
**Проблема:**
```yaml
pip install black mypy pandas boddle pytest nltk pymorphy3 deep-translator scikit-learn
```
Нет контроля версий, разные версии в разных запусках.

**Исправление:**
```yaml
pip install -r requirements.txt
```

**requirements.txt:**
```
numpy==1.26.0
pandas==2.1.4
nltk==3.8.1
pymorphy3==2.0.0
scikit-learn==1.3.2
deep-translator==1.11.4
boddle==0.2.9
```

Фиксированные версии обеспечивают воспроизводимость.

---

### Плохая практика 6: Сложная условная логика для зависимостей
**Проблема:**
```yaml
if [ -f ${{ github.head_ref }}/requirements.txt ];
then
  pip install -r ${{ github.head_ref }}/requirements.txt
fi
```
Переменная `github.head_ref` может быть не определена, сложно отлаживать.

**Исправление:** Убрана условная логика, используется единый `requirements.txt` в корне проекта.

---

### Дополнение: Ручное перечисление зависимостей

Можно было добавить параллельное выполнение jobs (parallel jobs) или разделение workflow на независимые задачи: 

```yaml
jobs:
  job's name:
    # Job 1: проверка кода
  test:
    # Job 2: запуск тестов
```

Но в данном примере CI/CD это кажется излишним

## 4. Сравнение производительности

good_ci_cd.yml

<img width="286" height="203" alt="image" src="https://github.com/user-attachments/assets/c022143d-471c-4e15-a083-8f964924a5da" />

<img width="1146" height="537" alt="image" src="https://github.com/user-attachments/assets/93cac49c-fdbe-4d4a-8133-4e71d3742ec4" />

bad_ci_cd.yml

<img width="440" height="205" alt="image" src="https://github.com/user-attachments/assets/aa0774c7-ca72-4428-b568-7f526a546432" />

<img width="1149" height="502" alt="image" src="https://github.com/user-attachments/assets/399aed6c-8956-4e03-b1dc-4ad047ce5803" />

Как и ожидалось:
-  Setup Python with cache работает быстрее, чем Set up Python 3.11.9
-  Install dependencies работает быстрее, если оптимизировать работу с requirements.txt

Кэширование замедляет работу good_ci_cd.yml, но это только в первый раз

## 5. Структура проекта

```
spam-classifier/
├── .github/
│   └── workflows/
│       ├── bad_ci_cd.yml      # Плохой пример
│       └── good_ci_cd.yml     # Хороший пример
├── requirements.txt        # Зависимости с версиями
├── tests/                  # Тесты
├── spam_classifier/        # Исходный код
└── README.md              # Документация
```

## 6. Выводы

1. **Кэширование - ключевое улучшение**: Добавление кэширования pip и NLTK данных дало наибольший прирост скорости.

2. **NLTK с кэшированием**: Вместо загрузки 35MB данных каждый раз, мы загружаем один раз и используем кэш.

3. **Простота и эффективность**: Хороший CI/CD не должен быть сложным. Небольшие изменения дали 4-5-кратное ускорение.

4. **Воспроизводимость**: Фиксированные версии зависимостей в `requirements.txt` гарантируют одинаковое поведение.

5. **Ресурсоэффективность**: Ограничение триггеров экономит ресурсы CI/CD системы.

## 7. Что я узнал

- Как использовать GitHub Actions Cache для ускорения CI/CD
- Зачем нужны файлы зависимостей с фиксированными версиями
- Как работать с большими данными (NLTK) в CI/CD
- Почему важно обновлять версии Actions
- Как сделать CI/CD быстрым без сложных настроек

Эта работа показала, что даже простые улучшения могут значительно ускорить процесс разработки и сделать его более предсказуемым.


