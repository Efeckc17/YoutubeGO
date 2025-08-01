# 🎶 YoutubeGO 5.0 🎥

<div align="center">
  <img src="assets/banner.png" alt="YoutubeGO Logo" width="650"/>
  
  ### Современный загрузчик с расширенными возможностями
  
  [![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
  [![yt-dlp](https://img.shields.io/badge/Downloader-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
  [![requests](https://img.shields.io/badge/HTTP-requests-2496ED?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/requests/)
  [![FFmpeg](https://img.shields.io/badge/External-FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
</div>

## 📋 Содержание
- [Возможности](#-основные-возможности)
- [Установка](#-установка)
- [Использование](#-использование)
- [скриншот](showcase/showcase.md)
- [Участие в разработке](#-вклад-в-проект)
- [Лицензия](#-правовая-информация)
- [Структура проекта](#-структура-проекта)

## 🛠️ Технологический стек

### 📊 Статистика проекта
[![Code size](https://img.shields.io/github/languages/code-size/Efeckc17/YoutubeGO?style=for-the-badge&color=blueviolet)](https://github.com/Efeckc17/YoutubeGO)
[![Last commit](https://img.shields.io/github/last-commit/Efeckc17/YoutubeGO?style=for-the-badge&color=blue)](https://github.com/Efeckc17/YoutubeGO/commits)
[![Stars](https://img.shields.io/github/stars/Efeckc17/YoutubeGO?style=for-the-badge&color=yellow)](https://github.com/Efeckc17/YoutubeGO/stargazers)
[![Forks](https://img.shields.io/github/forks/Efeckc17/YoutubeGO?style=for-the-badge&color=orange)](https://github.com/Efeckc17/YoutubeGO/network/members)
[![GitHub release (latest by tag)](https://img.shields.io/github/v/tag/Efeckc17/YoutubeGO?style=for-the-badge&color=green&label=latest)](https://github.com/Efeckc17/YoutubeGO/releases)
[![Downloads](https://img.shields.io/github/downloads/Efeckc17/YoutubeGO/total?style=for-the-badge&color=brightgreen&label=downloads)](https://github.com/Efeckc17/YoutubeGO/releases)
### 📜 Правовая информация 
[![License](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=gnu&logoColor=white)](LICENSE)

### 📜 Лицензия Qt/PySide6

Пожалуйста, ознакомьтесь с [QtLicense.md](QtLicense.md) для получения полной информации о соответствии LGPL-3.0 в отношении PySide6 (Qt).

### 🌐 Ссылки
[![Сайт](https://img.shields.io/badge/Посетить-Сайт-1DA1F2?style=for-the-badge&logo=web&logoColor=white)](https://youtubego.org)
[![Discord](https://img.shields.io/badge/Присоединиться-Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/p4xYhqFwPR)

## 🌐 Языки

 | 🇬🇧 [English](README.md)

## 🌟 Основные возможности

### 🎯 Основные функции
- **Поддержка нескольких платформ**  
  Загружайте видео и аудио с платформ, поддерживающих HTTP-потоки, включая YouTube, Vimeo и другие.

- **Умная организация плейлистов**  
  Автоматически организует загрузки плейлистов в отдельные папки, названные в соответствии с названием плейлиста.

- **Загрузка плейлистов**  
  Сохраняйте целые плейлисты с последовательной обработкой всего за несколько кликов.

- **Несколько форматов**  
  Загрузка в форматах **MP4** (видео) и различных аудио форматах (**MP3**, **M4A**, **WAV**, **AAC**, **FLAC**, **OPUS**, **VORBIS**).

- **Поддержка высокого разрешения**  
  Поддерживает загрузку до **8K, 4K, 2K, 1080p, 720p, 360p**. Выберите предпочтительное разрешение в Настройках.

- **Модульная кодовой база**  
  Код полностью реорганизован в директории `core/`, `ui/` и `tests/` для более удобного обслуживания и внесения изменений.

### 🛠️ Расширенные функции
- **Пакетная обработка**  
  Очередь нескольких загрузок и управление ими одновременно. Легко приостанавливайте, возобновляйте или отменяйте загрузки.

- **Управление профилем**  
  Сохраняйте предпочтительные настройки, включая имя пользователя, фотографию профиля, пути загрузки, разрешения видео и аудио форматы.

- **Импорт/Экспорт профиля**  
  Легко экспортируйте свой профиль, настройки, историю и фотографию профиля в виде одного ZIP-файла и импортируйте их обратно в приложение на любом устройстве. Отлично подходит для резервного копирования, миграции или восстановления настроек.

- **Интерфейс Drag & Drop**  
  Добавляйте URL-адреса для загрузки, перетаскивая их в приложение.

- **Интеграция с системным треем**  
  Приложение работает в системном трее при сворачивании с быстрым доступом к меню для восстановления или выхода из приложения.

- **Улучшенная система загрузки**  
  Повышенная стабильность и эффективность с лучшей поддержкой загрузки больших файлов и множественных одновременных загрузок.

- **Оптимизация системы очередей**  
  Управление параллелизмом с функцией приостановки и возобновления всех загрузок и поддержкой ограничения пропускной способности через настройки прокси.

### 🎨 Пользовательский опыт
- **Темная и светлая темы**  
  Переключение между темной и светлой темами для лучшей удобства использования.

- **Обработка ошибок**  
  Отображение подробных журналов ошибок для отладки проблем.

- **Планировщик**  
  Планирование загрузок на определенную дату и время.

- **История загрузок**  
  Просмотр, поиск и управление предыдущими загрузками прямо в приложении.

- **Улучшенная система уведомлений**  
  Уведомления о завершении загрузки, предупреждения о сбоях загрузки и отмене загрузки.

- **Улучшенный интерфейс**  
  Лучшие анимации и отзывчивость интерфейса с цветовой кодировкой сообщений журнала и опциями поиска и фильтрации в истории и очереди.

### 🔧 Технические функции
- **Обнаружение FFmpeg**  
  Автоматическое обнаружение установки FFmpeg и запрос на настройку при отсутствии.

## ⚙️ Установка

### Windows
- Скачайте последний `.exe` установщик или `.zip` архив со страницы [Releases](https://github.com/Efeckc17/YoutubeGO/releases)
- Оба пакета включают все зависимости, включая FFmpeg
- Запустите установщик или распакуйте `.zip` и запустите `YoutubeGO.exe`

### macOS
- Скачайте последний `.dmg` пакет со страницы [Releases](https://github.com/Efeckc17/YoutubeGO/releases)
- Установите FFmpeg с помощью [Homebrew](https://brew.sh):
  ```bash
  brew install ffmpeg
  ```
- Смонтируйте `.dmg` файл и перетащите YoutubeGO в папку Applications

### Linux
- Скачайте последний `.AppImage` со страницы [Releases](https://github.com/Efeckc17/YoutubeGO/releases)
- Установите FFmpeg с помощью вашего пакетного менеджера:
  ```bash
  # Ubuntu/Debian
  sudo apt install ffmpeg

  # Fedora
  sudo dnf install ffmpeg

  # Arch Linux
  sudo pacman -S ffmpeg
  ```
- Сделайте AppImage исполняемым:
  ```bash
  chmod +x YoutubeGO.AppImage
  ```
- Запустите AppImage

### Из исходного кода
- Python 3.7 или выше (только при запуске из исходного кода)
- FFmpeg (для обработки аудио/видео)
- Git (для клонирования репозитория)

### Быстрый старт
```bash
# Клонировать репозиторий
git clone https://github.com/Efeckc17/YoutubeGO.git
cd YoutubeGO

# Убедитесь, что установлен Python 3.7+
python --version

# Установить зависимости
pip install -r requirements.txt

# Установить FFmpeg для обработки аудио и видео
winget install FFmpeg
```

## 🔧 Использование

### Базовое использование
```bash
# Запустить приложение
python main.py
```

### Использование основных функций
- Настройте свой профиль на странице **Настройки** или **Профиль**
- Используйте страницы MP4 или MP3 для загрузки видео или извлечения аудио
- Добавляйте несколько загрузок в очередь и управляйте ими со страницы Очередь
- Планируйте загрузки заранее с помощью Планировщика

### Советы и рекомендации
- Используйте перетаскивание для быстрого добавления URL
- Включите системный трей для работы в фоновом режиме
- Используйте планировщик для загрузок в нерабочее время
- Экспортируйте свой профиль для легкой миграции

## ⚠️ Примечания

### Требования
```bash
# Требуется FFmpeg
# Некоторые функции, такие как извлечение аудио и объединение видео, зависят от FFmpeg.
# Убедитесь, что он установлен и доступен в системном PATH.

# Сторонние библиотеки
# Приложение использует yt_dlp для загрузки и извлечения метаданных.
# Подробности смотрите на их странице GitHub.
https://github.com/yt-dlp/yt-dlp
```

## 🙏 Вклад в проект

### Как внести свой вклад
```bash
# Мы приветствуем вклад в улучшение YoutubeGO 5.0.
# Пожалуйста, отправляйте проблемы или запросы на включение через GitHub.

# Наслаждайтесь использованием YoutubeGO 5.0!
🚀
```

### Настройка для разработки
1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите свои изменения
4. Отправьте pull request

## ⚠️ Юридическое уведомление

YoutubeGO - это независимый проект с открытым исходным кодом. Он работает независимо от YouTube и Google, выполняя загрузки и другие операции без использования их API. Этот проект не связан условиями обслуживания или правилами YouTube.

---

<div align="center">
  <sub>Создано с ❤️ от <a href="https://github.com/Efeckc17">Efeckc17</a></sub>
</div>
