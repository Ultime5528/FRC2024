# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/drivesquares.py         |       28 |       16 |        8 |        0 |     33% |13-17, 20, 23-32, 35, 38 |
| commands/climber/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/extendclimber.py     |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/forceresetclimber.py |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/climber/lockratchet.py       |       19 |        0 |        0 |        0 |    100% |           |
| commands/climber/retractclimber.py    |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/unlockratchet.py     |       21 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/\_\_init\_\_.py   |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py          |       63 |       11 |        6 |        2 |     78% |16, 20-23, 45-59, 62, 104 |
| commands/drivetrain/drivedistance.py  |       41 |       26 |        4 |        0 |     33% |17-26, 29-37, 46-61, 64, 67 |
| commands/intake/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/drop.py               |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/load.py               |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/pickup.py             |       22 |        0 |        2 |        0 |    100% |           |
| commands/pivot/forceresetpivot.py     |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/pivot/movepivot.py           |       49 |        0 |       16 |        3 |     95% |10->exit, 16->exit, 28->exit |
| commands/pivot/resetpivotdown.py      |       19 |        0 |        2 |        0 |    100% |           |
| commands/pivot/resetpivotup.py        |       19 |        7 |        2 |        0 |     57% |13, 16-20, 23, 26 |
| gyro.py                               |      122 |       50 |       14 |        5 |     60% |19, 28->exit, 31->exit, 34->exit, 37->exit, 43, 49-51, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 114, 122, 126, 131-135, 138, 141, 144, 147, 152-161, 164, 167, 170-171, 174-175, 178, 181 |
| ports.py                              |       25 |        0 |        0 |        0 |    100% |           |
| properties.py                         |       71 |       71 |       24 |        0 |      0% |     1-141 |
| robot.py                              |       89 |        3 |       10 |        3 |     94% |137, 142, 151 |
| subsystems/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                 |      128 |        3 |       63 |        8 |     94% |19->exit, 22->exit, 25->exit, 28->exit, 31->exit, 34->exit, 37->exit, 77->exit, 123, 149, 152 |
| subsystems/drivetrain.py              |       96 |        7 |        4 |        2 |     91% |97->exit, 116, 136, 148, 154-163 |
| subsystems/intake.py                  |       39 |        1 |        2 |        1 |     95% |28->exit, 54 |
| subsystems/pivot.py                   |       85 |        6 |       18 |        4 |     90% |33->exit, 45-46, 64, 80, 110, 113 |
| tests/climber\_test.py                |       74 |        0 |       18 |        0 |    100% |           |
| tests/intake\_test.py                 |       74 |        0 |       16 |        0 |    100% |           |
| tests/pivot\_test.py                  |       59 |        3 |       12 |        1 |     94% |     26-28 |
| tests/pyfrc\_test.py                  |        1 |        0 |        0 |        0 |    100% |           |
| tests/switch\_test.py                 |       21 |        0 |        2 |        0 |    100% |           |
| tests/test\_commands.py               |       55 |        2 |       42 |        3 |     95% |62->54, 64-67, 82->79 |
| tests/test\_subsystems.py             |       17 |        0 |        8 |        0 |    100% |           |
| tests/utils.py                        |       17 |        2 |        6 |        0 |     91% |     21-22 |
| utils/property.py                     |       62 |        5 |       32 |       10 |     80% |36, 40, 52, 60->82, 61->64, 64->67, 67->70, 73->76, 76->80, 83, 105 |
| utils/safecommand.py                  |       37 |       19 |        8 |        0 |     40% | 13, 17-38 |
| utils/safesubsystem.py                |        5 |        0 |        0 |        0 |    100% |           |
| utils/sparkmaxsim.py                  |       20 |        2 |        0 |        0 |     90% |    25, 28 |
| utils/sparkmaxutils.py                |       38 |       11 |       12 |        3 |     68% |14, 37-56, 76, 86-88 |
| utils/swerve.py                       |      116 |        0 |        2 |        1 |     99% | 137->exit |
| utils/switch.py                       |       40 |        3 |       24 |        7 |     84% |19->exit, 24->exit, 33, 37, 40->exit, 45, 48->exit |
| utils/trapezoidalmotion.py            |       99 |       32 |       44 |       10 |     59% |20, 22, 40-44, 59->exit, 73-91, 110-111, 140-146, 161, 168, 188, 194 |
|                             **TOTAL** | **1797** |  **280** |  **421** |   **65** | **81%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Ultime5528/FRC2024/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Ultime5528/FRC2024/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FUltime5528%2FFRC2024%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.