# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                       |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/aligneverything.py                |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshoot.py              |       17 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshootline.py          |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshoottwicegofar.py    |       14 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshoottwiceline.py     |       20 |        0 |        0 |        0 |    100% |           |
| commands/auto/centershoot.py               |       17 |        0 |        0 |        0 |    100% |           |
| commands/auto/centershootline.py           |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/centershoottwiceline.py      |       19 |        0 |        0 |        0 |    100% |           |
| commands/auto/drivesquares.py              |       28 |       16 |        8 |        0 |     33% |13-17, 20, 23-32, 35, 38 |
| commands/auto/megamodeautonome.py          |       19 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshoot.py           |       18 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshootgofar.py      |       14 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshootline.py       |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshoottwicegofar.py |       14 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshoottwiceline.py  |       20 |        0 |        0 |        0 |    100% |           |
| commands/climber/\_\_init\_\_.py           |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/extendclimber.py          |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/forceresetclimber.py      |       23 |        0 |        0 |        0 |    100% |           |
| commands/climber/lockratchet.py            |       22 |        1 |        2 |        1 |     92% |        33 |
| commands/climber/retractclimber.py         |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/unlockratchet.py          |       24 |        1 |        2 |        1 |     92% |        35 |
| commands/drivetoposes.py                   |       58 |       22 |        4 |        0 |     58% |46-59, 69-70, 73-100, 103, 106, 109, 115 |
| commands/drivetrain/\_\_init\_\_.py        |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py               |       56 |       12 |       12 |        4 |     71% |18, 22-25, 68-70, 79-80, 83-85 |
| commands/drivetrain/drivedistance.py       |       41 |       26 |        4 |        0 |     33% |17-26, 29-37, 46-61, 64, 67 |
| commands/drivetrain/resetgyro.py           |       17 |        1 |        2 |        1 |     89% |        18 |
| commands/drivetrain/resetpose.py           |       13 |        2 |        0 |        0 |     85% |    15, 18 |
| commands/intake/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/drop.py                    |       20 |        0 |        0 |        0 |    100% |           |
| commands/intake/load.py                    |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/pickup.py                  |       22 |        0 |        2 |        0 |    100% |           |
| commands/pivot/forceresetpivot.py          |       23 |        0 |        0 |        0 |    100% |           |
| commands/pivot/maintainpivot.py            |       13 |        0 |        2 |        0 |    100% |           |
| commands/pivot/movepivot.py                |       57 |        2 |        4 |        2 |     93% |    76, 81 |
| commands/pivot/movepivotcontinuous.py      |       30 |       15 |        8 |        0 |     39% |19, 22-39, 42-43 |
| commands/pivot/resetpivotdown.py           |       19 |        0 |        2 |        0 |    100% |           |
| commands/pivot/resetpivotup.py             |       19 |        7 |        2 |        0 |     57% |13, 16-20, 23, 26 |
| commands/shooter/manualshoot.py            |       13 |        2 |        0 |        0 |     85% |    15, 18 |
| commands/shooter/prepareshoot.py           |       20 |        2 |        2 |        1 |     86% |    23, 28 |
| commands/shooter/shoot.py                  |       23 |        0 |        0 |        0 |    100% |           |
| commands/shooter/waitshootspeed.py         |       23 |        0 |        2 |        0 |    100% |           |
| commands/vibratenote.py                    |       39 |        9 |        8 |        1 |     70% |     36-45 |
| commands/vision/alignwithtag2d.py          |       50 |       19 |       10 |        0 |     52% |50-76, 79-81 |
| gyro.py                                    |      122 |       51 |       10 |        5 |     58% |19, 28->exit, 31->exit, 34->exit, 37->exit, 40, 43, 49-51, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 114, 122, 126, 131-135, 138, 141, 144, 147, 152-161, 164, 167, 170-171, 174-175, 178, 181 |
| make\_test\_requirements.py                |       10 |       10 |        0 |        0 |      0% |      1-17 |
| ports.py                                   |       28 |        0 |        0 |        0 |    100% |           |
| properties.py                              |       90 |       90 |       16 |        0 |      0% |     1-175 |
| robot.py                                   |      198 |       22 |       24 |        4 |     84% |270-278, 376->exit, 394-408, 417, 421->424 |
| subsystems/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                      |      146 |       18 |       30 |       11 |     84% |20->exit, 23->exit, 26->exit, 29->exit, 32->exit, 35->exit, 38->exit, 41->exit, 44->exit, 84->exit, 121, 133, 156-174 |
| subsystems/controller.py                   |       16 |        4 |        0 |        0 |     75% |     18-23 |
| subsystems/drivetrain.py                   |       95 |        7 |        4 |        2 |     91% |94->exit, 121, 141, 144, 153-162 |
| subsystems/intake.py                       |       30 |        5 |        0 |        0 |     83% |     42-48 |
| subsystems/led.py                          |      153 |       23 |       46 |        8 |     80% |16-17, 67, 69, 150-151, 166-168, 189, 194-203, 207, 211, 217-218 |
| subsystems/pivot.py                        |      110 |       24 |       12 |        3 |     78% |54->exit, 85, 101, 109, 112-113, 140-167 |
| subsystems/shooter.py                      |       67 |       14 |        4 |        1 |     79% |48->exit, 76, 79-83, 90-105 |
| subsystems/vision.py                       |       60 |       35 |       18 |        1 |     36% |12-19, 38-47, 54-57, 60-77 |
| tests/properties\_test.py                  |        3 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                     |       92 |        0 |        8 |        0 |    100% |           |
| tests/test\_commands.py                    |       80 |        6 |       58 |        6 |     91% |70->62, 72-75, 84-87, 88->78, 90-93, 107->104 |
| tests/test\_drive.py                       |       10 |        0 |        0 |        0 |    100% |           |
| tests/test\_intake.py                      |       58 |        0 |        0 |        0 |    100% |           |
| tests/test\_led.py                         |       17 |        0 |        0 |        0 |    100% |           |
| tests/test\_pivot.py                       |      108 |        2 |        8 |        1 |     97% |     46-47 |
| tests/test\_pyfrc.py                       |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_shooter.py                     |       64 |        0 |        4 |        0 |    100% |           |
| tests/test\_subsystems.py                  |       17 |        0 |        8 |        0 |    100% |           |
| tests/test\_switch.py                      |       33 |        0 |        0 |        0 |    100% |           |
| tests/utils.py                             |       17 |        2 |        6 |        0 |     91% |     21-22 |
| utils/\_\_init\_\_.py                      |        0 |        0 |        0 |        0 |    100% |           |
| utils/affinecontroller.py                  |       77 |       77 |        2 |        0 |      0% |     1-122 |
| utils/alignbaseutils.py                    |        2 |        2 |        0 |        0 |      0% |       1-2 |
| utils/auto.py                              |        5 |        0 |        0 |        0 |    100% |           |
| utils/autostartup.py                       |       64 |       64 |       10 |        0 |      0% |      1-99 |
| utils/axistrigger.py                       |        8 |        1 |        2 |        1 |     80% |        15 |
| utils/coroutinecommand.py                  |       27 |        6 |        6 |        2 |     76% |14, 19, 32->exit, 34-35, 38, 41 |
| utils/linearinterpolator.py                |       25 |       14 |        6 |        0 |     35% |11-12, 15-16, 19, 22, 25-36 |
| utils/property.py                          |       58 |       31 |       20 |        2 |     37% |35, 39, 53-102 |
| utils/safecommand.py                       |       40 |       19 |        6 |        0 |     46% | 14, 18-39 |
| utils/safesubsystem.py                     |       23 |       16 |        4 |        0 |     26% |     11-32 |
| utils/sparkmaxsim.py                       |       20 |        2 |        0 |        0 |     90% |    25, 28 |
| utils/sparkmaxutils.py                     |       38 |       10 |       12 |        4 |     72% |14, 37-56, 70, 76, 88 |
| utils/swerve.py                            |      115 |        0 |        2 |        1 |     99% | 136->exit |
| utils/switch.py                            |       66 |        6 |       42 |        7 |     88% |24->exit, 36, 48, 52, 62, 66, 76 |
| utils/trapezoidalmotion.py                 |      104 |       32 |       42 |        9 |     61% |20, 22, 40-44, 59->exit, 73-91, 110-111, 161, 168, 188, 194, 199-200, 203 |
|                                  **TOTAL** | **3232** |  **730** |  **488** |   **79** | **74%** |           |


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