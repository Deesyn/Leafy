# Azurite documents<br>

Để có thể setup được plugin hoàn chỉnh đầu tiên bạn cần viết mapping.json<br>
file mapping hoàn chỉnh có dạng như sau. Cuộn xuống để xem chi tiết từng phần
```json5
{
  "name": "example",
  "description": "This is a example plugins",
  "version": "1.0.0",
  "author": "kenftr",
  "license": "MIT",
  "open_source": true,
  "module": {
    "status": {
      "start": true,
      "stop": true
    },
    "event_file_name": "event.py",
    "start_function": "on_start",
    "stop_function": "on_stop",
    "init_variable": {
      "app": "Azurite.app"
    }
  },

  "plugins_setting": {
    "enable": {
      "prefix_command_enable_list": [],
      "slash_command_enable_list": [],
      "command_group_enable_list": [],
      "events_enable_list": []
    }

  },

  "mapping": {
    "format": "Azurite-mapping-v2",
    "path": {
      "prefix_command_path": "prefix_command",
      "slash_command_path": "slash_command",
      "command_group_path": "command_group",
      "event_command_path": "event"
    },

    "prefix_command_list": [],
    "slash_command_list": [
      {
        "file_name": "ping_command.py",
        "class": "ping_command",
        "custom_mapping": {
          "enable": true,
          "path": "ping_mapping.json"
        }

      }
    ],
    "command_group_list": [],
    "events_list": []
  },

  "hooks": {
    "on_load": "on_load.py",
    "on_reload": "on_reload.py"
  },

  "require":{
    "python_version": ">=3.8",
    "potato_pc": true,
    "packages": ["discord.py",
                 "colorama"]
  },
  "orther": {
    "loader-mode": "advanced"
  }
}
```

## 🗒️ **Các thông tin cơ bản**
```json5
{
  "name": "",
  "description": "",
  "version": "1.0.0",
  "author": "",
  "license": "MIT",
  "open_source": true,
}
```
**Các key cần biết**
> **name:** Tên plugin, cần trùng với tên folder chứa plugin<br>
> **description:** Mô tả ngắn về plugin <br>
> **version:** Phiên bản plugin<br>
> **author:** Tác giả<br>
> **license:** Giấy phép
> **open_source:** Plugin có open source hay không<br>

## 📦 Module

`Module.status`: Đây là setting chứa các event khi plugin được **load** và **stop**.  
```json
{
  "start": true,
  "stop": true
}
```
**Nếu bạn bật phần này, chúng ta sẽ quan tâm đến các thiết lập bên dưới:**
```json
{
  "event_file_name": "event.py",
  "start_function": "on_start",
  "stop_function": "on_stop",
  "init_variable": {
    "app": "Azurite.app"
  }
}
```

### Giải thích

- `event_file_name:` File chứa các event start và stop.  
- `start_function:` Tên hàm sẽ được gọi khi plugin được load.  
- `stop_function:` Tên hàm sẽ được gọi khi plugin được stop.  
- `init_variable:` Các tham số cần thiết cho hàm, Azurite sẽ tự động inject khi load.

### **Ví dụ:**
```py
async def on_start(app):
    latency = app.latency() * 1000
    print(latency)
```
> Trong ví dụ trên, hàm `on_start` cần tham số `app`. Vì vậy, ta đưa app vào init_variable kèm với api bạn cần ở đây ta sử dụng `Azurite.app`.<br>

`Azurite.app` là object commands.Bot của discord.py

##  📦 Plugin Setting
```json
"plugins_setting": {
    "enable": {
      "prefix_command_enable_list": [],
      "slash_command_enable_list": [],
      "command_group_enable_list": [],
      "events_enable_list": []
    }
```
Nếu bạn đưa module vào enable_list thì chỉ có các module đó được load. Nếu không thì sẽ load toàn bộ

##  🗺️ Mapping

```json5
"mapping": {
    "format": "Azurite-mapping-v2",
    "path": {
      "prefix_command_path": "prefix_command",
      "slash_command_path": "slash_command",
      "command_group_path": "command_group",
      "event_command_path": "event"
    },

    "prefix_command_list": [],
    "slash_command_list": [
      {
        "file_name": "ping_command.py",
        "class": "ping_command",
        "custom_mapping": {
          "enable": true,
          "path": "ping_mapping.json"
        }

      }
    ],
    "command_group_list": [],
    "events_list": []
  },
```
**Thông tin các key**<br>
`format`: format của mapping. Hiện tại là `Azurite-mapping-v2`<br>
`path`: các path của module<br>
**Ví dụ**
```
example/
    ├── slash_command/
    │   └── ping_command.py
    ├── custom_mapping/
    │   └── ping_mapping.json
    └── prefix_command

```
`slash_command_path` = `slash_command` thì Azurite sẽ load các **slash command** tại `example/slash_command`
