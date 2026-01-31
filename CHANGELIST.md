# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.2] - 2026-01-30

- `rsxml.util.safe_makedirs` better tested and documented, implemented with pathlib, and now accepts Path or string objects

## [2.2.1] - 2025-12-15

- Fixed multipart ETag calculation in tests to ensure accurate verification against S3 ETags.

## [2.2.0] - 2025-12-12

### Added
- Added a codespace configuration.
- Implemented new unit tests and various improvements.

### Changed
- Reworked project structure for best practices.
- Updated configuration for trusted publishing.
- Moving the package to its own repo.
- Implemented more of the Riverscapes Project XSD spec. 
