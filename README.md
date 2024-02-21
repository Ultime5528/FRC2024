# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| alignbase.py                          |       59 |       32 |        7 |        1 |     44% |29-32, 35->exit, 38-50, 53-72, 80, 87 |
| commands/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/drivesquares.py         |       28 |       16 |        8 |        0 |     33% |13-17, 20, 23-32, 35, 38 |
| commands/climber/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/extendclimber.py     |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/forceresetclimber.py |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/climber/lockratchet.py       |       19 |        0 |        0 |        0 |    100% |           |
| commands/climber/retractclimber.py    |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/unlockratchet.py     |       21 |        0 |        0 |        0 |    100% |           |
| commands/drivetopos.py                |        9 |        3 |        0 |        0 |     67% |  9-10, 13 |
| commands/drivetoposes.py              |       73 |       43 |        8 |        0 |     37% |34-37, 40-54, 57-99, 102, 105 |
| commands/drivetrain/\_\_init\_\_.py   |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py          |       63 |       11 |        6 |        2 |     78% |16, 20-23, 45-59, 62, 104 |
| commands/drivetrain/drivedistance.py  |       41 |       26 |        4 |        0 |     33% |17-26, 29-37, 46-61, 64, 67 |
| commands/intake/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/drop.py               |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/load.py               |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/pickup.py             |       22 |        0 |        2 |        0 |    100% |           |
| commands/pivot/forceresetpivot.py     |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/pivot/maintainpivot.py       |       13 |        1 |        2 |        1 |     87% |        17 |
| commands/pivot/movepivot.py           |       57 |        2 |       20 |        2 |     95% |    76, 81 |
| commands/pivot/resetpivotdown.py      |       19 |        0 |        2 |        0 |    100% |           |
| commands/pivot/resetpivotup.py        |       19 |        7 |        2 |        0 |     57% |13, 16-20, 23, 26 |
| commands/shooter/manualshoot.py       |       13 |        2 |        0 |        0 |     85% |    15, 18 |
| commands/shooter/prepareshoot.py      |       27 |        7 |        6 |        1 |     64% | 27-33, 36 |
| commands/shooter/shoot.py             |       14 |        0 |        0 |        0 |    100% |           |
| commands/shooter/waitshootspeed.py    |       10 |        0 |        0 |        0 |    100% |           |
| commands/vision/alignwithtag2d.py     |       46 |       20 |       18 |        1 |     45% |15-18, 22-26, 49->exit, 53-63, 66-68 |
| gyro.py                               |      122 |       50 |       14 |        5 |     60% |19, 28->exit, 31->exit, 34->exit, 37->exit, 43, 49-51, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 114, 122, 126, 131-135, 138, 141, 144, 147, 152-161, 164, 167, 170-171, 174-175, 178, 181 |
| ports.py                              |       27 |        0 |        0 |        0 |    100% |           |
| properties.py                         |       71 |       71 |       24 |        0 |      0% |     1-141 |
| robot.py                              |      107 |        3 |       12 |        4 |     94% |161, 166, 173, 177->180 |
| subsystems/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                 |      137 |        4 |       77 |       11 |     93% |19->exit, 22->exit, 25->exit, 28->exit, 31->exit, 34->exit, 37->exit, 40->exit, 43->exit, 75->exit, 110, 121, 147, 150 |
| subsystems/drivetrain.py              |       96 |        7 |        4 |        2 |     91% |94->exit, 113, 133, 145, 151-160 |
| subsystems/intake.py                  |       30 |        1 |        0 |        0 |     97% |        45 |
| subsystems/pivot.py                   |      102 |        8 |       20 |        4 |     90% |47->exit, 59-60, 78, 94, 99, 128, 131, 134 |
| subsystems/shooter.py                 |       56 |        5 |        8 |        1 |     91% |44->exit, 65-68, 78 |
| tests/climber\_test.py                |       85 |        0 |       24 |        0 |    100% |           |
| tests/intake\_test.py                 |       58 |        0 |       10 |        0 |    100% |           |
| tests/pivot\_test.py                  |       82 |        2 |       18 |        1 |     97% |     41-42 |
| tests/pyfrc\_test.py                  |        1 |        0 |        0 |        0 |    100% |           |
| tests/shooter\_test.py                |       42 |        0 |        8 |        0 |    100% |           |
| tests/switch\_test.py                 |       33 |        0 |        2 |        0 |    100% |           |
| tests/test\_commands.py               |       67 |        6 |       56 |        6 |     90% |62->54, 64-67, 76-79, 80->70, 82-85, 99->96 |
| tests/test\_subsystems.py             |       17 |        0 |        8 |        0 |    100% |           |
| tests/utils.py                        |       17 |        2 |        6 |        0 |     91% |     21-22 |
| utils/alignbaseutils.py               |        2 |        1 |        0 |        0 |     50% |         2 |
| utils/property.py                     |       62 |        5 |       32 |       10 |     80% |36, 40, 52, 60->82, 61->64, 64->67, 67->70, 73->76, 76->80, 83, 105 |
| utils/safecommand.py                  |       40 |       19 |        8 |        0 |     44% | 14, 18-39 |
| utils/safesubsystem.py                |       23 |        1 |        4 |        0 |     96% |        28 |
| utils/sparkmaxsim.py                  |       20 |        2 |        0 |        0 |     90% |    25, 28 |
| utils/sparkmaxutils.py                |       38 |       10 |       12 |        4 |     72% |14, 37-56, 70, 76, 88 |
| utils/swerve.py                       |      115 |        0 |        2 |        1 |     99% | 136->exit |
| utils/switch.py                       |       64 |        6 |       42 |        7 |     88% |24->exit, 36, 48, 52, 62, 66, 76 |
| utils/trapezoidalmotion.py            |       99 |       30 |       44 |       11 |     60% |20, 22, 40-44, 59->exit, 73-91, 110-111, 136->exit, 161, 168, 176, 188, 194 |
|                             **TOTAL** | **2292** |  **403** |  **540** |   **77** | **80%** |           |


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