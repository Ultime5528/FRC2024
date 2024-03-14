# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2024/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                       |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/aligneverything.py                |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshoot.py              |       18 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshootline.py          |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshoottwicegofar.py    |       14 |        0 |        0 |        0 |    100% |           |
| commands/auto/ampsideshoottwiceline.py     |       21 |        0 |        0 |        0 |    100% |           |
| commands/auto/centershoot.py               |       18 |        0 |        0 |        0 |    100% |           |
| commands/auto/centershootline.py           |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/centershoottwiceline.py      |       19 |        0 |        0 |        0 |    100% |           |
| commands/auto/drivesquares.py              |       28 |       16 |        8 |        0 |     33% |13-17, 20, 23-32, 35, 38 |
| commands/auto/farmodeautonome.py           |       19 |        0 |        0 |        0 |    100% |           |
| commands/auto/megamodeautonome.py          |       22 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshoot.py           |       18 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshootline.py       |       13 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshoottwicegofar.py |       14 |        0 |        0 |        0 |    100% |           |
| commands/auto/sourcesideshoottwiceline.py  |       21 |        0 |        0 |        0 |    100% |           |
| commands/climber/\_\_init\_\_.py           |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/extendclimber.py          |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/forceresetclimber.py      |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/climber/lockratchet.py            |       22 |        1 |        2 |        1 |     92% |        33 |
| commands/climber/retractclimber.py         |       18 |        0 |        0 |        0 |    100% |           |
| commands/climber/unlockratchet.py          |       24 |        1 |        2 |        1 |     92% |        35 |
| commands/drivetoposes.py                   |       73 |       37 |       10 |        0 |     46% |48-68, 71-100, 103, 106, 109-111 |
| commands/drivetrain/\_\_init\_\_.py        |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py               |       51 |        9 |       10 |        3 |     74% |18, 22-25, 67-69, 78-79 |
| commands/drivetrain/drivedistance.py       |       41 |       26 |        4 |        0 |     33% |17-26, 29-37, 46-61, 64, 67 |
| commands/drivetrain/resetgyro.py           |       17 |        1 |        2 |        1 |     89% |        18 |
| commands/drivetrain/resetpose.py           |       13 |        2 |        0 |        0 |     85% |    15, 18 |
| commands/intake/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/drop.py                    |       20 |        0 |        0 |        0 |    100% |           |
| commands/intake/load.py                    |       22 |        0 |        2 |        0 |    100% |           |
| commands/intake/pickup.py                  |       22 |        0 |        2 |        0 |    100% |           |
| commands/pivot/forceresetpivot.py          |       23 |        0 |        8 |        1 |     97% |  15->exit |
| commands/pivot/maintainpivot.py            |       13 |        0 |        2 |        0 |    100% |           |
| commands/pivot/movepivot.py                |       57 |        2 |       20 |        2 |     95% |    76, 81 |
| commands/pivot/movepivotcontinuous.py      |       29 |       14 |        8 |        0 |     41% |19, 22-36, 39-40 |
| commands/pivot/resetpivotdown.py           |       19 |        0 |        2 |        0 |    100% |           |
| commands/pivot/resetpivotup.py             |       19 |        7 |        2 |        0 |     57% |13, 16-20, 23, 26 |
| commands/shooter/manualshoot.py            |       13 |        2 |        0 |        0 |     85% |    15, 18 |
| commands/shooter/prepareshoot.py           |       20 |        2 |        2 |        1 |     86% |    23, 28 |
| commands/shooter/shoot.py                  |       23 |        0 |        0 |        0 |    100% |           |
| commands/shooter/waitshootspeed.py         |       23 |        0 |        2 |        0 |    100% |           |
| commands/vibratenote.py                    |       39 |        9 |        8 |        1 |     70% |     36-45 |
| commands/vision/alignwithtag2d.py          |       50 |       19 |       14 |        1 |     53% |43->exit, 50-76, 79-81 |
| gyro.py                                    |      122 |       51 |       14 |        5 |     59% |19, 28->exit, 31->exit, 34->exit, 37->exit, 40, 43, 49-51, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 114, 122, 126, 131-135, 138, 141, 144, 147, 152-161, 164, 167, 170-171, 174-175, 178, 181 |
| ports.py                                   |       28 |        0 |        0 |        0 |    100% |           |
| properties.py                              |       71 |       71 |       24 |        0 |      0% |     1-141 |
| robot.py                                   |      172 |        1 |       12 |        3 |     98% |361->exit, 379, 383->386 |
| subsystems/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/climber.py                      |      146 |        4 |       79 |       11 |     93% |20->exit, 23->exit, 26->exit, 29->exit, 32->exit, 35->exit, 38->exit, 41->exit, 44->exit, 84->exit, 121, 133, 159, 162 |
| subsystems/controller.py                   |       16 |        1 |        2 |        0 |     94% |        21 |
| subsystems/drivetrain.py                   |       95 |        7 |        4 |        2 |     91% |94->exit, 121, 141, 144, 153-162 |
| subsystems/intake.py                       |       30 |        1 |        0 |        0 |     97% |        45 |
| subsystems/led.py                          |      153 |       21 |       50 |        8 |     82% |16-17, 67, 69, 150-151, 166-168, 189, 194-203, 207, 211 |
| subsystems/pivot.py                        |      110 |        8 |       18 |        3 |     91% |54->exit, 85, 101, 109, 112-113, 143, 146, 149 |
| subsystems/shooter.py                      |       67 |        7 |       10 |        1 |     90% |48->exit, 76, 79-83, 93 |
| subsystems/vision.py                       |       41 |        7 |       12 |        5 |     74% |12, 14, 32-33, 38, 43, 49 |
| tests/test\_climber.py                     |       92 |        0 |       24 |        0 |    100% |           |
| tests/test\_commands.py                    |       80 |        6 |       62 |        6 |     92% |70->62, 72-75, 84-87, 88->78, 90-93, 107->104 |
| tests/test\_drive.py                       |       10 |        0 |        2 |        0 |    100% |           |
| tests/test\_intake.py                      |       58 |        0 |       10 |        0 |    100% |           |
| tests/test\_led.py                         |       17 |        0 |        2 |        0 |    100% |           |
| tests/test\_pivot.py                       |      108 |        2 |       20 |        1 |     98% |     46-47 |
| tests/test\_pyfrc.py                       |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_shooter.py                     |       64 |        0 |       14 |        0 |    100% |           |
| tests/test\_subsystems.py                  |       17 |        0 |        8 |        0 |    100% |           |
| tests/test\_switch.py                      |       33 |        0 |        2 |        0 |    100% |           |
| tests/utils.py                             |       17 |        2 |        6 |        0 |     91% |     21-22 |
| utils/\_\_init\_\_.py                      |        0 |        0 |        0 |        0 |    100% |           |
| utils/affinecontroller.py                  |       79 |       57 |        4 |        0 |     27% |7-17, 22-42, 45, 48, 51, 54, 57, 60, 65-66, 69, 72, 75, 78, 81-82, 85, 88-90, 93, 96-120, 123 |
| utils/alignbaseutils.py                    |        2 |        2 |        0 |        0 |      0% |       1-2 |
| utils/auto.py                              |        5 |        0 |        2 |        1 |     86% |   7->exit |
| utils/autostartup.py                       |       64 |       64 |       12 |        0 |      0% |      1-99 |
| utils/axistrigger.py                       |        8 |        1 |        4 |        1 |     83% |        15 |
| utils/coroutinecommand.py                  |       27 |        6 |        6 |        2 |     76% |14, 19, 32->exit, 34-35, 38, 41 |
| utils/linearinterpolator.py                |       25 |       12 |        6 |        0 |     42% |11-12, 15-16, 25-36 |
| utils/property.py                          |       62 |       34 |       32 |        2 |     36% |36, 40, 54-108 |
| utils/safecommand.py                       |       40 |       19 |        8 |        0 |     44% | 14, 18-39 |
| utils/safesubsystem.py                     |       23 |        1 |        4 |        0 |     96% |        28 |
| utils/sparkmaxsim.py                       |       20 |        2 |        0 |        0 |     90% |    25, 28 |
| utils/sparkmaxutils.py                     |       38 |       10 |       12 |        4 |     72% |14, 37-56, 70, 76, 88 |
| utils/swerve.py                            |      115 |        0 |        2 |        1 |     99% | 136->exit |
| utils/switch.py                            |       66 |        6 |       42 |        7 |     88% |24->exit, 36, 48, 52, 62, 66, 76 |
| utils/trapezoidalmotion.py                 |       99 |       29 |       44 |        9 |     62% |20, 22, 40-44, 59->exit, 73-91, 110-111, 161, 168, 188, 194 |
|                                  **TOTAL** | **3177** |  **580** |  **671** |   **85** | **79%** |           |


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