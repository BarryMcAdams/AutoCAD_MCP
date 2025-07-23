# Mock Markdown Test Document

This is a test document demonstrating various markdown features and formatting options.

## Table of Contents

- [Headers](#headers)
- [Text Formatting](#text-formatting)
- [Lists](#lists)
- [Links and References](#links-and-references)
- [Code Examples](#code-examples)
- [Tables](#tables)
- [Blockquotes](#blockquotes)
- [Task Lists](#task-lists)

---

## Headers

# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

## Text Formatting

**Bold text** using double asterisks

*Italic text* using single asterisks

~~Strikethrough text~~ using double tildes

***Bold and italic*** using triple asterisks

`Inline code` using backticks

## Lists

### Unordered List

- First item
- Second item
  - Nested item
  - Another nested item
- Third item

### Ordered List

1. First ordered item
2. Second ordered item
   1. Nested ordered item
   2. Another nested item
3. Third ordered item

## Links and References

[Link to Google](https://www.google.com)

[Link with title](https://www.github.com "GitHub Homepage")

[Reference link][ref1]

[ref1]: https://www.example.com "Example Website"

## Code Examples

### Inline Code

Here's some `inline code` in a sentence.

### Code Blocks

```javascript
function greetUser(name) {
    console.log(`Hello, ${name}!`);
    return `Welcome, ${name}`;
}

const user = "Alice";
greetUser(user);
```

```python
def calculate_area(radius):
    """Calculate the area of a circle."""
    import math
    return math.pi * radius ** 2

area = calculate_area(5)
print(f"Area: {area:.2f}")
```

```bash
# Example bash commands
ls -la
cd /home/user
git status
npm install
```

## Tables

| Name | Age | City | Occupation |
|------|-----|------|------------|
| Alice | 28 | New York | Developer |
| Bob | 35 | London | Designer |
| Charlie | 42 | Tokyo | Manager |
| Diana | 31 | Paris | Analyst |

### Table with Alignment

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Item 1 | Item 2 | Item 3 |
| A longer item | Short | $99.99 |
| Test | Testing | $1,234.56 |

## Blockquotes

> This is a blockquote. It can span multiple lines and is useful for highlighting important information or quotes from other sources.

> **Nested blockquote example:**
> 
> > This is a nested blockquote within another blockquote.
> > It demonstrates how blockquotes can be layered.

## Task Lists

- [x] Completed task
- [x] Another completed task
- [ ] Pending task
- [ ] Another pending task
  - [x] Nested completed subtask
  - [ ] Nested pending subtask

## Images

![Alt text for image](https://via.placeholder.com/400x200/0066cc/ffffff?text=Sample+Image)

*Caption: This is a sample placeholder image*

## Horizontal Rules

---

## Additional Features

### Emphasis Combinations

- **Bold** and *italic* can be combined: ***bold italic***
- **Bold** with `inline code`
- *Italic* with `inline code`

### Line Breaks

This is a paragraph with a  
line break using two spaces.

This is a new paragraph separated by a blank line.

### Escape Characters

To display literal asterisks: \*not italic\*

To display literal backticks: \`not code\`

---

## Footnotes

Here's a sentence with a footnote[^1].

Another sentence with a footnote[^2].

[^1]: This is the first footnote.
[^2]: This is the second footnote with more detailed information.

## Mathematical Expressions

Inline math: $E = mc^2$

Block math:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

---

## Conclusion

This document demonstrates various markdown formatting options including headers, text formatting, lists, links, code blocks, tables, blockquotes, and more. It serves as a comprehensive reference for markdown syntax testing.

**Last updated:** 2025-01-17  
**Version:** 1.0  
**Author:** Test User