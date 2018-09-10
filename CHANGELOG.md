# nio-cli Changelog

## [1.0.0](https://github.com/niolabs/nio-cli/tree/1.0.0) (2018-09-10)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.7.3...1.0.0)

**Added:**

- add ssl flag to config [\#118](https://github.com/niolabs/nio-cli/pull/118) ([tyoungNIO](https://github.com/tyoungNIO))

**Fixed bugs:**

- No username/password on config project [\#120](https://github.com/niolabs/nio-cli/pull/120) ([tlugger](https://github.com/tlugger))
- Use correct localhost ip [\#115](https://github.com/niolabs/nio-cli/pull/115) ([tlugger](https://github.com/tlugger))
- Unshallow clone [\#114](https://github.com/niolabs/nio-cli/pull/114) ([tyoungNIO](https://github.com/tyoungNIO))

**Merged pull requests:**

- Use bcrypt hashing for user/pasword creation [\#117](https://github.com/niolabs/nio-cli/pull/117) ([tlugger](https://github.com/tlugger))

## [0.7.3](https://github.com/niolabs/nio-cli/tree/0.7.3) (2018-08-21)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.7.2...0.7.3)

**Fixed bugs:**

- fix options reference to pk host/port in config [\#113](https://github.com/niolabs/nio-cli/pull/113) ([tlugger](https://github.com/tlugger))

## [0.7.2](https://github.com/niolabs/nio-cli/tree/0.7.2) (2018-07-31)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.7.1...0.7.2)

**Added:**

- Add block url to etc/blocks.cfg on nio add [\#109](https://github.com/niolabs/nio-cli/pull/109) ([tlugger](https://github.com/tlugger))

## [0.7.1](https://github.com/niolabs/nio-cli/tree/0.7.1) (2018-07-20)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.7.0...0.7.1)

**Fixed bugs:**

- Allow prompt to show given cli defaults [\#106](https://github.com/niolabs/nio-cli/pull/106) ([tlugger](https://github.com/tlugger))

## [0.7.0](https://github.com/niolabs/nio-cli/tree/0.7.0) (2018-07-06)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.6.2...0.7.0)

**Added:**

- User mgmt and credentials [\#104](https://github.com/niolabs/nio-cli/pull/104) ([f1401martin](https://github.com/f1401martin))
- Use --user flag for all dependancy install [\#103](https://github.com/niolabs/nio-cli/pull/103) ([tlugger](https://github.com/tlugger))

## [0.6.2](https://github.com/niolabs/nio-cli/tree/0.6.2) (2018-05-23)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.6.1...0.6.2)

**Added:**

- Update package metadata [\#102](https://github.com/niolabs/nio-cli/pull/102) ([tlugger](https://github.com/tlugger))

## [0.6.1](https://github.com/niolabs/nio-cli/tree/0.6.1) (2018-05-17)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.6.0...0.6.1)

**Added:**

- Hide id in blockspec [\#101](https://github.com/niolabs/nio-cli/pull/101) ([aaronranard](https://github.com/aaronranard))

## [0.6.0](https://github.com/niolabs/nio-cli/tree/0.6.0) (2018-05-02)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.6...0.6.0)

**Added:**

- Add optional pubkeeper args to new command [\#98](https://github.com/niolabs/nio-cli/pull/98) ([hansmosh](https://github.com/hansmosh))

**Fixed bugs:**

- Fix buildspec unit test [\#99](https://github.com/niolabs/nio-cli/pull/99) ([hansmosh](https://github.com/hansmosh))

## [0.5.6](https://github.com/niolabs/nio-cli/tree/0.5.6) (2018-04-26)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.5...0.5.6)

**Added:**

- `nio list` supports nio 3 block and service ids [\#88](https://github.com/niolabs/nio-cli/pull/88) ([tlugger](https://github.com/tlugger))

**Fixed bugs:**

- Works with pip 10 [\#94](https://github.com/niolabs/nio-cli/pull/94) ([deliciousmonster](https://github.com/deliciousmonster))
- Silently fail on git commit errors [\#91](https://github.com/niolabs/nio-cli/pull/91) ([tlugger](https://github.com/tlugger))

## [0.5.5](https://github.com/niolabs/nio-cli/tree/0.5.5) (2018-03-15)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.4...0.5.5)

**Added:**

- nio new command searches project template for requirements.txt and installs libraries [\#87](https://github.com/niolabs/nio-cli/pull/87) ([cowleyk](https://github.com/cowleyk))
- Add optional SSL cert generation and secure instance configuration [\#73](https://github.com/niolabs/nio-cli/pull/73) ([gingajake](https://github.com/gingajake))

## [0.5.4](https://github.com/niolabs/nio-cli/tree/0.5.4) (2018-02-05)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.3...0.5.4)

**Added:**

- add docs link to help close \#17 [\#78](https://github.com/niolabs/nio-cli/pull/78) ([tyoungNIO](https://github.com/tyoungNIO))

## [0.5.3](https://github.com/niolabs/nio-cli/tree/0.5.3) (2018-01-29)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.2...0.5.3)

**Fixed bugs:**

- close tmp file before rename [\#76](https://github.com/niolabs/nio-cli/pull/76) ([tyoungNIO](https://github.com/tyoungNIO))

## [0.5.2](https://github.com/niolabs/nio-cli/tree/0.5.2) (2018-01-26)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.1...0.5.2)

**Added:**

- config for nio.conf user defined [\#72](https://github.com/niolabs/nio-cli/pull/72) ([tlugger](https://github.com/tlugger))

## [0.5.1](https://github.com/niolabs/nio-cli/tree/0.5.1) (2018-01-24)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.5.0...0.5.1)

**Added:**

- refactor configure to not use sed [\#71](https://github.com/niolabs/nio-cli/pull/71) ([tlugger](https://github.com/tlugger))
- fix niolabs and cli docs links [\#70](https://github.com/niolabs/nio-cli/pull/70) ([ssclay](https://github.com/ssclay))

**Fixed bugs:**

- refactor configure to not use sed [\#71](https://github.com/niolabs/nio-cli/pull/71) ([tlugger](https://github.com/tlugger))
- Handle failed git clone on 'nio new' [\#68](https://github.com/niolabs/nio-cli/pull/68) ([hansmosh](https://github.com/hansmosh))

## [0.5.0](https://github.com/niolabs/nio-cli/tree/0.5.0) (2018-01-05)
[Full Changelog](https://github.com/niolabs/nio-cli/compare/0.4.4...0.5.0)

**Added:**

- Config project [\#66](https://github.com/niolabs/nio-cli/pull/66) ([tlugger](https://github.com/tlugger))
- Launch items [\#65](https://github.com/niolabs/nio-cli/pull/65) ([tlugger](https://github.com/tlugger))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*