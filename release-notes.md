Release Notes
-------------
#### v1.0.3rc
- Add statistical prediction
- Refactoring (move code to mathstat)
- Improve history-future contact point on chart

#### v1.0.2 (2017-04-20)
- Fix #20: Preserve user config after reinstall
- Fix #16: Remove changing file permissions
- Add `install_log.txt` to `.gitignore`
- Add `set -e` and verbose output to `(un)install.sh`
- Update unit tests
- Refactoring (reaname `misc` to `fileio`)

#### v1.0.1 (2017-04-16)
- Fix #16: File permission issue 

#### v1.0.0 (2017-04-14)
- Preserve history after reinstall
- Add config (theme, smoothing, etc)
- Remember theme selection after restart
- Dependencies for build tools (e.g. coverage)
- Fix #2: Limit log file size
- Fix #1: Install as non-root user
