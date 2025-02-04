## EthorenllScriptProgress

一个用于解 / 封包 BGI 引擎脚本的工具


### 用法

#### progress.py

一个简单的批量解包封包脚本

##### 解包

```
python progress.py decode input_dir output_dir
```

**input_dir**：包含脚本文件的文件夹

**output_dir**：输出文件夹


##### 封包

```
python progress.py encode input_dir json_dir output_dir
```

**input_dir**：包含原始脚本文件的文件夹

**json_dir**：包含文本的json的文件夹

**output_dir**：输出目录


### EthorenllProgress.py

核心库文件

#### `decode(path: Path) -> list`

接受一个原始文件路径的Path对象，返回包含字符串的list，如有误返回空列表


返回对象格式

```
[
    {
        index: int 在列表中的位置
        offset: int 位移数据
	string: string 字符串/台词
	type: string 若为command为指令字符串，message则为字符串（台词）
     }
]
```


### `encode(orgin_file: Path,json_file: Path,output_file: Path,encode_format="UTF-8") ->bool`

将json合并到原始脚本文件，并输出一个新脚本文件

参数

| 参数            | 定义                     |
| --------------- | ------------------------ |
| `orgin_file`  | 原始文件路径             |
| `json_file`   | 译文json文件路径         |
| `output_file` | 输出文件路径（不是目录） |

成功返回`True`
