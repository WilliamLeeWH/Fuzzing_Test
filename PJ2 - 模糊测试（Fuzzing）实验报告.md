# PJ2 - 模糊测试（Fuzzing）实验报告

软件质量保障与测试  2023-2024春

## 一、分工情况

| 姓名 | 学号 | 工作内容 | 分工占比自评 |
| :--: | :--: | :------: | :----------: |
|      |      |          |              |
|      |      |          |              |
|      |      |          |              |
|      |      |          |              |
|      |      |          |              |
|      |      |          |              |

## 二、Mutator

`在本章中，阐述你新增的 Mutator 的代码以及实现思路，以下为示例`

1. delete_char

   ```python
   def delete_random_character(s: str) -> str:
       ...
   ```

   实现思路：这个 Mutator 是用于随机删除字符串中的某个字符...


## 三、Schedule

`在本章中，你需要阐述你新增编写的 Schedule 的实现思路,以下为示例`

1. LevelPowerSchedule

   ```python
   class LevelPowerSchedule(Schedule):
   
       def assign_energy(self, population: Sequence[Seed]) -> None:
           ...
   
   ```

   实现思路：基于种子变异的层级...

## 四、新增功能实现介绍

`介绍你们在实现将 input 动态存储本地的过程中的设计思路以及实现效果`
