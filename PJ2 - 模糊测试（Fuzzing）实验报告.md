# PJ2 - 模糊测试（Fuzzing）实验报告

软件质量保障与测试  2023-2024春

## 一、分工情况

| 姓名 | 学号 | 工作内容 | 分工占比自评 |
| :--: | :--: | :------: | :----------: |
| 李文昊 | 21302010007 | Mutator、Schedule 编写 | 20% |
|钟杰铖 | 21302010025 | Mutator、Schedule 编写 | 20% |
| 王正     | 21302010018 | Schedule 编写 | 20% |
| 孙靖斌    | 22300240002 | Seed List 编写 | 20% |
| 张晟恺  |  21302010021 | Mutator编写、报告撰写 | 20% |

## 二、Mutator

### 1. `insert_random_character`

```python
def insert_random_character(s: str) -> str:
    i = random.randint(0, len(s))
    s = s[0:i]+chr(random.randint(32, 127))+s[i:len(s)]

    return s
```

**实现思路：**  
这个 Mutator 是用于在字符串的随机位置插入一个随机字符。实现方式是首先随机生成一个位置，然后生成一个范围在 [32, 127] 的随机字符并插入到该位置。可以模拟用户输入的随机字符插入情况。

### 2. `flip_random_bits`

```python
def flip_random_bits(s: str) -> str:
    N = 1 << random.randint(0, 2)
    ii = random.randint(0, 7)
    i = random.randint(0, len(s)-1 if ii + N <= 7 else len(s) - 2)
    if ii + N > 8:
        # s[i] = chr(ord(s[i]) ^ (1 << (7-ii)))
        s = s[:i] + chr(ord(s[i]) ^ (1 << (7-ii))) + s[i+1:]
        i += 1
        N = ii + N - 8
        ii = 0
    # s[i] = chr(ord(s[i]) ^ ((1 << (7-ii)) - 1 << (7-ii-N)))
    s = s[:i] + chr(ord(s[i]) ^ ((1 << (7-ii)) - 1 << (7-ii-N))) + s[i+1:]

    return s
```

**实现思路：**  
这个 Mutator 是用于随机翻转字符串中的一些位。实现方式是首先随机生成翻转的位数，然后随机选择一个位置，进行位翻转操作。可以模拟用户输入的随机比特翻转情况。

### 3. `arithmetic_random_bytes`

```python
def arithmetic_random_bytes(s: str) -> str:
    N = 1 << random.randint(0, 2)
    i = random.randint(0, len(s)-N)
    while N > 0:
        # s[i] = chr((ord(s[i]) + random.randint(-35, 35)) % 256)
        s = s[:i] + chr((ord(s[i]) + random.randint(-35, 35)) % 256) + s[i+1:]
        i += 1
        N -= 1

    return s
```

**实现思路：**  
这个 Mutator 是用于随机增加或减少字符串中的一些字节值。实现方式是随机选择一个位置，然后对该位置及其后面的字节值进行加减操作，使其变化在一定范围内。可以模拟用户输入的随机字节值变化情况。

### 4. `interesting_random_bytes`

```python
def interesting_random_bytes(s: str) -> str:
    interesting_values = {
        1: '.',
        2: '<>',
        4: '-<>.'
    }
    N = 1 << random.randint(0, 2)
    i = random.randint(0, len(s)-N)
    s = s[:i] + interesting_values[N] + s[i+1:]

    return s
```

**实现思路：**  
这个 Mutator 是用于将字符串中的一些字节替换为预定义的有趣值。实现方式是随机选择一个位置，然后将该位置及其后面的字节替换为有趣值，以模拟特定错误场景。

### 5. `havoc_random_insert`

```python
def havoc_random_insert(s: str) -> str:
    i = random.randint(0, len(s))
    a = random.randint(0, len(s)-1)
    b = random.randint(a, len(s))

    p = random.randint(0, 3)
    if p:
        for x in range(a, b):
            s = s[0:i]+chr(random.randint(0, 255))+s[i:len(s)]
    else:
        s = s[0:i]+s[a:b]+s[i:len(s)]

    return s
```

**实现思路：**  
这个 Mutator 是用于在字符串中随机位置插入随机内容。实现方式是随机选择插入位置，然后插入原文中的一段内容或随机生成的一段内容。可以模拟用户输入的随机插入情况。

### 6. `havoc_random_replace`

```python
def havoc_random_replace(s: str) -> str:
    i = random.randint(0, len(s))
    l = random.randint(1, len(s)-i+1)

    p = random.randint(0, 3)
    if p:
        while l > 0:
            # s[i] = chr(random.randint(0, 255))
            s = s[:i] + chr(random.randint(0, 255)) + s[i+1:]
            i += 1
            l -= 1
    else:
        _i = random.randint(0, len(s) - l)
        s = s[:i] + s[_i:_i+l] + s[i+l:]

    return s
```

**实现思路：**  
这个 Mutator 是用于随机替换字符串中的一些内容。实现方式是随机选择替换位置和长度，然后用原文中的一段内容或随机生成的一段内容进行替换。可以模拟用户输入的随机替换情况。

### 7. `my_delete_random_bytes`

```python
def my_delete_random_bytes(s: str) -> str:
    N = 1 << random.randint(0, 2)
    if len(s) < N:
        return s
    i = random.randint(0, len(s) - N)
    s = s[0:i]+s[i+N:len(s)]

    return s
```

**实现思路：**  
这个 Mutator 是用于删除字符串中的一些字节。实现方式是随机选择删除的位置和长度，然后进行删除操作。可以模拟数据丢失的情况。

### 8. `my_havoc_random_delete`

```python
def my_havoc_random_delete(s: str) -> str:
    a = random.randint(0, len(s)-1)
    b = random.randint(a, len(s))

    s = s[0:a] + s[b:len(s)]
    return s
```

**实现思路：**  
这个 Mutator 是用于在字符串中随机删除一段内容。实现方式是随机选择删除的起始位置和结束位置，然后进行删除操作。可以模拟数据丢失的情况。

### 9. `my_splice_and_reverse`

```python
def my_splice_and_reverse(s: str) -> str:
    i = random.randint(0, len(s))

    s = s[i:len(s)] + s[0:i]
    return s
```

**实现思路：**  
这个 Mutator 是用于在字符串中切出一部分内容，然后颠倒顺序并重新拼接。实现方式是随机选择一个位置，然后把前后的字符顺序颠倒地重复拼接。可以模拟数据错位的情况。

### 10. `my_splice_and_shuffle`

```python
def my_splice_and_shuffle(s: str) -> str:
    i = random.randint(1, 5)
    ii = []
    for i in range(0, i):
        ii.append(random.randint(0, len(s)))
    ii.sort()
    ii.append(0)
    ii.append(len(s))

    sub = []
    for _i in range(0, i+1):
        sub.append(s[ii[_i]:ii[_i+1]])

    _s = ""
    while len(sub):
        _s += sub.pop(random.randint(0, len(sub)-1))

    return _s
```

**实现思路：**  
这个 Mutator 是用于将字符串随机分割成多个部分，并将这些部分随机重新排列，形成一个新的字符串返回。实现方式是随机选择1到5个位置，分别切割出子字符串并储存，最后打乱顺序拼接。可以模拟数据大量错位的情况。

### 11. `my_havoc_replace_all`

```python
def my_havoc_replace_all(s: str) -> str:
    a = random.randint(0, len(s)-1)
    b = random.randint(0, len(s)-1)

    s = s.replace(s[a], s[b])
    return s
```

**实现思路：**  
这个 Mutator 是用于将输入字符串中的所有字符替换为随机生成的字符。生成的随机字符的范围是从 ASCII 码 32 到 127 之间的可打印字符。可以模拟数据字符非常不符合预期的情况。

### 12. `my_insert_interesting_clips`

```python
def my_insert_interesting_clips(s: str) -> str:
    if len(interesting_clips) == 0:
        return s

    a = random.randint(0, len(s)-1)
    b = random.randint(a, len(s))
    interesting_clips.append(s[a:b])

    i = random.randint(0, len(s))
    s = s[0:i] + \
        interesting_clips[random.randint(
            0, len(interesting_clips)-1)]+s[i:len(s)]
    
    return s
```

**实现思路：**  
该函数会在输入字符串中的随机位置插入一些预定义的有趣片段（例如 HTML 标签）。实现方式是随机选择插入位置，然后插入随机选择的一段有趣片段。可以模拟用户输入的恶意数据或特定的格式，以测试系统在处理这些特殊情况时的行为。

### 13. `my_change_lower_upper_case`

```python
def my_change_lower_upper_case(s: str) -> str:
    n = random.choice([1, 2, 4])
    i = min(n, len(s))
    if len(s) - n > 0:
        pos = random.randint(0, len(s) - n)
    else:
        pos = 0
    for i in range(i):
        char = s[pos + i]
        if char.isalpha():
            s = s[:pos + i] + char.swapcase() + s[pos + i + 1:]
    return s
```

**实现思路：**  
该函数随机选取字符串中的一些字符，并将它们的大小写互换。实现方式是先随机选择一些字符，然后使用swapcase进行大小写的互换。可以模拟用户输入出现大小写问题的情况。

### 14. `insert_html_tag`

```python
def insert_html_tag(s: str) -> str:
    tags = ['<html>', '</html>', '<body>', '</body>', '<div>', '</div>', '<p>', '</p>', '<!-- comment -->']
    tag = random.choice(tags)
    pos = random.randint(0, len(s))
    return s[:pos] + tag + s[pos:]
```

**实现思路：**  
这个 Mutator 在字符串的随机位置插入一个随机 HTML 标签。实现方式是选择一个随机位置，然后插入一个预定义的 HTML 标签。可以模拟 HTML 内容的随机插入情况。

### 16. `insert_html_attribute`

```python
def insert_html_attribute(s: str) -> str:
    attributes = [' id="random"', ' class="random"', ' style="color: red;"']
    attribute = random.choice(attributes)
    tags = ['<div', '<p', '<span', '<a']
    for tag in tags:
        if tag in s:
            pos = s.find(tag) + len(tag)
            s = s[:pos] + attribute + s[pos:]
            break
    return s
```

**实现思路：**  
这个 Mutator 在字符串中的 HTML 标签中随机插入一个属性。实现方式是在随机选择的 HTML 标签中插入一个预定义的属性。可以模拟 HTML 内容的属性插入情况。

### 18. `insert_html_entity`

```python
def insert_html_entity(s: str) -> str:
    entities = ['&amp;', '&lt;', '&gt;', '&quot;', '&#39;']
    entity = random.choice(entities)
    pos = random.randint(0, len(s))
    return s[:pos] + entity + s[pos:]
```

**实现思路：**  
这个 Mutator 在字符串的随机位置插入一个随机的 HTML 实体。实现方式是选择一个随机位置并插入一个预定义的 HTML 实体。可以模拟 HTML 内容的实体插入情况。

## 三、Schedule

1. `PathPowerSchedule`

   ```python
   class PathPowerSchedule(PowerSchedule):
       def __init__(self) -> None:
           super().__init__()
           self.path_freq = {}
           self.line_freq = {}
           self.alpla = 1
           self.beta = 100

       def update_path_freq(self, path: Set[Location]):
           path = frozenset(path)
           if path in self.path_freq:
               self.path_freq[path] += 1
               return False
           else:
               self.path_freq[path] = 1
               return True
        
       def update_line_freq(self, line: Location):
           if line in self.line_freq:
               self.line_freq[line] += 1
               return False
           else:
               self.line_freq[line] = 1
               return True

       def assign_energy(self, population: Sequence[Seed]) -> None:
           seed_freq = {}
           for seed in population:
               seed_sum = 0
               for cov in seed.coverage:
                   seed_sum += self.line_freq[cov]
               seed_freq[seed] = seed_sum / len(seed.coverage)

           for seed in seed_freq:
               seed.energy = self.beta * (1 - seed_freq[seed]/sum(seed_freq.values()))
   ```

   实现思路：`PathPowerSchedule` 基于路径频率分配能量，路径频率越低的种子获得的能量越高。通过更新路径频率和行频率来调整种子的能量分配，以提高 Fuzzing 效率。

2. `BlendPowerSchedule`

   ```python
   class BlendPowerSchedule(PowerSchedule):
       def __init__(self) -> None:
           super().__init__()
           self.paths = {}
           self.alpla = 100
           self.beta = 20
           self.gamma = 5
           self.delta = 2
           self.fails = []
           self.time = {}

       def update_path_freq(self, path: Set[Location]):
           path = frozenset(path)
           if path in self.paths:
               self.paths[path] += 1
               return False
           else:
               self.paths[path] = 1
               return True

       def assign_energy(self, population: Sequence[Seed]) -> None:
           for seed in population:
               if len(seed.data) <= 1:
                   seed.energy = 0
                   continue
               seed.energy = 1.0

               path_freq = self.paths[frozenset(seed.coverage)] / sum(self.paths.values())

               if seed.data in self.fails:
                   seed.energy *= math.exp(self.gamma)
               else:
                   seed.energy *= math.exp(-self.delta * path_freq)

               seed.energy *= self.alpla * self.time[seed.data]/len(seed.data)
               try:
                   seed.energy *= math.log(self.beta, len(seed.data))
               except:
                   print(self.beta, len(seed.data))
   ```

   实现思路：`BlendPowerSchedule` 结合了路径频率、失败次数和种子处理时间等因素来分配能量。失败次数越多、处理时间越长、路径频率越低的种子获得的能量越高。

## 四、新增功能实现介绍

### Seed List 磁盘持久化操作
1. **种子管理：** 每个种子都包含数据、覆盖范围和路径信息。我们将种子数据保存在本地文件中，并通过路径进行管理。
2. **文件存储：** 使用 `dump_object` 和 `load_object` 函数进行种子的序列化和反序列化操作，以便在需要时将种子加载到内存中。
3. **日志记录：** 为了确保每次操作都有记录，我们使用 `logging` 模块记录种子的保存和加载操作。

以下是代码实现：

```python
logging.basicConfig(filename=os.path.join('logs', 'seeds_persistence.log'), filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class Seed:
    """Represent an input with additional attributes"""

    def __init__(self, data: str, _coverage: Set[Location], path: str = None, directory: str = './seeds') -> None:
        """Initialize from seed data"""
        self.energy = 0.0
        self.data = data
        if data is not None:
            self.id = get_md5_of_object(data)
            self.path = path if path else os.path.join(directory, f"{self.id}.seed")
            self.save(data, _coverage)
            self.coverage: Set[Location] = _coverage
        else:
            self.id = None
            self.path = path

    def __str__(self) -> str:
        data = self.load_data()
        return data if data else ''

    __repr__ = __str__

    def save(self, data: str, coverage: Set[Location], directory: str = './seeds') -> None:
        dump_object(self.path, {
            'data': data,
            'coverage': coverage
        })
        logger.info(f"Seed saved to {self.path}")

    def load_data(self) -> str:
        if not os.path.exists(self.path):
            logger.warning("Seed path is not set. Nothing to load.")
            raise (FileNotFoundError(f"Seed file not found: {self.path}"))
            return None
        seed = load_object(self.path)
        data = seed['data']
        logger.info(f"Seed data loaded from {self.path}")
        if data:
            return data
        else:
            return self.data

    def load_coverage(self) -> str:
        if not os.path.exists(self.path):
            logger.warning("Nothing to be loaded.")
            raise (FileNotFoundError(f"Seed not found: {self.path}"))
            return None
        seed = load_object(self.path)
        coverage = seed['coverage']
        logger.info(f"Seed coverage loaded from {self.path}")
        return coverage
```

### 测试结果

在对 Sample Programs 进行 Fuzzing 测试的结果：

1. **Sample 1**
   Crashes:
   Covered Lines:
2. **Sample 2**
   Crashes:
   Covered Lines:
3. **Sample 3**
   Crashes:
   Covered Lines:
4. **Sample 4**
   Crashes:
   Covered Lines: