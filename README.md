# lss

[English](#english) | [繁體中文](#繁體中文)

## English

A Python CLI that lists the system's serial ports, including the device path,
port name, and device description. Supports Windows, macOS, and Linux.
Requires Python 3.10 or newer.

### Install

Install from PyPI with uv:

```console
uv tool install lss
```

Or with pip:

```console
python -m pip install lss
```

### Usage

```console
lss
lss USB
lss --filter "USB Serial"
lss -f com3
lss --help
```

The optional keyword performs a case-insensitive, literal substring search
across the device path, port name, and description. Use either the positional
keyword or `--filter`. Regular expressions are not interpreted.

Example output (actual information depends on the operating system):

```text
PORT  NAME  DESCRIPTION
COM3  COM3  USB Serial Device (COM3)
COM8  COM8  USB-SERIAL CH340 (COM8)
```

Results are sorted by port name in natural order, such as COM2 before COM10.
The command only discovers ports; it does not open them or test whether they
are busy. Some devices or platforms may not provide a description.

If no ports are found or no ports match, the command prints a message and exits
with code 0. Discovery failures exit with code 1; invalid arguments exit with
code 2.

### Development

```console
git clone https://github.com/codemee/lss.git
cd lss
uv sync
uv run lss
uv run python -m unittest discover -s tests -v
uv build
```

To install the local checkout as a CLI, run `uv tool install .`.
If uv's tool directory is missing from PATH, run `uv tool update-shell` and
restart your terminal.

## 繁體中文

以 Python 列出系統目前的 serial port，包含連接埠路徑、名稱與裝置描述。
使用 uv 管理環境與依賴。

## 執行

```powershell
uv sync
uv run lss
uv run lss USB
uv run lss --filter "USB Serial"
uv run lss -f com3
uv run lss --help
```

關鍵字會在連接埠路徑、名稱與描述中進行不區分大小寫的子字串比對，
不使用正規表示式。位置引數與 `--filter` 擇一使用。

輸出範例（實際資訊由作業系統提供）：

```text
PORT  NAME  DESCRIPTION
COM3  COM3  USB Serial Device (COM3)
COM8  COM8  USB-SERIAL CH340 (COM8)
```

沒有連接埠或沒有符合項目時會顯示提示，結束碼為 0；
列舉失敗時結束碼為 1，引數錯誤為 2。
此指令只列舉資訊，不會開啟連接埠。
Windows、macOS 與 Linux 的裝置描述可能不同，部分裝置不提供描述。

## 安裝成 CLI

從 PyPI 安裝（需要 Python 3.10 或更新版本）：

```powershell
uv tool install lss
```

在專案資料夾執行：

```powershell
uv tool install .
lss
lss USB
```

若 uv 提示工具目錄尚未加入 PATH，可執行 `uv tool update-shell` 後重新開啟終端機。

## 測試

```powershell
uv run python -m unittest discover -s tests -v
```
