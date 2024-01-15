# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.6] - 2021-01-02

Installation see project description.
This is the first release. It is based on the
project [Yandex Images Download](https://pypi.org/project/yandex-images-download/)
1.0.4 from Alexander Kozlov.

### Added

- Existing images can be skipped.
- Set search keywords as Lightroom keywords.
- Set image url as creator web address (IPTC)

### Changed

### Fixed

- Replaced request.path by request.url in get_response() module download.py.

## [1.0.7] - 2021-01-07

To update run  
```pip install yandex2lightroom==1.0.7```

### Added

- Added wallpaper as additional image size (option --isize=wallpaper)

### Changed

### Fixed

## [1.0.8] - 2021-01-08

To update run  
```pip install yandex2lightroom==1.0.8```

### Added

### Changed

### Fixed

- Option ``--num-workers`` did not work

## [1.0.8.1] - 2021-01-09

To update run  
```pip install yandex2lightroom==1.0.8.1```

### Added

### Changed

-- Change the update command in this file

### Fixed

## [1.0.8.2] - 2021-04-18

To update run  
```pip install yandex2lightroom==1.0.8.2```

### Added

### Changed

- Complete install_requires and allow all builds of major releases.

### Fixed

## [1.0.9.0] - 2021-04-19

To update run  
```pip install yandex2lightroom==1.0.9.0```

### Added

### Changed

- Add command line option --error-log to pass error messages via file to Lightroom.

### Fixed

## [1.0.9.1] - 2021-10-30

To update run  
```pip install yandex2lightroom==1.0.9.1```

### Added

### Changed

### Fixed

- Shift to selenium-wire 4.5.4 because of captcha issue with current yandex page.
  Updated all other packages as well.

## [1.0.9.2] - 2021-10-31

To update run  
```pip install yandex2lightroom==1.0.9.2```

### Added

### Changed

### Fixed

- Shift to urllib3 1.26.7 for security reasons

## [1.0.9.3] - 2021-12-28

To update run  
```pip install yandex2lightroom==1.0.9.3```
Remarks: As only documentation has changed an update is not really necessary.

### Added

### Changed

Add installation documentation for yandex2lightroom itself.

### Fixed

## [1.0.9.4] - 2023-09-17

To update run  
```pip install yandex2lightroom==1.0.9.4```
Remarks: As only documentation has changed an update is not really necessary.

### Added

### Changed

- Change setup.py: Shift to selenium-wire>=5.1.0, certifi>=2023.7.22, lxml>=4.9.1, requests>=2.31.0

### Fixed

## [1.1.0.0] - 2023-12-28

### Added

- Added Firefox support
- Added cookies support

### Changed

- Browser is displayed by default

### Fixed

- Fix issue with new page structure
- Fix isize and wallpaper issue
- Fixed captcha handling
