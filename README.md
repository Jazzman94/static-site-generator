# Static Site Generator

A static site generator built from scratch in pure Python — no frameworks, no third-party dependencies, just the standard library. It converts a directory of Markdown files into a fully linked, styled HTML site, ready to be published on GitHub Pages.

> **Note:** This is a *semi-guided* project from the [boot.dev](https://www.boot.dev) backend curriculum. boot.dev provides the spec, requirements, and test cases; the implementation, structure, and design decisions are entirely my own.

## Why build this?

It's tempting to reach for Jekyll, Hugo, or Next.js the moment you need a static site — but building a generator yourself, even a small one, is one of the highest-leverage exercises for a backend developer:

- **You demystify the tools you use every day.** Every SSG, template engine, and doc generator does some version of "parse text → build a tree → render output." Implementing it once means you'll never treat that pipeline as a black box again.
- **It's a real parsing exercise without the intimidation factor.** Markdown is small enough to fully implement in an evening, but it still forces you to deal with tokenizing, nested inline styles, and edge cases — the same skills that scale up to writing linters, compilers, or config-file parsers.
- **It's a natural excuse to practice recursion and tree structures.** Rendering nested block/inline elements into an HTML node tree (and recursively mirroring a content directory into a build directory) is a clean, self-contained recursion problem with an immediately visible, satisfying result.
- **It rewards test-driven development.** Because the correctness of "does this Markdown produce this HTML" is so easy to assert, this is a great place to actually practice writing tests before/alongside implementation instead of skipping it.
- **You end up with something you can actually use.** Unlike a lot of learning exercises, at the end you have a working tool that deploys a real website — good motivation to push through the boring parts.

## Features

- **Custom Markdown → HTML engine**, no libraries — supports headings, paragraphs, bold, italic, inline code, links, images, block quotes, and ordered/unordered lists.
- **Node-based rendering**, `HTMLNode` / `LeafNode` / `ParentNode` classes model the HTML tree the way a real templating engine would, instead of string-concatenating HTML.
- **Recursive site generation** — mirrors the `content/` directory structure into the output directory, converting every `.md` file into `.html` along the way.
- **Static asset pipeline** — copies images, CSS, and other static files into the build output.
- **Simple templating** — injects page title and rendered content into `template.html` via `{{ Title }}` / `{{ Content }}` placeholders.
- **GitHub Pages ready** — supports a configurable base path so the site works correctly when served from a project subdirectory (`username.github.io/repo-name/`).

## Project structure

```
.
├── content/           # Markdown source files (gitignored, not included)
├── static/             # Static assets (CSS, images) copied as-is into the build
├── docs/                # Generated site output (served by GitHub Pages)
├── template.html        # HTML shell with {{ Title }} / {{ Content }} placeholders
├── src/
│   ├── main.py                # Build entry point: copies static files, walks content/, generates pages
│   ├── markdown_parser.py     # Markdown → block/inline parsing and HTML node generation
│   ├── textnode.py             # TextNode: represents inline text with a type (bold, link, image, ...)
│   ├── htmlnode.py             # HTMLNode / LeafNode / ParentNode: the HTML tree model
│   ├── node_transformer.py     # Converts TextNode instances into HTMLNode instances
│   └── test_*.py                # Unit test suite (unittest)
├── build.sh              # Build the site with the GitHub Pages base path
├── main.sh                # Build the site and serve it locally
└── test.sh                 # Run the full test suite
```

## Getting started

Requires Python 3.10+ (no external dependencies).

**Build and serve locally:**

```bash
./main.sh
```

This generates the site into the output directory and starts a local server at `http://localhost:8888`.

**Build for GitHub Pages:**

```bash
./build.sh
```

**Run the tests:**

```bash
./test.sh
```

## How it works

1. Markdown files under `content/` are read and split into blocks (paragraphs, headings, lists, quotes, code blocks).
2. Each block is parsed into inline `TextNode`s (handling bold, italic, code, links, and images).
3. `TextNode`s are converted into an `HTMLNode` tree (`LeafNode`/`ParentNode`).
4. The tree is rendered to an HTML string and injected into `template.html`.
5. The process repeats recursively for every file in `content/`, mirroring the directory structure into the output directory, alongside a copy of everything in `static/`.
