## Class: Loader

| Thuộc tính | Kiểu | Ghi chú |
|-----------|------|---------|
| app | Optional[commands.Bot] | Instance bot Discord truyền vào loader |
| multi_thread | bool | Cài đặt loader: bật tắt đa luồng |
| max_thread | int | Số luồng tối đa |
| timeout | int | Thời gian timeout của loader |
| allow_prefix | bool | Cho phép load prefix commands |
| allow_slash | bool | Cho phép load slash commands |
| allow_group | bool | Cho phép load command groups |
| allow_events | bool | Cho phép load events |
| allowed_formats | list | Danh sách định dạng plugin được phép |
| script_loader_enabled | bool | Bật/tắt script loader |
| disabled_scripts | list | Danh sách script bị tắt |
| prefix_path | str | Đường dẫn prefix commands (set trong _load_plugin) |
| slash_path | str | Đường dẫn slash commands (set trong _load_plugin) |
| event_path | str | Đường dẫn event commands (set trong _load_plugin) |
| command_group_path | str | Đường dẫn command group commands (set trong _load_plugin) |
| prefix_commands | list | Danh sách prefix commands (set trong _load_plugin) |
| slash_commands | list | Danh sách slash commands (set trong _load_plugin) |
| event | list | Danh sách events (set trong _load_plugin) |
| group_commands | list | Danh sách command groups (set trong _load_plugin) |
| packages_list | list | Danh sách package cần tải về/load (set trong _load_plugin) |

### Phương thức:

| Phương thức | Tham số | Biến nội bộ | Ghi chú |
|-------------|---------|------------|---------|
| `__init__` | `app` | Không có | Khởi tạo instance loader và đọc cấu hình từ Config |
| `_load_plugin` | `plugin_name: str`, `plugin_object` | `mapping`, `mapping_config`, `mapping_paths`, `tasks` | Async method load một plugin: prefix/slash/events/group |
| `start_loader` | Không có | `plugin_list`, `len_plugin_list`, `data`, `total_thread`, `plugin_per_thread`, `file_path` | Async method bắt đầu load tất cả plugin, xử lý zip/rar/folder, hỗ trợ đa luồng |

## Function: _load_plugin

| Tham số | Kiểu | Ghi chú |
|---------|------|---------|
| plugin_name | str | Tên plugin cần load |
| plugin_object | Any | Đối tượng plugin (thường giống tên hoặc thư mục) |

| Biến nội bộ | Kiểu | Ghi chú |
|------------|------|---------|
| mapping | dict | Thông tin mapping các lệnh và event |
| mapping_config | Config.Mapping | Object config để kiểm tra định dạng plugin |
| mapping_paths | dict | Đường dẫn cho các lệnh/event/group |
| tasks | list | Danh sách async tasks load plugin |

**Ghi chú:**  
Function async load một plugin:  
- Load prefix commands  
- Load slash commands  
- Load events  
- Load command groups  

Kiểm tra định dạng plugin và phiên bản Python, tải các package cần thiết và chạy tasks song song nếu fast_module bật.


## function: start_loader

| Tham số | Kiểu | Ghi chú |
|---------|------|---------|
| Không có | - | Không có tham số, dùng thuộc tính của Loader |

| Biến nội bộ | Kiểu | Ghi chú |
|------------|------|---------|
| plugin_list | list | Danh sách tên plugin trong thư mục plugin |
| len_plugin_list | int | Số plugin được phát hiện |
| data | dict | Dữ liệu tính toán đa luồng (total_thread, plugin_per_thread) |
| total_thread | int | Tổng số luồng tính toán |
| plugin_per_thread | int | Số plugin mỗi luồng |
| file_path | str | Đường dẫn tuyệt đối của plugin đang load |

**Ghi chú:**  
function async load tất cả plugin từ thư mục plugin:  
- In cây thư mục plugin  
- Hỗ trợ load đa luồng  
- Phát hiện loại plugin: zip, rar, thư mục  
- Gọi `_load_plugin` cho từng plugin
