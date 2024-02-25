# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                         |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| alignbase.py                                 |       59 |       32 |        7 |        1 |     44% |29-32, 35->exit, 38-50, 53-72, 80, 87 |
| commands/\_\_init\_\_.py                     |        0 |        0 |        0 |        0 |    100% |           |
| commands/aligneverything.py                  |       11 |        0 |        0 |        0 |    100% |           |
| commands/auto/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/drivesquares.py                |       28 |       16 |        8 |        0 |     33% |13-17, 20, 23-32, 35, 38 |
| commands/climber/\_\_init\_\_.py             |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/extendclimber.py            |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/forceresetclimber.py        |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/climber/lockratchet.py              |       22 |        1 |        2 |        1 |     92% |        33 |
| commands/climber/retractclimber.py           |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/unlockratchet.py            |       24 |        1 |        2 |        1 |     92% |        35 |
| commands/drivetopos.py                       |        9 |        3 |        0 |        0 |     67% |  9-10, 13 |
| commands/drivetoposes.py                     |       73 |       43 |        8 |        0 |     37% |34-37, 40-54, 57-99, 102, 105 |
| commands/drivetrain/\_\_init\_\_.py          |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py                 |       64 |       11 |        6 |        2 |     79% |17, 21-24, 46-60, 63, 105 |
| commands/drivetrain/drivedistance.py         |       41 |       26 |        4 |        0 |     33% |17-26, 29-37, 46-61, 64, 67 |
| commands/drivetrain/resetgyro.py             |       11 |        0 |        0 |        0 |    100% |           |
| commands/intake/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/drop.py                      |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/load.py                      |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/pickup.py                    |       22 |        0 |        2 |        0 |    100% |           |
| commands/led/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| commands/led/lightall.py                     |       11 |        2 |        0 |        0 |     82% |    12, 15 |
| commands/pivot/forceresetpivot.py            |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/pivot/maintainpivot.py              |       13 |        0 |        2 |        0 |    100% |           |
| commands/pivot/movepivot.py                  |       57 |        2 |       20 |        2 |     95% |    76, 81 |
| commands/pivot/movepivotcontinuous.py        |       27 |       13 |        8 |        0 |     40% |19-33, 36-37 |
| commands/pivot/resetpivotdown.py             |       19 |        0 |        2 |        0 |    100% |           |
| commands/pivot/resetpivotup.py               |       19 |        7 |        2 |        0 |     57% |13, 16-20, 23, 26 |
| commands/shooter/manualshoot.py              |       13 |        2 |        0 |        0 |     85% |    15, 18 |
| commands/shooter/prepareshoot.py             |       20 |        2 |        2 |        1 |     86% |    23, 28 |
| commands/shooter/shootandmovepivotloading.py |       17 |        0 |        0 |        0 |    100% |           |
| commands/shooter/waitshootspeed.py           |       23 |        0 |        2 |        0 |    100% |           |
| commands/vision/alignwithtag2d.py            |       41 |       11 |        6 |        1 |     70% |39->exit, 46-63, 66-67 |
| gyro.py                                      |      122 |       50 |       14 |        5 |     60% |19, 28->exit, 31->exit, 34->exit, 37->exit, 43, 49-51, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 114, 122, 126, 131-135, 138, 141, 144, 147, 152-161, 164, 167, 170-171, 174-175, 178, 181 |
| ports.py                                     |       28 |        0 |        0 |        0 |    100% |           |
| properties.py                                |       71 |       71 |       24 |        0 |      0% |     1-141 |
| robot.py                                     |      138 |        3 |       12 |        4 |     95% |214, 218, 229, 233->236 |
| subsystems/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                        |      146 |        4 |       79 |       11 |     93% |20->exit, 23->exit, 26->exit, 29->exit, 32->exit, 35->exit, 38->exit, 41->exit, 44->exit, 84->exit, 121, 133, 159, 162 |
| subsystems/drivetrain.py                     |       98 |        8 |        4 |        2 |     90% |94->exit, 113, 133, 145, 151-160, 243 |
| subsystems/intake.py                         |       30 |        1 |        0 |        0 |     97% |        45 |
| subsystems/led.py                            |      132 |       51 |       44 |        4 |     54% |15-16, 20-21, 60->exit, 70-71, 74, 77-79, 82, 85-92, 95-98, 101-104, 107-118, 127-133, 139, 142, 152-161, 168, 178-179, 184 |
| subsystems/pivot.py                          |      104 |        4 |       18 |        1 |     96% |52->exit, 107, 137, 140, 143 |
| subsystems/shooter.py                        |       56 |        5 |        8 |        1 |     91% |44->exit, 65-68, 78 |
| subsystems/vision.py                         |       41 |        7 |       12 |        5 |     74% |12, 14, 32-33, 38, 43, 49 |
| tests/climber\_test.py                       |       92 |        0 |       24 |        0 |    100% |           |
| tests/drive\_test.py                         |       10 |        0 |        2 |        0 |    100% |           |
| tests/intake\_test.py                        |       58 |        0 |       10 |        0 |    100% |           |
| tests/pivot\_test.py                         |      108 |        2 |       20 |        1 |     98% |     46-47 |
| tests/pyfrc\_test.py                         |        1 |        0 |        0 |        0 |    100% |           |
| tests/shooter\_test.py                       |       64 |        0 |       14 |        0 |    100% |           |
| tests/switch\_test.py                        |       33 |        0 |        2 |        0 |    100% |           |
| tests/test\_commands.py                      |       67 |        4 |       56 |        5 |     93% |65->57, 67-70, 83->73, 85-88, 102->99 |
| tests/test\_subsystems.py                    |       17 |        0 |        8 |        0 |    100% |           |
| tests/utils.py                               |       17 |        2 |        6 |        0 |     91% |     21-22 |
| utils/alignbaseutils.py                      |        2 |        1 |        0 |        0 |     50% |         2 |
| utils/axistrigger.py                         |        8 |        1 |        4 |        1 |     83% |        15 |
| utils/linearinterpolator.py                  |       13 |        8 |        6 |        0 |     26% |      9-20 |
| utils/property.py                            |       62 |        5 |       32 |       10 |     80% |36, 40, 52, 60->82, 61->64, 64->67, 67->70, 73->76, 76->80, 83, 105 |
| utils/safecommand.py                         |       40 |       19 |        8 |        0 |     44% | 14, 18-39 |
| utils/safesubsystem.py                       |       23 |        1 |        4 |        0 |     96% |        28 |
| utils/sparkmaxsim.py                         |       20 |        2 |        0 |        0 |     90% |    25, 28 |
| utils/sparkmaxutils.py                       |       38 |       10 |       12 |        4 |     72% |14, 37-56, 70, 76, 88 |
| utils/swerve.py                              |      115 |        0 |        2 |        1 |     99% | 136->exit |
| utils/switch.py                              |       66 |        6 |       42 |        7 |     88% |24->exit, 36, 48, 52, 62, 66, 76 |
| utils/trapezoidalmotion.py                   |       99 |       29 |       44 |        9 |     62% |20, 22, 40-44, 59->exit, 73-91, 110-111, 161, 168, 188, 194 |
|                                    **TOTAL** | **2669** |  **466** |  **614** |   **82** | **80%** |           |


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