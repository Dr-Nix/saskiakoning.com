# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static HTML website for artist Saskia Koning showcasing her sculptures and artwork. The repository contains an archive of an older website version stored in the `oldsite/` directory.

## Repository Structure

- `oldsite/` - Contains the complete legacy HTML website with:
  - Static HTML pages for different artwork categories (bronze sculptures, stone sculptures, paintings)
  - CSS stylesheets (`standaard-saskia.css`, `saskia subpaginas.css`)
  - Image galleries organized by artwork type and series
  - Individual pages for each sculpture/artwork piece

## Technology Stack

This is a pure static HTML/CSS website with no build system or dependencies:
- HTML 4.01/XHTML 1.0 markup
- CSS for styling with background images and layout
- No JavaScript framework or build tools
- No package.json or other configuration files

## File Organization

The website follows a simple structure:
- `index.html` - Main homepage with navigation grid
- Category pages: `bronzen beelden.html`, `stenen beelden.html`, `schilderijen.html`, etc.
- Individual artwork pages: `brons [name].html`, `steen [name].html`
- Image directories organized by sculpture series (e.g., `Bronzen beelden/`, `Stenen Beelden/`)

## CSS Architecture

Two main stylesheets:
- `standaard-saskia.css` - Base typography and layout styles
- `saskia subpaginas.css` - Background image handling for subpages

Common CSS pattern used across pages:
- Fixed background images using `#bg` div with full viewport coverage
- Content overlay using `#content` div with relative positioning
- Responsive layout using percentage-based widths

## Development Workflow

Since this is a static site with no build process:
- Edit HTML/CSS files directly
- Test by opening HTML files in browser
- No compilation or preprocessing required
- Deploy by copying files to web server

## Content Management

Images are organized by:
- Sculpture type (bronze vs stone)
- Individual series/collections
- Thumbnail and full-size versions stored together