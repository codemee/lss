# lss

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
