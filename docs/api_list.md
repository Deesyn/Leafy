# Danh sách swit api

## Cách sử dụng<br>
Được dùng để đưa vào `init_variable`.<br>
Cú pháp chuẩn:

```json
{
  "init_variable": {
    "parameter": "Api" 
  }
}
```

`paramater`: là tham số bạn ghi trong hàm.<br>
`Api`: là api bạn sử dụng, xem bên dưới!

### 1. `swit.bot`
> Swit sẽ tự động gán object `commands.Bot` của discord.py vào biến của bạn.

### 2. `swit.plugin.total`
> Danh sách tất cả plugin đã load thành công và không thành công.

### 3. `swit.plugin.success`
> Danh sách tất cả plugin load thành công.

### 4. `swit.plugin.unsuccess`
> Danh sách tất cả plugin load không thành công.

### 5. `swit.permission.plugin.reload`
> Cung cấp quyền reload plugin chỉ định.
> ### 5.1 Reload
> `{parameter}.reload(plugin_name)`<br>
> `parameter`: ở đây là parameter bạn đưa vào trong `init_variable`<br>
> `plugin_name`: là tên plugin bạn muốn reload
### 6. `swit.permission.plugin.load`
> Cung cấp quyền load plugin chỉ định
> > ### 6.1 Reload
> `{parameter}.load(plugin_name)`<br>
> `parameter`: ở đây là parameter bạn đưa vào trong `init_variable`<br>
> `plugin_name`: là tên plugin bạn muốn reload