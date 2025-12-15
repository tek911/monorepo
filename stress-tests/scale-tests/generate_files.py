#!/usr/bin/env python3
"""
Large-Scale Code File Generator

Generates configurable numbers of valid source code files for stress testing
security scanners, code analysis tools, and IDE performance.

Usage:
    python generate_files.py --count 10000 --output ./generated-files
    python generate_files.py --count 50000 --languages python,javascript,java
    python generate_files.py --count 100000 --output ./massive-test --languages all
"""

import argparse
import os
import random
import string
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed


# Language templates - minimal but valid compilable/parseable code
# Using __PLACEHOLDER__ format to avoid conflicts with code braces
TEMPLATES: Dict[str, Dict] = {
    "python": {
        "extension": ".py",
        "templates": [
            '''"""Module __MODULE_NAME__."""

def __FUNC_NAME__(x: int) -> int:
    """Calculate result for input x."""
    return x * __MULTIPLIER__ + __OFFSET__


class __CLASS_NAME__:
    """A simple data holder."""

    def __init__(self, value: int = __DEFAULT_VAL__):
        self.value = value

    def compute(self) -> int:
        return __FUNC_NAME__(self.value)


if __name__ == "__main__":
    obj = __CLASS_NAME__()
    print(obj.compute())
''',
            '''"""Utility module __MODULE_NAME__."""
from typing import List, Optional


def __FUNC_NAME__(items: List[int]) -> Optional[int]:
    """Process a list of items."""
    if not items:
        return None
    return sum(items) // len(items) + __OFFSET__


def __FUNC_NAME2__(text: str) -> str:
    """Transform input text."""
    return text.upper()[::__STEP__]


__VAR_NAME__ = [__VAL1__, __VAL2__, __VAL3__]
''',
            '''"""Data processing module __MODULE_NAME__."""
import json
from dataclasses import dataclass


@dataclass
class __CLASS_NAME__:
    id: int
    name: str
    value: float = __DEFAULT_FLOAT__


def __FUNC_NAME__(data: dict) -> __CLASS_NAME__:
    """Parse dictionary into data class."""
    return __CLASS_NAME__(
        id=data.get("id", __DEFAULT_ID__),
        name=data.get("name", "__DEFAULT_NAME__"),
        value=data.get("value", __DEFAULT_FLOAT__)
    )
''',
        ]
    },
    "javascript": {
        "extension": ".js",
        "templates": [
            '''// Module: __MODULE_NAME__
"use strict";

const __CONST_NAME__ = __CONST_VAL__;

function __FUNC_NAME__(x) {
    return x * __MULTIPLIER__ + __OFFSET__;
}

class __CLASS_NAME__ {
    constructor(value = __DEFAULT_VAL__) {
        this.value = value;
    }

    compute() {
        return __FUNC_NAME__(this.value);
    }
}

module.exports = { __CLASS_NAME__, __FUNC_NAME__, __CONST_NAME__ };
''',
            '''// Utility: __MODULE_NAME__
"use strict";

const __FUNC_NAME__ = (items) => {
    if (!items || items.length === 0) return null;
    return items.reduce((a, b) => a + b, 0) / items.length + __OFFSET__;
};

const __FUNC_NAME2__ = (text) => {
    return text.toUpperCase().split("").filter((_, i) => i % __STEP__ === 0).join("");
};

const __VAR_NAME__ = [__VAL1__, __VAL2__, __VAL3__];

module.exports = { __FUNC_NAME__, __FUNC_NAME2__, __VAR_NAME__ };
''',
            '''// Data handler: __MODULE_NAME__
"use strict";

class __CLASS_NAME__ {
    constructor({ id = __DEFAULT_ID__, name = "__DEFAULT_NAME__", value = __DEFAULT_FLOAT__ } = {}) {
        this.id = id;
        this.name = name;
        this.value = value;
    }

    toJSON() {
        return { id: this.id, name: this.name, value: this.value };
    }

    static fromJSON(data) {
        return new __CLASS_NAME__(data);
    }
}

module.exports = { __CLASS_NAME__ };
''',
        ]
    },
    "typescript": {
        "extension": ".ts",
        "templates": [
            '''// Module: __MODULE_NAME__

export const __CONST_NAME__: number = __CONST_VAL__;

export function __FUNC_NAME__(x: number): number {
    return x * __MULTIPLIER__ + __OFFSET__;
}

export class __CLASS_NAME__ {
    private value: number;

    constructor(value: number = __DEFAULT_VAL__) {
        this.value = value;
    }

    compute(): number {
        return __FUNC_NAME__(this.value);
    }
}
''',
            '''// Utility: __MODULE_NAME__

export interface __INTERFACE_NAME__ {
    id: number;
    name: string;
    value: number;
}

export const __FUNC_NAME__ = (items: number[]): number | null => {
    if (!items || items.length === 0) return null;
    return items.reduce((a, b) => a + b, 0) / items.length + __OFFSET__;
};

export const __VAR_NAME__: number[] = [__VAL1__, __VAL2__, __VAL3__];
''',
        ]
    },
    "java": {
        "extension": ".java",
        "templates": [
            '''package com.generated.module__FILE_NUM__;

/**
 * __CLASS_NAME__ - Auto-generated class
 */
public class __CLASS_NAME__ {
    private int value;

    public __CLASS_NAME__() {
        this.value = __DEFAULT_VAL__;
    }

    public __CLASS_NAME__(int value) {
        this.value = value;
    }

    public int compute() {
        return this.value * __MULTIPLIER__ + __OFFSET__;
    }

    public int getValue() {
        return this.value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public static void main(String[] args) {
        __CLASS_NAME__ obj = new __CLASS_NAME__();
        System.out.println(obj.compute());
    }
}
''',
            '''package com.generated.util__FILE_NUM__;

import java.util.List;
import java.util.ArrayList;

/**
 * __CLASS_NAME__ - Utility class
 */
public class __CLASS_NAME__ {
    private static final int OFFSET = __OFFSET__;

    public static Integer processItems(List<Integer> items) {
        if (items == null || items.isEmpty()) {
            return null;
        }
        int sum = 0;
        for (int item : items) {
            sum += item;
        }
        return sum / items.size() + OFFSET;
    }

    public static List<Integer> generateList() {
        List<Integer> result = new ArrayList<>();
        result.add(__VAL1__);
        result.add(__VAL2__);
        result.add(__VAL3__);
        return result;
    }
}
''',
        ]
    },
    "go": {
        "extension": ".go",
        "templates": [
            '''package main

import "fmt"

const __CONST_NAME__ = __CONST_VAL__

type __STRUCT_NAME__ struct {
	Value int
}

func New__STRUCT_NAME__(value int) *__STRUCT_NAME__ {
	return &__STRUCT_NAME__{Value: value}
}

func (s *__STRUCT_NAME__) Compute() int {
	return s.Value*__MULTIPLIER__ + __OFFSET__
}

func __FUNC_NAME__(x int) int {
	return x*__MULTIPLIER__ + __OFFSET__
}

func main() {
	obj := New__STRUCT_NAME__(__DEFAULT_VAL__)
	fmt.Println(obj.Compute())
}
''',
            '''package util__FILE_NUM__

// __STRUCT_NAME__ holds configuration data
type __STRUCT_NAME__ struct {
	ID    int
	Name  string
	Value float64
}

// New__STRUCT_NAME__ creates a new instance
func New__STRUCT_NAME__(id int, name string) *__STRUCT_NAME__ {
	return &__STRUCT_NAME__{
		ID:    id,
		Name:  name,
		Value: __DEFAULT_FLOAT__,
	}
}

// ProcessItems calculates average plus offset
func ProcessItems(items []int) *int {
	if len(items) == 0 {
		return nil
	}
	sum := 0
	for _, item := range items {
		sum += item
	}
	result := sum/len(items) + __OFFSET__
	return &result
}
''',
        ]
    },
    "rust": {
        "extension": ".rs",
        "templates": [
            '''//! Module __MODULE_NAME__

const __CONST_NAME__: i32 = __CONST_VAL__;

pub struct __STRUCT_NAME__ {
    value: i32,
}

impl __STRUCT_NAME__ {
    pub fn new(value: i32) -> Self {
        Self { value }
    }

    pub fn compute(&self) -> i32 {
        self.value * __MULTIPLIER__ + __OFFSET__
    }
}

pub fn __FUNC_NAME__(x: i32) -> i32 {
    x * __MULTIPLIER__ + __OFFSET__
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test___FUNC_NAME__() {
        assert_eq!(__FUNC_NAME__(__TEST_INPUT__), __TEST_OUTPUT__);
    }
}
''',
            '''//! Utility module __MODULE_NAME__

#[derive(Debug, Clone)]
pub struct __STRUCT_NAME__ {
    pub id: i32,
    pub name: String,
    pub value: f64,
}

impl Default for __STRUCT_NAME__ {
    fn default() -> Self {
        Self {
            id: __DEFAULT_ID__,
            name: String::from("__DEFAULT_NAME__"),
            value: __DEFAULT_FLOAT__,
        }
    }
}

pub fn process_items(items: &[i32]) -> Option<i32> {
    if items.is_empty() {
        return None;
    }
    let sum: i32 = items.iter().sum();
    Some(sum / items.len() as i32 + __OFFSET__)
}
''',
        ]
    },
    "c": {
        "extension": ".c",
        "templates": [
            '''/* Module: __MODULE_NAME__ */
#include <stdio.h>
#include <stdlib.h>

#define __CONST_NAME__ __CONST_VAL__

typedef struct {
    int value;
} __STRUCT_NAME__;

__STRUCT_NAME__* __STRUCT_NAME___new(int value) {
    __STRUCT_NAME__* obj = malloc(sizeof(__STRUCT_NAME__));
    if (obj) {
        obj->value = value;
    }
    return obj;
}

void __STRUCT_NAME___free(__STRUCT_NAME__* obj) {
    free(obj);
}

int __STRUCT_NAME___compute(__STRUCT_NAME__* obj) {
    return obj->value * __MULTIPLIER__ + __OFFSET__;
}

int __FUNC_NAME__(int x) {
    return x * __MULTIPLIER__ + __OFFSET__;
}

int main(void) {
    __STRUCT_NAME__* obj = __STRUCT_NAME___new(__DEFAULT_VAL__);
    if (obj) {
        printf("%d\\n", __STRUCT_NAME___compute(obj));
        __STRUCT_NAME___free(obj);
    }
    return 0;
}
''',
        ]
    },
    "cpp": {
        "extension": ".cpp",
        "templates": [
            '''// Module: __MODULE_NAME__
#include <iostream>
#include <vector>
#include <numeric>

constexpr int __CONST_NAME__ = __CONST_VAL__;

class __CLASS_NAME__ {
private:
    int value_;

public:
    explicit __CLASS_NAME__(int value = __DEFAULT_VAL__) : value_(value) {}

    int compute() const {
        return value_ * __MULTIPLIER__ + __OFFSET__;
    }

    int getValue() const { return value_; }
    void setValue(int value) { value_ = value; }
};

int __FUNC_NAME__(int x) {
    return x * __MULTIPLIER__ + __OFFSET__;
}

int main() {
    __CLASS_NAME__ obj;
    std::cout << obj.compute() << std::endl;
    return 0;
}
''',
        ]
    },
    "ruby": {
        "extension": ".rb",
        "templates": [
            '''# Module: __MODULE_NAME__
# frozen_string_literal: true

module __MODULE_NAME__
  __CONST_NAME__ = __CONST_VAL__

  class __CLASS_NAME__
    attr_accessor :value

    def initialize(value = __DEFAULT_VAL__)
      @value = value
    end

    def compute
      @value * __MULTIPLIER__ + __OFFSET__
    end
  end

  def self.__FUNC_NAME__(x)
    x * __MULTIPLIER__ + __OFFSET__
  end
end

if __FILE__ == $PROGRAM_NAME
  obj = __MODULE_NAME__::__CLASS_NAME__.new
  puts obj.compute
end
''',
        ]
    },
    "php": {
        "extension": ".php",
        "templates": [
            '''<?php
declare(strict_types=1);

namespace Generated\\Module__FILE_NUM__;

const __CONST_NAME__ = __CONST_VAL__;

class __CLASS_NAME__
{
    private int $value;

    public function __construct(int $value = __DEFAULT_VAL__)
    {
        $this->value = $value;
    }

    public function compute(): int
    {
        return $this->value * __MULTIPLIER__ + __OFFSET__;
    }

    public function getValue(): int
    {
        return $this->value;
    }

    public function setValue(int $value): void
    {
        $this->value = $value;
    }
}

function __FUNC_NAME__(int $x): int
{
    return $x * __MULTIPLIER__ + __OFFSET__;
}
''',
        ]
    },
    "csharp": {
        "extension": ".cs",
        "templates": [
            '''using System;
using System.Collections.Generic;
using System.Linq;

namespace Generated.Module__FILE_NUM__
{
    public class __CLASS_NAME__
    {
        private int _value;

        public const int __CONST_NAME__ = __CONST_VAL__;

        public __CLASS_NAME__(int value = __DEFAULT_VAL__)
        {
            _value = value;
        }

        public int Compute()
        {
            return _value * __MULTIPLIER__ + __OFFSET__;
        }

        public int Value
        {
            get => _value;
            set => _value = value;
        }

        public static int __FUNC_NAME__(int x)
        {
            return x * __MULTIPLIER__ + __OFFSET__;
        }
    }
}
''',
        ]
    },
    "kotlin": {
        "extension": ".kt",
        "templates": [
            '''package com.generated.module__FILE_NUM__

const val __CONST_NAME__ = __CONST_VAL__

class __CLASS_NAME__(private var value: Int = __DEFAULT_VAL__) {

    fun compute(): Int = value * __MULTIPLIER__ + __OFFSET__

    fun getValue(): Int = value

    fun setValue(newValue: Int) {
        value = newValue
    }
}

fun __FUNC_NAME__(x: Int): Int = x * __MULTIPLIER__ + __OFFSET__

fun main() {
    val obj = __CLASS_NAME__()
    println(obj.compute())
}
''',
        ]
    },
    "swift": {
        "extension": ".swift",
        "templates": [
            '''// Module: __MODULE_NAME__
import Foundation

let __CONST_NAME__ = __CONST_VAL__

class __CLASS_NAME__ {
    var value: Int

    init(value: Int = __DEFAULT_VAL__) {
        self.value = value
    }

    func compute() -> Int {
        return value * __MULTIPLIER__ + __OFFSET__
    }
}

func __FUNC_NAME__(x: Int) -> Int {
    return x * __MULTIPLIER__ + __OFFSET__
}
''',
        ]
    },
    "scala": {
        "extension": ".scala",
        "templates": [
            '''package com.generated.module__FILE_NUM__

object __OBJECT_NAME__ {
  val __CONST_NAME__: Int = __CONST_VAL__

  def __FUNC_NAME__(x: Int): Int = x * __MULTIPLIER__ + __OFFSET__
}

class __CLASS_NAME__(var value: Int = __DEFAULT_VAL__) {
  def compute(): Int = value * __MULTIPLIER__ + __OFFSET__
}

object Main extends App {
  val obj = new __CLASS_NAME__()
  println(obj.compute())
}
''',
        ]
    },
}


def generate_identifier(prefix: str, seed: int) -> str:
    """Generate a valid identifier from seed."""
    random.seed(seed)
    suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"{prefix}_{suffix}"


def generate_code(language: str, file_num: int) -> str:
    """Generate valid code for a specific language and file number."""
    if language not in TEMPLATES:
        raise ValueError(f"Unknown language: {language}")

    lang_info = TEMPLATES[language]
    template = random.Random(file_num).choice(lang_info["templates"])

    # Generate deterministic but varied values based on file number
    seed = file_num
    rng = random.Random(seed)

    # Generate identifiers
    replacements = {
        "__FILE_NUM__": str(file_num),
        "__MODULE_NAME__": generate_identifier("Module", seed),
        "__FUNC_NAME__": generate_identifier("process", seed + 1),
        "__FUNC_NAME2__": generate_identifier("transform", seed + 2),
        "__CLASS_NAME__": generate_identifier("Handler", seed + 3).replace("_", "").title(),
        "__STRUCT_NAME__": generate_identifier("Data", seed + 4).replace("_", "").title(),
        "__CONST_NAME__": generate_identifier("CONFIG", seed + 5).upper(),
        "__VAR_NAME__": generate_identifier("items", seed + 6),
        "__INTERFACE_NAME__": f"I{generate_identifier('Config', seed + 7).replace('_', '').title()}",
        "__OBJECT_NAME__": generate_identifier("Util", seed + 8).replace("_", "").title(),

        # Numeric values
        "__MULTIPLIER__": str(rng.randint(2, 10)),
        "__OFFSET__": str(rng.randint(1, 100)),
        "__CONST_VAL__": str(rng.randint(100, 9999)),
        "__DEFAULT_VAL__": str(rng.randint(1, 50)),
        "__DEFAULT_ID__": str(rng.randint(1, 1000)),
        "__DEFAULT_FLOAT__": f"{rng.uniform(0.1, 99.9):.2f}",
        "__VAL1__": str(rng.randint(1, 100)),
        "__VAL2__": str(rng.randint(1, 100)),
        "__VAL3__": str(rng.randint(1, 100)),
        "__STEP__": str(rng.randint(2, 5)),
        "__TEST_INPUT__": str(rng.randint(1, 10)),
        "__TEST_OUTPUT__": str(rng.randint(1, 10) * rng.randint(2, 10) + rng.randint(1, 100)),
        "__DEFAULT_NAME__": f"item_{file_num}",
    }

    code = template
    for key, value in replacements.items():
        code = code.replace(key, value)

    return code


def generate_file(output_dir: Path, file_num: int, language: str) -> str:
    """Generate a single file and return its path."""
    lang_info = TEMPLATES[language]
    extension = lang_info["extension"]

    # Create subdirectory structure for large file counts
    subdir_num = file_num // 1000
    subdir = output_dir / f"batch_{subdir_num:04d}"
    subdir.mkdir(parents=True, exist_ok=True)

    filename = f"generated_{file_num:06d}{extension}"
    filepath = subdir / filename

    code = generate_code(language, file_num)
    filepath.write_text(code)

    return str(filepath)


def generate_files(
    count: int,
    output_dir: str,
    languages: List[str],
    workers: int = 8,
    progress_interval: int = 1000
) -> None:
    """Generate multiple code files with parallel execution."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Validate languages
    for lang in languages:
        if lang not in TEMPLATES:
            raise ValueError(f"Unknown language: {lang}. Available: {list(TEMPLATES.keys())}")

    print(f"Generating {count:,} files in {output_dir}")
    print(f"Languages: {', '.join(languages)}")
    print(f"Using {workers} worker threads")
    print()

    generated = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}

        for i in range(count):
            # Round-robin language selection
            lang = languages[i % len(languages)]
            future = executor.submit(generate_file, output_path, i, lang)
            futures[future] = i

        for future in as_completed(futures):
            file_num = futures[future]
            try:
                future.result()
                generated += 1
            except Exception as e:
                errors += 1
                print(f"Error generating file {file_num}: {e}")

            if generated % progress_interval == 0:
                print(f"  Generated {generated:,} / {count:,} files ({100*generated/count:.1f}%)")

    print()
    print(f"Complete! Generated {generated:,} files, {errors} errors")
    print(f"Output directory: {output_path.absolute()}")

    # Print summary of file distribution
    print("\nFile distribution by language:")
    for lang in languages:
        ext = TEMPLATES[lang]["extension"]
        lang_count = len(list(output_path.rglob(f"*{ext}")))
        print(f"  {lang}: {lang_count:,} files")


def main():
    parser = argparse.ArgumentParser(
        description="Generate large numbers of valid source code files for stress testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --count 10000 --output ./generated
  %(prog)s --count 50000 --languages python,javascript,java
  %(prog)s --count 100000 --output ./massive --languages all --workers 16

Available languages:
  python, javascript, typescript, java, go, rust, c, cpp,
  ruby, php, csharp, kotlin, swift, scala

Use '--languages all' to include all available languages.
        """
    )

    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1000,
        help="Number of files to generate (default: 1000)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./generated-files",
        help="Output directory (default: ./generated-files)"
    )

    parser.add_argument(
        "--languages", "-l",
        type=str,
        default="python,javascript,java,go",
        help="Comma-separated list of languages, or 'all' (default: python,javascript,java,go)"
    )

    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=8,
        help="Number of parallel workers (default: 8)"
    )

    parser.add_argument(
        "--progress-interval", "-p",
        type=int,
        default=1000,
        help="Print progress every N files (default: 1000)"
    )

    parser.add_argument(
        "--list-languages",
        action="store_true",
        help="List available languages and exit"
    )

    args = parser.parse_args()

    if args.list_languages:
        print("Available languages:")
        for lang, info in sorted(TEMPLATES.items()):
            print(f"  {lang} ({info['extension']})")
        return

    if args.languages.lower() == "all":
        languages = list(TEMPLATES.keys())
    else:
        languages = [lang.strip() for lang in args.languages.split(",")]

    generate_files(
        count=args.count,
        output_dir=args.output,
        languages=languages,
        workers=args.workers,
        progress_interval=args.progress_interval
    )


if __name__ == "__main__":
    main()
