# Cross-Platform Build Guide

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+ with pip
- **Electron Builder** installed

## Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r python/requirements.txt
```

## Build for Current Platform

```bash
npm run electron:build
```

This builds for your current platform (macOS, Windows, or Linux).

## Platform-Specific Builds

### macOS

```bash
npm run electron:build:mac
```

**Outputs:**
- `.dmg` - macOS disk image (drag-and-drop install)
- `.zip` - Portable ZIP archive

**Supported Architectures:** arm64 (Apple Silicon), x64 (Intel)

### Windows

**Note:** Windows builds must be done on Windows or using a CI/CD pipeline.

```bash
npm run electron:build:win
```

**Outputs:**
- `.exe` - NSIS installer
- `.exe` (portable) - Portable executable

**Supported Architectures:** x64, ia32

### Linux

**Note:** Linux builds must be done on Linux or using a CI/CD pipeline.

```bash
npm run electron:build:linux
```

**Outputs:**
- `.AppImage` - Portable AppImage (works on most distributions)
- `.deb` - Debian/Ubuntu package

**Supported Architectures:** x64

## Build for All Platforms

**Note:** This requires building on each platform or using CI/CD.

```bash
npm run electron:build:all
```

## CI/CD with GitHub Actions

Create `.github/workflows/build.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: npm install
      - run: pip install -r python/requirements.txt
      - run: npm run electron:build
      - uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.os }}-build
          path: release/**
```

## Troubleshooting

### Windows Build on macOS

Windows builds cannot be done on macOS. Options:
1. Build on actual Windows machine
2. Use GitHub Actions (see CI/CD section)
3. Use Docker with Wine (advanced)

### Linux Build on macOS

Linux builds cannot be done on macOS. Options:
1. Build on actual Linux machine
2. Use GitHub Actions (see CI/CD section)
3. Use Docker with Linux container

### Code Signing

- **macOS:** Requires Apple Developer ID certificate for notarization
- **Windows:** Requires code signing certificate
- **Linux:** No code signing required

## Size Optimization

The built app includes:
- Electron runtime (~150MB)
- Python backend (~50MB)
- Templates (~5MB)
- Node modules (~10MB)

**Total size:** ~200-250MB per platform

## Distribution

### macOS
- Upload `.dmg` to website for download
- Submit to Mac App Store (requires additional signing)

### Windows
- Upload `.exe` installer to website
- Submit to Microsoft Store (requires MSIX package)

### Linux
- Upload `.AppImage` to website
- Submit to Snap Store (requires snap package)
- Add to repository (requires `.deb` or `.rpm`)
