# Araneus

**Araneus** is an asynchronous command-line domain reconnaissance tool written in Python. It allows users to configure external security and reconnaissance utilities, execute them against a target domain, and collect their output into a single report.

The project is designed to be extensible: users can add, edit, and remove tools without changing the source code.

---

# English

## Features

- **Asynchronous execution** — run multiple tools concurrently.
- **Custom tool configuration** — add external utilities with custom arguments.
- **Target placeholders** — automatically substitute domain names, IP addresses, and URLs.
- **Root permission handling** — mark tools that require elevated privileges.
- **Execution timeout** — prevent tools from running indefinitely.
- **Error handling** — a failed tool does not stop the entire scan.
- **Logging** — readable console output with colored log levels.
- **Report generation** — collect tool output, errors, and execution statuses into a report.

## Requirements

- Python
- External reconnaissance utilities you want to use (for example, `nmap`, `dig`, `whois`, `curl`, or `whatweb`).

Some tools may require additional system packages or elevated privileges.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Araneus.git
cd Araneus
```

Install the Python dependencies:

```bash
pip install pydantic colorlog
```

Make sure the external tools you want to use are installed and available in your system's `PATH`.

## Usage

### Start a scan

```bash
python araneus.py -d example.com
```

Run Araneus with elevated privileges:

```bash
python araneus.py --sudo -d example.com
```

The `--sudo` option requests a restart through `sudo`. It is intended for tools that require root privileges.

### Tool management

List configured tools:

```bash
python araneus.py --list-tools
```

Add a tool:

```bash
python araneus.py --add-tool "Tool Name" executable [arguments...]
```

Example:

```bash
python araneus.py --add-tool "Dig A" dig {domain} A
```

Edit a tool:

```bash
python araneus.py --edit-tool 1
```

Delete a tool:

```bash
python araneus.py --delete-tool 1
```

Tool IDs are assigned automatically when a tool is added.

## Target placeholders

Araneus supports placeholders that are automatically replaced with target information.

| Placeholder | Description | Example |
|---|---|---|
| `{domain}` | Target domain without a URL scheme | `example.com` |
| `{ip}` | Resolved IP address | `93.184.216.34` |
| `{url}` | HTTPS URL | `https://example.com` |
| `{https_url}` | HTTPS URL | `https://example.com` |
| `{http_url}` | HTTP URL | `http://example.com` |

You do not need to manually add `https://` or `http://` when using URL placeholders.

### Examples

DNS lookup:

```bash
python araneus.py --add-tool "Dig A" dig {domain} A
```

WHOIS lookup:

```bash
python araneus.py --add-tool "Whois" whois {domain}
```

Nmap scan:

```bash
python araneus.py --add-tool "Nmap" nmap -sT -sV {ip}
```

HTTP headers:

```bash
python araneus.py --add-tool "Curl HTTPS" curl -I {https_url}
```

Web technology detection:

```bash
python araneus.py --add-tool "WhatWeb" whatweb {url}
```

## Tool configuration

Tools are stored in:

```text
tools/tools.json
```

Example configuration:

```json
{
  "1": {
    "id": "1",
    "name": "Dig A",
    "executable": "dig",
    "args": [
      "{domain}",
      "A"
    ],
    "required": [
      "domain"
    ],
    "requires_root": false
  },
  "2": {
    "id": "2",
    "name": "Nmap SYN Scan",
    "executable": "nmap",
    "args": [
      "-sS",
      "-sV",
      "{ip}"
    ],
    "required": [
      "ip"
    ],
    "requires_root": true
  }
}
```

### Configuration fields

| Field | Description |
|---|---|
| `id` | Unique tool identifier |
| `name` | Display name of the tool |
| `executable` | Executable name or path |
| `args` | Command-line arguments |
| `required` | Target values required by the tool |
| `requires_root` | Whether the tool requires root privileges |

### Root privileges

Some utilities and scanning modes require elevated privileges.

For example:

- Nmap `-sS` (SYN scan) generally requires root privileges or appropriate capabilities.
- Nmap `-sT` (TCP connect scan) usually works without root privileges.

Set:

```json
"requires_root": true
```

for tools that require elevated privileges.

Without root permissions, Araneus skips these tools and continues executing the remaining ones.

Run the scan with:

```bash
python araneus.py --sudo -d example.com
```

## Reports

After a scan, Araneus generates a report in:

```text
report/
```

Reports contain:

- Tool name and ID
- Execution status
- Standard output (`stdout`)
- Error output (`stderr`)

Possible execution statuses:

| Status | Description |
|---|---|
| `SUCCESS` | Tool completed successfully |
| `FAILED` | Tool returned an error |
| `TIMEOUT` | Tool exceeded the execution timeout |
| `SKIPPED` | Tool was skipped, for example, due to missing root privileges |

## Logging

Araneus uses Python logging with colored console output.

Example:

```text
Tool Dig A ~ success
Tool NMAP ~ failed
Tool WhatWeb ~ skipped
```

## Project structure

```text
Araneus/
│
├── araneus.py
├── cli.py
├── cli_parser.py
│
├── service/
│   ├── manager.py
│   └── runner.py
│
├── tools/
│   ├── tools.py
│   ├── tool_model.py
│   └── tools.json
│
├── src/
│   ├── logger.py
│   ├── json_parser.py
│   ├── report.py
│   └── ...
│
└── report/
```

## Security notice

Araneus executes external programs configured by the user. Only add tools and commands you understand and trust.

Use Araneus only against domains, IP addresses, and systems you own or have explicit permission to test.

The `--sudo` option runs the application with elevated privileges. Use it only when necessary.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

If you find a bug or have an idea for improvement, feel free to open an issue or submit a pull request.

---

# Русская версия

## О проекте

**Araneus** — это асинхронный CLI-инструмент для разведки доменов, написанный на Python. Он позволяет настраивать внешние утилиты для анализа и сбора информации о целевом домене, запускать их и сохранять результаты в единый отчёт.

Проект спроектирован с упором на расширяемость: пользователь может добавлять, редактировать и удалять инструменты без изменения исходного кода.

## Возможности

- **Асинхронное выполнение** — одновременный запуск нескольких инструментов.
- **Пользовательская конфигурация** — добавление внешних утилит с собственными аргументами.
- **Плейсхолдеры целей** — автоматическая подстановка домена, IP-адреса и URL.
- **Управление root-правами** — возможность указать, каким инструментам нужны повышенные привилегии.
- **Таймаут выполнения** — защита от бесконечного выполнения процессов.
- **Обработка ошибок** — ошибка одной утилиты не останавливает всё сканирование.
- **Логирование** — читаемый вывод в консоль с цветными уровнями логов.
- **Генерация отчётов** — сохранение вывода, ошибок и статусов выполнения инструментов.

## Требования

- Python.
- Внешние утилиты, которые вы планируете использовать (например, `nmap`, `dig`, `whois`, `curl`, `whatweb`).

Некоторым инструментам могут потребоваться дополнительные системные пакеты или повышенные привилегии.

## Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/YOUR_USERNAME/Araneus.git
cd Araneus
```

Установите Python-зависимости:

```bash
pip install pydantic colorlog
```

Убедитесь, что необходимые внешние утилиты установлены и доступны через системный `PATH`.

## Использование

### Запуск сканирования

```bash
python araneus.py -d example.com
```

Запуск Araneus с повышенными привилегиями:

```bash
python araneus.py --sudo -d example.com
```

Параметр `--sudo` запрашивает перезапуск программы через `sudo`. Он предназначен для инструментов, которым нужны root-права.

### Управление инструментами

Посмотреть список добавленных инструментов:

```bash
python araneus.py --list-tools
```

Добавить инструмент:

```bash
python araneus.py --add-tool "Tool Name" executable [arguments...]
```

Пример:

```bash
python araneus.py --add-tool "Dig A" dig {domain} A
```

Редактировать инструмент:

```bash
python araneus.py --edit-tool 1
```

Удалить инструмент:

```bash
python araneus.py --delete-tool 1
```

При добавлении инструмента его ID назначается автоматически.

## Плейсхолдеры целей

Araneus поддерживает специальные плейсхолдеры, которые автоматически заменяются информацией о целевом домене.

| Плейсхолдер | Описание | Пример |
|---|---|---|
| `{domain}` | Домен без URL-схемы | `example.com` |
| `{ip}` | Разрешённый IP-адрес домена | `93.184.216.34` |
| `{url}` | HTTPS URL | `https://example.com` |
| `{https_url}` | HTTPS URL | `https://example.com` |
| `{http_url}` | HTTP URL | `http://example.com` |

При использовании URL-плейсхолдеров не нужно самостоятельно добавлять `https://` или `http://`.

### Примеры

DNS-запрос:

```bash
python araneus.py --add-tool "Dig A" dig {domain} A
```

WHOIS-запрос:

```bash
python araneus.py --add-tool "Whois" whois {domain}
```

Сканирование Nmap:

```bash
python araneus.py --add-tool "Nmap" nmap -sT -sV {ip}
```

Получение HTTP-заголовков:

```bash
python araneus.py --add-tool "Curl HTTPS" curl -I {https_url}
```

Определение веб-технологий:

```bash
python araneus.py --add-tool "WhatWeb" whatweb {url}
```

## Конфигурация инструментов

Конфигурация инструментов хранится в файле:

```text
tools/tools.json
```

Пример:

```json
{
  "1": {
    "id": "1",
    "name": "Dig A",
    "executable": "dig",
    "args": [
      "{domain}",
      "A"
    ],
    "required": [
      "domain"
    ],
    "requires_root": false
  },
  "2": {
    "id": "2",
    "name": "Nmap SYN Scan",
    "executable": "nmap",
    "args": [
      "-sS",
      "-sV",
      "{ip}"
    ],
    "required": [
      "ip"
    ],
    "requires_root": true
  }
}
```

### Описание полей

| Поле | Описание |
|---|---|
| `id` | Уникальный идентификатор инструмента |
| `name` | Название инструмента |
| `executable` | Имя или путь к исполняемому файлу |
| `args` | Аргументы командной строки |
| `required` | Необходимые целевые значения |
| `requires_root` | Требуются ли root-права |

### Root-права

Некоторым утилитам и режимам сканирования нужны повышенные привилегии.

Например:

- Nmap `-sS` (SYN scan) обычно требует root-прав или соответствующих capabilities.
- Nmap `-sT` (TCP connect scan) обычно работает без root-прав.

Для инструментов, которым нужны повышенные привилегии, укажите:

```json
"requires_root": true
```

Если у Araneus нет root-прав, такие инструменты будут пропущены, а остальные продолжат выполняться.

Запустить сканирование с повышенными привилегиями можно командой:

```bash
python araneus.py --sudo -d example.com
```

## Отчёты

После сканирования Araneus создаёт отчёт в директории:

```text
report/
```

Отчёт содержит:

- Название и ID инструмента.
- Статус выполнения.
- Стандартный вывод (`stdout`).
- Вывод ошибок (`stderr`).

Возможные статусы:

| Статус | Описание |
|---|---|
| `SUCCESS` | Инструмент завершился успешно |
| `FAILED` | Инструмент завершился с ошибкой |
| `TIMEOUT` | Превышено время ожидания выполнения |
| `SKIPPED` | Инструмент был пропущен, например, из-за отсутствия root-прав |



