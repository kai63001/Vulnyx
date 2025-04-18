#!/bin/bash

# Exit ถ้ามี error
set -e

echo "📦 Starting build for Vulnyx..."

# ชื่อไฟล์ต้นทาง
SOURCE="main.py"

# ชื่อ binary ที่ต้องการได้
OUTPUT="vulnyx.bin"

python3 -m nuitka "$SOURCE" \
  --standalone \
  --show-progress \
  --include-module=main \
  --include-module=passlib \
  --include-module=passlib.handlers \
  --include-module=passlib.handlers.bcrypt \
  --include-module=sqlalchemy \
  --include-module=sqlalchemy.ext \
  --include-module=sqlalchemy.ext.declarative \
  --include-module=sqlalchemy.orm \
  --include-data-dir=templates=templates \
  --include-data-dir=results=results \
  --include-data-dir=public=public \
  --include-data-dir=modules=modules \
  --output-filename="$OUTPUT" \
  --remove-output

# สร้าง build ด้วย Nuitka
# python3 -m nuitka "$SOURCE" \
#   --standalone \
#   --onefile \
#   --lto=yes \
#   --show-progress \
#   --include-module=main \
#   --include-data-dir=templates=templates \
#   --include-data-dir=results=results \
#   --include-data-dir=public=public \
#   --output-filename="$OUTPUT" \
#   --remove-output

echo "✅ Build completed!"
echo "📂 Output binary: ./$OUTPUT"
