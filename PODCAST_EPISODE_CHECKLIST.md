# Podcast Episode Checklist

Quick reference guide for adding new Rationally Writing episodes by copying the previous one.

## Steps to Add a New Episode

### 1. Copy Previous Episode
```bash
cp -r rationally-writing/66/ rationally-writing/67/
```
(Or just copy the folder in your file explorer)

### 2. Edit `rationally-writing/67/index.html`

Find and replace these items (use Find & Replace in your editor):

#### What to Change:

1. **Line 6 - Page Title** (in `<title>` tag)
   - Change: `66` → `67`
   - Change: Episode title text

2. **Line 309 - Episode Heading** (in `<h1 class="episode-title">`)
   - Change: `66` → `67`
   - Change: Episode title text

3. **Lines 315-320 - Episode Content** (in `<div class="episode-content">`)
   - Delete old embed code
   - Paste your new podcast embed
   - Update description and links

4. **Line 325 - Previous Link** (if needed)
   - Already updated to: `<a href="../66/" class="nav-button">← Previous</a>`
   - ✓ Should be correct

### 3. Update Episode 66's "Next" Button (Optional)

Edit `rationally-writing/66/index.html`:

**Line 327** - Change from:
```html
<span class="nav-button disabled">Next →</span>
```
To:
```html
<a href="../67/" class="nav-button">Next →</a>
```

### 4. Update the Index (Optional)

Edit `rationally-writing/index.html`:

Add new entry to the episode list (around line 446):
```html
<li><a href="./67/">67. Your Episode Title</a></li>
```

---

## Quick Find & Replace

Open `rationally-writing/67/index.html` and do these replacements:

| Find | Replace With |
|------|--------------|
| `[YOUR EPISODE TITLE HERE]` | Your actual episode title |
| `<!-- PASTE YOUR PODCAST EMBED HERE -->` | Your embed code |
| `<!-- ADD YOUR DESCRIPTION AND LINKS HERE -->` | Your description and links |

---

## Example Content Format

```html
<div class="episode-content">
    
<iframe style="border-radius: 12px;" src="https://open.spotify.com/embed/episode/YOUR_EPISODE_ID" width="100%" height="352" frameborder="0" allowfullscreen="allowfullscreen"></iframe>

<p>Episode description goes here. You can use <a href="https://example.com">links</a> as needed.</p>

<p>Hosted by <a href="/">Daystar Eld</a> and <a href="http://alexanderwales.com/">Alexander Wales</a>.</p>

<p>With thanks to Tim Yarbrough for the Intro/Outro music, <a href="http://amzn.to/2pnwPsP">G.A.T.O Must Be Respected</a></p>

</div>
```

---

## Files to Edit Summary

- [ ] Create `rationally-writing/67/index.html` (copy from 66)
- [ ] Update title in two places (line 6 and 309)
- [ ] Replace embed and description
- [ ] Update `rationally-writing/66/index.html` - "Next" button (optional)
- [ ] Update `rationally-writing/index.html` - add to list (optional)

