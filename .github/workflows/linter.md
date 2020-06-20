---

name: Lint code base
# https://github.com/github/super-linter/

on:
  push

jobs:
  build:
    name: Lint code base
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v2
      - name: Lint Code Base
        uses: docker://github/super-linter:v2.1.0
        env:
          VALIDATE_ALL_CODEBASE: true
          #VALIDATE_PYTHON: false
